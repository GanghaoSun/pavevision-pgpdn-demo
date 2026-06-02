"""Run PG-PDN inference on a public feature-schema table.

This script uses initialized model parameters unless a user supplies their own
checkpoint in downstream work. It is a schema and architecture demonstration,
not a reproduction of the restricted-data results in the manuscript.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd
import torch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from pgpdn.features import feature_array, load_feature_table
from pgpdn.model import PGPDN, PGPDNConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", type=Path, required=True, help="CSV file following the PG-PDN feature schema.")
    parser.add_argument("--output", type=Path, default=Path("outputs/synthetic_predictions.csv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load_feature_table(args.features)
    x = torch.from_numpy(feature_array(frame))

    model = PGPDN(PGPDNConfig())
    model.eval()
    with torch.no_grad():
        output = model(x)

    result = frame.copy()
    result["delta_pqi_points_demo"] = output["delta_pqi_points"].cpu().numpy()
    result["next_pqi_points_demo"] = output["next_pqi_points"].cpu().numpy()
    result["physical_rate_demo"] = output["physical_rate"].cpu().numpy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Wrote demonstration predictions to {args.output}")
    print("These outputs use initialized parameters only and are not calibrated field predictions.")
    print(pd.DataFrame(result[["pqi_star", "delta_pqi_points_demo", "next_pqi_points_demo"]]).head())


if __name__ == "__main__":
    main()
