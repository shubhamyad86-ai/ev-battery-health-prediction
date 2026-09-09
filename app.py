import matplotlib.pyplot as plt
import textwrap
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from src.battery_predictor import BatteryPredictor
from src.auth import require_login, is_admin, USERS
from src.theme import inject_css, kpi_card, card_open, card_close, style_plotly, status_badge_class, ACCENT, _html
from src.dashboard import show_dashboard

# ----------------------------------------------------
# Page setup
# ----------------------------------------------------

st.set_page_config(
    page_title="EV Battery Health Prediction",
    page_icon="🔋",
    layout="wide"
)

# Gate the entire app behind login. Shows a login form and halts here
# (via st.stop()) if the user isn't authenticated yet. Once logged in,
# this also renders the sidebar nav + "logged in as ... / Log Out" box,
# and sets st.session_state["page"] to the current page.
require_login()

inject_css()

predictor = BatteryPredictor()

page = st.session_state.get("page", "dashboard")

header_left, header_right = st.columns([3, 1])
with header_left:
    st.markdown(_html(f"""
        <h1 style="margin-bottom:0;">🔋 EV Battery Health Prediction</h1>
        <p style="color:#94a3b8;margin-top:0.2rem;">Battery Health Analysis</p>
        """), unsafe_allow_html=True)
with header_right:
    st.markdown(_html(f"""
        <div style="text-align:right;padding-top:1rem;">
            <span style="color:#94a3b8;">Welcome,</span><br>
            <span style="font-weight:700;color:{ACCENT};">{st.session_state.get('display_name', '')}</span>
        </div>
        """), unsafe_allow_html=True)
st.markdown("---")

# Raw feature columns used everywhere (single prediction + batch prediction)
RAW_FEATURE_COLUMNS = [
    "battery_voltage", "battery_current", "soc", "battery_temp",
    "ambient_temp", "charge_cycles", "fast_charge_count",
    "total_distance_km", "trip_distance_km", "avg_speed_kmh",
    "max_speed_kmh", "acceleration_ms2", "regenerative_energy_kwh",
    "energy_consumption_kwh_100km", "motor_temp", "inverter_temp",
    "charging_duration_min", "cell_voltage_std", "internal_resistance",
    "battery_age_days", "humidity", "remaining_range_km", "rul_cycles",
]

