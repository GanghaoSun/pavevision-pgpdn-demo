# PaveVision UI Interface Contract

This document describes the source-level interface expected between the PG-PDN method layer and a PaveVision UI layer. It contains field names and responsibilities only.

## Method Output Fields

| Field | Source |
| --- | --- |
| `delta_norm` | `pgpdn.model.PGPDN.forward()` |
| `delta_pqi_points` | `pgpdn.model.PGPDN.forward()` |
| `next_pqi_points` | `pgpdn.model.PGPDN.forward()` |
| `physical_rate` | `pgpdn.model.PGPDN.forward()` |
| `physical_delta_norm` | `pgpdn.model.PGPDN.forward()` |
| `residual_delta_norm` | `pgpdn.model.PGPDN.forward()` |

## UI Panel Responsibilities

| Panel | Responsibility |
| --- | --- |
| Quality assessment | Present current pavement quality fields supplied by an upstream application. |
| Degradation prediction | Present PG-PDN predicted deterioration and next-period PQI*. |
| Branch attribution | Present physical and residual contributions when supplied by the method layer. |
| Method metadata | Present configuration names, feature names and model-output labels. |

## Separation Rule

The UI layer should consume method outputs and metadata through named fields. It should not redefine PG-PDN feature order, physical-branch coefficients or loss weights.
