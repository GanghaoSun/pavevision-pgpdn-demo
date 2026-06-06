# Data and Model Release Statement

This repository is released in stages alongside the associated manuscript.

## Currently Released

- PG-PDN source code and configuration files.
- Processed pavement quality data for all three surveyed routes at their full
  length (about 5.40 km in total), covering the 0.5 m grid-level and 20 m
  maintenance-unit assessments for the three survey periods.
- Precomputed PG-PDN prediction outputs used by the PaveVision web system.
- The PaveVision web system (front-end and back-end).
- Feature-schema templates.
- Figure-generation utilities and plotting templates.
- Supplementary method notes.

## Planned Additions

The repository will be updated progressively as the manuscript advances through
peer review and publication. Materials to be added after acceptance include
extended documentation and reproducibility examples, together with the upstream
multi-sensor perception resources (raw point clouds, images and the segmentation
pipeline), which are developed as separate work and are therefore not part of the
current release.

## Notes

The processed data and code released here allow readers to inspect the model
equations, the software interfaces and the complete quality-assessment and
degradation-prediction workflow, and to reproduce the manuscript's grid-level and
unit-level results. The PaveVision prediction view reads the precomputed PG-PDN
outputs for the three routes.
