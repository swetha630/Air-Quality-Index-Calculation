import streamlit as st
import pandas as pd

st.set_page_config(page_title="AQI Estimator", page_icon="🌫️")

st.title("🌫️ Air Quality Index (AQI) Estimator")
st.markdown("Enter the concentrations of pollutants (in µg/m³ or ppm as applicable):")

# User inputs for pollutant concentrations
pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0)
pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0)
no2 = st.number_input("NO₂ (µg/m³)", min_value=0.0)
so2 = st.number_input("SO₂ (µg/m³)", min_value=0.0)
co = st.number_input("CO (mg/m³)", min_value=0.0)
o3 = st.number_input("O₃ (µg/m³)", min_value=0.0)
nh3 = st.number_input("NH₃ (µg/m³)", min_value=0.0)
pb = st.number_input("Pb (µg/m³)", min_value=0.0)

# AQI Calculation
if st.button("Calculate AQI"):
    values = [pm25, pm10, no2, so2, co, o3, nh3, pb]
    aqi = max(values)  # Simplified AQI logic

    # AQI Levels
    if aqi <= 50:
        level = "Good"
        color = "green"
    elif aqi <= 100:
        level = "Satisfactory"
        color = "lightgreen"
    elif aqi <= 200:
        level = "Moderate"
        color = "orange"
    elif aqi <= 300:
        level = "Poor"
        color = "red"
    elif aqi <= 400:
        level = "Very Poor"
        color = "purple"
    else:
        level = "Severe"
        color = "maroon"

    st.markdown(f"### 🧪 Estimated AQI: `{aqi:.2f}`")
    st.markdown(f"### 🔍 Air Quality Level: `{level}`")
    st.markdown(
        f"<div style='background-color:{color}; padding:10px; border-radius:5px; color:white;'>Status: {level}</div>",
        unsafe_allow_html=True
    )

# CSV Upload
st.markdown("---")
st.markdown("## 📁 Upload CSV for Bulk AQI Estimation")

uploaded_file = st.file_uploader("Upload CSV file with pollutant values", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3", "Pb"]

    if not all(p in df.columns for p in pollutants):
        st.error("CSV must contain these columns: " + ", ".join(pollutants))
    else:
        df["Estimated_AQI"] = df[pollutants].max(axis=1)

        # AQI Level based on estimated AQI
        def classify_aqi(aqi):
            if aqi <= 50:
                return "Good"
            elif aqi <= 100:
                return "Satisfactory"
            elif aqi <= 200:
                return "Moderate"
            elif aqi <= 300:
                return "Poor"
            elif aqi <= 400:
                return "Very Poor"
            else:
                return "Severe"

        df["AQI_Level"] = df["Estimated_AQI"].apply(classify_aqi)
        st.success("✅ AQI estimated for uploaded data:")
        st.dataframe(df)

        # Download result
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Result CSV",
            data=csv,
            file_name="aqi_results.csv",
            mime="text/csv"
        )
