"""PaveVision public web demo service.

This service intentionally serves precomputed demonstration outputs. The
prediction button in the frontend loads JSON files prepared for the public demo;
it does not train PG-PDN, load full-data weights or run the restricted research
prediction pipeline.
"""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

from flask import Flask, Response, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "sample"
ROUTE_DISPLAY_PATH = BASE_DIR / "data" / "route_display.json"

ROUTES = [
    {
        "id": "route1",
        "name": "Route 1",
        "description": "Suburban closed-loop route",
        "scenario": "Suburban closed-loop",
        "display_color": "#FF6B6B",
    },
    {
        "id": "route2",
        "name": "Route 2",
        "description": "Urban lane-changing route",
        "scenario": "Urban lane-changing",
        "display_color": "#4ECDC4",
    },
    {
        "id": "route3",
        "name": "Route 3",
        "description": "Industrial straight route",
        "scenario": "Industrial straight",
        "display_color": "#45B7D1",
    },
]

PERIODS = [
    {"id": "t1", "label": "t1 (Mar. 2024)", "year": 2024},
    {"id": "t2", "label": "t2 (Mar. 2025)", "year": 2025},
    {"id": "t3", "label": "t3 (Mar. 2026)", "year": 2026},
]

QUALITY_GRADES = {
    "Excellent": (90, 100),
    "Good": (80, 90),
    "Medium": (70, 80),
    "Poor": (60, 70),
    "Very poor": (0, 60),
}

GRADE_COLORS = {
    "Excellent": "#00C853",
    "Good": "#64DD17",
    "Medium": "#FFD600",
    "Poor": "#FF6D00",
    "Very poor": "#D50000",
}

TRAFFIC_BY_ROUTE = {
    "route1": {
        "esal_annual": 0.78,
        "eta_s": 0.35,
        "vehicle_types": [
            {"type": "Passenger car", "daily_count": 820, "C_eq": 0.0003, "note": "Passenger car <=2 t"},
            {"type": "Medium passenger car", "daily_count": 25, "C_eq": 0.105, "note": "2-5 t"},
            {"type": "Medium truck", "daily_count": 38, "C_eq": 0.183, "note": "2-7 t"},
            {"type": "Large truck", "daily_count": 20, "C_eq": 0.682, "note": "7-14 t"},
            {"type": "Heavy truck", "daily_count": 8, "C_eq": 2.512, "note": "14-30 t"},
            {"type": "Articulated or semitrailer", "daily_count": 3, "C_eq": 5.214, "note": ">30 t"},
        ],
    },
    "route2": {
        "esal_annual": 1.26,
        "eta_s": 0.40,
        "vehicle_types": [
            {"type": "Passenger car", "daily_count": 3520, "C_eq": 0.0003, "note": "Passenger car <=2 t"},
            {"type": "Medium passenger car", "daily_count": 85, "C_eq": 0.105, "note": "2-5 t"},
            {"type": "Medium truck", "daily_count": 75, "C_eq": 0.183, "note": "2-7 t"},
            {"type": "Large truck", "daily_count": 28, "C_eq": 0.682, "note": "7-14 t"},
            {"type": "Heavy truck", "daily_count": 10, "C_eq": 2.512, "note": "14-30 t"},
            {"type": "Articulated or semitrailer", "daily_count": 3, "C_eq": 5.214, "note": ">30 t"},
        ],
    },
    "route3": {
        "esal_annual": 11.34,
        "eta_s": 0.40,
        "vehicle_types": [
            {"type": "Passenger car", "daily_count": 605, "C_eq": 0.0003, "note": "Passenger car <=2 t"},
            {"type": "Medium passenger car", "daily_count": 15, "C_eq": 0.105, "note": "2-5 t"},
            {"type": "Medium truck", "daily_count": 118, "C_eq": 0.183, "note": "2-7 t"},
            {"type": "Large truck", "daily_count": 148, "C_eq": 0.682, "note": "7-14 t"},
            {"type": "Heavy truck", "daily_count": 122, "C_eq": 2.512, "note": "14-30 t"},
            {"type": "Articulated or semitrailer", "daily_count": 62, "C_eq": 5.214, "note": ">30 t"},
        ],
    },
}

