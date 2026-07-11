"""
Phase 4 - Lesson 4.2
Data Cleaning Pipeline
Python 3.10.10
"""

import pandas as pd
from pathlib import Path

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

PROCESSED_DATA.mkdir(exist_ok=True)

FILE = RAW_DATA / "ev_battery_telemetry_synthetic.xlsx"

# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_excel(FILE)

print("Rows :", len(df))
print()

# ----------------------------------------------------
# Remove Duplicate Rows
# ----------------------------------------------------

duplicates = df.duplicated().sum()

print("Duplicate Rows :", duplicates)

df = df.drop_duplicates()

print("Rows After Removing Duplicates :", len(df))
print()

# ----------------------------------------------------
# Missing Values
# ----------------------------------------------------

print("=" * 60)
print("Missing Values")
print("=" * 60)

print(df.isnull().sum())
print()

# ----------------------------------------------------
# Validate Sensor Values
# ----------------------------------------------------

print("=" * 60)
print("Removing Invalid Sensor Values")
print("=" * 60)

# State of Charge must be between 0 and 100
df = df[(df["soc"] >= 0) & (df["soc"] <= 100)]

# SOH must be between 60 and 100
df = df[(df["soh"] >= 60) & (df["soh"] <= 100)]

# Battery temperature
df = df[(df["battery_temp"] >= -20) & (df["battery_temp"] <= 80)]

# Battery Voltage
df = df[(df["battery_voltage"] >= 250) & (df["battery_voltage"] <= 500)]

# Charge Cycles
df = df[df["charge_cycles"] >= 0]

print("Rows After Validation :", len(df))
print()

# ----------------------------------------------------
# Save Clean Dataset
# ----------------------------------------------------

output = PROCESSED_DATA / "battery_clean.csv"

df.to_csv(output, index=False)

print("=" * 60)
print("Clean Dataset Saved")
print(output)
print("=" * 60)