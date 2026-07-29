from enum import Enum


class AssetType(str, Enum):
    BRIDGE = "Bridge"
    ROAD_SEGMENT = "Road Segment"
    PIPELINE = "Pipeline"
    TRANSFORMER = "Transformer"


class HealthStatus(str, Enum):
    HEALTHY = "Healthy"
    WARNING = "Warning"
    CRITICAL = "Critical"


class Recommendation(str, Enum):
    REPAIR = "Repair"
    DELAY = "Delay"
    REPLACE = "Replace"