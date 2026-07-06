# Method Scope

This repository is maintained as a method-level companion for PG-PDN.

## Provided

| Area | Provided files |
| --- | --- |
| PG-PDN source implementation | `pgpdn/model.py` |
| Feature names and validation utilities | `pgpdn/constants.py`, `pgpdn/features.py` |
| Default architecture and loss configuration | `configs/pgpdn_default.yaml` |
| Equation-to-code traceability | `docs/equation_to_code_mapping.md` |
| Input-field contract | `docs/input_contract.md` |
| PaveVision UI boundary | `pavevision_ui/` |

## Method Boundary

The repository covers the implementation of the PG-PDN method described in manuscript Section 3:

- the physical degradation branch;
- the residual GRU branch;
- the final deterioration and next-period PQI* outputs;
- the composite loss terms;
- the field names, tensor shapes, units and constraints expected by the method;
- the interface boundary between the PG-PDN method layer and the PaveVision UI layer.

The repository does not present route records, inspection frames, point clouds, imagery, 0.5 m grid outputs, 20 m maintenance-unit tables or field-survey measurement tables.

## Intended Review Use

Readers can use this repository to answer three method-coverage questions:

1. Where is each Section 3 method component implemented?
2. What exact tensor contract does PG-PDN expect?
3. How are the physical branch, residual branch and loss terms connected in code?

The recommended entry points are [docs/equation_to_code_mapping.md](equation_to_code_mapping.md), [docs/input_contract.md](input_contract.md) and [pgpdn/model.py](../pgpdn/model.py).
