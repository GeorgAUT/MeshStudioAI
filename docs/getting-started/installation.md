# Installation

## Prerequisites

Please note MeshStudioAI currently requires Python 3.10-3.13 and [Firedrake](https://www.firedrakeproject.org/).

Install Firedrake following the official [Firedrake installation guide](https://www.firedrakeproject.org/install.html#installing-firedrake) and activate the Firedrake virtual environment. Please be mindful to use Python 3.10-3.13 when installing Firedrake.

## Install MeshStudioAI

With the Firedrake environment activated:

```bash
git clone https://github.com/GeorgAUT/MeshStudioAI
cd MeshStudioAI
pip install -e .
```

## Notes on PyTorch / PyG

This project depends on PyTorch and PyTorch Geometric. Depending on your platform, installing `torch-scatter` and related packages may require platform-specific wheels.