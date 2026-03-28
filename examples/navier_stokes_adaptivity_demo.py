import argparse
import os
import sys

import imageio.v2 as imageio
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import torch
import yaml

from firedrake import *
from firedrake.pyplot import tripcolor


def _repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


sys.path.append(os.path.join(_repo_root(), "src"))

from data import firedrake_mesh_to_PyG  # noqa: E402
from models.mesh_adaptor_model import Mesh_Adaptor  # noqa: E402


def load_opt_from_wandb_style_yaml(path: str) -> dict:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    opt = {}
    for k, v in raw.items():
        if isinstance(v, dict) and "value" in v:
            opt[k] = v["value"]

    return opt


def compute_hessian_frob_norm(mesh, u_now, p_now, dim=2):
    Hessian_squared = 0
    n_fd = FacetNormal(mesh)
    V_hess = FunctionSpace(mesh, "CG", 1)

    for l in range(dim):
        ul = assemble(interpolate(u_now[l], V_hess))
        for i in range(dim):
            for j in range(dim):
                u_ij = Function(V_hess)
                v_h = TestFunction(V_hess)
                w_h = TrialFunction(V_hess)
                solve(
                    w_h * v_h * dx
                    == -outer(grad(ul), grad(v_h))[i, j] * dx
                    + (outer(n_fd, grad(ul)) * v_h)[i, j] * ds,
                    u_ij,
                    bcs=[DirichletBC(V_hess, 0, "on_boundary")],
                )
                Hessian_squared += u_ij**2

    for i in range(dim):
        for j in range(dim):
            p_ij = Function(V_hess)
            v_h = TestFunction(V_hess)
            w_h = TrialFunction(V_hess)
            solve(
                w_h * v_h * dx
                == -outer(grad(p_now), grad(v_h))[i, j] * dx
                + (outer(n_fd, grad(p_now)) * v_h)[i, j] * ds,
                p_ij,
                bcs=[DirichletBC(V_hess, 0, "on_boundary")],
            )
            Hessian_squared += p_ij**2

    return Function(V_hess, name="||H||_F").project(sqrt(Hessian_squared))


def build_navier_stokes_solver(mesh, nu_val, dt_val, U_mean):
    nu = Constant(nu_val)
    k = Constant(dt_val)

    V = VectorFunctionSpace(mesh, "CG", 2)
    Q = FunctionSpace(mesh, "CG", 1)

    u_trial = TrialFunction(V)
    v_test = TestFunction(V)
    p_trial = TrialFunction(Q)
    q_test = TestFunction(Q)

    u_now = Function(V)
    u_next = Function(V)
    u_star = Function(V)
    p_now = Function(Q)
    p_next = Function(Q)

    n = FacetNormal(mesh)
    f = Constant((0.0, 0.0))

    coords = mesh.coordinates.dat.data_ro
    x0 = float(coords[:, 0].min())
    x1 = float(coords[:, 0].max())
    y0 = float(coords[:, 1].min())
    y1 = float(coords[:, 1].max())
    H = y1 - y0

    x, y = SpatialCoordinate(mesh)
    inflow_u = as_vector((4.0 * U_mean * (y - y0) * (y1 - y) / (H * H), 0.0))

    markers = list(mesh.topology.exterior_facets.unique_markers)
    need = {1, 2, 3, 4}
    if not need.issubset(set(markers)):
        raise ValueError(f"Mesh boundary markers are {sorted(markers)} but this script expects {sorted(need)}")

    bcu = [
        DirichletBC(V, Constant((0.0, 0.0)), (1, 4)),
        DirichletBC(V, inflow_u, 2),
    ]
    bcp = [DirichletBC(Q, Constant(0.0), 3)]

    def sigma(u, p):
        return 2 * nu * sym(nabla_grad(u)) - p * Identity(len(u))

    u_mid = 0.5 * (u_now + u_trial)

    F1 = (
        inner((u_trial - u_now) / k, v_test) * dx
        + inner(dot(u_now, nabla_grad(u_mid)), v_test) * dx
        + inner(sigma(u_mid, p_now), sym(nabla_grad(v_test))) * dx
        + inner(p_now * n, v_test) * ds
        - inner(nu * dot(nabla_grad(u_mid), n), v_test) * ds
        - inner(f, v_test) * dx
    )

    a1, L1 = system(F1)

    a2 = inner(nabla_grad(p_trial), nabla_grad(q_test)) * dx
    L2 = inner(nabla_grad(p_now), nabla_grad(q_test)) * dx - (1.0 / k) * inner(div(u_star), q_test) * dx

    a3 = inner(u_trial, v_test) * dx
    L3 = inner(u_star, v_test) * dx - k * inner(nabla_grad(p_next - p_now), v_test) * dx

    problem1 = LinearVariationalProblem(a1, L1, u_star, bcs=bcu)
    problem2 = LinearVariationalProblem(a2, L2, p_next, bcs=bcp)
    problem3 = LinearVariationalProblem(a3, L3, u_next)

    solver1 = LinearVariationalSolver(problem1, solver_parameters={"ksp_type": "gmres", "pc_type": "sor"})
    solver2 = LinearVariationalSolver(problem2, solver_parameters={"ksp_type": "cg", "pc_type": "gamg"})
    solver3 = LinearVariationalSolver(problem3, solver_parameters={"ksp_type": "cg", "pc_type": "sor"})

    u_now.assign(Constant((0.0, 0.0)))
    p_now.assign(Constant(0.0))
    u_star.assign(u_now)
    u_next.assign(u_now)
    p_next.assign(p_now)

    return (solver1, solver2, solver3), (u_now, u_next, u_star, p_now, p_next)


