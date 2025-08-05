import streamlit as st
import pandas as pd

st.set_page_config(page_title="AQI Estimator", page_icon="🌫️")
st.title("🌫️ Air Quality Index (AQI) Estimator")

st.markdown("### 📌 Enter pollutant values manually:")
pm25 = st.number_input("PM2.5 (µg/m³)", min_value=0.0)
pm10 = st.number_input("PM10 (µg/m³)", min_value=0.0)
no2 = st.number_input("NO₂ (µg/m³)", min_value=0.0)
so2 = st.number_input("SO₂ (µg/m³)", min_value=0.0)
co = st.number_input("CO (mg/m³)", min_value=0.0)
o3 = st.number_input("O₃ (µg/m³)", min_value=0.0)
nh3 = st.number_input("NH₃ (µg/m³)", min_value=0.0)
pb = st.number_input("Pb (µg/m³)", min_value=0.0)

# Function to calculate AQI based on simplified logic
def calculate_aqi(row):
    pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'NH3', 'Pb']
    values = [row.get(p, 0) for p in pollutants]
    return max(values)

# AQI Category
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

if st.button("Calculate AQI"):
    input_data = {
        'PM2.5': pm25, 'PM10': pm10, 'NO2': no2,
        'SO2': so2, 'CO': co, 'O3': o3, 'NH3': nh3, 'Pb': pb
    }
    aqi = calculate_aqi(input_data)
    level, color = classify_aqi(aqi)
    st.markdown(f"### 🧪 Estimated AQI: `{aqi:.2f}`")
    st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px; color:white;'>Status: {level}</div>", unsafe_allow_html=True)

# ---------------------- CSV Upload Section --------------------
st.markdown("### 📁 Or Upload a CSV file:")
file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    try:
        df = pd.read_csv(file)

        # Normalize column names for flexibility
        col_map = {
            'pm2.5': 'PM2.5', 'pm25': 'PM2.5',
            'pm10': 'PM10',
            'no2': 'NO2',
            'so2': 'SO2',
            'co': 'CO',
            'o3': 'O3',
            'nh3': 'NH3',
            'pb': 'Pb'
        }

        # Standardize column names
        new_cols = {}
        for col in df.columns:
            key = col.strip().lower().replace("_", "").replace(".", "")
            if key in col_map:
                new_cols[col] = col_map[key]

        df = df.rename(columns=new_cols)

        # Fill missing pollutants with 0
        for p in ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'NH3', 'Pb']:
            if p not in df.columns:
                df[p] = 0

        # Calculate AQI for each row
        df['AQI'] = df.apply(calculate_aqi, axis=1)
        df['Category'], df['Color'] = zip(*df['AQI'].map(classify_aqi))

        st.success("✅ AQI calculated for uploaded file.")
        st.dataframe(df[['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'NH3', 'Pb', 'AQI', 'Category']])

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download AQI Results CSV", csv, "aqi_results.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing CSV: {e}")
