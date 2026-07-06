# Method Scope

This page explains the PG-PDN method layer within the public PaveVision demonstration package.

## Provided

| Area | Provided files |
| --- | --- |
| PG-PDN source implementation | `pgpdn/model.py` |
| Feature names and validation utilities | `pgpdn/constants.py`, `pgpdn/features.py` |
| Default architecture and loss configuration | `configs/pgpdn_default.yaml` |
| Equation-to-code traceability | `docs/equation_to_code_mapping.md` |
| Input-field contract | `docs/input_contract.md` |
| PaveVision UI boundary | `pavevision_ui/` |
| Public route and visualization package | `web_demo/`, `web_demo/data/sample/`, `assets/`, `docs/data_schema.md` |

## Method Boundary

The method layer covers the implementation of the PG-PDN method described in manuscript Section 3:

- the physical degradation branch;
- the residual GRU branch;
- the final deterioration and next-period PQI* outputs;
- the composite loss terms;
- the field names, tensor shapes, units and constraints expected by the method;
- the interface boundary between the PG-PDN method layer and the PaveVision UI layer.

The public demonstration layer provides processed route-quality JSON files, interface screenshots and manuscript-style grid figures so reviewers can inspect the assessment-to-prediction workflow alongside the PG-PDN source code.

## Intended Review Use

Readers can use this repository to answer four method-coverage questions:

1. Where is each Section 3 method component implemented?
2. What exact tensor contract does PG-PDN expect?
3. How are the physical branch, residual branch and loss terms connected in code?
4. How does the PaveVision presentation layer consume PG-PDN method outputs?

The recommended entry points are [docs/equation_to_code_mapping.md](equation_to_code_mapping.md), [docs/input_contract.md](input_contract.md) and [pgpdn/model.py](../pgpdn/model.py).
