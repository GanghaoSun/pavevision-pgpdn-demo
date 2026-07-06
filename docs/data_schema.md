# Data Schema

This page documents the public CSV and JSON interfaces used by the demonstration package.

## PG-PDN CSV Feature Table

`sample_data/synthetic_grid_features.csv` contains the public feature-table schema:

| Column | Meaning |
| --- | --- |
| `s_m` | Frenet arc length in meters, used for visualization. |
| `d_m` | Lateral offset in meters, used for visualization. |
| `unit_id` | 20 m maintenance-unit identifier. |
| `pqi_star` | Current grid-level PQI* value. |
| `esal_1e4` | ESAL in units of 10^4 passes. |
| `precip_mm` | Precipitation in millimeters. |
| `temp_range_c` | Mean daily temperature range in degrees Celsius. |
| `low_temp_days` | Number of low-temperature days. |
| `density_transverse` | Transverse crack density. |
| `density_longitudinal` | Longitudinal crack density. |
| `density_alligator` | Alligator crack density. |
| `density_pothole` | Pothole density. |
| `intensity_mean` | Mean LiDAR intensity feature. |
| `intensity_std` | Standard deviation of LiDAR intensity. |
| `intensity_low_prop` | Proportion of low-intensity cells. |

The model consumes the following 12 columns in manuscript order:

```text
pqi_star, esal_1e4, precip_mm, temp_range_c, low_temp_days,
density_transverse, density_longitudinal, density_alligator, density_pothole,
intensity_mean, intensity_std, intensity_low_prop
```

## PaveVision JSON Files

The web demo reads processed JSON files from `web_demo/data/sample/`.

Assessment files use names such as:

```text
route1_2026.assessment.json
route1_2026_predicted.assessment.json
```

Grid files use names such as:

```text
route1_2026.grid_0.5.json
route1_2026_predicted.grid_0.5.json
```

The `manifest.json` file lists all generated files and records the total route length used by the public demo.

## Route Labels

The public route labels match the manuscript route definitions:

| Route | Label |
| --- | --- |
| `route1` | Suburban closed-loop route |
| `route2` | Urban lane-changing route |
| `route3` | Industrial straight route |
