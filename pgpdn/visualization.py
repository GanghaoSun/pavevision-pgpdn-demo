"""Visualization helpers for synthetic PG-PDN demonstrations.

The functions here are intentionally data-agnostic. They operate on tables
with Frenet coordinates and PQI* values and do not require restricted survey
data or model weights.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap


QUALITY_CMAP = LinearSegmentedColormap.from_list(
    "pqi_star",
    [
        (0.00, "#d7191c"),
        (0.60, "#fdae61"),
        (0.70, "#fee08b"),
        (0.80, "#a6d96a"),
        (0.90, "#1a9641"),
        (1.00, "#006837"),
    ],
)


def plot_quality_scatter(frame: pd.DataFrame, output: str | Path, value_col: str = "pqi_star") -> None:
    """Plot a simple Frenet-coordinate PQI* scatter map."""
    required = {"s_m", "d_m", value_col}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing plotting columns: {sorted(missing)}")

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8.5, 2.8), constrained_layout=True)
    sc = ax.scatter(
        frame["s_m"],
        frame["d_m"],
        c=np.clip(frame[value_col], 0, 100),
        cmap=QUALITY_CMAP,
        vmin=0,
        vmax=100,
        s=24,
        marker="s",
        linewidths=0,
    )
    ax.set_xlabel("Arc length s (m)")
    ax.set_ylabel("Lateral offset d (m)")
    ax.set_title("Synthetic grid-level PQI* map")
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label("PQI*")
    fig.savefig(output, dpi=300)
    plt.close(fig)

