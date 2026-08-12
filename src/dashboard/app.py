import pandas as pd
import plotly.express as px
import streamlit as st

from src.bayesian import get_scenario_risk
from src.config.constants import AssetType
from src.data.synthetic_generator import make_asset_data
from src.diagnosis import get_asset_health
from src.explainability.engine import evaluate_decision_trust
from src.forecasting import get_risk_forecast
from src.optimizer.optimizer import calculate_best_action


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Pulse | Infrastructure Intelligence",
    layout="wide",
)

st.title("🏥 Pulse — Urban Infrastructure Decision Intelligence")
st.markdown("---")


# ---------------------------------------------------------
# Asset selection
# ---------------------------------------------------------

st.sidebar.header("🕹️ Asset Selection")

asset_options = [
    "Bridge-12",
    "Road-45",
    "Pipeline-A17",
    "Transformer-T9",
]

selected_id = st.sidebar.selectbox(
    "Select Target Asset",
    asset_options,
)


# Asset metadata
if "Bridge" in selected_id:
    asset_type = AssetType.BRIDGE
    age = 42.0
    location = "Bhubaneswar"

elif "Road" in selected_id:
    asset_type = AssetType.ROAD_SEGMENT
    age = 5.0
    location = "Cuttack"

elif "Pipeline" in selected_id:
    asset_type = AssetType.PIPELINE
    age = 15.0
    location = "Puri"

else:
    asset_type = AssetType.TRANSFORMER
    age = 28.0
    location = "Sambalpur"


# ---------------------------------------------------------
# Generate asset data
# ---------------------------------------------------------

df = make_asset_data(
    selected_id,
    asset_type,
    age,
    days=365,
)

latest_row = df.iloc[-1].to_dict()


# ---------------------------------------------------------
# Asset information
# ---------------------------------------------------------

st.caption(
    f"Asset: {selected_id} | "
    f"Type: {asset_type.value} | "
    f"Location: {location} | "
    f"Age: {age:.0f} years"
)


# ---------------------------------------------------------
# Current sensor readings
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Vibration Level",
        f"{latest_row['vibration_hz']:.2f} Hz",
    )

with col2:
    st.metric(
        "Material Strain",
        f"{latest_row['structural_strain']:.1f} µE",
    )

with col3:
    st.metric(
        "Corrosion Index",
        f"{latest_row['corrosion_index']:.3f}",
    )

with col4:
    st.metric(
        "Temperature",
        f"{latest_row['temperature_c']:.1f} °C",
    )


st.markdown("---")


# ---------------------------------------------------------
# Diagnosis and decision support
# ---------------------------------------------------------

left_col, right_col = st.columns(2)


# ---------------------------------------------------------
# Diagnostic health
# ---------------------------------------------------------

with left_col:
    st.subheader("❤️ Diagnostic Health")

    status, health_score = get_asset_health(latest_row)

    status_colors = {
        "Healthy": "green",
        "Warning": "orange",
        "Critical": "red",
    }

    status_name = status.value

    st.markdown(
        f"**Current Status:** "
        f":{status_colors.get(status_name, 'blue')}[{status_name}]"
    )

    st.progress(health_score / 100.0)

    st.caption(
        f"Baseline System Health Score: "
        f"{health_score}/100"
    )

    # -----------------------------------------------------
    # Risk forecasting
    # -----------------------------------------------------

    st.markdown("#### 📈 7/30/90-Day Risk Projection")

    forecasts = get_risk_forecast(latest_row)

    forecast_df = pd.DataFrame(
        {
            "Timeline": [
                "7 Days",
                "30 Days",
                "90 Days",
            ],
            "Failure Probability (%)": [
                forecasts[7],
                forecasts[30],
                forecasts[90],
            ],
        }
    )

    fig_line = px.line(
        forecast_df,
        x="Timeline",
        y="Failure Probability (%)",
        markers=True,
        range_y=[0, 100],
    )

    st.plotly_chart(
        fig_line,
        use_container_width=True,
    )


# ---------------------------------------------------------
# Optimized treatment support
# ---------------------------------------------------------

with right_col:
    st.subheader("🛠️ Optimized Treatment Support")

    best_action, options = calculate_best_action(
        status,
        health_score,
        priority_weight=3.5,
    )

    confidence, feature_contributions = evaluate_decision_trust(
        latest_row,
        best_action.value,
    )

    action_name = best_action.value.replace("_", " ")

    st.info(
        f"👉 **Recommended Action:** **{action_name}**\n\n"
        f"🎯 **System Confidence:** **{confidence}%**"
    )

    # -----------------------------------------------------
    # Feature contribution visualization
    # -----------------------------------------------------

    st.markdown(
        "#### 🛡️ Decision Attribution Breakdown"
    )

    contribution_df = pd.DataFrame(
        list(feature_contributions.items()),
        columns=[
            "Sensor Driver",
            "Contribution (%)",
        ],
    )

    fig_bar = px.bar(
        contribution_df,
        x="Contribution (%)",
        y="Sensor Driver",
        orientation="h",
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True,
    )


st.markdown("---")


# ---------------------------------------------------------
# What-if scenario simulation
# ---------------------------------------------------------

st.subheader("🔄 What-If Stress-Test Scenario Simulation")

st.markdown(
    "Change the environmental conditions below to see "
    "how the estimated failure risk changes."
)

sim_col1, sim_col2 = st.columns(2)

with sim_col1:
    traffic_input = st.select_slider(
        "Simulated Traffic Load",
        options=[
            "Low",
            "Medium",
            "High",
        ],
        value="Medium",
    )

with sim_col2:
    weather_input = st.radio(
        "Simulated Weather Severity",
        options=[
            "Normal",
            "Severe",
        ],
        value="Normal",
    )


# Calculate scenario risk
simulated_risk = get_scenario_risk(
    status_name,
    traffic_input,
    weather_input,
)

st.markdown(
    f"### 🚨 Simulated Risk of Failure: "
    f"**{simulated_risk}%**"
)

st.progress(simulated_risk / 100.0)