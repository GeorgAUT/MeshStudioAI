# MeshStudioAI

MeshStudioAI is a collection of AI tools for adaptive meshing in the context of finite element methods (FEM). It builds on the official implementation of [G-Adaptivity](https://openreview.net/forum?id=pyIXyl4qFx): a GNN-based approach to adaptive mesh relocation for FEM.

<video controls autoplay muted loop playsinline style="max-width: 100%; height: auto;">
  <source src="assets/videos/cylinder_g-adaptivity_flow+mesh.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

The full repository is available on [GitHub](https://github.com/georgaut/MeshStudioAI).

## Functionality

- Use the pretrained G-Adaptivity framework on your own FEM problem
- Train a mesh relocation model (typically `MeshAdaptor`)
- Evaluate trained models on precomputed datasets
- Plot qualitative and quantitative results
- Log experiments to Weights & Biases (W&B)

## Quickstart

To run your first mesh adaptivity example please see the [Installation guide](getting-started/installation.md), and the [First demo notebook](getting-started/navier-stokes-adaptivity.md)


## License and citation

This open-source version of our code is licensed under Apache 2.0. If you use this work, please cite:

```text
@inproceedings{Rowbottom_G-Adaptivity_optimised_graph-based_2025,
    author = {Rowbottom, James and Maierhofer, Georg and Deveney, Teo and Müller, Eike Hermann and Paganini, Alberto and Schratz, Katharina and Lio, Pietro and Schönlieb, Carola-Bibiane and Budd, Chris},
    booktitle = {Proceedings of the Forty-second International Conference on Machine Learning},
    title = {{G-Adaptivity: optimised graph-based mesh relocation for finite element methods}},
    year = {2025}
}
```
