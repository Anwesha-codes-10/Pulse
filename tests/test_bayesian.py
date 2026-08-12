from src.bayesian import get_scenario_risk


def test_bayesian_risk_calculation():
    """
    Test the scenario risk engine under different operational conditions.

    """

    # Test Node A:
    # Healthy asset under normal operating conditions
    low_risk = get_scenario_risk(
        "Healthy",
        "Low",
        "Normal",
    )

    assert 0.0 <= low_risk <= 100.0

    # Test Node B:
    # Critical asset under high traffic and severe weather
    high_risk = get_scenario_risk(
        "Critical",
        "High",
        "Severe",
    )

    assert high_risk > low_risk
    assert high_risk == 100.0 or high_risk > 75.0