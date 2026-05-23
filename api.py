# app.py

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background-color: #0E1117;
}

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #00BFFF;
    margin-top: -40px;
}

.subtitle {
    text-align: center;
    color: white;
    font-size: 20px;
    margin-bottom: 30px;
}

.metric-box {
    background: linear-gradient(135deg, #1f1f1f, #2b2b2b);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    color: white;
}

.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    '<div class="title">🌍 Weather Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Real Time Weather Data Using OpenWeather API</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.header("📍 Location Settings")

lat = st.sidebar.number_input(
    "Enter Latitude",
    value=25.276987,
    format="%.6f"
)

lon = st.sidebar.number_input(
    "Enter Longitude",
    value=55.296249,
    format="%.6f"
)

# ---------------- API KEY ----------------
api_key = "e70a7528249e1c3633e76ba75a6897bd"

# ---------------- BUTTON ----------------
search = st.sidebar.button("🔍 Get Weather")

# ---------------- API REQUEST ----------------
if search:

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

    response = requests.get(url)

    # ---------------- SUCCESS ----------------
    if response.status_code == 200:

        final = response.json()

        # ---------------- DATA ----------------
        city = final["name"]

        temp = round(final["main"]["temp"] - 273.15, 2)

        max_temp = round(final["main"]["temp_max"] - 273.15, 2)

        min_temp = round(final["main"]["temp_min"] - 273.15, 2)

        humidity = final["main"]["humidity"]

        pressure = final["main"]["pressure"]

        wind_speed = final["wind"]["speed"]

        description = final["weather"][0]["description"].title()

        # ---------------- METRICS ----------------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🌡 Temperature", f"{temp} °C")

        with col2:
            st.metric("💨 Wind Speed", f"{wind_speed} m/s")

        with col3:
            st.metric("💧 Humidity", f"{humidity}%")

        with col4:
            st.metric("☁ Condition", description)

        st.write("")

        # ---------------- DATAFRAME ----------------
        data = {
            "City": [city],
            "Latitude": [lat],
            "Longitude": [lon],
            "Temperature": [temp],
            "Max Temp": [max_temp],
            "Min Temp": [min_temp],
            "Humidity": [humidity],
            "Pressure": [pressure],
            "Wind Speed": [wind_speed],
            "Description": [description]
        }

        df = pd.DataFrame(data)

        # ---------------- SHOW DATAFRAME ----------------
        st.subheader("📊 Weather Data Table")

        st.dataframe(df, width="stretch")

        # ---------------- BAR GRAPH ----------------
        st.subheader("📈 Temperature Analysis")

        graph_df = pd.DataFrame({
            "Type": ["Current Temp", "Max Temp", "Min Temp"],
            "Temperature": [temp, max_temp, min_temp]
        })

        fig = px.bar(
            graph_df,
            x="Type",
            y="Temperature",
            text="Temperature",
            title="Temperature Comparison"
        )

        fig.update_traces(textposition='outside')

        st.plotly_chart(fig, width="stretch")

        # ---------------- LINE CHART ----------------
        st.subheader("📉 Weather Parameters")

        line_df = pd.DataFrame({
            "Parameter": ["Humidity", "Pressure", "Wind Speed"],
            "Value": [humidity, pressure, wind_speed]
        })

        line_fig = px.line(
            line_df,
            x="Parameter",
            y="Value",
            markers=True,
            title="Weather Parameter Analysis"
        )

        st.plotly_chart(line_fig, width="stretch")

        # ---------------- PIE CHART ----------------
        st.subheader("🥧 Distribution Chart")

        pie_fig = px.pie(
            line_df,
            names="Parameter",
            values="Value",
            hole=0.5,
            title="Weather Distribution"
        )

        st.plotly_chart(pie_fig, width="stretch")

        # ---------------- RAW JSON ----------------
        with st.expander("🔍 View Raw JSON Data"):
            st.json(final)

        # ---------------- FOOTER ----------------
        st.write("---")

        st.caption(
            f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

    # ---------------- ERROR ----------------
    else:

        st.error("❌ Failed to Fetch Weather Data")

        st.write("Status Code:", response.status_code)

        try:
            st.json(response.json())
        except:
            st.write(response.text)