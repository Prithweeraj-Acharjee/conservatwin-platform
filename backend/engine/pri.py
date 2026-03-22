"""
Preservation Risk Index (PRI) Engine
Calculates environmental stress on artifacts based on:
  - Temperature deviation from target range
  - Humidity deviation from target range
  - Stability (variance over recent readings)
  - Rate of change (sudden swings are dangerous)

PRI ranges: 0 (perfect) to 100 (critical damage risk)
"""

import math
from dataclasses import dataclass


@dataclass
class PRIResult:
    pri: float
    temp_deviation: float
    rh_deviation: float
    stability_score: float
    risk_level: str  # stable, elevated, high, critical
    factors: list[str]


# Material-specific tolerances
MATERIAL_PROFILES = {
    "general": {"temp_weight": 1.0, "rh_weight": 1.0, "slew_limit": 2.0},
    "oil_painting": {"temp_weight": 1.2, "rh_weight": 1.5, "slew_limit": 1.5},
    "watercolor": {"temp_weight": 1.0, "rh_weight": 2.0, "slew_limit": 1.0},
    "textile": {"temp_weight": 0.8, "rh_weight": 1.8, "slew_limit": 1.5},
    "wood": {"temp_weight": 1.0, "rh_weight": 2.0, "slew_limit": 1.2},
    "metal": {"temp_weight": 1.5, "rh_weight": 1.3, "slew_limit": 2.5},
    "paper": {"temp_weight": 1.0, "rh_weight": 2.0, "slew_limit": 0.8},
    "ceramic": {"temp_weight": 0.5, "rh_weight": 0.5, "slew_limit": 3.0},
    "photograph": {"temp_weight": 1.5, "rh_weight": 1.8, "slew_limit": 0.5},
    "stone": {"temp_weight": 0.3, "rh_weight": 1.0, "slew_limit": 3.0},
}


def calculate_pri(
    readings: list[dict],
    target_temp_min: float,
    target_temp_max: float,
    target_rh_min: float,
    target_rh_max: float,
    material_type: str = "general",
) -> PRIResult:
    if not readings:
        return PRIResult(0, 0, 0, 100, "stable", [])

    profile = MATERIAL_PROFILES.get(material_type, MATERIAL_PROFILES["general"])
    factors = []

    latest = readings[-1]
    temp = latest["temperature"]
    rh = latest["humidity"]

    # --- Temperature deviation (0-30 points) ---
    temp_mid = (target_temp_min + target_temp_max) / 2
    temp_range = (target_temp_max - target_temp_min) / 2

    if target_temp_min <= temp <= target_temp_max:
        temp_dev = 0
    else:
        temp_dev = min(abs(temp - temp_mid) - temp_range, 10) / 10
    temp_dev *= profile["temp_weight"]
    temp_score = temp_dev * 30

    if temp_dev > 0.3:
        direction = "high" if temp > target_temp_max else "low"
        factors.append(f"Temperature is {abs(temp - temp_mid):.1f}°C {direction}")

    # --- Humidity deviation (0-35 points) ---
    rh_mid = (target_rh_min + target_rh_max) / 2
    rh_range = (target_rh_max - target_rh_min) / 2

    if target_rh_min <= rh <= target_rh_max:
        rh_dev = 0
    else:
        rh_dev = min(abs(rh - rh_mid) - rh_range, 20) / 20
    rh_dev *= profile["rh_weight"]
    rh_score = rh_dev * 35

    if rh_dev > 0.3:
        direction = "high" if rh > target_rh_max else "low"
        factors.append(f"Humidity is {abs(rh - rh_mid):.1f}% {direction}")

    # --- Stability / variance (0-20 points) ---
    stability = 100.0
    if len(readings) >= 5:
        temps = [r["temperature"] for r in readings[-20:]]
        rhs = [r["humidity"] for r in readings[-20:]]
        temp_var = _variance(temps)
        rh_var = _variance(rhs)
        instability = (temp_var * profile["temp_weight"] + rh_var * profile["rh_weight"]) / 2
        stability = max(0, 100 - instability * 10)
        stability_score = (1 - stability / 100) * 20

        if stability < 60:
            factors.append(f"Environment is unstable (variance: T={temp_var:.1f}, RH={rh_var:.1f})")
    else:
        stability_score = 0

    # --- Rate of change / slew (0-15 points) ---
    slew_score = 0
    if len(readings) >= 2:
        prev = readings[-2]
        dt = abs(temp - prev["temperature"])
        drh = abs(rh - prev["humidity"])
        slew = max(dt, drh / 2)
        if slew > profile["slew_limit"]:
            slew_score = min((slew - profile["slew_limit"]) * 5, 15)
            factors.append(f"Rapid environmental change detected ({slew:.1f}°/interval)")

    # --- Total PRI ---
    pri = min(temp_score + rh_score + stability_score + slew_score, 100)
    pri = round(pri, 1)

    if pri < 20:
        risk_level = "stable"
    elif pri < 45:
        risk_level = "elevated"
    elif pri < 70:
        risk_level = "high"
    else:
        risk_level = "critical"

    return PRIResult(
        pri=pri,
        temp_deviation=round(temp_dev * 100, 1),
        rh_deviation=round(rh_dev * 100, 1),
        stability_score=round(stability, 1),
        risk_level=risk_level,
        factors=factors,
    )


def _variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0
    mean = sum(values) / len(values)
    return sum((v - mean) ** 2 for v in values) / len(values)
