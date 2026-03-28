# Configuration

Experiments are configured via YAML files in `configs/`.

The configuration system composes:

- `configs/base_config.yaml`: shared defaults
- `configs/<experiment>.yaml`: experiment overrides

Any parameter set in an experiment config file overwrites the corresponding value in `base_config.yaml`.

## Minimal example

```yaml
run:
  pde_type: "Poisson"
  data_type: "randg_mix"
  model: "MeshAdaptor"

data:
  mesh_geometry: "rectangle"
  mesh_dims_train: [[15, 15], [20, 20]]
  mesh_dims_test: [[12, 12], [14, 14]]
```
