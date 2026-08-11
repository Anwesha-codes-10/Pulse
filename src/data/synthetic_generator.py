"""
Pulse Data Simulation Engine.
"""

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from src.config.constants import AssetType

def make_asset_data(asset_id: str, asset_type: AssetType, age: float, days: int = 365) -> pd.DataFrame:
    #Use asset numeric seed to keep tracking dterministic
    seed = sum(ord(c) for c in asset_id)
    np.random.seed(seed)

    start = datetime(2025, 1, 1)
    dates = [(start + timedelta(days=x)).strftime("%Y-%m-%d") for x in range(days)]

    # Set physics baseline paramters per asset category
    if asset_type == AssetType.BRIDGE:
        v_base, s_base = 12.0, 140.0
    elif asset_type == AssetType.ROAD_SEGMENT:
        v_base, s_base = 6.0, 40.0
    elif asset_type == AssetType.PIPELINE:
        v_base, s_base = 4.0, 80.0
    else:
        v_base, s_base = 5.0, 70.0

    #Aging scaling factor
    age_factor = 1.0 + (age * 0.015)
    t = np.arange(days)

    #Seasonal weather cycles(sinusodial temp wave)
    seasons = np.sin(2 * np.pi * t / 365.0)
    temp = 25.0 + (15.0 * seasons) + np.random.normal(0, 1.2, days)

    #Accumulative linear wear-and-tear
    wear = (t / days) * 0.12 * age_factor

    #Telemetry generation channels
    vib = v_base * age_factor + (v_base * wear) + np.random.normal(0, 0.3, days) + (seasons * 0.5)
    strain = s_base * age_factor + (temp * 0.8) + np.random.normal(0, 4.0, days)
    corr = np.cumsum(np.abs(np.random.normal(0.002, 0.0004, days))) * age_factor

    #Force dicrete trauma anamolies to test XGBoost training paths later
    anom = np.zeros(days, dtype=int)

    if days > 185:
        vib[180:185] *= 1.5 #hydrolic flood washout range
        strain[180:185] += 75.0
        anom[180:185] = 1

    if days > 323:
        strain[320:322] *= 1.35 # Frost contraction shock
        anom[320:322] = 1

    return pd.DataFrame({
        "timestamp": dates,
        "asset_id": asset_id,
        "temperature_c": temp,
        "vibration_hz": vib,
        "structural_strain": strain,
        "corrosion_index": corr,
        "is_anomaly": anom
    })