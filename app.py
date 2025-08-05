%%writefile app.py
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="AQI Estimator", page_icon="🌫️")

st.title("🌫️ Air Quality Index (AQI) Estimator")
st.markdown("Choose input method:")

input_mode = st.radio("Select mode", ["Manual Input", "CSV Upload"])

def classify_aqi(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Satisfactory", "lightgreen"
    elif aqi <= 200:
        return "Moderate", "orange"
    elif aqi <= 300:
        return "Poor", "red"
    elif aqi <= 400:
        return "Very Poor", "purple"
    else:
        return "Severe", "maroon"

# 1. Manual Input Mode
if input_mode == "Manual Input":
    st.subheader("🔧 Manual Pollutant Input")
    pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0)
    pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0)
    no2 = st.number_input("NO₂ (µg/m³)", min_value=0.0)
    so2 = st.number_input("SO₂ (µg/m³)", min_value=0.0)
    co = st.number_input("CO (mg/m³)", min_value=0.0)
    o3 = st.number_input("O₃ (µg/m³)", min_value=0.0)
    nh3 = st.number_input("NH₃ (µg/m³)", min_value=0.0)
    pb = st.number_input("Pb (µg/m³)", min_value=0.0)

    if st.button("Calculate AQI"):
        values = [pm25, pm10, no2, so2, co, o3, nh3, pb]
        aqi = max(values)
        level, color = classify_aqi(aqi)

        st.markdown(f"### 🧪 Estimated AQI: `{aqi:.2f}`")
        st.markdown(f"### 🔍 Air Quality Level: `{level}`")
        st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; color:white;'>Status: {level}</div>", unsafe_allow_html=True)

# 2. CSV Upload Mode
else:
    st.subheader("📄 Upload CSV File")
    uploaded_file = st.file_uploader("Upload a CSV with pollutant columns", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        required_columns = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3", "Pb"]
        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"Missing required columns: {', '.join(missing)}")
        else:
            df["AQI"] = df[required_columns].max(axis=1)
            df["Level"], df["Color"] = zip(*df["AQI"].apply(classify_aqi))

            st.success("✅ AQI calculated for uploaded data.")
            st.dataframe(df[required_columns + ["AQI", "Level"]])

            # Download button
            output = BytesIO()
            df.to_csv(output, index=False)
            st.download_button("📥 Download AQI Results", data=output.getvalue(),
                               file_name="AQI_results.csv", mime="text/csv")
