"""
Premium dashboard components for EV Battery Health Prediction.
"""

import os

import pandas as pd
import streamlit as st

from src.theme import premium_card, section_header, _html


def show_dashboard(
    total_users=0,
    total_predictions=0,
    average_soh=0,
):
    """Render the main premium dashboard."""

    section_header(
        "🔋 EV Battery Analytics",
        "Monitor battery health, prediction performance and fleet insights."
    )

    # ============================
    # KPI ROW
    # ============================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            premium_card(
                "REGISTERED USERS",
                total_users,
                "Active system users",
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            premium_card(
                "PREDICTIONS",
                total_predictions,
                "Total battery assessments",
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            premium_card(
                "AVERAGE SOH",
                f"{average_soh:.2f}%",
                "Fleet battery health",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ============================
    # MAIN DASHBOARD
    # ============================

    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(_html("""
            <div class="ev-card">
                <div class="ev-card-title">📈 Battery Health Overview</div>
                <p style="color:#8297ad;">
                    Track State of Health across recorded predictions.
                </p>
            </div>
            """), unsafe_allow_html=True)

        if os.path.exists("predictions.csv"):

            history = pd.read_csv("predictions.csv")

            if "SOH" in history.columns:

                chart_data = history[["SOH"]].copy()

                st.line_chart(
                    chart_data,
                    height=320,
                )

            else:
                st.info("SOH data is not available.")

        else:
            st.info(
                "Make your first battery prediction to generate analytics."
            )

    with right:

        st.markdown(_html("""
            <div class="ev-card">
                <div class="ev-card-title">⚡ Battery Status</div>
                <p><b>Health monitoring</b></p>
                <p style="color:#8297ad;">
                    The system evaluates battery telemetry and
                    estimates State of Health using the trained
                    machine learning model.
                </p>
            </div>
            """), unsafe_allow_html=True)

    st.markdown("")

    # ============================
    # QUICK ACTIONS
    # ============================

    section_header(
        "Quick Actions",
        "Start a new battery assessment or explore previous results."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "🔋 New Prediction",
            use_container_width=True,
        ):
            st.session_state["page"] = "prediction"
            st.rerun()

    with col2:
        if st.button(
            "📊 Analytics",
            use_container_width=True,
        ):
            st.session_state["page"] = "analytics"
            st.rerun()

    with col3:
        if st.button(
            "📜 Prediction History",
            use_container_width=True,
        ):
            st.session_state["page"] = "history"
            st.rerun()