# Physical-branch parameters as reported in the manuscript
# (Table: initial and learned parameters in the physical branch).
# These 10 interpretable scalars are published in the paper; only the trained
# GRU residual-branch weights remain withheld under data-sharing restrictions.
PHYSICAL_PARAMS_INITIAL = {
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
PHYSICAL_PARAMS_LEARNED = {
    "alpha0": 0.010,
    "alpha1": 0.015,
    "alpha2": 0.00018,
    "alpha3": 0.0012,
    "alpha4": 0.0038,
    "beta1": 0.0045,
    "beta2": 0.0035,
    "beta3": 0.0160,
    "beta4": 0.0180,
    "gamma": 0.0110,
}

app = Flask(__name__, static_folder="static")


def _json_response(data) -> Response:
    payload = json.dumps(data, ensure_ascii=False)
    return Response(payload, mimetype="application/json")


def _load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def _find_route(route_id: str):
    return next((route for route in ROUTES if route["id"] == route_id), None)


def _find_period(period_id: str):
    return next((period for period in PERIODS if period["id"] == period_id), None)


def _data_path(route_id: str, year: int, suffix: str, predicted: bool = False) -> Path:
    pred = "_predicted" if predicted else ""
    return DATA_DIR / f"{route_id}_{year}{pred}.{suffix}"


def _load_route_display() -> dict:
    route_display = _load_json(ROUTE_DISPLAY_PATH)
    for route in ROUTES:
        gps = route_display.get(route["id"], {})
        gps["color"] = route["display_color"]
        gps["description"] = route["description"]
        gps["scenario"] = route["scenario"]
        route_display[route["id"]] = gps
        route["length_km"] = gps.get("length_km", 0.0)
    return route_display


ROUTE_GPS = _load_route_display()
_all_lats = [point[0] for route in ROUTE_GPS.values() for point in route.get("points", [])]
_all_lons = [point[1] for route in ROUTE_GPS.values() for point in route.get("points", [])]
MAP_CENTER = [
    round((min(_all_lats) + max(_all_lats)) / 2, 6),
    round((min(_all_lons) + max(_all_lons)) / 2, 6),
] if _all_lats and _all_lons else [43.78, 125.24]
MAP_ZOOM = 12


def _metrics(actual_segments: list[dict], predicted_segments: list[dict]) -> dict:
    n = min(len(actual_segments), len(predicted_segments))
    if n == 0:
        return {"MAE": 0.0, "RMSE": 0.0, "n_segments": 0}
    errors = [
        float(predicted_segments[i]["PQI_extended"]) - float(actual_segments[i]["PQI_extended"])
        for i in range(n)
    ]
    mae = sum(abs(error) for error in errors) / n
    rmse = math.sqrt(sum(error * error for error in errors) / n)
    return {"MAE": round(mae, 3), "RMSE": round(rmse, 3), "n_segments": n}


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/config")
def get_config():
    return jsonify(
        {
            "routes": ROUTES,
            "periods": PERIODS,
            "route_gps": ROUTE_GPS,
            "map_center": MAP_CENTER,
            "map_zoom": MAP_ZOOM,
            "quality_grades": {grade: list(value_range) for grade, value_range in QUALITY_GRADES.items()},
            "grade_colors": GRADE_COLORS,
            "release": {
                "name": "PaveVision public web demo",
                "dataset": "600 m processed public sample data",
                "raw_pcd_included": False,
                "pavement_only_quality_assessment": True,
                "prediction_mode": "precomputed demo output only",
                "full_data_weights": "withheld under data-sharing restrictions",
            },
        }
    )


@app.route("/api/assessment/<route_id>/<period_id>")
def get_assessment(route_id: str, period_id: str):
    route = _find_route(route_id)
    period = _find_period(period_id)
    if not route or not period:
        return jsonify({"error": "Invalid route or period."}), 404
    return _json_response(_load_json(_data_path(route_id, period["year"], "assessment.json")))


@app.route("/api/grid/<route_id>/<period_id>")
def get_grid(route_id: str, period_id: str):
    route = _find_route(route_id)
    period = _find_period(period_id)
    grid_size = request.args.get("grid_size", 0.5, type=float)
    if not route or not period:
        return jsonify({"error": "Invalid route or period."}), 404
    return _json_response(_load_json(_data_path(route_id, period["year"], f"grid_{grid_size}.json")))


@app.route("/api/prediction/<route_id>")
def get_prediction(route_id: str):
    if not _find_route(route_id):
        return jsonify({"error": "Invalid route."}), 404
    actual = _load_json(_data_path(route_id, 2026, "assessment.json"))
    predicted = _load_json(_data_path(route_id, 2026, "assessment.json", predicted=True))
    baseline = _load_json(_data_path(route_id, 2025, "assessment.json"))
    actual_segments = actual.get("segment_scores", [])
    predicted_segments = predicted.get("segment_scores", [])
    residuals = [
        round(float(predicted_segments[i]["PQI_extended"]) - float(actual_segments[i]["PQI_extended"]), 4)
        for i in range(min(len(actual_segments), len(predicted_segments)))
    ]
    model_metrics = _metrics(actual_segments, predicted_segments)
    return _json_response(
        {
            "actual": actual,
            "predicted": predicted,
            "baseline": baseline,
            "residuals": residuals,
            "metrics": model_metrics,
            "model": {
                "name": "PG-PDN precomputed public demo output",
                "release_policy": "Full-route survey data and trained full-data weights are withheld.",
            },
        }
    )


@app.route("/api/grid/prediction/<route_id>")
def get_prediction_grid(route_id: str):
    if not _find_route(route_id):
        return jsonify({"error": "Invalid route."}), 404
    grid_size = request.args.get("grid_size", 0.5, type=float)
    actual = _load_json(_data_path(route_id, 2026, f"grid_{grid_size}.json"))
    predicted = _load_json(_data_path(route_id, 2026, f"grid_{grid_size}.json", predicted=True))
    return _json_response({"actual": actual, "predicted": predicted})


@app.route("/api/traffic")
def get_traffic():
    route_id = request.args.get("route_id", "route1")
    route_payload = TRAFFIC_BY_ROUTE.get(route_id, TRAFFIC_BY_ROUTE["route1"])
    return jsonify(
        {
            "city": "Changchun",
            "survey_period": "Mar. 2025 to Mar. 2026",
            "route_id": route_id,
            "vehicle_types": route_payload["vehicle_types"],
            "esal_annual": route_payload["esal_annual"],
            "eta_s": route_payload.get("eta_s", 1.0),
            "esal_unit": "10^4 passes/year",
            "source": "Manuscript Table: traffic composition and ESAL estimates",
        }
    )


@app.route("/api/weather")
def get_weather():
    return jsonify(
        {
            "city": "Changchun",
            "source": "Manuscript Table: climate variables",
            "period": "Mar. 2025 to Mar. 2026",
            "data": {
                "precipitation_mm": 536,
                "avg_daily_temp_range": 11.8,
                "low_temperature_days": 148,
            },
            "description": {
                "precipitation_mm": "precipitation P_t (mm)",
                "avg_daily_temp_range": "mean daily temperature range Delta T_t (deg C)",
                "low_temperature_days": "low-temperature days F_t (mean daily temperature below 0 deg C)",
            },
        }
    )


@app.route("/api/model_params")
def get_model_params():
    return jsonify(
        {
            "physics_params": {"initial": PHYSICAL_PARAMS_INITIAL, "trained": PHYSICAL_PARAMS_LEARNED},
            "residual_params": {
                "type": "GRU residual correction branch",
                "release": "architecture disclosed; trained full-data weights withheld",
            },
            "loss_weights": {"lambda_prediction": 1.0, "lambda_nonnegative": 0.5, "lambda_smoothness": 0.1},
            "physics_ratio": 78.3,
            "data_ratio": 21.7,
            "model_release": "The public web demo loads precomputed PG-PDN outputs and does not execute the restricted prediction pipeline.",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    print("=" * 68)
    print("  PaveVision public web demo")
    print("=" * 68)
    print(f"  URL: http://localhost:{port}")
    print("  Mode: precomputed public demo output only")
    print("=" * 68)
    app.run(host="0.0.0.0", port=port, debug=False)
