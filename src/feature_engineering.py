"""
=========================================================
Project : EV Battery Health Analytics
Module  : Feature Engineering
Python  : 3.10.10
=========================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd

# --------------------------------------------------------
# Project Paths
# --------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DATA = BASE_DIR / "data" / "processed"

OUTPUT_FILE = PROCESSED_DATA / "battery_features.csv"

# --------------------------------------------------------
# Load Data
# --------------------------------------------------------

df = pd.read_csv(PROCESSED_DATA / "battery_clean.csv")

print("Dataset Loaded Successfully")

# --------------------------------------------------------
# Feature Engineering
# --------------------------------------------------------

# Battery age in years
df["battery_age_years"] = df["battery_age_days"] / 365

# Fast charge ratio
df["fast_charge_ratio"] = (
    df["fast_charge_count"] /
    (df["charge_cycles"] + 1)
)

# Battery stress index
df["battery_stress_index"] = (
    df["battery_temp"] *
    df["internal_resistance"]
)

# Temperature difference
df["temperature_difference"] = (
    df["battery_temp"] -
    df["ambient_temp"]
)

# Average distance per charge cycle
df["avg_distance_per_cycle"] = (
    df["total_distance_km"] /
    (df["charge_cycles"] + 1)
)

# Power to voltage ratio
df["power_to_voltage_ratio"] = (
    df["battery_power_kw"] /
    df["battery_voltage"]
)

# Remaining range per SOC
df["range_per_soc"] = (
    df["remaining_range_km"] /
    (df["soc"] + 1)
)

print("\nNew Features Created")

new_features = [
    "battery_age_years",
    "fast_charge_ratio",
    "battery_stress_index",
    "temperature_difference",
    "avg_distance_per_cycle",
    "power_to_voltage_ratio",
    "range_per_soc"
]

print(df[new_features].head())

# --------------------------------------------------------
# Save Dataset
# --------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\nFeature Engineered Dataset Saved")

print(OUTPUT_FILE)