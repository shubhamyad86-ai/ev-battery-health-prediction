"""
=========================================================
EV Battery Health Analytics
reports.py

Generate Professional Reports
Python 3.10.10
=========================================================
"""

from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

REPORTS = BASE_DIR / "reports"

REPORTS.mkdir(exist_ok=True)


# ==========================================================
# Save Metrics CSV
# ==========================================================

def save_metrics(metrics):

    df = pd.DataFrame({

        "Metric": list(metrics.keys()),

        "Value": list(metrics.values())

    })

    df.to_csv(

        REPORTS/"metrics.csv",

        index=False

    )


# ==========================================================
# Save Predictions
# ==========================================================

def save_predictions(

        y_true,

        y_pred

):

    df = pd.DataFrame({

        "Actual SOH": y_true,

        "Predicted SOH": y_pred,

        "Residual": y_true-y_pred

    })

    df.to_csv(

        REPORTS/"prediction_results.csv",

        index=False

    )


# ==========================================================
# Evaluation Report
# ==========================================================

def save_evaluation_report(metrics):

    with open(

        REPORTS/"evaluation_report.txt",

        "w"

    ) as file:

        file.write(
            "EV BATTERY HEALTH ANALYTICS\n"
        )

        file.write("="*50)

        file.write("\n\n")

        for key,value in metrics.items():

            file.write(

                f"{key:<25}: {value:.4f}\n"

            )


# ==========================================================
# Business Summary
# ==========================================================

def save_business_summary(metrics):

    with open(

        REPORTS/"business_summary.txt",

        "w"

    ) as file:

        file.write(
            "Business Summary\n\n"
        )

        file.write(

            f"Model explains "

            f"{metrics['R2']*100:.2f}% "

            "of battery SOH variation.\n\n"

        )

        file.write(

            f"Average prediction error "

            f"is {metrics['MAE']:.3f} SOH.\n\n"

        )

        file.write(

            "Model is suitable "

            "for battery health estimation."

        )


# ==========================================================
# Save Everything
# ==========================================================

def create_reports(

        metrics,

        y_true,

        y_pred

):

    print("\nSaving Reports...\n")

    save_metrics(metrics)

    save_predictions(

        y_true,

        y_pred

    )

    save_evaluation_report(metrics)

    save_business_summary(metrics)

    print("✓ metrics.csv")

    print("✓ prediction_results.csv")

    print("✓ evaluation_report.txt")

    print("✓ business_summary.txt")