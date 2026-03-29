# Navier–Stokes adaptivity demo

This demo shows:

- a simple Navier–Stokes FEM solver in Firedrake (cylinder flow),
- a GNN-based mesh relocation step using pretrained weights,
- and a GIF video of the time evolution on the adapted mesh.

## Governing equations

We consider the **incompressible Navier–Stokes equations** for velocity $\mathbf{u}(\mathbf{x}, t)$ and pressure $p(\mathbf{x}, t)$:

```math
\begin{aligned}
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u}\cdot\nabla)\mathbf{u} - \nu\,\Delta \mathbf{u} + \nabla p &= \mathbf{f} \quad \text{in } \Omega,\\
\nabla\cdot\mathbf{u} &= 0 \quad \text{in } \Omega.
\end{aligned}
```

with viscosity $\nu>0$, forcing $\mathbf{f}$, an initial condition $\mathbf{u}(\mathbf{x},0)=\mathbf{u}_0(\mathbf{x})$, and appropriate boundary conditions on $\partial\Omega$ (e.g. inflow/outflow and no-slip on obstacles).

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
