# Changelog

## 2026-07-06

- Restored the rich reviewer-facing README from the `b9a06ca` release style, including Web demo screenshots, manuscript-style grid figures, quick-start commands, route package details, API documentation, quality checks and update record.
- Restored the previously removed `web_demo/`, example scripts, sample CSV, GitHub Actions workflow, tests and the tracked `assets/fig10*.png` and `assets/web_*.png` images.
- Kept the new method-coverage additions: `docs/equation_to_code_mapping.md`, `docs/method_scope.md`, `docs/input_contract.md`, Section 3 comments in `pgpdn/model.py` and the `pavevision_ui/` source skeleton.

## 2026-06-28

- Rewrote the README as a reviewer-facing project homepage with richer visual guidance, quick-start commands, API documentation, repository structure and manuscript-to-code mapping.
- Added the CI badge to the README, documented expected command outputs and cleaned the public package test logs.
- Refined README and supplementary release statements so public pages focus on the materials available in this repository.
- Added documentation pages for the public workflow, data schema and manuscript-to-code mapping.
- Added `CITATION.cff` for citation metadata.
- Added unit tests for public documentation text, data manifest consistency, PG-PDN model outputs and Flask API endpoints.
- Added GitHub Actions CI for the public package checks.
- Aligned PaveVision web-demo model descriptions with the included precomputed route outputs.

## 2026-06-07

- Updated the PaveVision web system to use processed pavement quality data for all three routes.
- Added precomputed PG-PDN prediction outputs, refreshed screenshots and responsive maintenance-unit views.

## 2026-06-03

- Added the initial public PG-PDN demo package with model code, configuration files, examples, sample data and a Flask web demo.
