# First full training + evaluation

This page shows a minimal end-to-end run: evaluate a pretrained or existing model via the evaluation pipeline, or run training directly.

With Firedrake activated and data available under `./data`, run a minimal example:

```bash
python src/run_pipeline.py --exp_config configs/poisson_square_mixed.yaml
```

If you only want to train (without the evaluation wrapper):

```bash
python src/run_GNN.py --exp_config configs/poisson_square_mixed.yaml
```
