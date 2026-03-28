# W&B and checkpoints

## Logging

Enable Weights & Biases logging:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml --wandb
```

Run W&B offline:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml --wandb --wandb_offline
```

## Loading a model

`src/run_pipeline.py` can load a trained model:

From W&B:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml \
  --wandb_load_model wandb \
  --wandb_model_path <entity>/<project>/<run_id>
```

From a local checkpoint:

```bash
python src/run_pipeline.py --exp_config configs/XXX.yaml \
  --wandb_load_model local \
  --local_model_path /path/to/model_best.pt
```
