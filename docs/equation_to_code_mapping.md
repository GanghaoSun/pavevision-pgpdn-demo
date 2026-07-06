# Equation-to-Code Mapping

This page maps manuscript Section 3 method components to repository files. It is written for code-level inspection of the PG-PDN method implementation and does not define route records or display data.

| Manuscript Section 3 item | Code location | Implementation note |
| --- | --- | --- |
| Grid-level prediction target `PQI*` | `pgpdn/constants.py::FEATURE_COLUMNS`; `pgpdn/features.py::validate_feature_table` | `pqi_star` is the first model feature and is constrained to `[0, 100]`. |
| Feature vector construction, Eq. (9) | `pgpdn/constants.py::FEATURE_COLUMNS`; `docs/input_contract.md` | The 12 fields are ordered as `[PQI*, ESAL, P, DeltaT, F, D1, D2, D3, D4, I_mean, I_std, I_low]`. |
| Traffic loading term `log(1+ESAL)` | `pgpdn/model.py::PhysicalBranch.forward` | `torch.log1p(torch.clamp(esal, min=0.0))` implements the non-negative ESAL transform. |
| Climate terms `P`, `DeltaT`, `F` | `pgpdn/model.py::PhysicalBranch.forward` | `precip`, `temp_range` and `low_temp_days` map to the three climate coefficients. |
| Distress-density terms `D1`-`D4` | `pgpdn/model.py::PhysicalBranch.forward` | The four semantic distress densities are multiplied by `beta1`-`beta4`. |
| LiDAR intensity term `1-I_mean` | `pgpdn/model.py::PhysicalBranch.forward` | `gamma * (1.0 - intensity_mean)` links intensity degradation evidence to the physical branch. |
| Physical branch non-negative deterioration rate | `pgpdn/model.py::PhysicalBranch.forward` | `torch.clamp(rate, min=0.0)` enforces the non-negative physical rate. |
| Physical-parameter initialization | `pgpdn/constants.py::PHYSICAL_PARAMETER_DEFAULTS`; `configs/pgpdn_default.yaml::physical_branch.initial_parameters` | Default parameters are named consistently with the manuscript notation. |
| Physical-parameter clipping | `pgpdn/model.py::PhysicalBranch.clipped_theta`; `configs/pgpdn_default.yaml::physical_branch.parameter_clip_ratio` | The default ratio is `0.5`, giving a +/-50% clipping interval around the initial parameter values. |
| Physical deterioration contribution | `pgpdn/model.py::PGPDN.forward` | `delta_phys_norm = pqi_norm * r_phys` converts the physical rate to normalized PQI* deterioration. |
| Residual-branch input subset | `pgpdn/model.py::PGPDN.residual_inputs` | The residual branch receives `[PQI*, D1, D2, D3, D4, I_mean, I_std, I_low]` after PQI* normalization. |
| GRU residual correction | `pgpdn/model.py::PGPDN.__init__`; `pgpdn/model.py::PGPDN.forward` | A single-layer GRU followed by dropout and a linear head predicts `residual_delta_norm`. |
| PG-PDN final deterioration | `pgpdn/model.py::PGPDN.forward` | `delta_norm = delta_phys_norm + residual_norm` combines the physical and residual branches. |
| Next-period pavement quality | `pgpdn/model.py::PGPDN.forward` | `next_pqi_points` subtracts predicted deterioration from current PQI* and clips to `[0, 100]`. |
| Prediction-error loss | `pgpdn/model.py::PGPDNLoss.forward` | `mae` is the mean absolute error between predicted and target normalized deterioration. |
| Non-negative deterioration penalty | `pgpdn/model.py::PGPDNLoss.forward` | `neg = mean(relu(-pred_delta_norm))` penalizes negative predicted deterioration. |
| Along-route smoothness penalty | `pgpdn/model.py::PGPDNLoss.forward` | When `unit_ids` are supplied, adjacent maintenance-unit means are penalized by absolute difference. |
| Composite loss weights | `configs/pgpdn_default.yaml::loss`; `pgpdn/model.py::PGPDNConfig` | `lambda_neg` and `lambda_smooth` control the two regularization terms. |

## Physical Branch

`PhysicalBranch` corresponds to the Section 3 physics-guided deterioration-rate module. The parameter order in code is:

```text
alpha0, alpha1, alpha2, alpha3, alpha4,
beta1, beta2, beta3, beta4, gamma
```

The branch returns a non-negative deterioration rate `r_phys`, which is then multiplied by normalized current PQI* inside `PGPDN.forward()`.

## Residual Branch

`PGPDN.residual_inputs()` forms the residual-branch tensor by concatenating normalized current PQI*, four distress densities and three intensity descriptors. `PGPDN.forward()` then reshapes this tensor to a one-step sequence before applying the GRU.

## Loss Terms

`PGPDNLoss.forward()` returns the total loss and each component:

```text
loss, mae, neg, smooth
```

This mirrors the Section 3 training objective while keeping the terms independently inspectable in code.
