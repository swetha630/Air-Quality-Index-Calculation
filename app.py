import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="AQI Estimator", page_icon="🌫️")

st.title(":foggy: Air Quality Index (AQI) Estimator")
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

if st.button("Calculate AQI"):
    # Dummy AQI logic – AQI based on highest pollutant value
    values = [pm25, pm10, no2, so2, co, o3, nh3, pb]
    aqi = max(values)

    # Classification
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
    st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; color:white;'>Status: {level}</div>", unsafe_allow_html=True)

    # Optional: Let user download results
    result_df = pd.DataFrame([{
        "Date": datetime.date.today(),
        "PM2.5": pm25,
        "PM10": pm10,
        "NO2": no2,
        "SO2": so2,
        "CO": co,
        "O3": o3,
        "NH3": nh3,
        "Pb": pb,
        "AQI": aqi,
        "Level": level
    }])

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download AQI Report", data=csv, file_name="aqi_result.csv", mime='text/csv')