def main():
    parser = argparse.ArgumentParser(description="Navier–Stokes + GNN mesh adaptivity demo (writes GIFs)")
    parser.add_argument(
        "--mesh",
        type=str,
        default=os.path.join(_repo_root(), "meshes", "cylinder_050.msh"),
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=os.path.join(_repo_root(), "pretrained", "generic_model_weights.pt"),
    )
    parser.add_argument(
        "--model_config",
        type=str,
        default=os.path.join(_repo_root(), "examples", "extensions_navier_stokes", "pretrained", "config.yaml"),
    )
    parser.add_argument("--nu", type=float, default=0.001)
    parser.add_argument("--dt", type=float, default=0.02)
    parser.add_argument("--steps", type=int, default=250)
    parser.add_argument("--U_mean", type=float, default=1.0)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--frame_every", type=int, default=1)
    parser.add_argument(
        "--out_dir",
        type=str,
        default=os.path.join(_repo_root(), "outputs", "navier_stokes_demo"),
    )
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    mesh = Mesh(os.path.abspath(args.mesh))
    ghost_mesh = Mesh(os.path.abspath(args.mesh))

    (solver1, solver2, solver3), (u_now, u_next, u_star, p_now, p_next) = build_navier_stokes_solver(
        mesh=mesh,
        nu_val=args.nu,
        dt_val=args.dt,
        U_mean=args.U_mean,
    )

    opt = load_opt_from_wandb_style_yaml(os.path.abspath(args.model_config))
    opt["wandb"] = False
    opt["wandb_offline"] = True
    os.environ["WANDB_MODE"] = "disabled"

    opt.setdefault("grand_diffusion", True)
    opt.setdefault("grand_step_size", 0.1)
    opt.setdefault("grand_diffusion_steps", 20)

    opt["new_model_monitor_type"] = "Hessian_Frob_u_tensor"
    opt["device"] = torch.device("cpu")
    opt["mesh_dims"] = [25, 25]

    state_dict = torch.load(os.path.abspath(args.weights), map_location="cpu")
    model = Mesh_Adaptor(opt, gfe_in_c=3, lfe_in_c=3, deform_in_c=3).to(opt["device"])
    model.load_state_dict(state_dict)
    model.eval()

    ghost_reg_coords = ghost_mesh.coordinates.copy(deepcopy=True)
    pyg_data_ghost = firedrake_mesh_to_PyG(ghost_mesh)
    pyg_data_ghost.coarse_mesh = [ghost_mesh]

    V_ghost = VectorFunctionSpace(ghost_mesh, "CG", 2)
    Vmag_ghost = FunctionSpace(ghost_mesh, "CG", 1)
    u_ghost = Function(V_ghost)
    u_mag_ghost = Function(Vmag_ghost)

    out_u_gif = os.path.join(args.out_dir, "navier_stokes_adapted_u.gif")
    out_mesh_gif = os.path.join(args.out_dir, "navier_stokes_adapted_mesh.gif")

    fig_u, ax_u = plt.subplots(nrows=1, ncols=1, figsize=(10, 8), dpi=200)
    writer_u = imageio.get_writer(out_u_gif, mode="I", duration=1.0 / float(args.fps))

    fig_m, ax_m = plt.subplots(nrows=1, ncols=1, figsize=(10, 8), dpi=200)
    writer_m = imageio.get_writer(out_mesh_gif, mode="I", duration=1.0 / float(args.fps))

    for step in range(args.steps):
        print("Remaining Steps: ", args.steps - step, end="\r")
        solver1.solve()
        solver2.solve()
        solver3.solve()
        u_now.assign(u_next)
        p_now.assign(p_next)

        if step % args.frame_every != 0:
            continue

        ghost_mesh.coordinates.assign(ghost_reg_coords)

        Hessian_frob = compute_hessian_frob_norm(mesh, u_now, p_now, dim=2)
        pyg_data_ghost.Hessian_Frob_u_tensor = torch.from_numpy(Hessian_frob.dat.data_ro.copy()).float()

        coords_np = ghost_mesh.coordinates.dat.data_ro.copy()
        coords_t = torch.from_numpy(coords_np).float()
        pyg_data_ghost.x_in = coords_t
        pyg_data_ghost.x_comp = coords_t

        with torch.no_grad():
            x_phys = model(pyg_data_ghost)

        V_coords = VectorFunctionSpace(ghost_mesh, "CG", 1)
        new_coordinates = Function(V_coords)
        new_coordinates.dat.data[:] = x_phys.detach().cpu().numpy()
        ghost_mesh.coordinates.assign(new_coordinates)

        u_ghost.dat.data[:] = u_now.dat.data_ro
        u_mag_ghost.project(sqrt(inner(u_ghost, u_ghost)))

        triang = mtri.Triangulation(
            ghost_mesh.coordinates.dat.data[:, 0],
            ghost_mesh.coordinates.dat.data[:, 1],
            ghost_mesh.coordinates.cell_node_map().values,
        )

        ax_u.clear()
        tripcolor(u_mag_ghost, axes=ax_u)
        ax_u.triplot(triang, linewidth=0.25, color="k")
        ax_u.set_aspect("equal")
        ax_u.set_title(f"Adapted mesh: |u|  t={(step + 1) * float(args.dt):.3f}")
        fig_u.tight_layout()
        fig_u.canvas.draw()
        rgba = np.asarray(fig_u.canvas.buffer_rgba())
        writer_u.append_data(rgba[:, :, :3].copy())

        ax_m.clear()
        ax_m.triplot(triang, linewidth=0.25, color="k")
        ax_m.set_aspect("equal")
        ax_m.set_title(f"Adapted mesh  t={(step + 1) * float(args.dt):.3f}")
        fig_m.tight_layout()
        fig_m.canvas.draw()
        rgba_m = np.asarray(fig_m.canvas.buffer_rgba())
        writer_m.append_data(rgba_m[:, :, :3].copy())

    writer_u.close()
    plt.close(fig_u)
    writer_m.close()
    plt.close(fig_m)

    print("")
    print(f"Wrote: {out_u_gif}")
    print(f"Wrote: {out_mesh_gif}")


if __name__ == "__main__":
    main()
