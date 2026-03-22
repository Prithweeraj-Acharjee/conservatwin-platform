"""
ConservaTwin AI Conservation Advisor
Generates actionable recommendations based on current conditions,
PRI score, material type, and reading trends.

No external API needed — runs entirely on rules + heuristics.
(Can be upgraded to LLM-powered later)
"""

from dataclasses import dataclass
from .pri import PRIResult, MATERIAL_PROFILES


@dataclass
class Recommendation:
    priority: str  # immediate, soon, routine
    action: str
    reason: str
    category: str  # temperature, humidity, stability, maintenance


def generate_recommendations(
    pri_result: PRIResult,
    current_temp: float,
    current_rh: float,
    target_temp_min: float,
    target_temp_max: float,
    target_rh_min: float,
    target_rh_max: float,
    material_type: str = "general",
    readings_count: int = 0,
) -> list[Recommendation]:
    recs = []
    profile = MATERIAL_PROFILES.get(material_type, MATERIAL_PROFILES["general"])

    # --- Temperature recommendations ---
    if current_temp > target_temp_max:
        diff = current_temp - target_temp_max
        if diff > 5:
            recs.append(Recommendation(
                priority="immediate",
                action=f"Reduce temperature by {diff:.1f}°C urgently. Activate cooling or increase ventilation.",
                reason=f"Temperature ({current_temp:.1f}°C) is critically above safe range ({target_temp_min}-{target_temp_max}°C).",
                category="temperature",
            ))
        else:
            recs.append(Recommendation(
                priority="soon",
                action=f"Lower temperature by {diff:.1f}°C. Consider adjusting HVAC setpoint or opening vents during cooler hours.",
                reason=f"Temperature ({current_temp:.1f}°C) exceeds target range.",
                category="temperature",
            ))

    elif current_temp < target_temp_min:
        diff = target_temp_min - current_temp
        if diff > 5:
            recs.append(Recommendation(
                priority="immediate",
                action=f"Increase temperature by {diff:.1f}°C. Activate heating immediately.",
                reason=f"Temperature ({current_temp:.1f}°C) is critically below safe range.",
                category="temperature",
            ))
        else:
            recs.append(Recommendation(
                priority="soon",
                action=f"Raise temperature by {diff:.1f}°C. Adjust heating or reduce drafts.",
                reason=f"Temperature ({current_temp:.1f}°C) is below target range.",
                category="temperature",
            ))

    # --- Humidity recommendations ---
    if current_rh > target_rh_max:
        diff = current_rh - target_rh_max
        if diff > 15:
            recs.append(Recommendation(
                priority="immediate",
                action="Deploy dehumidifiers immediately. Check for water ingress or leaks.",
                reason=f"Humidity ({current_rh:.1f}%) is dangerously high. Risk of mold, foxing, and material swelling.",
                category="humidity",
            ))
        elif diff > 5:
            recs.append(Recommendation(
                priority="soon",
                action="Activate dehumidification. Improve air circulation. Check HVAC drain lines.",
                reason=f"Humidity ({current_rh:.1f}%) exceeds safe range by {diff:.1f}%.",
                category="humidity",
            ))
        else:
            recs.append(Recommendation(
                priority="routine",
                action="Monitor humidity trend. Consider running dehumidifier during peak hours.",
                reason=f"Humidity ({current_rh:.1f}%) is slightly above target.",
                category="humidity",
            ))

    elif current_rh < target_rh_min:
        diff = target_rh_min - current_rh
        if diff > 15:
            recs.append(Recommendation(
                priority="immediate",
                action="Add humidification urgently. Desiccation risk is high.",
                reason=f"Humidity ({current_rh:.1f}%) is critically low. Risk of cracking, flaking, and embrittlement.",
                category="humidity",
            ))
        else:
            recs.append(Recommendation(
                priority="soon",
                action="Increase humidity. Use humidifiers or reduce ventilation rate.",
                reason=f"Humidity ({current_rh:.1f}%) is below safe range.",
                category="humidity",
            ))

    # --- Material-specific advice ---
    if material_type == "oil_painting" and current_rh > 60:
        recs.append(Recommendation(
            priority="immediate",
            action="Oil paintings are highly sensitive to moisture. Reduce RH below 55% to prevent canvas warping and paint delamination.",
            reason="Oil paint on canvas expands/contracts with humidity changes, causing cracking over time.",
            category="humidity",
        ))

    if material_type == "paper" and current_rh > 55:
        recs.append(Recommendation(
            priority="soon",
            action="Paper artifacts need RH below 55%. Risk of foxing (brown spots) and acid migration increases with humidity.",
            reason="High humidity accelerates cellulose degradation in paper.",
            category="humidity",
        ))

    if material_type == "photograph" and current_temp > 20:
        recs.append(Recommendation(
            priority="soon",
            action="Photographic materials should be stored below 20°C. Consider relocating to a cooler area.",
            reason="Elevated temperature accelerates dye fading and gelatin deterioration in photographs.",
            category="temperature",
        ))

    if material_type == "wood" and pri_result.stability_score < 60:
        recs.append(Recommendation(
            priority="immediate",
            action="Stabilize environment immediately. Wood artifacts are splitting/warping risk when conditions fluctuate.",
            reason="Rapid humidity changes cause differential stress in wood grain.",
            category="stability",
        ))

    if material_type == "textile" and current_rh > 65:
        recs.append(Recommendation(
            priority="immediate",
            action="Textile conservation emergency: RH above 65% promotes mold growth within 48-72 hours.",
            reason="Organic textile fibers provide nutrients for fungal growth in high humidity.",
            category="humidity",
        ))

    # --- Stability recommendations ---
    if pri_result.stability_score < 40:
        recs.append(Recommendation(
            priority="immediate",
            action="Environment is highly unstable. Check for HVAC cycling, open windows/doors, or seasonal transitions causing rapid changes.",
            reason="Fluctuating conditions cause more damage than steady slightly-off conditions.",
            category="stability",
        ))
    elif pri_result.stability_score < 70:
        recs.append(Recommendation(
            priority="soon",
            action="Improve environmental stability. Consider buffering materials (silica gel) or adjusting HVAC dead bands.",
            reason="Moderate instability detected in recent readings.",
            category="stability",
        ))

    # --- General maintenance ---
    if readings_count < 10:
        recs.append(Recommendation(
            priority="routine",
            action="Continue collecting data. Reliable risk assessment requires at least 24 hours of continuous readings.",
            reason="Insufficient data for trend analysis.",
            category="maintenance",
        ))

    if pri_result.pri < 15 and not recs:
        recs.append(Recommendation(
            priority="routine",
            action="Conditions are excellent. Continue current environmental controls. Schedule next calibration check.",
            reason="All parameters within target range with good stability.",
            category="maintenance",
        ))

    return recs
