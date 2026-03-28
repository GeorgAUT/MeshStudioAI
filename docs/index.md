# MeshStudioAI

MeshStudioAI is a collection of AI tools for adaptive meshing in the context of finite element methods (FEM). It builds on the official implementation of [G-Adaptivity](https://openreview.net/forum?id=pyIXyl4qFx): a GNN-based approach to adaptive mesh relocation for FEM.

<video controls muted playsinline style="max-width: 100%; height: auto;">
  <source src="assets/videos/cylinder_g-adaptivity_flow+mesh.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## What you can do

- Use the pretrained G-Adaptivity framework on your own FEM problem
- Train a mesh relocation model (typically `MeshAdaptor`)
- Evaluate trained models on precomputed datasets
- Plot qualitative and quantitative results
- Log experiments to Weights & Biases (W&B)

## Quickstart

To run your first mesh adaptivity example please see the [Installation guide](getting-started/installation.md), and the [First demo notebook](getting-started/navier-stokes-adaptivity.md)