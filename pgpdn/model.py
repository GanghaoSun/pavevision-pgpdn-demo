"""PG-PDN model architecture for public method inspection.

Inputs:
    Tensor shaped (..., 12) in the feature order documented in constants.py.

Outputs:
    Predicted deterioration in normalized PQI* units and in PQI* points.

Chapter:
    Manuscript subsection: Physics-guided pavement degradation prediction network.

Notes:
    This file provides architecture code only. No trained weights from the
    raw field data are included in the public package.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import torch
from torch import Tensor, nn
import torch.nn.functional as F

from .constants import PHYSICAL_PARAMETER_DEFAULTS


@dataclass
class PGPDNConfig:
    """Configuration matching the manuscript unless explicitly changed."""

    input_dim: int = 12
    residual_input_dim: int = 8
    hidden_dim: int = 16
    dropout: float = 0.1
    pqi_scale: float = 100.0
    parameter_clip_ratio: float = 0.5
    lambda_neg: float = 0.5
    lambda_smooth: float = 0.1


class PhysicalBranch(nn.Module):
    """Interpretable physical degradation branch.

    The branch implements:
        r_phys = max(0, alpha0 + alpha1*log(1+ESAL) + alpha2*P
                     + alpha3*DeltaT + alpha4*F
                     + sum(beta_k*D_k) + gamma*(1-I_mean)).

    Parameters are clipped to +/-50% of the initial values by default,
    matching the training strategy described in the manuscript.
    """

    def __init__(self, config: PGPDNConfig, defaults: Dict[str, float] | None = None) -> None:
        super().__init__()
        self.config = config
        defaults = defaults or PHYSICAL_PARAMETER_DEFAULTS
        ordered = [
            "alpha0",
            "alpha1",
            "alpha2",
            "alpha3",
            "alpha4",
            "beta1",
            "beta2",
            "beta3",
            "beta4",
            "gamma",
        ]
        initial = torch.tensor([defaults[name] for name in ordered], dtype=torch.float32)
        self.register_buffer("initial", initial)
        self.theta = nn.Parameter(initial.clone())

    def clipped_theta(self) -> Tensor:
        ratio = self.config.parameter_clip_ratio
        lower = self.initial * (1.0 - ratio)
        upper = self.initial * (1.0 + ratio)
        return torch.minimum(torch.maximum(self.theta, lower), upper)

    def forward(self, x: Tensor) -> Tensor:
        theta = self.clipped_theta()
        alpha0, alpha1, alpha2, alpha3, alpha4 = theta[:5]
        beta = theta[5:9]
        gamma = theta[9]

        esal = x[..., 1]
        precip = x[..., 2]
        temp_range = x[..., 3]
        low_temp_days = x[..., 4]
        distress = x[..., 5:9]
        intensity_mean = x[..., 9]

        rate = (
            alpha0
            + alpha1 * torch.log1p(torch.clamp(esal, min=0.0))
            + alpha2 * precip
            + alpha3 * temp_range
            + alpha4 * low_temp_days
            + torch.sum(beta * distress, dim=-1)
            + gamma * (1.0 - intensity_mean)
        )
        return torch.clamp(rate, min=0.0)


class PGPDN(nn.Module):
    """Physics-guided pavement degradation prediction network."""

    def __init__(self, config: PGPDNConfig | None = None) -> None:
        super().__init__()
        self.config = config or PGPDNConfig()
        self.physical = PhysicalBranch(self.config)
        self.gru = nn.GRU(
            input_size=self.config.residual_input_dim,
            hidden_size=self.config.hidden_dim,
            num_layers=1,
            batch_first=True,
        )
        self.dropout = nn.Dropout(self.config.dropout)
        self.fc = nn.Linear(self.config.hidden_dim, 1)

    def residual_inputs(self, x: Tensor) -> Tensor:
        pqi_norm = torch.clamp(x[..., 0:1] / self.config.pqi_scale, 0.0, 1.0)
        return torch.cat([pqi_norm, x[..., 5:9], x[..., 9:12]], dim=-1)

    def forward(self, x: Tensor) -> Dict[str, Tensor]:
        if x.shape[-1] != self.config.input_dim:
            raise ValueError(f"Expected last dimension {self.config.input_dim}, got {x.shape[-1]}")

        pqi_norm = torch.clamp(x[..., 0] / self.config.pqi_scale, 0.0, 1.0)
        r_phys = self.physical(x)
        delta_phys_norm = pqi_norm * r_phys

        residual_x = self.residual_inputs(x)
        if residual_x.ndim == 1:
            residual_x = residual_x.unsqueeze(0).unsqueeze(1)
        elif residual_x.ndim == 2:
            residual_x = residual_x.unsqueeze(1)
        gru_out, _ = self.gru(residual_x)
        residual_norm = self.fc(self.dropout(gru_out[:, -1, :])).squeeze(-1)

        delta_norm = delta_phys_norm + residual_norm
        next_pqi_points = torch.clamp(x[..., 0] - delta_norm * self.config.pqi_scale, min=0.0, max=100.0)
        return {
            "delta_norm": delta_norm,
            "delta_pqi_points": delta_norm * self.config.pqi_scale,
            "next_pqi_points": next_pqi_points,
            "physical_rate": r_phys,
            "physical_delta_norm": delta_phys_norm,
            "residual_delta_norm": residual_norm,
        }


class PGPDNLoss(nn.Module):
    """Composite loss used for PG-PDN training."""

    def __init__(self, config: PGPDNConfig | None = None) -> None:
        super().__init__()
        self.config = config or PGPDNConfig()

    def forward(self, pred_delta_norm: Tensor, target_delta_norm: Tensor, unit_ids: Tensor | None = None) -> Dict[str, Tensor]:
        mae = torch.mean(torch.abs(pred_delta_norm - target_delta_norm))
        neg = torch.mean(F.relu(-pred_delta_norm))
        smooth = pred_delta_norm.new_tensor(0.0)

        if unit_ids is not None and unit_ids.numel() == pred_delta_norm.numel():
            unique_units = torch.unique(unit_ids)
            unit_means = []
            for unit in unique_units:
                unit_means.append(torch.mean(pred_delta_norm[unit_ids == unit]))
            if len(unit_means) > 1:
                series = torch.stack(unit_means)
                smooth = torch.mean(torch.abs(series[1:] - series[:-1]))

        total = mae + self.config.lambda_neg * neg + self.config.lambda_smooth * smooth
        return {"loss": total, "mae": mae, "neg": neg, "smooth": smooth}
