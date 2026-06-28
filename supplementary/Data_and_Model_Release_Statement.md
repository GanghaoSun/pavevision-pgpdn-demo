# Data and Model Release Statement

This repository provides the public software and demonstration materials associated with the manuscript "Physics-guided pavement degradation prediction from grid-level semantic distress maps".

## Released Materials

- PG-PDN source code and configuration files.
- Processed pavement quality data for all three surveyed routes at their full length (about 5.40 km in total), covering the 0.5 m grid-level and 20 m maintenance-unit assessment views for three survey periods.
- Precomputed PG-PDN prediction outputs used by the PaveVision web system.
- The PaveVision web system, including front-end pages and Flask API endpoints.
- Feature-schema templates and a synthetic feature table for interface checks.
- Figure-generation utilities and plotting templates.
- Supplementary method notes and public workflow documentation.

## Reproducible Public Workflow

The repository supports the following checks directly from the files in this package:

1. Inspect the PG-PDN model equations, feature order and loss terms.
2. Run the web demo and review route-level quality assessment and prediction views.
3. Load processed 0.5 m grid-level and 20 m maintenance-unit JSON files.
4. Run the synthetic feature-table example through the public PG-PDN interface.
5. Execute the unit tests to verify imports, endpoints, manifest consistency and public-facing documentation text.

## Notes

The processed data and code released here allow readers to inspect the model equations, the software interfaces and the quality-assessment and degradation-prediction workflow. The PaveVision prediction view reads the precomputed PG-PDN outputs for the three routes.
