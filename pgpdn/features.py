"""Feature loading and validation utilities for PG-PDN.

Inputs:
    CSV files with the 12 feature columns listed in pgpdn.constants.FEATURE_COLUMNS.

Outputs:
    Pandas DataFrames or NumPy arrays ready for PG-PDN inference.

Chapter:
    Manuscript subsection: Prediction task and feature vector (PG-PDN).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .constants import FEATURE_COLUMNS


def validate_feature_table(frame: pd.DataFrame, columns: Iterable[str] = FEATURE_COLUMNS) -> None:
    """Validate that a feature table follows the public PG-PDN schema."""
    missing = [name for name in columns if name not in frame.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    numeric = frame[list(columns)].apply(pd.to_numeric, errors="coerce")
    bad = numeric.isna().any(axis=1)
    if bool(bad.any()):
        first_bad = int(np.flatnonzero(bad.to_numpy())[0])
        raise ValueError(f"Non-numeric or missing feature value at row {first_bad}")

    if not frame["pqi_star"].between(0, 100).all():
        raise ValueError("pqi_star must be in [0, 100].")

    density_cols = [
        "density_transverse",
        "density_longitudinal",
        "density_alligator",
        "density_pothole",
        "intensity_mean",
        "intensity_std",
        "intensity_low_prop",
    ]
    for name in density_cols:
        if not frame[name].between(0, 1).all():
            raise ValueError(f"{name} must be in [0, 1].")


def load_feature_table(path: str | Path) -> pd.DataFrame:
    """Load and validate a PG-PDN feature table."""
    frame = pd.read_csv(path)
    validate_feature_table(frame)
    return frame


def feature_array(frame: pd.DataFrame) -> np.ndarray:
    """Return the 12-dimensional feature matrix in manuscript order."""
    validate_feature_table(frame)
    return frame[FEATURE_COLUMNS].to_numpy(dtype=np.float32)