FULL_FEATURE_ORDER = RAW_FEATURE_COLUMNS + [
    "battery_age_years",
    "fast_charge_ratio",
    "battery_stress_index",
    "temperature_difference",
    "avg_distance_per_cycle",
    "power_to_voltage_ratio",
    "range_per_soc",
]
# NOTE: battery_power_kw is inserted right after battery_current below to
# match the exact order battery_predictor.py's feature_names list expects.
FULL_FEATURE_ORDER.insert(2, "battery_power_kw")


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add the engineered columns the model was trained on to a raw dataframe."""
    df = df.copy()
    df["battery_power_kw"] = (df["battery_voltage"] * df["battery_current"]) / 1000
    df["battery_age_years"] = df["battery_age_days"] / 365
    df["fast_charge_ratio"] = df["fast_charge_count"] / (df["charge_cycles"] + 1)
    df["battery_stress_index"] = df["battery_temp"] * df["internal_resistance"]
    df["temperature_difference"] = df["battery_temp"] - df["ambient_temp"]
    df["avg_distance_per_cycle"] = df["total_distance_km"] / (df["charge_cycles"] + 1)
    df["power_to_voltage_ratio"] = df.apply(
        lambda row: row["battery_power_kw"] / row["battery_voltage"]
        if row["battery_voltage"] != 0 else 0,
        axis=1,
    )
    df["range_per_soc"] = df["remaining_range_km"] / (df["soc"] + 1)
    return df


def status_for(soh: float) -> str:
    if soh >= 90:
        return "🟢 Excellent"
    elif soh >= 80:
        return "🟢 Good"
    elif soh >= 70:
        return "🟡 Moderate"
    elif soh >= 60:
        return "🟠 Weak"
    else:
        return "🔴 Replace Battery"


def compute_risk(prediction, battery_temp, internal_resistance, charge_cycles, battery_voltage):
    """Shared risk-score logic, used by both the prediction page's quick
    preview and the full Risk Analysis section on the Analytics page."""
    risk_score = 0
    if prediction < 70:
        risk_score += 40
    elif prediction < 80:
        risk_score += 20
    if battery_temp > 45:
        risk_score += 20
    elif battery_temp > 35:
        risk_score += 10
    if internal_resistance > 0.05:
        risk_score += 20
    elif internal_resistance > 0.03:
        risk_score += 10
    if charge_cycles > 1500:
        risk_score += 20
    elif charge_cycles > 1000:
        risk_score += 10
    if battery_voltage < 300:
        risk_score += 10
    risk_score = min(risk_score, 100)

    if risk_score < 20:
        label, color = "Low Risk", "#22c55e"
    elif risk_score < 50:
        label, color = "Moderate Risk", "#f59e0b"
    elif risk_score < 80:
        label, color = "High Risk", "#f97316"
    else:
        label, color = "Critical Risk", "#ef4444"
    return risk_score, label, color


def compute_recommendations(prediction, battery_temp, internal_resistance, charge_cycles, battery_voltage):
    recommendations = []
    if prediction < 80:
        recommendations.append("Replace the battery soon or schedule a detailed inspection.")
    if battery_temp > 45:
        recommendations.append("Reduce battery temperature before charging.")
    if internal_resistance > 0.05:
        recommendations.append("Internal resistance is high. Inspect battery cells.")
    if charge_cycles > 1000:
        recommendations.append("Battery has completed many charge cycles.")
    if battery_voltage < 300:
        recommendations.append("Battery voltage is lower than expected.")
    return recommendations


# ======================================================
# PAGE: Dashboard
# ======================================================
if page == "dashboard":

    total_users = len(USERS)
    total_predictions = 0
    average_soh = 0.0

    if os.path.exists("predictions.csv"):
        history = pd.read_csv("predictions.csv")
        if not history.empty and "SOH" in history.columns:
            total_predictions = len(history)
            average_soh = history["SOH"].mean()

    show_dashboard(
        total_users=total_users,
        total_predictions=total_predictions,
        average_soh=average_soh,
    )

# ======================================================
# PAGE: New Prediction
# ======================================================
elif page == "prediction":

    st.subheader("Battery Input")

    col1, col2 = st.columns(2)

    with col1:
        battery_voltage = st.number_input("Battery Voltage (V)", min_value=0.0, value=400.0)
        battery_current = st.number_input("Battery Current (A)", value=120.0)
        soc = st.number_input("State of Charge (%)", min_value=0.0, max_value=100.0, value=80.0)
        battery_temp = st.number_input("Battery Temperature (°C)", value=30.0)
        ambient_temp = st.number_input("Ambient Temperature (°C)", value=25.0)
        charge_cycles = st.number_input("Charge Cycles", min_value=0, value=350)
        fast_charge_count = st.number_input("Fast Charge Count", min_value=0, value=80)
        total_distance_km = st.number_input("Total Distance (km)", value=60000.0)
        trip_distance_km = st.number_input("Trip Distance (km)", value=120.0)
        avg_speed_kmh = st.number_input("Average Speed (km/h)", value=55.0)
        max_speed_kmh = st.number_input("Maximum Speed (km/h)", value=120.0)
        acceleration_ms2 = st.number_input("Acceleration (m/s²)", value=3.2)

    with col2:
        regenerative_energy_kwh = st.number_input("Regenerative Energy (kWh)", value=2.5)
        energy_consumption_kwh_100km = st.number_input("Energy Consumption (kWh/100km)", value=16.0)
        motor_temp = st.number_input("Motor Temperature (°C)", value=45.0)
        inverter_temp = st.number_input("Inverter Temperature (°C)", value=42.0)
        charging_duration_min = st.number_input("Charging Duration (min)", value=90.0)
        cell_voltage_std = st.number_input("Cell Voltage Std", value=0.02)
        internal_resistance = st.number_input("Internal Resistance", value=0.03)
        battery_age_days = st.number_input("Battery Age (Days)", value=900)
        humidity = st.number_input("Humidity (%)", value=55.0)
        remaining_range_km = st.number_input("Remaining Range (km)", value=280.0)
        rul_cycles = st.number_input("Remaining Useful Life (Cycles)", value=650)

    battery_power_kw = (battery_voltage * battery_current) / 1000
    battery_age_years = battery_age_days / 365
    fast_charge_ratio = fast_charge_count / (charge_cycles + 1)
    battery_stress_index = battery_temp * internal_resistance
    temperature_difference = battery_temp - ambient_temp
    avg_distance_per_cycle = total_distance_km / (charge_cycles + 1)
    power_to_voltage_ratio = battery_power_kw / battery_voltage if battery_voltage != 0 else 0
    range_per_soc = remaining_range_km / (soc + 1)

    st.markdown("---")

    if st.button("🔋 Predict Battery Health"):

        features = [
            battery_voltage, battery_current, battery_power_kw, soc,
            battery_temp, ambient_temp, charge_cycles, fast_charge_count,
            total_distance_km, trip_distance_km, avg_speed_kmh, max_speed_kmh,
            acceleration_ms2, regenerative_energy_kwh, energy_consumption_kwh_100km,
            motor_temp, inverter_temp, charging_duration_min, cell_voltage_std,
            internal_resistance, battery_age_days, humidity, remaining_range_km,
            rul_cycles, battery_age_years, fast_charge_ratio, battery_stress_index,
            temperature_difference, avg_distance_per_cycle, power_to_voltage_ratio,
            range_per_soc,
        ]

        try:
            prediction = predictor.predict(features)
            status = status_for(prediction)

            new_prediction = pd.DataFrame([{
                "SOH": round(prediction, 2),
                "Battery Age (Days)": battery_age_days,
                "Remaining Useful Life (Cycles)": rul_cycles,
                "Status": status
            }])

            if os.path.exists("predictions.csv"):
                new_prediction.to_csv("predictions.csv", mode="a", header=False, index=False)
            else:
                new_prediction.to_csv("predictions.csv", index=False)

            risk_score, risk_label, risk_color = compute_risk(
                prediction, battery_temp, internal_resistance, charge_cycles, battery_voltage
            )
            recommendations = compute_recommendations(
                prediction, battery_temp, internal_resistance, charge_cycles, battery_voltage
            )

            st.session_state["has_predicted"] = True
            st.session_state["prediction"] = prediction
            st.session_state["status"] = status
            st.session_state["battery_age_days"] = battery_age_days
            st.session_state["battery_age_years"] = battery_age_years
            st.session_state["rul_cycles"] = rul_cycles
            st.session_state["battery_temp"] = battery_temp
            st.session_state["battery_voltage"] = battery_voltage
            st.session_state["soc"] = soc
            st.session_state["charge_cycles"] = charge_cycles
            st.session_state["internal_resistance"] = internal_resistance
            st.session_state["total_distance_km"] = total_distance_km
            st.session_state["energy_consumption_kwh_100km"] = energy_consumption_kwh_100km
            st.session_state["risk_score"] = risk_score
            st.session_state["risk_label"] = risk_label
            st.session_state["risk_color"] = risk_color
            st.session_state["recommendations"] = recommendations

        except Exception as e:
            st.error(f"Prediction failed: {e}")

    if st.session_state.get("has_predicted"):

        prediction = st.session_state["prediction"]
        status = st.session_state["status"]
        risk_score = st.session_state["risk_score"]
        risk_label = st.session_state["risk_label"]
        risk_color = st.session_state["risk_color"]

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            kpi_card("SOH (State of Health)", f"{prediction:.2f}%", status)
        with k2:
            kpi_card("RUL (Remaining Useful Life)", f"{st.session_state['rul_cycles']}", "Cycles Estimated")
        with k3:
            kpi_card("Battery Status", status.split(" ", 1)[-1] if " " in status else status, "Performance")
        with k4:
            kpi_card("Risk Level", risk_label, f"Score: {risk_score}%", sub_color=risk_color)

        gauge_col, summary_col = st.columns([1.3, 1])

        with gauge_col:
            card_open("SOH Gauge")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                title={"text": "Battery State of Health (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#22c55e"},
                    "steps": [
                        {"range": [0, 50], "color": "#7f1d1d"},
                        {"range": [50, 70], "color": "#7c2d12"},
                        {"range": [70, 90], "color": "#78350f"},
                        {"range": [90, 100], "color": "#14532d"},
                    ],
                    "threshold": {
                        "line": {"color": "white", "width": 4},
                        "thickness": 0.8,
                        "value": prediction,
                    },
                },
            ))
            fig.update_layout(height=340)
            style_plotly(fig)
            st.plotly_chart(fig, use_container_width=True)
            card_close()

        with summary_col:
            card_open("Prediction Summary")
            st.write(f"**Battery Age:** {st.session_state['battery_age_days']} Days")
            st.write(f"**Remaining Useful Life:** {st.session_state['rul_cycles']} Cycles")
            st.write(f"**Status:** {status}")
            st.markdown("<br>", unsafe_allow_html=True)
            if prediction >= 90:
                st.success("Battery is healthy. Continue normal charging.")
            elif prediction >= 80:
                st.info("Battery is in good condition. Avoid excessive fast charging.")
            elif prediction >= 70:
                st.warning("Battery health is decreasing. Schedule a battery inspection.")
            else:
                st.error("Battery health is poor. Replacement may be required.")
            card_close()

        params_col, temp_col = st.columns([1, 1])

        with params_col:
            card_open("Key Battery Parameters")
            st.write(f"🔋 Battery Voltage &nbsp; **{st.session_state['battery_voltage']:.2f} V**")
            st.write(f"🔌 State of Charge (SOC) &nbsp; **{st.session_state['soc']:.2f} %**")
            st.write(f"🌡️ Battery Temperature &nbsp; **{st.session_state['battery_temp']:.2f} °C**")
            st.write(f"🔁 Charge Cycles &nbsp; **{st.session_state['charge_cycles']}**")
            st.write(f"🛣️ Total Distance &nbsp; **{st.session_state['total_distance_km']:,.1f} km**")
            st.write(f"⚡ Energy Consumption &nbsp; **{st.session_state['energy_consumption_kwh_100km']:.2f} kWh/100km**")
            st.write(f"🧯 Internal Resistance &nbsp; **{st.session_state['internal_resistance']:.3f} Ω**")
            st.write(f"📅 Battery Age &nbsp; **{st.session_state['battery_age_years']:.1f} Years**")
            card_close()

        with temp_col:
            card_open("Battery Temperature")
            temp_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=st.session_state["battery_temp"],
                title={"text": "Battery Temperature (°C)"},
                gauge={
                    "axis": {"range": [0, 80]},
                    "bar": {"color": "#22c55e"},
                    "steps": [
                        {"range": [0, 35], "color": "#14532d"},
                        {"range": [35, 50], "color": "#78350f"},
                        {"range": [50, 80], "color": "#7f1d1d"}
                    ]
                }
            ))
            temp_fig.update_layout(height=300)
            style_plotly(temp_fig)
            st.plotly_chart(temp_fig, use_container_width=True)
            card_close()

        st.markdown("---")
        st.header("📄 Generate Battery Health Report")

        if st.button("Generate PDF Report"):
            try:
                from reportlab.platypus import SimpleDocTemplate, Paragraph
                from reportlab.lib.styles import getSampleStyleSheet

                r_recommendations = st.session_state.get("recommendations", [])

                pdf_file = "battery_health_report.pdf"
                doc = SimpleDocTemplate(pdf_file)
                styles = getSampleStyleSheet()
                story = []

                story.append(Paragraph("<b>Battery Health Report</b>", styles["Title"]))
                story.append(Paragraph(f"Predicted SOH: {prediction:.2f}%", styles["BodyText"]))
                story.append(Paragraph(f"Battery Status: {status}", styles["BodyText"]))
                story.append(Paragraph(f"Battery Age: {st.session_state['battery_age_days']} Days", styles["BodyText"]))
                story.append(Paragraph(f"Remaining Useful Life: {st.session_state['rul_cycles']} Cycles", styles["BodyText"]))
                story.append(Paragraph(f"Battery Temperature: {st.session_state['battery_temp']} °C", styles["BodyText"]))
                story.append(Paragraph(f"Risk Score: {risk_score}%", styles["BodyText"]))

                if r_recommendations:
                    story.append(Paragraph(
                        "Maintenance Recommendations:<br/>" + "<br/>".join(r_recommendations),
                        styles["BodyText"]
                    ))
                else:
                    story.append(Paragraph(
                        "Maintenance Recommendations: Battery is operating normally.",
                        styles["BodyText"]
                    ))

                doc.build(story)
                st.success("✅ PDF Report Generated Successfully")

                with open(pdf_file, "rb") as pdf:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf,
                        file_name="battery_health_report.pdf",
                        mime="application/pdf"
                    )
            except Exception as e:
                st.error(f"Could not generate PDF report: {e}")

# ======================================================
# PAGE: Prediction History
# ======================================================
elif page == "history":

    st.header("📋 Prediction History")

    if os.path.exists("predictions.csv"):
        history = pd.read_csv("predictions.csv")

        if history.empty:
            st.info("No predictions yet. Make one from the New Prediction page.")
        else:
            st.dataframe(history, use_container_width=True)

            csv_bytes = history.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Prediction History",
                data=csv_bytes,
                file_name="predictions.csv",
                mime="text/csv"
            )

            st.markdown("---")
            st.subheader("📈 Battery Health Trend")
            if "SOH" not in history.columns:
                st.error("SOH column not found in predictions.csv.")
            else:
                trend_fig = px.line(history, y="SOH", title="Battery State of Health History", markers=True)
                trend_fig.update_traces(line_color="#22c55e")
                style_plotly(trend_fig)
                st.plotly_chart(trend_fig, use_container_width=True)

            st.markdown("---")
            st.subheader("🥧 Battery Status Distribution")
            if "Status" in history.columns:
                status_count = history["Status"].value_counts()
                pie = px.pie(values=status_count.values, names=status_count.index, title="Prediction Distribution")
                style_plotly(pie)
                st.plotly_chart(pie, use_container_width=True)
    else:
        st.info("No predictions yet. Make one from the New Prediction page.")

# ======================================================
# PAGE: Analytics
# ======================================================
elif page == "analytics":

    st.header("⚠️ Battery Risk Analysis")

    if not st.session_state.get("has_predicted"):
        st.info("Make a prediction on the New Prediction page first to see risk analysis and recommendations.")
    else:
        risk_score = st.session_state["risk_score"]

        rc1, rc2 = st.columns(2)
        with rc1:
            st.metric("Battery Risk Score", f"{risk_score}%")
        with rc2:
            if risk_score < 20:
                st.success("🟢 LOW")
            elif risk_score < 50:
                st.warning("🟡 MODERATE")
            elif risk_score < 80:
                st.error("🟠 HIGH")
            else:
                st.error("🔴 CRITICAL")
        st.progress(risk_score / 100)

        st.markdown("---")
        st.header("🛠️ Maintenance Recommendations")
        recommendations = st.session_state.get("recommendations", [])
        if not recommendations:
            st.success("Battery is operating normally.")
        else:
            for item in recommendations:
                st.write(f"• {item}")

    if is_admin():
        st.markdown("---")
        st.header("📊 Executive Dashboard")

        if os.path.exists("predictions.csv"):
            history = pd.read_csv("predictions.csv")
            if history.empty:
                st.warning("No prediction history available.")
            elif "SOH" not in history.columns:
                st.error("SOH column not found in predictions.csv.")
            else:
                avg_soh = history["SOH"].mean()
                max_soh = history["SOH"].max()
                min_soh = history["SOH"].min()
                total_predictions = len(history)

                e1, e2, e3, e4 = st.columns(4)
                with e1:
                    st.metric("Average SOH", f"{avg_soh:.2f}%")
                with e2:
                    st.metric("Maximum SOH", f"{max_soh:.2f}%")
                with e3:
                    st.metric("Minimum SOH", f"{min_soh:.2f}%")
                with e4:
                    st.metric("Predictions", total_predictions)

    st.markdown("---")
    st.subheader("📊 Battery Health Distribution")

    if os.path.exists("predictions.csv"):
        history = pd.read_csv("predictions.csv")
        if not history.empty and "SOH" in history.columns:
            histogram = px.histogram(history, x="SOH", nbins=20, title="Battery State of Health Distribution")
            style_plotly(histogram)
            st.plotly_chart(histogram, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Feature Correlation")

    if os.path.exists("predictions.csv"):
        history = pd.read_csv("predictions.csv")
        if history.empty:
            st.warning("No prediction history available.")
        else:
            numeric_history = history.select_dtypes(include="number")
            if numeric_history.shape[1] < 2:
                st.warning("Not enough numeric columns for correlation.")
            else:
                corr = numeric_history.corr()
                heatmap = px.imshow(
                    corr, text_auto=True, title="Feature Correlation Matrix",
                    color_continuous_scale="RdBu_r"
                )
                style_plotly(heatmap)
                st.plotly_chart(heatmap, use_container_width=True)

# ======================================================
# PAGE: Batch Prediction
# ======================================================
elif page == "batch":

    st.header("📁 Batch Prediction")

    uploaded_file = st.file_uploader("Upload a battery dataset (CSV)", type=["csv"])

    if uploaded_file is not None:
        batch_data = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Dataset")
        st.dataframe(batch_data, use_container_width=True)

        try:
            st.write(f"Columns in the uploaded dataset: {batch_data.columns.tolist()}")

            missing_columns = [c for c in RAW_FEATURE_COLUMNS if c not in batch_data.columns]
            if missing_columns:
                st.error(f"Uploaded CSV is missing required columns: {missing_columns}")
            else:
                st.success("Columns verified. Proceeding with predictions...")

                batch_data = engineer_features(batch_data)
                batch_predictions = predictor.predict(batch_data)

                batch_data["Predicted SOH"] = batch_predictions
                batch_data["Battery Status"] = batch_data["Predicted SOH"].apply(status_for)

                st.subheader("Prediction Results")
                st.dataframe(batch_data, use_container_width=True)

                batch_csv = batch_data.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download Results",
                    batch_csv,
                    "batch_predictions.csv",
                    "text/csv"
                )

        except Exception as e:
            st.exception(e)

# ======================================================
# PAGE: Feature Importance (admin only)
# ======================================================
elif page == "importance":

    if not is_admin():
        st.warning("This page is only available to admin users.")
    else:
        st.header("📊 Feature Importance")

        try:
            model = predictor.model

            if hasattr(model, "feature_importances_"):
                feature_importance = pd.DataFrame({
                    "Feature": FULL_FEATURE_ORDER,
                    "Importance": model.feature_importances_
                }).sort_values(by="Importance", ascending=False)

                st.dataframe(feature_importance, use_container_width=True)

                fig2, ax = plt.subplots(figsize=(10, 6))
                ax.barh(feature_importance["Feature"], feature_importance["Importance"])
                ax.set_xlabel("Importance")
                ax.set_title("Model Feature Importance")
                st.pyplot(fig2)

            elif hasattr(model, "coef_"):
                coefs = model.coef_
                coefs = coefs.flatten() if hasattr(coefs, "flatten") else coefs
                feature_importance = pd.DataFrame({
                    "Feature": FULL_FEATURE_ORDER,
                    "Coefficient": coefs
                }).sort_values(by="Coefficient", key=abs, ascending=False)

                st.dataframe(feature_importance, use_container_width=True)

                fig2, ax = plt.subplots(figsize=(10, 6))
                ax.barh(feature_importance["Feature"], feature_importance["Coefficient"])
                ax.set_xlabel("Coefficient")
                ax.set_title("Model Coefficients")
                st.pyplot(fig2)

            else:
                st.info("This model does not support feature importance.")

        except Exception as e:
            st.error(f"Unable to display feature importance: {e}")