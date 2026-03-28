import time
import os

import matplotlib.pyplot as plt
from firedrake import DirichletBC, Function, FunctionSpace, SpatialCoordinate, TestFunction, TrialFunction
from firedrake import assemble, dx, exp, grad, inner, solve, sqrt
from firedrake import UnitSquareMesh
from firedrake.pyplot import tripcolor, triplot


def main():
    nx = 14
    ny = nx
    mesh = UnitSquareMesh(nx, ny)
    V = FunctionSpace(mesh, "CG", 1)

    x = SpatialCoordinate(mesh)

    s0, s1 = 0.15, 0.15

    def _gaussian_and_laplacian(x, cx, cy, sx, sy):
        g = exp(-((x[0] - cx) ** 2) / (sx**2) - ((x[1] - cy) ** 2) / (sy**2))
        lap = -(
            (4 * (x[0] - cx) ** 2 - 2 * (sx**2)) / (sx**4)
            + (4 * (x[1] - cy) ** 2 - 2 * (sy**2)) / (sy**4)
        ) * g
        return g, lap

    centers = [(0.1, 0.1), (0.5, 0.2), (0.6, 1.0)]

    u_true_expr = 0.0
    f_expr = 0.0
    for (cx, cy) in centers:
        g, lap_g = _gaussian_and_laplacian(x, cx, cy, s0, s1)
        u_true_expr += g
        f_expr += lap_g

    u_bc = u_true_expr
    f = f_expr

    u = TrialFunction(V)
    v = TestFunction(V)

    a = inner(grad(u), grad(v)) * dx
    L = f * v * dx

    uu = Function(V, name="uu")
    bc = DirichletBC(V, u_bc, "on_boundary")

    t0 = time.perf_counter()
    solve(a == L, uu, bcs=[bc], solver_parameters={"ksp_type": "preonly", "pc_type": "lu"})
    t1 = time.perf_counter()

    u_true = Function(V, name="u_true")
    u_true.interpolate(u_true_expr)

    l2_err = sqrt(assemble(inner(uu - u_true, uu - u_true) * dx))

    print(f"Mesh: UnitSquareMesh({nx}, {ny})  (structured {(nx + 1)}x{(ny + 1)} vertices)")
    print(f"DoFs (CG1): {V.dof_dset.size}")
    print(f"Solve time (s): {t1 - t0:.6f}")
    print(f"L2 error: {float(l2_err):.6e}")

    fig_mesh, ax_mesh = plt.subplots(nrows=1, ncols=1, figsize=(6, 6), constrained_layout=True)
    triplot(mesh, axes=ax_mesh)
    ax_mesh.set_aspect("equal")
    ax_mesh.set_title("Mesh")
    mesh_png_path = os.path.join(os.path.dirname(__file__), "mesh.png")
    fig_mesh.savefig(mesh_png_path, dpi=300, bbox_inches="tight")
    plt.close(fig_mesh)
    print(f"Wrote mesh plot to: {mesh_png_path}")

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5), constrained_layout=True)
    pcm0 = tripcolor(uu, axes=axs[0])
    axs[0].set_aspect("equal")
    axs[0].set_title("Poisson solution: uu")
    fig.colorbar(pcm0, ax=axs[0])

    pcm1 = tripcolor(u_true, axes=axs[1])
    axs[1].set_aspect("equal")
    axs[1].set_title("Manufactured solution: u_true")
    fig.colorbar(pcm1, ax=axs[1])

    plt.show()


if __name__ == "__main__":
    main()
