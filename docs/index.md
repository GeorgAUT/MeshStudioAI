# MeshStudioAI

MeshStudioAI is a collection of AI tools for adaptive meshing in the context of finite element methods (FEM). It builds on the official implementation of [G-Adaptivity](https://openreview.net/forum?id=pyIXyl4qFx): a GNN-based approach to adaptive mesh relocation for FEM.

## What you can do

- Train a mesh relocation model (typically `MeshAdaptor`)
- Evaluate trained models on precomputed datasets
- Plot qualitative and quantitative results
- Log experiments to Weights & Biases (W&B)

## Key entry points

- `src/run_GNN.py`: training
- `src/run_pipeline.py`: evaluation (and optional training wrapper)

## Quickstart

1. Install and activate Firedrake.
2. Download a dataset into `./data`.
3. Run:

```bash
python src/run_pipeline.py --exp_config configs/poisson_square_mixed.yaml
```
