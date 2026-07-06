# Changelog

## 2026-07-06

- Added `docs/equation_to_code_mapping.md` to map manuscript Section 3 equations, the physical branch, the residual branch and loss terms to exact code locations.
- Added `docs/method_scope.md` to define the repository as a PG-PDN method implementation, configuration and interface-definition package.
- Added `docs/input_contract.md` to specify required field names, tensor shapes, units and constraints without example records.
- Added Section 3 mapping comments and docstrings for `PhysicalBranch`, `PGPDN` and `PGPDNLoss` in `pgpdn/model.py`.
- Strengthened `pgpdn/features.py` validation so the code contract matches the documented field constraints.
- Reworked the README and supplementary pages around method inspection, source traceability and the PaveVision UI boundary.
- Replaced the previous browser presentation folder with `pavevision_ui/`, a source skeleton that documents UI-facing method outputs and responsibilities.
- Removed tracked scripts, JSON files and auxiliary scaffolding that were outside the method-implementation scope.
- Restricted `.gitignore` so only the PG-PDN architecture image is intentionally tracked under `assets/`.

## 2026-06-28

- Reorganized the repository homepage and supporting documentation for reviewer-facing method inspection.
- Added citation metadata and manuscript-to-repository mapping documentation.

## 2026-06-03

- Added the initial PG-PDN source package with model code, configuration files and repository documentation.
