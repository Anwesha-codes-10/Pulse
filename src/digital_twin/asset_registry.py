"""
Pulse Asset Registry.

Defines the identity and static metadata of infrastructure assets.
"""

from dataclasses import dataclass
from typing import Optional
from src.config.constants import AssetType

@dataclass(frozen=True)
class InfrastructureAsset:
    """Represents a single infrastructure asset with its static metadata."""

    asset_id: str
    asset_type: AssetType
    location: str
    metadata: Optional[dict[str, str]] = None