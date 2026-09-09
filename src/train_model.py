"""
=========================================================
Project : EV Battery Health Analytics
Module  : Train Machine Learning Model
Python  : 3.10.10
=========================================================
"""

import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

try:
    from .config import FEATURE_COLUMNS, TARGET, FEATURE_DATASET, MODELS_DIR, REPORTS_DIR, RANDOM_STATE, TEST_SIZE
    from .models import get_models
except ImportError:
    from config import FEATURE_COLUMNS, TARGET, FEATURE_DATASET, MODELS_DIR, REPORTS_DIR, RANDOM_STATE, TEST_SIZE
    from models import get_models

MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

print("=" * 60)
print("Loading Dataset")
print("=" * 60)

df = pd.read_csv(FEATURE_DATASET)

# ---------------------------------------------------------
# Features and Target
#
# IMPORTANT: we use the fixed FEATURE_COLUMNS list from
# config.py (not an auto-detected column order) so that the
# scaler/model are trained on exactly the same feature order
# that src/battery_predictor.py uses at inference time.
# ---------------------------------------------------------

missing = [c for c in FEATURE_COLUMNS if c not in df.columns]
if missing:
    raise ValueError(
        f"battery_features.csv is missing expected columns: {missing}. "
        "Check src/feature_engineering.py output."
    )

print("\nUsing Fixed Feature List (config.FEATURE_COLUMNS)")
print("=" * 60)
for i, feature in enumerate(FEATURE_COLUMNS, 1):
    print(f"{i:2d}. {feature}")
print("=" * 60)
print(f"Total Features: {len(FEATURE_COLUMNS)}")

X = df[FEATURE_COLUMNS]
y = df[TARGET]

print(f"\nFeature Shape : {X.shape}")
print(f"Target Shape  : {y.shape}")

# ---------------------------------------------------------
# Train Test Split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)

# ---------------------------------------------------------
# Feature Scaling
# ---------------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, MODELS_DIR / "scaler.pkl")

print("StandardScaler saved successfully.")
print("\nTraining Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

# ---------------------------------------------------------
# Train Models (reuses the shared registry in models.py
# instead of redefining it here)
# ---------------------------------------------------------

models = get_models()

results = []
trained_models = {}
predictions_by_model = {}

print("\nTraining Models...\n")

for name, model in models.items():
    print(f"Training {name}...")

    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    trained_models[name] = model
    predictions_by_model[name] = predictions

    results.append({
        "Model": name,
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3),
        "R2": round(r2, 3),
    })

    print(f"{name} Completed")

results_df = pd.DataFrame(results).sort_values(by="R2", ascending=False)

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)
print(results_df)

results_df.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)

# ---------------------------------------------------------
# Best model (this is what gets reported AND saved —
# previously this used the last-trained model by mistake)
# ---------------------------------------------------------

best_name = results_df.iloc[0]["Model"]
best_model = trained_models[best_name]
best_predictions = predictions_by_model[best_name]

mae = mean_absolute_error(y_test, best_predictions)
mse = mean_squared_error(y_test, best_predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, best_predictions)

print("\nBest Model Performance")
print("=" * 60)
print(f"Best Model : {best_name}")
print(f"MAE  : {mae:.3f}")
print(f"RMSE : {rmse:.3f}")
print(f"R²   : {r2:.3f}")

# ---------------------------------------------------------
# Save Models
# ---------------------------------------------------------

print("\nSaving Models...\n")

for name, model in trained_models.items():
    filename = name.lower().replace(" ", "_") + ".pkl"
    joblib.dump(model, MODELS_DIR / filename)

print("All Models Saved")

joblib.dump(best_model, MODELS_DIR / "best_model.pkl")
print(f"\nBest Model saved as best_model.pkl ({best_name})")

with open(REPORTS_DIR / "best_model.txt", "w") as file:
    file.write(f"Best Model : {best_name}\n")
    file.write(results_df.iloc[0].to_string())
