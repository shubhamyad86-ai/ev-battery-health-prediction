"""
==============================================================
Project : EV Battery Health Analytics
Module  : Exploratory Data Analysis (EDA)
Author  : Shubham Yadav
Python  : 3.10.10
Version : 1.0
==============================================================

Description
-----------
This module performs Exploratory Data Analysis (EDA)
on the EV Battery Telemetry Dataset.

Features
--------
✓ Dataset Overview
✓ Missing Value Analysis
✓ Duplicate Analysis
✓ Statistical Summary
✓ Memory Usage
✓ Data Types
✓ Automatic Report Generation

==============================================================
"""

# ==========================================================
# IMPORT LIBRARIES
# ==========================================================

from pathlib import Path
import logging
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

RAW_DATA = DATA_DIR / "raw"

PROCESSED_DATA = DATA_DIR / "processed"

REPORTS = BASE_DIR / "reports"

IMAGES = BASE_DIR / "images"

REPORTS.mkdir(exist_ok=True)

IMAGES.mkdir(exist_ok=True)

# ==========================================================
# LOAD DATASET
# ==========================================================

def load_dataset():

    logger.info("Loading Clean Dataset")

    file = PROCESSED_DATA / "battery_clean.csv"

    if not file.exists():

        raise FileNotFoundError(
            f"\nDataset Not Found\n{file}"
        )

    df = pd.read_csv(file)

    logger.info("Dataset Loaded Successfully")

    return df

# ==========================================================
# DATASET INFORMATION
# ==========================================================

def dataset_information(df):

    print("\n")
    print("=" * 70)
    print("DATASET INFORMATION")
    print("=" * 70)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names\n")

    for column in df.columns:

        print(column)

    print("\nData Types\n")

    print(df.dtypes)

# ==========================================================
# MEMORY USAGE
# ==========================================================

def memory_usage(df):

    print("\n")
    print("=" * 70)
    print("MEMORY USAGE")
    print("=" * 70)

    memory = df.memory_usage(deep=True).sum() / 1024 ** 2

    print(f"{memory:.2f} MB")

# ==========================================================
# MISSING VALUES
# ==========================================================

def missing_values(df):

    print("\n")
    print("=" * 70)
    print("MISSING VALUES")
    print("=" * 70)

    missing = df.isnull().sum()

    percentage = (missing / len(df)) * 100

    report = pd.DataFrame({

        "Missing Values": missing,

        "Percentage": percentage

    })

    print(report)

    report.to_csv(

        REPORTS / "missing_values.csv",

        index=True

    )

# ==========================================================
# DUPLICATE ANALYSIS
# ==========================================================

def duplicate_analysis(df):

    print("\n")
    print("=" * 70)
    print("DUPLICATE RECORDS")
    print("=" * 70)

    duplicates = df.duplicated().sum()

    print(f"Duplicate Rows : {duplicates}")

# ==========================================================
# DATA TYPES
# ==========================================================

def data_types(df):

    print("\n")
    print("=" * 70)
    print("DATA TYPES")
    print("=" * 70)

    print(df.dtypes)

# ==========================================================
# STATISTICAL SUMMARY
# ==========================================================

def statistical_summary(df):

    print("\n")
    print("=" * 70)
    print("STATISTICAL SUMMARY")
    print("=" * 70)

    summary = df.describe(include="all")

    print(summary)

    summary.to_csv(

        REPORTS / "summary_statistics.csv"

    )

# ==========================================================
# NUMERICAL FEATURES
# ==========================================================

def numerical_features(df):

    numerical = df.select_dtypes(

        include=np.number

    ).columns.tolist()

    print("\n")
    print("=" * 70)
    print("NUMERICAL FEATURES")
    print("=" * 70)

    for feature in numerical:

        print(feature)

# ==========================================================
# CATEGORICAL FEATURES
# ==========================================================

def categorical_features(df):

    categorical = df.select_dtypes(

        exclude=np.number

    ).columns.tolist()

    print("\n")
    print("=" * 70)
    print("CATEGORICAL FEATURES")
    print("=" * 70)

    for feature in categorical:

        print(feature)

# ==========================================================
# SAVE DATASET INFORMATION
# ==========================================================

def save_dataset_report(df):

    report_file = REPORTS / "dataset_information.txt"

    with open(report_file, "w") as file:

        file.write("EV Battery Analytics\n")

        file.write("=" * 60)

        file.write("\n\n")

        file.write(f"Rows : {df.shape[0]}\n")

        file.write(f"Columns : {df.shape[1]}\n\n")

        file.write("Columns\n")

        file.write("-" * 30)

        file.write("\n")

        for column in df.columns:

            file.write(column + "\n")

        file.write("\n")

        file.write("Data Types\n")

        file.write("-" * 30)

        file.write("\n")

        file.write(str(df.dtypes))

        file.write("\n")

    logger.info("Dataset report saved.")



