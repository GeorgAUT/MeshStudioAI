# First run

With Firedrake activated and data downloaded into `./data`, run a minimal example:

```bash
python src/run_pipeline.py --exp_config configs/poisson_square_mixed.yaml
```

If you only want to train (without the evaluation wrapper):

```bash
python src/run_GNN.py --exp_config configs/poisson_square_mixed.yaml
```
