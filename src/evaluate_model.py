"""
=========================================================
Project : EV Battery Health Analytics
Module  : Model Evaluation
Author  : Shubham Yadav
Python  : 3.10.10
=========================================================
"""

# ==========================================================
# Imports
# ==========================================================

from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from metrics import evaluate
from plots import create_all_plots
from reports import create_reports


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA = BASE_DIR / "data" / "processed"

MODELS = BASE_DIR / "models"


# ==========================================================
# Load Dataset
# ==========================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_csv(
    DATA / "battery_features.csv"
)

print(f"Dataset Shape : {df.shape}")


# ==========================================================
# Remove Non-ML Columns
# ==========================================================

drop_columns = [

    "vehicle_id",

    "timestamp",

    "charger_type",

    "battery_failure_risk"

]

existing = [

    c for c in drop_columns

    if c in df.columns

]

df = df.drop(columns=existing)


# ==========================================================
# Features and Target
# ==========================================================

X = df.drop(columns=["soh"])

y = df["soh"]


# ==========================================================
# Train Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

)

print(f"Training Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")


# ==========================================================
# Load Best Model
# ==========================================================

print("\nLoading Best Model...")

model = joblib.load(

    MODELS / "best_model.pkl"

)

print("Model Loaded Successfully")


# ==========================================================
# Make Prediction
# ==========================================================

print("\nMaking Predictions...")

predictions = model.predict(X_test)

print("Prediction Completed")

# ==========================================================
# Model Evaluation
# ==========================================================

print("\n")
print("=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

results = evaluate(
    y_test,
    predictions
)

for metric, value in results.items():

    print(f"{metric:<25}: {value:.4f}")

# ==========================================================
# Generate Reports
# ==========================================================

create_reports(
    results,
    y_test,
    predictions
)

# ==========================================================
# Generate Plots
# ==========================================================

create_all_plots(
    y_test,
    predictions
)

# ==========================================================
# Finish
# ==========================================================

print("\n")
print("=" * 60)
print("MODEL EVALUATION COMPLETED")
print("=" * 60)

print("\nReports Generated")

print("✓ metrics.csv")
print("✓ prediction_results.csv")
print("✓ evaluation_report.txt")
print("✓ business_summary.txt")

print("\nPlots Generated")

print("✓ actual_vs_predicted.png")
print("✓ residual_plot.png")
print("✓ residual_histogram.png")
print("✓ prediction_distribution.png")

print("\nProject Finished Successfully.")
