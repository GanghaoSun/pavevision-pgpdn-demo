# Supplementary Methods: Public PG-PDN Demonstration

This note documents the public implementation scope for the PG-PDN demonstration package. It is intended to help readers inspect the model structure without exposing restricted field data or trained weights.

## S1. Feature Vector

The public code follows the 12-dimensional feature vector used in the manuscript:

`[PQI*, ESAL, P, DeltaT, F, D1, D2, D3, D4, I_mean, I_std, I_low]`.

The first component is the current grid-level quality index. ESAL is expressed in units of 10^4. Precipitation, temperature range and low-temperature days retain their engineering units in the physical branch. Distress densities and LiDAR intensity features are grid-level variables in [0, 1].

In the Python feature schema this index is named `pqi_star`. In the processed web-demo JSON files (`web_demo/data/`) the same index appears under the field name `PQI_extended`; both denote the manuscript PQI* index, defined as PQI* = 100 - PCI.

## S2. PG-PDN Architecture

PG-PDN contains two branches:

- Physical branch: an interpretable non-negative deterioration-rate function initialized from engineering knowledge and clipped within +/-50% of its initial parameters during training.
- GRU residual branch: a single-layer GRU with hidden dimension 16 and dropout 0.1. It receives `[PQI*, D1, D2, D3, D4, I_mean, I_std, I_low]` and predicts a residual correction.

The predicted deterioration is the sum of the physical deterioration and the residual correction. The public implementation exposes this architecture but does not include trained weights.

## S3. Loss Function

The composite loss contains:

- MAE loss for deterioration magnitude.
- Non-negative deterioration penalty.
- Along-route smoothness penalty on 20 m maintenance-unit predictions.

The default coefficients are `lambda_neg = 0.5` and `lambda_smooth = 0.1`, matching the manuscript.

## S4. Visualization

The public visualization functions support:

- Frenet-coordinate grid-level PQI* maps.
- Residual maps when user-supplied predictions are available.
- Figure templates for manuscript-style outputs.

The repository also includes a browser-based PaveVision web demo under `web_demo/`. Its frontend layout follows the manuscript system interface, while the backend serves processed public sample JSON files and precomputed PG-PDN demo outputs. The demo is intended for workflow inspection only; it does not expose raw point clouds, full-route data, trained full-data weights or the restricted prediction pipeline.

The standalone sample figures in `assets/` illustrate the manuscript-style visualization workflow. They should not be interpreted as an additional validation dataset beyond the experiments reported in the manuscript.
