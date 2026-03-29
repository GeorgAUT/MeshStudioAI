# Navier–Stokes adaptivity demo

This demo shows:

- a simple Navier–Stokes FEM solver in Firedrake (cylinder flow),
- a GNN-based mesh relocation step using pretrained weights,
- and a GIF video of the time evolution on the adapted mesh.

## Governing equations

We consider the **incompressible Navier–Stokes equations** for velocity `u(x, t)` and pressure `p(x, t)`:

```text
∂u/∂t + (u · ∇)u - ν Δu + ∇p = f   in Ω
∇ · u = 0                         in Ω
```

with viscosity `ν > 0`, forcing `f`, an initial condition `u(x, 0) = u0(x)`, and appropriate boundary conditions on `∂Ω` (e.g. inflow/outflow and no-slip on obstacles).

## Prerequisites

- A working Firedrake installation and activated environment.
- Project dependencies installed (see Installation).

## Run

### Notebook (recommended)

Open the notebook:

`examples/navier_stokes_adaptivity_demo.ipynb`

Then run all cells in Jupyter/JupyterLab.

### Inputs

The demo defaults to:

- Mesh: `meshes/cylinder_050.msh`
- Weights: `pretrained/generic_model_weights.pt`
- Model config: `examples/extensions_navier_stokes/pretrained/config.yaml`

## Outputs

The demo writes GIFs under:

```text
outputs/navier_stokes_demo/
```

Files:

- `navier_stokes_adapted_u.gif`
- `navier_stokes_adapted_mesh.gif`
