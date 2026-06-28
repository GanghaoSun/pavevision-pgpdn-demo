# Manuscript-to-Code Mapping

This page maps the main manuscript components to the public repository files.

| Manuscript component | Repository files |
| --- | --- |
| PG-PDN feature vector | `pgpdn/constants.py`, `pgpdn/features.py`, `docs/data_schema.md` |
| Physical degradation branch | `pgpdn/model.py`, `configs/pgpdn_default.yaml` |
| GRU residual branch | `pgpdn/model.py` |
| Composite loss terms | `pgpdn/model.py`, `configs/pgpdn_default.yaml` |
| Synthetic model-interface check | `examples/run_inference_template.py`, `sample_data/synthetic_grid_features.csv` |
| Grid-level visualization | `pgpdn/visualization.py`, `examples/plot_synthetic_quality_map.py` |
| PaveVision route map | `web_demo/static/index.html`, `web_demo/app.py`, `web_demo/data/route_display.json` |
| PaveVision quality assessment | `web_demo/app.py`, `web_demo/data/sample/*.assessment.json`, `web_demo/data/sample/*.grid_0.5.json` |
| PaveVision prediction view | `web_demo/app.py`, `web_demo/data/sample/*_predicted.*.json` |
| Manuscript-style figures | `assets/` |
| Public package checks | `tests/`, `.github/workflows/ci.yml` |

The mapping is intended to help readers move from the manuscript description to the exact implementation files used by the public package.
