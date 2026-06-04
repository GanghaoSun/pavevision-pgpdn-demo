# Data and Model Release Statement

The public release is intentionally limited to method-inspection materials.

## Planned Updates

This repository will be updated progressively as the associated manuscript advances through peer review and publication. Additional documentation, examples, processed demonstration data and reproducibility materials may be added after the manuscript is accepted and the corresponding data-sharing permissions are confirmed.

At the current pre-publication stage, full survey materials, full-route feature tables, trained full-data weights and restricted training or inference pipelines are intentionally withheld to protect unpublished research results and to comply with institutional data-sharing constraints.

## Publicly Included

- PG-PDN source code and configuration files.
- Feature-schema templates.
- Synthetic demonstration records.
- PaveVision frontend demonstration code.
- Processed 600 m public sample JSON files for interface demonstration.
- Precomputed PG-PDN demo outputs used by the public web interface.
- Figure-generation utilities and plotting templates.
- Supplementary method notes.

## Not Publicly Included

- Raw mobile mapping point clouds, images or LiDAR scans.
- Full-route feature tables used in the manuscript experiments.
- Trained PG-PDN weights or any full-data model parameters.
- Core training scripts, full-data inference services or restricted prediction pipelines.
- Raw GPS logs or complete route-level files that could reconstruct restricted survey assets.

## Rationale

The field surveys were collected under institutional data-sharing restrictions. The public package therefore enables readers to inspect the model equations, software interfaces and visualization workflow while preventing reconstruction of confidential survey data or learned parameters derived from the full restricted dataset. The web demo prediction button reads precomputed public outputs; it does not execute the restricted PG-PDN training or full-data inference pipeline.
