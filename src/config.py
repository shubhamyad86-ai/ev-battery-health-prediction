"""
=========================================
Project Configuration
=========================================
Single source of truth for paths and the
feature list, so training and inference
can never drift out of sync.
"""

from pathlib import Path

# Root Project Folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Data
RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

# Models
MODELS_DIR = BASE_DIR / "models"

# Reports
REPORTS_DIR = BASE_DIR / "reports"

# Images
IMAGES_DIR = BASE_DIR / "images"

# Database
DATABASE_DIR = BASE_DIR / "database"

# Logs
LOGS_DIR = BASE_DIR / "logs"

# Saved Files
BEST_MODEL = MODELS_DIR / "best_model.pkl"
FALLBACK_MODEL = MODELS_DIR / "linear_regression.pkl"
SCALER_FILE = MODELS_DIR / "scaler.pkl"

FEATURE_DATASET = PROCESSED_DATA / "battery_features.csv"
CLEAN_DATASET = PROCESSED_DATA / "battery_clean.csv"
ML_DATASET = PROCESSED_DATA / "battery_ml.csv"

# Random Seed
RANDOM_STATE = 42

# Test Size
TEST_SIZE = 0.20

# Default Figure Size
FIGURE_SIZE = (10, 6)

# Target column
TARGET = "soh"

# Columns present in the raw/feature dataset that are NOT model inputs
EXCLUDE_COLUMNS = [
    TARGET,
    "vehicle_id",
    "timestamp",
    "charger_type",
    "battery_failure_risk",
]

# ------------------------------------------------------------------
# THE canonical, ordered feature list.
#
# Both src/train_model.py (training) and src/battery_predictor.py
# (inference) import this instead of each defining their own copy.
# This is what prevents a silent train/serve feature-order mismatch.
# ------------------------------------------------------------------
FEATURE_COLUMNS = [
    "battery_voltage",
    "battery_current",
    "battery_power_kw",
    "soc",
    "battery_temp",
    "ambient_temp",
    "charge_cycles",
    "fast_charge_count",
    "total_distance_km",
    "trip_distance_km",
    "avg_speed_kmh",
    "max_speed_kmh",
    "acceleration_ms2",
    "regenerative_energy_kwh",
    "energy_consumption_kwh_100km",
    "motor_temp",
    "inverter_temp",
    "charging_duration_min",
    "cell_voltage_std",
    "internal_resistance",
    "battery_age_days",
    "humidity",
    "remaining_range_km",
    "rul_cycles",
    "battery_age_years",
    "fast_charge_ratio",
    "battery_stress_index",
    "temperature_difference",
    "avg_distance_per_cycle",
    "power_to_voltage_ratio",
    "range_per_soc",
]
