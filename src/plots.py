"""
=========================================================
EV Battery Health Analytics
plots.py

Professional visualization module
Python 3.10.10
=========================================================
"""

from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================================
# Create Images Folder
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGES = BASE_DIR / "images"

IMAGES.mkdir(exist_ok=True)

# ==========================================================
# 1. Actual vs Predicted
# ==========================================================

def actual_vs_predicted(y_true, y_pred):

    plt.figure(figsize=(8,6))

    plt.scatter(
        y_true,
        y_pred,
        alpha=0.6
    )

    plt.plot(
        [min(y_true), max(y_true)],
        [min(y_true), max(y_true)],
        "r--",
        linewidth=2
    ) 

    plt.title("Actual vs Predicted SOH")

    plt.xlabel("Actual SOH")

    plt.ylabel("Predicted SOH")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES/"actual_vs_predicted.png")

    plt.close()

# ==========================================================
# 2. Residual Plot
# ==========================================================

def residual_plot(y_true, y_pred):

    residuals = y_true - y_pred

    plt.figure(figsize=(8,6))

    plt.scatter(
        y_pred,
        residuals,
        alpha=0.6
    )

    plt.axhline(
        y=0,
        color="red",
        linestyle="--"
    )

    plt.title("Residual Plot")

    plt.xlabel("Predicted SOH")

    plt.ylabel("Residual")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES/"residual_plot.png")

    plt.close()

# ==========================================================
# 3. Residual Histogram
# ==========================================================

def residual_histogram(y_true, y_pred):

    residuals = y_true - y_pred

    plt.figure(figsize=(8,6))

    plt.hist(
        residuals,
        bins=30,
        edgecolor="black"
    )

    plt.title("Residual Histogram")

    plt.xlabel("Residual")

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES/"residual_histogram.png")

    plt.close()

# ==========================================================
# 4. Prediction Distribution
# ==========================================================

def prediction_distribution(y_pred):

    plt.figure(figsize=(8,6))

    plt.hist(
        y_pred,
        bins=30,
        edgecolor="black"
    )

    plt.title("Prediction Distribution")

    plt.xlabel("Predicted SOH")

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES/"prediction_distribution.png")

    plt.close()

# ==========================================================
# Create All Plots
# ==========================================================

def create_all_plots(y_true, y_pred):

    print("\nGenerating Professional Visualizations...\n")

    actual_vs_predicted(y_true, y_pred)

    residual_plot(y_true, y_pred)

    residual_histogram(y_true, y_pred)

    prediction_distribution(y_pred)

    print("✓ Actual vs Predicted")

    print("✓ Residual Plot")

    print("✓ Residual Histogram")

    print("✓ Prediction Distribution")

    print("\nAll plots created successfully.")