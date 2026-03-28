# MeshStudioAI

MeshStudioAI presents a collection of AI tools for adaptive meshing in the context of finite element methods (FEM). The repository builds on the official implementation of [G-Adaptivity](https://openreview.net/forum?id=pyIXyl4qFx): a GNN-based approach to adaptive mesh relocation for finite element methods (FEM).

The main entry points are:

- `src/run_GNN.py`: train a model (typically `MeshAdaptor`)
- `src/run_pipeline.py`: evaluate a trained model (with optional plotting and W&B logging)

## Quickstart

1. Install and activate a Firedrake environment (see Installation).
2. Download the dataset (see Datasets) into `./data`.
3. Run an experiment config:

```bash
python src/run_pipeline.py --exp_config configs/poisson_square_mixed.yaml
```

## Installation

This code depends on [Firedrake](https://www.firedrakeproject.org/), a Python-based finite element library used to solve the PDEs.

We recommend installing Firedrake via the official guide, which also sets up a dedicated virtual environment:

https://www.firedrakeproject.org/install.html#installing-firedrake

Once Firedrake is installed and its virtual environment is activated, install this repo and its Python dependencies:

```bash
git clone <THIS_REPO_URL>
cd MeshStudioAI
pip install -e .
```

## Datasets

The code can generate training/test datasets directly, but this is computationally expensive due to the number of FEM solves.

Precomputed datasets are available via Zenodo:

https://zenodo.org/records/15800768

After downloading, place the datasets in the `data/` folder at the repository root:

```text
MeshStudioAI/
└── data/
    └── <your_downloaded_data_here>
```

The `data/` folder may not exist until you create it manually or run a script that uses it.

## Training and evaluation

To train and evaluate models from the paper, run:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml
```

The folder `configs/` contains experiment configs used in the paper. A simple starting point is `configs/poisson_square_mixed.yaml`.

If you only want to train (without the evaluation wrapper), run:

```bash
python src/run_GNN.py --exp_config configs/XXX.yaml
```

## Configuration

The configuration system composes:

- `configs/base_config.yaml`: shared defaults
- `configs/<experiment>.yaml`: experiment overrides

Any parameter set in an experiment config file overwrites the corresponding value in `base_config.yaml`.

Example structure:

```yaml
run:
  pde_type: "Poisson"  # 'Poisson', 'Burgers', 'NavierStokes'
  data_type: "randg_mix"  # 'randg', 'randg_mix', 'RBF'
  model: "MeshAdaptor"  # 'MeshAdaptor', 'backFEM_2D'

data:
  mesh_geometry: "rectangle"
  mesh_dims_train: [[15, 15], [20, 20]]
  mesh_dims_test: [[12, 12], [14, 14], [16, 16], [18, 18], [20, 20], [22, 22]]
```

You can also work with your own mesh by placing a custom `.mesh` file in `meshes/` and setting `mesh_geometry` to the filename (without the `.mesh` suffix).

## W&B logging and loading models

This project supports logging to Weights & Biases (W&B).

- To log a run, pass `--wandb` (and optionally `--wandb_entity`, `--wandb_project`, `--wandb_group`).
- To run W&B offline, pass `--wandb_offline`.

`src/run_pipeline.py` can also load a trained model:

- From W&B:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml \
  --wandb_load_model wandb \
  --wandb_model_path <entity>/<project>/<run_id>
```

- From a local checkpoint:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml \
  --wandb_load_model local \
  --local_model_path /path/to/model_best.pt
```

## Reproducibility

`src/params.py` currently overrides the configured `seed` with a random seed at runtime. If you need deterministic runs, you will want to modify that behavior.

## Repository layout

- `src/run_GNN.py`: training loop (PyTorch + PyTorch Geometric)
- `src/run_pipeline.py`: evaluation + plotting + W&B integration
- `src/pde_solvers.py`: Firedrake PDE solvers used to generate data / compute losses
- `src/data.py`, `src/data_mixed.py`: dataset definitions
- `src/models/`: GNN mesh adaptor model(s) and baselines
- `configs/`: experiment configurations

## Known issues

- Anaconda is known to cause issues when installing Firedrake on macOS. Homebrew is recommended where possible. See the Firedrake installation guide and Firedrake issue tracker for help.

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
