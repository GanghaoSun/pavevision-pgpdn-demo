"""Plot a synthetic Frenet-coordinate PQI* map."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from pgpdn.visualization import plot_quality_scatter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs/synthetic_quality_map.png"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = pd.read_csv(args.features)
    plot_quality_scatter(frame, args.output)
    print(f"Wrote synthetic quality map to {args.output}")


if __name__ == "__main__":
    main()
