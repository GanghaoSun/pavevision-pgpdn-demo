# PG-PDN Input Contract

This document specifies field names, tensor shapes, units and constraints for the PG-PDN method implementation. It intentionally contains no example records.

## Model Feature Tensor

| Item | Contract |
| --- | --- |
| Tensor name | `x` |
| Accepted shape | `(..., 12)` |
| Final dimension order | `[pqi_star, esal_1e4, precip_mm, temp_range_c, low_temp_days, density_transverse, density_longitudinal, density_alligator, density_pothole, intensity_mean, intensity_std, intensity_low_prop]` |
| Numeric type | Floating point |
| PQI* scale | 0 to 100 points |
| Internal normalized PQI* | `pqi_star / 100.0`, clipped to `[0, 1]` |

## Required Fields

| Index | Field name | Manuscript symbol | Unit | Constraint |
| ---: | --- | --- | --- | --- |
| 0 | `pqi_star` | `PQI*` | points | `[0, 100]` |
| 1 | `esal_1e4` | `ESAL` | `10^4` equivalent standard axles | `>= 0` |
| 2 | `precip_mm` | `P` | mm | `>= 0` |
| 3 | `temp_range_c` | `DeltaT` | deg C | `>= 0` |
| 4 | `low_temp_days` | `F` | days | `>= 0` |
| 5 | `density_transverse` | `D1` | ratio | `[0, 1]` |
| 6 | `density_longitudinal` | `D2` | ratio | `[0, 1]` |
| 7 | `density_alligator` | `D3` | ratio | `[0, 1]` |
| 8 | `density_pothole` | `D4` | ratio | `[0, 1]` |
| 9 | `intensity_mean` | `I_mean` | normalized intensity | `[0, 1]` |
| 10 | `intensity_std` | `I_std` | normalized intensity dispersion | `[0, 1]` |
| 11 | `intensity_low_prop` | `I_low` | ratio | `[0, 1]` |

## Residual-Branch Tensor

`PGPDN.residual_inputs()` constructs an internal residual tensor with final dimension `8`:

| Internal order | Source field |
| ---: | --- |
| 0 | normalized `pqi_star` |
| 1 | `density_transverse` |
| 2 | `density_longitudinal` |
| 3 | `density_alligator` |
| 4 | `density_pothole` |
| 5 | `intensity_mean` |
| 6 | `intensity_std` |
| 7 | `intensity_low_prop` |

Before entering the GRU, a two-dimensional tensor with shape `(batch, 8)` is reshaped to `(batch, 1, 8)`.

## Optional Loss Input

| Tensor | Shape | Constraint | Used by |
| --- | --- | --- | --- |
| `unit_ids` | Same number of elements as `pred_delta_norm` | Integer maintenance-unit identifiers | `PGPDNLoss.forward()` smoothness term |

`unit_ids` is optional. When it is omitted, the smoothness component is zero.

## Model Output Contract

| Output key | Shape | Unit |
| --- | --- | --- |
| `delta_norm` | Matches the leading shape of `x` | normalized PQI* deterioration |
| `delta_pqi_points` | Matches the leading shape of `x` | PQI* points |
| `next_pqi_points` | Matches the leading shape of `x` | PQI* points |
| `physical_rate` | Matches the leading shape of `x` | non-negative deterioration rate |
| `physical_delta_norm` | Matches the leading shape of `x` | normalized PQI* deterioration |
| `residual_delta_norm` | Matches the leading shape of `x` | normalized PQI* deterioration |
