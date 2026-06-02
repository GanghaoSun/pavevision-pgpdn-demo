"""Shared constants for the PG-PDN demonstration package."""

FEATURE_COLUMNS = [
    "pqi_star",
    "esal_1e4",
    "precip_mm",
    "temp_range_c",
    "low_temp_days",
    "density_transverse",
    "density_longitudinal",
    "density_alligator",
    "density_pothole",
    "intensity_mean",
    "intensity_std",
    "intensity_low_prop",
]

DISTRESS_COLUMNS = [
    "density_transverse",
    "density_longitudinal",
    "density_alligator",
    "density_pothole",
]

INTENSITY_COLUMNS = [
    "intensity_mean",
    "intensity_std",
    "intensity_low_prop",
]

PHYSICAL_PARAMETER_DEFAULTS = {
    "alpha0": 0.008,
    "alpha1": 0.012,
    "alpha2": 0.00020,
    "alpha3": 0.0010,
    "alpha4": 0.0030,
    "beta1": 0.0050,
    "beta2": 0.0040,
    "beta3": 0.0120,
    "beta4": 0.0150,
    "gamma": 0.0100,
}