# ==========================================================
# HISTOGRAM
# ==========================================================

def plot_histogram(df, column, bins=30):

    plt.figure(figsize=(10,6))

    plt.hist(
        df[column],
        bins=bins,
        edgecolor="black"
    )

    plt.title(f"{column} Distribution")

    plt.xlabel(column)

    plt.ylabel("Frequency")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES / f"{column}_histogram.png")

    plt.close()

    logger.info(f"Histogram saved : {column}")

    # ==========================================================
# BOX PLOT
# ==========================================================

def plot_boxplot(df, column):

    plt.figure(figsize=(8,5))

    plt.boxplot(df[column])

    plt.title(f"{column} Box Plot")

    plt.ylabel(column)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES / f"{column}_boxplot.png")

    plt.close()

    logger.info(f"Boxplot saved : {column}")

# ==========================================================
# SCATTER PLOT
# ==========================================================

def scatter_plot(df, x, y):

    plt.figure(figsize=(8,6))

    plt.scatter(
        df[x],
        df[y],
        alpha=0.5
    )

    plt.title(f"{y} vs {x}")

    plt.xlabel(x)

    plt.ylabel(y)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(IMAGES / f"{y}_vs_{x}.png")

    plt.close()

    logger.info(f"Scatter Plot Saved : {y} vs {x}")

# ==========================================================
# CORRELATION MATRIX
# ==========================================================

def correlation_matrix(df):

    corr = df.select_dtypes(include=np.number).corr()

    plt.figure(figsize=(14,12))

    plt.imshow(
        corr,
        cmap="coolwarm",
        aspect="auto"
    )

    plt.colorbar()

    plt.xticks(
        range(len(corr.columns)),
        corr.columns,
        rotation=90
    )

    plt.yticks(
        range(len(corr.columns)),
        corr.columns
    )

    plt.title("Correlation Matrix")

    plt.tight_layout()

    plt.savefig(IMAGES / "correlation_matrix.png")

    plt.close()

    corr.to_csv(
        REPORTS / "correlation_matrix.csv"
    )

    logger.info("Correlation Matrix Saved")

# ==========================================================
# CORRELATION WITH SOH
# ==========================================================

def correlation_with_target(df):

    corr = df.select_dtypes(include=np.number).corr()

    soh_corr = corr["soh"]

    soh_corr = soh_corr.sort_values(
        ascending=False
    )

    print()

    print("="*60)

    print("Correlation With SOH")

    print("="*60)

    print(soh_corr)

    soh_corr.to_csv(
        REPORTS / "correlation_with_soh.csv"
    )

# ==========================================================
# DISTRIBUTION ANALYSIS
# ==========================================================

def distribution_analysis(df):

    columns = [

        "soh",

        "soc",

        "battery_voltage",

        "battery_current",

        "battery_temp",

        "charge_cycles",

        "internal_resistance",

        "remaining_range_km"

    ]

    for column in columns:

        plot_histogram(df, column)

        plot_boxplot(df, column)


# ==========================================================
# SCATTER ANALYSIS
# ==========================================================

def scatter_analysis(df):

    scatter_plot(
        df,
        "charge_cycles",
        "soh"
    )

    scatter_plot(
        df,
        "battery_temp",
        "soh"
    )

    scatter_plot(
        df,
        "battery_voltage",
        "soh"
    )

    scatter_plot(
        df,
        "internal_resistance",
        "soh"
    )

    scatter_plot(
        df,
        "battery_age_days",
        "soh"
    )

# ==========================================================
# FLEET STATISTICS
# ==========================================================

def fleet_statistics(df):

    print("\n")
    print("=" * 70)
    print("FLEET STATISTICS")
    print("=" * 70)

    stats = {

        "Total Vehicles": len(df),

        "Average SOH": round(df["soh"].mean(),2),

        "Minimum SOH": round(df["soh"].min(),2),

        "Maximum SOH": round(df["soh"].max(),2),

        "Average SOC": round(df["soc"].mean(),2),

        "Average Battery Temperature": round(df["battery_temp"].mean(),2),

        "Average Voltage": round(df["battery_voltage"].mean(),2),

        "Average Charge Cycles": round(df["charge_cycles"].mean(),2),

        "Average Remaining Range": round(df["remaining_range_km"].mean(),2)

    }

    report = pd.DataFrame(

        stats.items(),

        columns=["Metric","Value"]

    )

    print(report)

    report.to_csv(

        REPORTS/"fleet_statistics.csv",

        index=False

    )

