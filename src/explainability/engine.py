"""
Pulse Confidence and Explainability Engine.

Estimates how trustworthy a selected maintenance decision is and provides heuristic feature contributions explaining the decision.
"""


def evaluate_decision_trust(data, chosen_action):
    """
    Calculate a confidence score and feature contribution map for a maintenance decision.

    """
    vibration = float(data.get("vibration_hz", 0.0))
    strain = float(data.get("structural_strain", 0.0))
    corrosion = float(data.get("corrosion_index", 0.0))

    vibration_weight = max(10.0, min(45.0, vibration * 2.0),)
    strain_weight = max(10.0, min(35.0, strain * 0.15),)
    corrosion_weight = max(5.0, min(30.0, corrosion * 15.0),)

    total_weight = (vibration_weight + strain_weight + corrosion_weight)
    shap_map = {
        "Vibration Density": round((vibration_weight / total_weight) * 100, 1,),
        "Material Load Strain": round((strain_weight / total_weight) * 100,1,),
        "Erosion Accumulation": round((corrosion_weight / total_weight) * 100,1,),
    }

    if (chosen_action == "DELAY_MAINTENANCE" and vibration < 15.0 and corrosion < 0.5): 
        confidence = 94.5

    elif (chosen_action == "REPLACE_ASSET" and (vibration > 20.0 or corrosion > 1.0)):
        confidence = 92.0

    else:
        confidence = 85.0

    return confidence, shap_map