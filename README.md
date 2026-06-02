# PaveVision PG-PDN Demonstration Package

This repository accompanies the manuscript "Physics-guided pavement degradation prediction from grid-level semantic distress maps".

The package is designed for method inspection and software reuse. It exposes the PG-PDN architecture, feature schema, loss function, visualization utilities and synthetic demonstration records. It does not include raw point clouds, full-route feature tables, trained model weights, author-specific working files or any data needed to reconstruct the restricted field surveys.

## PaveVision Interface Preview

PaveVision is an English-language pavement quality assessment and performance-prediction interface built around semantic distress maps and grid-level PG-PDN inference. The screenshots below illustrate the public demonstration workflow and visual layout; they are provided as interface previews rather than additional experimental evidence.

### Route Map and Quality Popup

The route-map view provides the first entry point for pavement engineers. Clicking a route opens a quality summary popup with the survey period, public sample length, mean PQI*, distress deduction, number of 20 m maintenance units and 0.5 m grid resolution.

![PaveVision route map with pavement quality popup](assets/web_route_map_popup.png)

### Pavement Quality Assessment

![PaveVision pavement quality assessment module](assets/web_quality_module.png)

### Performance Prediction

![PaveVision performance prediction module](assets/web_prediction_module.png)

### PG-PDN Network Architecture

The PG-PDN architecture combines an interpretable physical degradation branch with a GRU residual correction branch. This public package keeps the model interface, feature schema, loss terms and visualization workflow consistent with the manuscript, while withholding full survey data and trained full-data weights.

![PG-PDN network architecture](assets/pgpdn_architecture.png)

### Historical Measurements and PG-PDN Prediction at 0.5 m Resolution

The fig10 series visualizes Route 3 at 0.5 m grid resolution: March 2024 measured quality, March 2025 measured quality, March 2026 PG-PDN prediction, March 2026 measured quality and the prediction residual. These images illustrate measured-to-predicted spatial continuity rather than a comparison among different learning algorithms.

#### March 2024 Measured

![Route 3 March 2024 measured grid-level PQI*](assets/fig10a_route3_2024_measured.png)

#### March 2025 Measured

![Route 3 March 2025 measured grid-level PQI*](assets/fig10b_route3_2025_measured.png)

#### March 2026 Predicted

![Route 3 March 2026 PG-PDN predicted grid-level PQI*](assets/fig10c_route3_2026_predicted.png)

#### March 2026 Measured

![Route 3 March 2026 measured grid-level PQI*](assets/fig10d_route3_2026_measured.png)

#### Prediction Residual

![Route 3 grid-level PG-PDN prediction residual](assets/fig10e_route3_prediction_residual.png)

## What Is Included

- `pgpdn/`: lightweight Python implementation of the PG-PDN inference architecture.
- `configs/pgpdn_default.yaml`: architecture and physical-parameter defaults reported in the manuscript.
- `examples/`: runnable examples using synthetic data only.
- `sample_data/`: small synthetic feature tables for checking input/output formats.
- `supplementary/`: method notes, data-release statement and figure-generation guidance.

## What Is Not Included

- Raw mobile mapping point clouds, images or LiDAR scans.
- Full-route survey data and full-route feature tables.
- Trained PG-PDN checkpoints or any learned full-data model weights.
- Data that can identify survey routes beyond the non-sensitive descriptions reported in the paper.

## Feature Schema

Each grid cell is represented by the 12-dimensional feature vector used in the manuscript:

```text
[PQI*, ESAL, P, DeltaT, F, D1, D2, D3, D4, I_mean, I_std, I_low]
```

where `PQI*` is the current grid-level pavement quality index, `ESAL` is expressed in units of 10^4, `P` is precipitation in mm, `DeltaT` is the mean daily temperature range in degrees Celsius, `F` is the number of low-temperature days with mean daily temperature below 0 degC, `D1`--`D4` are distress densities for transverse cracks, longitudinal cracks, alligator cracks and potholes, and `I_mean`, `I_std`, `I_low` are LiDAR intensity features.

## Quick Start

Install the minimal dependencies:

```bash
pip install -r requirements.txt
```

Run the synthetic inference example:

```bash
python examples/run_inference_template.py --features sample_data/synthetic_grid_features.csv
```

Generate a synthetic quality-map preview:

```bash
python examples/plot_synthetic_quality_map.py --features sample_data/synthetic_grid_features.csv --output outputs/synthetic_quality_map.png
```

The default model uses initialized physical parameters and random neural weights. The numerical outputs are not calibrated predictions; they are provided only to verify the architecture and data flow.

## Citation

Please cite the associated manuscript if you use this code or adapt the PG-PDN architecture.