# ==========================================================
# BATTERY HEALTH CATEGORY
# ==========================================================

def soh_category(df):

    conditions=[

        df["soh"]>=95,

        df["soh"]>=90,

        df["soh"]>=80,

        df["soh"]<80

    ]

    values=[

        "Excellent",

        "Good",

        "Fair",

        "Poor"

    ]

    df["Battery_Category"]=np.select(

        conditions,

        values,

        default="Unknown"

    )

    category=df["Battery_Category"].value_counts()

    print(category)

    category.to_csv(

        REPORTS/"battery_category.csv"

    )

# ==========================================================
# PIE CHART
# ==========================================================

def battery_category_plot(df):

    plt.figure(figsize=(8,8))

    df["Battery_Category"].value_counts().plot(

        kind="pie",

        autopct="%1.1f%%"

    )

    plt.ylabel("")

    plt.title("Battery Health Categories")

    plt.tight_layout()

    plt.savefig(

        IMAGES/"battery_category.png"

    )

    plt.close()

# ==========================================================
# Z SCORE
# ==========================================================

def iqr_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower) | (df[column] > upper)]

    print(f"{column} IQR Outliers: {len(outliers)}")

def zscore_outliers(df,column):

    mean=df[column].mean()

    std=df[column].std()

    z=np.abs(

        (df[column]-mean)/std

    )

    outliers=df[z>3]

    print(f"{column} Z Score Outliers : {len(outliers)}")

# ==========================================================
# FLEET RISK
# ==========================================================

def fleet_risk(df):

    risk=df["battery_failure_risk"].value_counts()

    print(risk)

    risk.to_csv(

        REPORTS/"fleet_risk.csv"

    )

    plt.figure(figsize=(7,5))

    risk.plot(

        kind="bar"

    )

    plt.title(

        "Battery Failure Risk"

    )

    plt.ylabel("Vehicles")

    plt.tight_layout()

    plt.savefig(

        IMAGES/"battery_failure_risk.png"

    )

    plt.close()

# ==========================================================
# BUSINESS REPORT
# ==========================================================

def business_report(df):

    report=[]

    report.append(

        "EV BATTERY ANALYSIS REPORT\n"

    )

    report.append(

        "="*50

    )

    report.append(

        f"\nVehicles : {len(df)}"

    )

    report.append(

        f"\nAverage SOH : {df['soh'].mean():.2f}"

    )

    report.append(

        f"\nAverage Temperature : {df['battery_temp'].mean():.2f}"

    )

    report.append(

        f"\nAverage Voltage : {df['battery_voltage'].mean():.2f}"

    )

    report.append(

        f"\nAverage Charge Cycles : {df['charge_cycles'].mean():.2f}"

    )

    report.append(

        f"\nAverage Remaining Range : {df['remaining_range_km'].mean():.2f}"

    )

    report.append(

        "\n\nRecommendations"

    )

    report.append(

        "\nIncrease monitoring for vehicles with low SOH."

    )

    report.append(

        "\nReduce excessive fast charging."

    )

    report.append(

        "\nMonitor high battery temperatures."

    )

    report.append(

        "\nSchedule maintenance for Poor batteries."

    )

    with open(

        REPORTS/"business_report.txt",

        "w"

    ) as f:

        f.writelines(report)


# ==========================================================
# MAIN
# ==========================================================

def main():

    logger.info("Starting EDA")

    df = load_dataset()

    dataset_information(df)

    memory_usage(df)

    missing_values(df)

    duplicate_analysis(df)

    data_types(df)

    statistical_summary(df)

    numerical_features(df)

    categorical_features(df)

    save_dataset_report(df)

    logger.info("EDA Part 1 Completed Successfully")

    distribution_analysis(df)

    scatter_analysis(df)

    correlation_matrix(df)

    correlation_with_target(df)

    logger.info("Visualization Completed")
    
    fleet_statistics(df)

    soh_category(df)

    battery_category_plot(df)

    fleet_risk(df)

    business_report(df)

    iqr_outliers(df,"battery_temp")
    iqr_outliers(df,"battery_voltage")
    iqr_outliers(df,"charge_cycles")
    iqr_outliers(df,"soh")

    zscore_outliers(df,"battery_temp")
    zscore_outliers(df,"battery_voltage")
    zscore_outliers(df,"charge_cycles")
    zscore_outliers(df,"soh")

if __name__ == "__main__":

    main()
