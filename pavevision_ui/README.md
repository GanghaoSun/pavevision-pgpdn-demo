# PaveVision UI Source Skeleton

This directory records the source-level boundary for a PaveVision interface that consumes PG-PDN method outputs.

The UI layer is treated as a separate presentation layer. In this repository it is represented as an interface skeleton so readers can see how the method layer is expected to connect to a PaveVision front end.

## Boundary

| Layer | Responsibility |
| --- | --- |
| `pgpdn/` | Defines the PG-PDN feature contract, model outputs and loss terms. |
| `configs/` | Defines default model dimensions, physical-branch parameters and loss weights. |
| `pavevision_ui/` | Documents UI-facing payload names and presentation responsibilities. |

## Included

- Method-output field names expected by the UI layer.
- UI panel responsibilities at a source-design level.
- Separation between model computation and presentation.

## Related Public Package Files

- Browser service and API endpoints: [`web_demo/`](../web_demo/)
- Processed route-quality JSON files: [`web_demo/data/sample/`](../web_demo/data/sample/)
- Interface screenshots and manuscript-style figures: [`assets/`](../assets/)
- Route and feature schema documentation: [`docs/data_schema.md`](../docs/data_schema.md)

See [interface_contract.md](interface_contract.md) for the UI-facing contract.
