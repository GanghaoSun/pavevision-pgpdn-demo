# Method Inspection Workflow

This page lists the method-level inspection path for readers who want to trace the manuscript method into source code.

## 1. Inspect the Method Scope

Start with [docs/method_scope.md](method_scope.md) to see what the repository is designed to cover.

## 2. Trace Section 3 to Code

Use [docs/equation_to_code_mapping.md](equation_to_code_mapping.md) to locate each PG-PDN branch, output equation and loss component.

## 3. Review the Input Contract

Use [docs/input_contract.md](input_contract.md) to check field names, tensor shapes, units and constraints.

## 4. Read the Core Method Files

The central files are:

- [pgpdn/model.py](../pgpdn/model.py)
- [pgpdn/constants.py](../pgpdn/constants.py)
- [pgpdn/features.py](../pgpdn/features.py)
- [configs/pgpdn_default.yaml](../configs/pgpdn_default.yaml)

## 5. Inspect the PaveVision UI Boundary

The UI boundary is documented in [pavevision_ui/](../pavevision_ui/). It records the intended source-level interface between the PG-PDN method layer and a PaveVision front end.
