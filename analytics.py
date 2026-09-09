import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


class BatteryAnalytics:

    def __init__(self, history):
        self.history = history.copy()

    # -----------------------------
    # Executive Dashboard
    # -----------------------------
    def executive_dashboard(self):

        st.header("📊 Executive Dashboard")

        avg_soh = self.history["SOH"].mean()
        max_soh = self.history["SOH"].max()
        min_soh = self.history["SOH"].min()
        total_predictions = len(self.history)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Average SOH", f"{avg_soh:.2f}%")

        with col2:
            st.metric("Maximum SOH", f"{max_soh:.2f}%")

        with col3:
            st.metric("Minimum SOH", f"{min_soh:.2f}%")

        with col4:
            st.metric("Predictions", total_predictions)

    # -----------------------------
    # SOH Trend
    # -----------------------------
    def soh_trend(self):

        st.subheader("📈 Battery SOH Trend")

        fig = px.line(
            self.history,
            y="SOH",
            markers=True,
            title="Battery State of Health"
        )

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Battery Status
    # -----------------------------
    def status_distribution(self):

        st.subheader("🥧 Battery Status Distribution")

        counts = self.history["Status"].value_counts()

        fig = px.pie(
            values=counts.values,
            names=counts.index
        )

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Battery Age Analysis
    # -----------------------------
    def battery_age_analysis(self):

        st.subheader("🔋 Battery Age vs SOH")

        fig = px.scatter(
            self.history,
            x="Battery Age (Days)",
            y="SOH",
            color="Status",
            size="Remaining Useful Life (Cycles)"
        )

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Remaining Useful Life
    # -----------------------------
    def rul_chart(self):

        st.subheader("🔄 Remaining Useful Life")

        fig = px.bar(
            self.history.tail(20),
            y="Remaining Useful Life (Cycles)"
        )

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Histogram
    # -----------------------------
    def soh_distribution(self):

        st.subheader("📊 SOH Distribution")

        fig = px.histogram(
            self.history,
            x="SOH",
            nbins=20
        )

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Correlation Matrix
    # -----------------------------
    def correlation_matrix(self):

        st.subheader("📈 Correlation Matrix")

        numeric = self.history.select_dtypes(include="number")

        corr = numeric.corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto"
        )

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Full Dashboard
    # -----------------------------
    def show_dashboard(self):

        self.executive_dashboard()

        st.markdown("---")

        self.soh_trend()

        self.status_distribution()

        self.battery_age_analysis()

        self.rul_chart()

        self.soh_distribution()

        self.correlation_matrix()