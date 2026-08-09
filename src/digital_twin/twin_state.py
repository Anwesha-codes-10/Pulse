"""
Pulse Digital Twin Live State Machine.

Tracks active sensor telemetry, historical buffers, and model prediction output registers for a specific registered infrastructure asset.

"""

from typing import List, Dict, Any, Optional
from src.config.constants import HealthStatus
from src.digital_twin.asset_registry import InfrastructureAssest, InfrastructureAsset

class DigitalTwinState:
    """
    Live state wrapper object tracking multiple operating metrics and analytical reccomendations for a single infrastructure asset.

    """

    def __init__(self, asset_metadata: InfrastructureAsset):
        """Intializes the live state tracker linked directly to an assest blueprint."""
        self.metadata: InfrastructureAsset = asset_metadata
        self.asset_id: str = asset_metadata.asset_id


        #1. Active Telemetry Snapshot vitals (Updated during pipeline ingestion)
        self.current_vitals: Dict[str, float] = {
            "vibration_hz":0.0,
            "structural_strain":0.0,
            "corrosion_index":0.0,
            "temperature_c":0.0,
            
        }
        self.telementry_history: List[Dict[str, Any]] = []

        #2. Dowmnstream Modeling Ingestion Tracking Registers
        self.current_health: HealthStatus = HealthStatus.HEALTHY
        self.health_score: float = 100.0  #Analytical score from 0.0 to 100.0

        #Horizon projection matrices (e.g. {7: 0.15, 30: 0.45})
        self.forecasted_health: Dict[int, float] = {}

    def update_vitals(self, telemetry: Dict[str, Any]) ->None:
        """Updates sensor snapshots and caches entires of technological inside the log buffer."""
        self.current_vitals = {
            "vibration_hz": float(telemetry.get("vibration_hz", self.current_vitals["vibration_hz"])),
            "structural_strain": float(telemetry.get("structural_strain", self.current_vitals["structural_strain"])),
            "corrosion_index": float(telemetry.get("corrosion_index", self.current_vitals["corrosion_index"])),
            "temperature_c": float(telemetry.get("temperature_c", self.current_vitals["temperature_c"])),
        }

        snapshot ={"timestamp": telemetry.get("timestamp"), **self.current_vitals}
        self.telemetry_history.append(snapshot)

    def update_diagnostics(self, status: HealthStatus, score: float) -> None:
        """Updates the diagnostic information for the digital twin."""
        self.current_health = status
        self.health_score = max(0.0, min(100.0, float(score)))

    def update_forecasts(self, projections: Dict[int, float]) -> None:
        """Maps trajectory calculations passed down by Forecasting  Engine."""
        self.forecasted_health = {int(k): float(v) for k, v in projections.items()}

    def to_dict(self) -> Dict[str, Any]:
        """Serializes active state metrics into primitive formats for immediate UI mapping."""

        return {
            "asset_id": self.asset_id,
            "asset_type": self.metadata.asset_type.value,
            "location": self.metadata.location,
            "vitals": self.current_vitals,
            "health_status": self.current_health.value,
            "health_score": self.health_score,
            "forecasted_risks": self.forecasted_risks
        }

    

    