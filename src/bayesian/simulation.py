"""
Pulse Scenario Simulation Engine.

Calculates an estimated failure risk based on the current asset health status and external operational conditions.

"""


def get_scenario_risk(vitals_status, traffic_load, weather_severity,):
    """
    Calculate the estimated failure risk for a given scenario.

    """
    if vitals_status == "Critical":
        base_probability = 0.75
    elif vitals_status == "Warning":
        base_probability = 0.35
    else:
        base_probability = 0.05


    traffic_multiplier = {
        "Low": 1.0,
        "Medium": 1.15,
        "High": 1.35,
    }.get(traffic_load, 1.0)

    
    weather_multiplier = {
        "Normal": 1.0,
        "Severe": 1.50,
    }.get(weather_severity, 1.0)

   
    conditional_probability = (base_probability * traffic_multiplier * weather_multiplier)

    
    final_risk = round(min(100.0, max(0.0, conditional_probability * 100)), 1,)

    return final_risk