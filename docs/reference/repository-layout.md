# Repository layout

- `src/run_GNN.py`: training loop
- `src/run_pipeline.py`: evaluation + plotting + W&B integration
- `src/pde_solvers.py`: Firedrake PDE solvers used for data generation and PDE-based losses
- `src/data.py`, `src/data_mixed.py`: dataset definitions
- `src/models/`: model architectures and baselines
- `configs/`: experiment configurations
- `meshes/`: mesh inputs
- `examples/`: example scripts and assets
