"""
Tests for the Pulse Digital Twin Live State Tracker.

"""

from src.config.constants import AssetType, HealthStatus
from src.digital_twin import InfrastructureAsset, DigitalTwinState

def test_twin_state_initializes_with_correct_defaults() -> None:
    """Verify that a live state machine boots up with proper baselines."""
    asset = InfrastructureAsset(
        asset_id="Bridge-12",
        asset_type=AssetType.BRIDGE,
        location="Bhubaneswar"
    )

    twin = DigitalTwinState(asset)

    assert twin.asset_id == "Bridge-12"
    assert twin.current_health == HealthStatus.HEALTHY
    assert twin.health_score == 100.0
    assert len(twin.telemetry_history) == 0

def test_twin_state_tracks_incoming_vitals() -> None:
    """Verify that sensory payloads accurately update live vitals."""
    asset = InfrastructureAsset(
        asset_id="Bridge-12",
        asset_type=AssetType.BRIDGE,
        location="Bhubaneswar"
    )

    twin = DigitalTwinState(asset)

    telemetry_input = {
        "timestamp": "2026-08-11 12:00:00",
        "vibration_hz": 12.4,
        "structural_strain": 145.8,
    }

    twin.update_vitals(telemetry_input)

    assert twin.current_vitals["vibration_hz"] == 12.4
    assert twin.current_vitals["structural_strain"] == 145.8
    assert twin.current_vitals["corrosion_index"] == 0.0
    assert len(twin.telemetry_history) == 1

def test_twin_state_serializes_cleanly_to_dict() -> None:
    """Verify that state serialization returns simple primitive matrices for the UI."""
    asset = InfrastructureAsset(
        asset_id="Bridge-12",
        asset_type=AssetType.BRIDGE,
        location="Bhubaneswar"
    )

    twin = DigitalTwinState(asset)

    twin.update_diagnostics(HealthStatus.WARNING, 76.5)
    twin.update_forecasts({7: 0.12, 30: 0.44})

   

    report = twin.to_dict()

    assert report["asset_id"] == "Bridge-12"
    assert report["health_score"] == 76.5
    assert report["health_status"] == "Warning"
    assert report["forecasted_health"][30] == 0.44