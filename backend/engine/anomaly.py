"""
ConservaTwin Anomaly Detection
Simple statistical anomaly detection for sensor readings.
Flags sudden spikes, sensor failures, and unusual patterns.
"""

from dataclasses import dataclass


@dataclass
class Anomaly:
    anomaly_type: str  # spike, flatline, drift, out_of_range
    severity: str  # warning, critical
    message: str
    value: float
    expected_range: tuple[float, float]


def detect_anomalies(
    readings: list[dict],
    target_temp_min: float,
    target_temp_max: float,
    target_rh_min: float,
    target_rh_max: float,
) -> list[Anomaly]:
    if len(readings) < 3:
        return []

    anomalies = []
    latest = readings[-1]
    temp = latest["temperature"]
    rh = latest["humidity"]

    # --- Spike detection (sudden jump from previous reading) ---
    prev = readings[-2]
    temp_delta = abs(temp - prev["temperature"])
    rh_delta = abs(rh - prev["humidity"])

    if temp_delta > 5:
        anomalies.append(Anomaly(
            anomaly_type="spike",
            severity="critical",
            message=f"Temperature spiked {temp_delta:.1f}°C in one interval. Possible sensor malfunction or HVAC failure.",
            value=temp,
            expected_range=(prev["temperature"] - 2, prev["temperature"] + 2),
        ))
    elif temp_delta > 3:
        anomalies.append(Anomaly(
            anomaly_type="spike",
            severity="warning",
            message=f"Unusual temperature change of {temp_delta:.1f}°C detected.",
            value=temp,
            expected_range=(prev["temperature"] - 2, prev["temperature"] + 2),
        ))

    if rh_delta > 10:
        anomalies.append(Anomaly(
            anomaly_type="spike",
            severity="critical",
            message=f"Humidity spiked {rh_delta:.1f}% in one interval. Check for water event or sensor issue.",
            value=rh,
            expected_range=(prev["humidity"] - 5, prev["humidity"] + 5),
        ))

    # --- Flatline detection (sensor stuck) ---
    if len(readings) >= 10:
        recent_temps = [r["temperature"] for r in readings[-10:]]
        recent_rhs = [r["humidity"] for r in readings[-10:]]

        if len(set(recent_temps)) == 1:
            anomalies.append(Anomaly(
                anomaly_type="flatline",
                severity="warning",
                message=f"Temperature sensor appears stuck at {temp:.1f}°C for 10+ readings. Check sensor connection.",
                value=temp,
                expected_range=(target_temp_min, target_temp_max),
            ))

        if len(set(recent_rhs)) == 1:
            anomalies.append(Anomaly(
                anomaly_type="flatline",
                severity="warning",
                message=f"Humidity sensor appears stuck at {rh:.1f}% for 10+ readings. Check sensor connection.",
                value=rh,
                expected_range=(target_rh_min, target_rh_max),
            ))

    # --- Out of physical range (impossible values) ---
    if temp < -20 or temp > 60:
        anomalies.append(Anomaly(
            anomaly_type="out_of_range",
            severity="critical",
            message=f"Temperature reading {temp:.1f}°C is physically implausible. Sensor failure likely.",
            value=temp,
            expected_range=(-20, 60),
        ))

    if rh < 0 or rh > 100:
        anomalies.append(Anomaly(
            anomaly_type="out_of_range",
            severity="critical",
            message=f"Humidity reading {rh:.1f}% is physically impossible. Sensor failure.",
            value=rh,
            expected_range=(0, 100),
        ))

    # --- Drift detection (gradual trend away from target) ---
    if len(readings) >= 20:
        early = readings[-20:-10]
        late = readings[-10:]
        early_temp_avg = sum(r["temperature"] for r in early) / len(early)
        late_temp_avg = sum(r["temperature"] for r in late) / len(late)
        drift = late_temp_avg - early_temp_avg

        if abs(drift) > 2:
            direction = "rising" if drift > 0 else "falling"
            anomalies.append(Anomaly(
                anomaly_type="drift",
                severity="warning",
                message=f"Temperature is steadily {direction} ({drift:+.1f}°C over last 20 readings). Possible HVAC degradation.",
                value=late_temp_avg,
                expected_range=(target_temp_min, target_temp_max),
            ))

    return anomalies
