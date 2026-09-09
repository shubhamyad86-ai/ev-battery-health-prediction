import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


class ModelEvaluator:

    def __init__(self, y_true, y_pred):

        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)

    # -----------------------------
    # Metrics
    # -----------------------------
    def calculate_metrics(self):

        mae = mean_absolute_error(
            self.y_true,
            self.y_pred
        )

        rmse = np.sqrt(
            mean_squared_error(
                self.y_true,
                self.y_pred
            )
        )

        r2 = r2_score(
            self.y_true,
            self.y_pred
        )

        return {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }

    # -----------------------------
    # Dashboard Metrics
    # -----------------------------
    def show_metrics(self):

        metrics = self.calculate_metrics()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "MAE",
                f"{metrics['MAE']:.3f}"
            )

        with col2:
            st.metric(
                "RMSE",
                f"{metrics['RMSE']:.3f}"
            )

        with col3:
            st.metric(
                "R² Score",
                f"{metrics['R2']:.4f}"
            )

    # -----------------------------
    # Actual vs Predicted
    # -----------------------------
    def plot_actual_vs_predicted(self):

        fig, ax = plt.subplots(figsize=(7,5))

        ax.scatter(
            self.y_true,
            self.y_pred
        )

        minimum = min(self.y_true.min(), self.y_pred.min())
        maximum = max(self.y_true.max(), self.y_pred.max())

        ax.plot(
            [minimum, maximum],
            [minimum, maximum]
        )

        ax.set_xlabel("Actual SOH")
        ax.set_ylabel("Predicted SOH")
        ax.set_title("Actual vs Predicted")

        st.pyplot(fig)

    # -----------------------------
    # Residual Plot
    # -----------------------------
    def residual_plot(self):

        residuals = self.y_true - self.y_pred

        fig, ax = plt.subplots(figsize=(7,5))

        ax.scatter(
            self.y_pred,
            residuals
        )

        ax.axhline(
            y=0,
            linestyle="--"
        )

        ax.set_xlabel("Predicted SOH")
        ax.set_ylabel("Residual")

        st.pyplot(fig)

    # -----------------------------
    # Residual Histogram
    # -----------------------------
    def residual_histogram(self):

        residuals = self.y_true - self.y_pred

        fig, ax = plt.subplots(figsize=(7,5))

        ax.hist(
            residuals,
            bins=20
        )

        ax.set_xlabel("Residual")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)

    # -----------------------------
    # Full Dashboard
    # -----------------------------
    def show_dashboard(self):

        st.header("📊 Model Evaluation")

        self.show_metrics()

        st.subheader("Actual vs Predicted")
        self.plot_actual_vs_predicted()

        st.subheader("Residual Plot")
        self.residual_plot()

        st.subheader("Residual Distribution")
        self.residual_histogram()