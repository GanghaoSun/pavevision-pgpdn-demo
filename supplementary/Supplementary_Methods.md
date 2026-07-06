# Supplementary Methods: PG-PDN Method Implementation

This note documents the method implementation scope for the PG-PDN package. It is intended to help readers inspect the model structure, input contract and Section 3 equation-to-code mapping.

## S1. Feature Vector

The code follows the 12-dimensional feature vector used in the manuscript:

`[PQI*, ESAL, P, DeltaT, F, D1, D2, D3, D4, I_mean, I_std, I_low]`.

The first component is the current grid-level quality index. ESAL is expressed in units of 10^4. Precipitation, temperature range and low-temperature days retain their engineering units in the physical branch. Distress densities and LiDAR intensity features are grid-level variables in `[0, 1]`.

In the Python feature contract this index is named `pqi_star`, and it denotes the manuscript PQI* index, defined as PQI* = 100 - PCI.

## S2. PG-PDN Architecture

PG-PDN contains two branches:

- Physical branch: an interpretable non-negative deterioration-rate function initialized from engineering knowledge and clipped within +/-50% of its initial parameters during training.
- GRU residual branch: a single-layer GRU with hidden dimension 16 and dropout 0.1. It receives `[PQI*, D1, D2, D3, D4, I_mean, I_std, I_low]` and predicts a residual correction.

The predicted deterioration is the sum of the physical deterioration and the residual correction. The implementation exposes the architecture, tensor interface and prediction components needed to inspect the method.

## S3. Loss Function

The composite loss contains:

- MAE loss for deterioration magnitude.
- Non-negative deterioration penalty.
- Along-route smoothness penalty on maintenance-unit predictions.

The default coefficients are `lambda_neg = 0.5` and `lambda_smooth = 0.1`, matching the method configuration.

## S4. PaveVision Interface Boundary

The `pavevision_ui/` directory documents the source-level interface boundary between the PG-PDN method layer and a PaveVision front end. It records expected method outputs and UI responsibilities without including route-specific records.
