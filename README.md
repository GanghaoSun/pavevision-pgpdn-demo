# pavevision-pgpdn-demo

PG-PDN method package for PaveVision.

Last updated: 2026-07-06 11:07 (Asia/Shanghai).

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.9-3776AB.svg)](pyproject.toml)

This repository accompanies the manuscript **"Physics-guided pavement degradation prediction from grid-level semantic distress maps"**.

The repository is organized as a method-level code companion for **PG-PDN**, with emphasis on the physics-guided network definition, feature contract, configuration defaults and equation-to-code traceability. It is intended to let readers inspect how the manuscript method is represented in source code.

## At a Glance

| Asset | What it provides |
| --- | --- |
| PG-PDN architecture | A PyTorch implementation of the physical degradation branch, GRU residual branch and prediction head. |
| Physics-guided branch | Interpretable deterioration-rate parameters initialized from engineering assumptions and clipped during optimization. |
| Residual branch | A compact GRU correction module using current quality, distress densities and LiDAR intensity descriptors. |
| Composite objective | Prediction error, non-negative deterioration penalty and along-route smoothness penalty. |
| Feature contract | Required field names, tensor shapes, units and constraints for the 12-dimensional PG-PDN input. |
| Method documentation | Section 3 equation-to-code mapping, method scope and manuscript-to-repository index. |
| PaveVision source skeleton | Interface boundary documentation for the PaveVision UI layer. |

## Reviewer Reading Path

| Review target | Recommended entry point |
| --- | --- |
| Method scope | [docs/method_scope.md](docs/method_scope.md) |
| Formula and module traceability | [docs/equation_to_code_mapping.md](docs/equation_to_code_mapping.md) |
| Required model inputs | [docs/input_contract.md](docs/input_contract.md) |
| Source-level manuscript mapping | [docs/manuscript_mapping.md](docs/manuscript_mapping.md) |
| PG-PDN implementation | [pgpdn/model.py](pgpdn/model.py) |
| Feature names and validation | [pgpdn/constants.py](pgpdn/constants.py), [pgpdn/features.py](pgpdn/features.py) |
| Default method configuration | [configs/pgpdn_default.yaml](configs/pgpdn_default.yaml) |
| PaveVision UI boundary | [pavevision_ui/README.md](pavevision_ui/README.md) |

## Method Overview

PG-PDN predicts grid-level pavement deterioration by combining an interpretable physical branch with a neural residual branch.

![PG-PDN network architecture](assets/pgpdn_architecture.png)

The physical branch estimates a non-negative deterioration rate from traffic loading, climate variables, semantic distress densities and LiDAR intensity statistics. The residual branch captures remaining nonlinear structure with a single-layer GRU. The final deterioration prediction is the sum of both components, and the next-period PQI* is obtained by subtracting the predicted deterioration from the current PQI*.

## Core Method Files

| Path | Role in the manuscript method |
| --- | --- |
| [pgpdn/model.py](pgpdn/model.py) | Defines `PhysicalBranch`, `PGPDN` and `PGPDNLoss`, corresponding to the Section 3 physical branch, residual branch and composite loss. |
| [pgpdn/constants.py](pgpdn/constants.py) | Defines the 12 PG-PDN feature names and default physical-branch parameters. |
| [pgpdn/features.py](pgpdn/features.py) | Validates the PG-PDN feature table contract and exports the 12-dimensional tensor order. |
| [configs/pgpdn_default.yaml](configs/pgpdn_default.yaml) | Records model dimensions, default physical parameters and loss weights. |
| [docs/equation_to_code_mapping.md](docs/equation_to_code_mapping.md) | Links manuscript Section 3 equations, branches and loss terms to exact code locations. |
| [docs/input_contract.md](docs/input_contract.md) | Specifies field names, tensor shapes, units and constraints. |

## PG-PDN Input Contract

Each grid cell is represented by the 12-dimensional feature vector:

```text
[PQI*, ESAL, P, DeltaT, F, D1, D2, D3, D4, I_mean, I_std, I_low]
```

The corresponding Python field names are:

```text
pqi_star, esal_1e4, precip_mm, temp_range_c, low_temp_days,
density_transverse, density_longitudinal, density_alligator, density_pothole,
intensity_mean, intensity_std, intensity_low_prop
```

The model accepts a tensor with shape `(..., 12)`. The residual branch internally uses an 8-dimensional subset:

```text
[PQI*, D1, D2, D3, D4, I_mean, I_std, I_low]
```

Full field-level units and constraints are documented in [docs/input_contract.md](docs/input_contract.md).

## Model Outputs

The `PGPDN.forward()` method returns named tensors for direct inspection:

| Output key | Meaning |
| --- | --- |
| `delta_norm` | Predicted normalized deterioration. |
| `delta_pqi_points` | Predicted deterioration in PQI* points. |
| `next_pqi_points` | Predicted next-period PQI*, clipped to `[0, 100]`. |
| `physical_rate` | Non-negative deterioration rate from the physical branch. |
| `physical_delta_norm` | Physical-branch contribution to normalized deterioration. |
| `residual_delta_norm` | GRU residual correction in normalized units. |

## Loss Terms

`PGPDNLoss` implements the composite Section 3 objective:

```text
loss = MAE(predicted deterioration, target deterioration)
     + lambda_neg * nonnegative-deterioration penalty
     + lambda_smooth * along-route smoothness penalty
```

Default coefficients are recorded in [configs/pgpdn_default.yaml](configs/pgpdn_default.yaml):

```text
lambda_neg = 0.5
lambda_smooth = 0.1
```

## Repository Structure

```text
.
|-- README.md
|-- CITATION.cff
|-- LICENSE
|-- configs/
|   `-- pgpdn_default.yaml
|-- docs/
|   |-- equation_to_code_mapping.md
|   |-- input_contract.md
|   |-- manuscript_mapping.md
|   |-- method_scope.md
|   `-- public_workflow.md
|-- pavevision_ui/
|   |-- README.md
|   `-- interface_contract.md
|-- pgpdn/
|   |-- constants.py
|   |-- features.py
|   |-- model.py
|   |-- visualization.py
|   `-- __init__.py
|-- supplementary/
|   |-- Data_and_Model_Release_Statement.md
|   `-- Supplementary_Methods.md
```

## Citation

Please cite the associated manuscript if you use this code or adapt the PG-PDN architecture. Citation metadata are provided in [CITATION.cff](CITATION.cff).

## License

This repository is released under the [MIT License](LICENSE).
