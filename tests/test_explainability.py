from src.explainability import evaluate_decision_trust


def test_confidence_and_explainability_engine():
    """
    Test the confidence scoring and feature explainability engine.
    """

    sample_asset_data = {
        "vibration_hz": 24.5,
        "structural_strain": 280.0,
        "corrosion_index": 1.2,
    }

    confidence, feature_contributions = evaluate_decision_trust(
        sample_asset_data,
        "REPLACE_ASSET",
    )

    assert 50.0 <= confidence <= 100.0
    assert confidence == 92.0
    assert isinstance(feature_contributions, dict)

    assert "Vibration Density" in feature_contributions
    assert "Material Load Strain" in feature_contributions
    assert "Erosion Accumulation" in feature_contributions

    for contribution in feature_contributions.values():
        assert 0.0 <= contribution <= 100.0

    total_contribution = sum(feature_contributions.values())
    assert 99.0 <= total_contribution <= 101.0