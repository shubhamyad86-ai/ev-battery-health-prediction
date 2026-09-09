"""
=========================================================
Project : EV Battery Health Analytics
Module  : Feature Selection
Python  : 3.10.10
=========================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_regression

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED = BASE_DIR / "data" / "processed"

REPORTS = BASE_DIR / "reports"

REPORTS.mkdir(exist_ok=True)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

print("=" * 70)
print("Loading Feature Dataset")
print("=" * 70)

df = pd.read_csv(PROCESSED / "battery_features.csv")

print(df.shape)

# --------------------------------------------------
# Remove Non-ML Columns
# --------------------------------------------------

drop_columns = [

    "vehicle_id",

    "timestamp",

    "charger_type",

    "battery_failure_risk"

]

existing = [c for c in drop_columns if c in df.columns]

df = df.drop(columns=existing)

# --------------------------------------------------
# Target
# --------------------------------------------------

TARGET = "soh"

X = df.drop(columns=[TARGET])

y = df[TARGET]

print()

print("Features :", X.shape[1])

print("Target :", TARGET)

# --------------------------------------------------
# Correlation with Target
# --------------------------------------------------

corr = df.corr(numeric_only=True)

target_corr = corr["soh"].sort_values(
    ascending=False
)

print()

print("=" * 70)

print("Correlation with SOH")

print("=" * 70)

print(target_corr)

target_corr.to_csv(

    REPORTS / "feature_correlation.csv"

)

# --------------------------------------------------
# Variance Threshold
# --------------------------------------------------

selector = VarianceThreshold(
    threshold=0.01
)

selector.fit(X)

selected_columns = X.columns[selector.get_support()]

print()

print("=" * 70)

print("Variance Selected Features")

print("=" * 70)

for col in selected_columns:

    print(col)
    
# --------------------------------------------------
# Mutual Information
# --------------------------------------------------

mi = mutual_info_regression(
    X,
    y,
    random_state=42
)

mi_scores = pd.Series(
    mi,
    index=X.columns
)

mi_scores = mi_scores.sort_values(
    ascending=False
)

print()

print("=" * 70)

print("Mutual Information Scores")

print("=" * 70)

print(mi_scores)

mi_scores.to_csv(

    REPORTS / "mutual_information.csv"

)

# --------------------------------------------------
# Select Top Features
# --------------------------------------------------

selector = SelectKBest(
    score_func=mutual_info_regression,
    k=10
)

selector.fit(X, y)

best_features = X.columns[
    selector.get_support()
]

print()

print("=" * 70)

print("Top 10 Features")

print("=" * 70)

for feature in best_features:

    print(feature)
    
# --------------------------------------------------
# Final Dataset
# --------------------------------------------------

final_df = df[
    list(best_features) + ["soh"]
]

final_df.to_csv(

    PROCESSED / "battery_ml.csv",

    index=False

)

print()

print("=" * 70)

print("Machine Learning Dataset Saved")

print("=" * 70)        