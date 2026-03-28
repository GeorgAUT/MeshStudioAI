# Navier–Stokes adaptivity demo

This demo shows:

- a simple Navier–Stokes FEM solver in Firedrake (cylinder flow),
- a GNN-based mesh relocation step using pretrained weights,
- and a GIF video of the time evolution on the adapted mesh.

## Prerequisites

- A working Firedrake installation and activated environment.
- Project dependencies installed (see Installation).

## Run

From the repo root:

```bash
python examples/navier_stokes_adaptivity_demo.py
```

### Inputs

The demo defaults to:

- Mesh: `meshes/cylinder_050.msh`
- Weights: `pretrained/generic_model_weights.pt`
- Model config: `examples/extensions_navier_stokes/pretrained/config.yaml`

You can override these:

```bash
python examples/navier_stokes_adaptivity_demo.py \
  --mesh meshes/cylinder_050.msh \
  --weights pretrained/generic_model_weights.pt \
  --model_config examples/extensions_navier_stokes/pretrained/config.yaml
```

## Outputs

The demo writes GIFs under:

```text
outputs/navier_stokes_demo/
```

Files:

- `navier_stokes_adapted_u.gif`
- `navier_stokes_adapted_mesh.gif`
