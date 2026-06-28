# Public Inspection Workflow

This guide describes the checks that can be run directly from the repository.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r web_demo/requirements.txt
```

## 2. Run Automated Checks

```bash
python -m unittest discover -s tests
```

The tests check package imports, model tensor outputs, web API endpoints, manifest consistency and public-facing documentation text.

## 3. Start PaveVision

```bash
python web_demo/app.py
```

Open `http://localhost:5000` and inspect the route map, pavement quality assessment and one-step-ahead prediction views.

## 4. Inspect Model Inputs

The public feature order is:

```text
[PQI*, ESAL, P, DeltaT, F, D1, D2, D3, D4, I_mean, I_std, I_low]
```

The Python column names are defined in `pgpdn/constants.py`.

## 5. Run the Synthetic Example

```bash
python examples/run_inference_template.py --features sample_data/synthetic_grid_features.csv
```

This verifies the CSV schema, constructs a PG-PDN model instance and writes demonstration predictions to `outputs/synthetic_predictions.csv`.
