"""
Phase 4 - Lesson 4.1
Load and Inspect EV Battery Dataset
Author: Shubham Yadav
Python Version: 3.10.10
"""

import pandas as pd
from pathlib import Path

# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw"

PROCESSED_DATA = BASE_DIR / "data" / "processed"

# Create processed folder if it doesn't exist
PROCESSED_DATA.mkdir(exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
file_path = RAW_DATA / "ev_battery_telemetry_synthetic.xlsx"

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_excel(file_path)

print("Dataset Loaded Successfully!\n")

# -----------------------------
# Basic Information
# -----------------------------

print("=" * 60)
print("Dataset Shape")
print("=" * 60)

print(df.shape)

print()

print("=" * 60)
print("Column Names")
print("=" * 60)

print(df.columns)

print()

print("=" * 60)
print("Data Types")
print("=" * 60)

print(df.dtypes)

print()

print("=" * 60)
print("First Five Rows")
print("=" * 60)

print(df.head())

print()

print("=" * 60)
print("Last Five Rows")
print("=" * 60)

print(df.tail())

print()

print("=" * 60)
print("Summary Statistics")
print("=" * 60)

print(df.describe())

print()

print("=" * 60)
print("Missing Values")
print("=" * 60)

print(df.isnull().sum())

print()

print("=" * 60)
print("Duplicate Rows")
print("=" * 60)

print(df.duplicated().sum())

print()

print("=" * 60)
print("Inspection Completed")
print("=" * 60)