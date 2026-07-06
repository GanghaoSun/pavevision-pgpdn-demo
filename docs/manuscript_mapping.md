# Manuscript-to-Repository Mapping

This page maps the main manuscript components to repository files that support method-level inspection.

| Manuscript component | Repository files |
| --- | --- |
| Section 3 method scope | `docs/method_scope.md` |
| PG-PDN feature vector | `pgpdn/constants.py`, `pgpdn/features.py`, `docs/input_contract.md` |
| Physical degradation branch | `pgpdn/model.py`, `configs/pgpdn_default.yaml` |
| GRU residual branch | `pgpdn/model.py` |
| Composite loss terms | `pgpdn/model.py`, `configs/pgpdn_default.yaml` |
| Equation-to-code traceability | `docs/equation_to_code_mapping.md` |
| PaveVision UI boundary | `pavevision_ui/README.md`, `pavevision_ui/interface_contract.md` |
| Architecture figure | `assets/pgpdn_architecture.png` |

The mapping is intended to help readers move from the manuscript description to the exact implementation files in this repository.
