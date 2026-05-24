import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

/* AQI colored badge styling */
.aqi-good       { color: #00e400; font-weight: bold; font-size: 22px; }
.aqi-fair       { color: #ffff00; font-weight: bold; font-size: 22px; }
.aqi-moderate   { color: #ff7e00; font-weight: bold; font-size: 22px; }
.aqi-poor       { color: #ff0000; font-weight: bold; font-size: 22px; }
.aqi-very-poor  { color: #8f3f97; font-weight: bold; font-size: 22px; }

.section-header {
    color: #00BFFF;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
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
api_key = st.secrets["OPENWEATHER_API_KEY"]

# ---------------- BUTTON ----------------
search = st.sidebar.button("🔍 Get Weather")

# ============================================================
# HELPER: AQI Label
# ============================================================
def aqi_label(aqi_index: int) -> tuple[str, str]:
    """Return (label, css_class) for an AQI index 1-5."""
    mapping = {
        1: ("Good", "aqi-good"),
        2: ("Fair", "aqi-fair"),
        3: ("Moderate", "aqi-moderate"),
        4: ("Poor", "aqi-poor"),
        5: ("Very Poor", "aqi-very-poor"),
    }
    return mapping.get(aqi_index, ("Unknown", "aqi-good"))


# ============================================================
# MAIN LOGIC
# ============================================================
if search:

    # ---------- Fetch all three APIs in parallel (sequential for simplicity) ----------
    weather_url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )
    air_url = (
        f"http://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )
    forecast_url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&appid={api_key}"
    )

    weather_resp  = requests.get(weather_url)
    air_resp      = requests.get(air_url)
    forecast_resp = requests.get(forecast_url)

    all_ok = (
        weather_resp.status_code == 200
        and air_resp.status_code == 200
        and forecast_resp.status_code == 200
    )

    if all_ok:

        weather_data  = weather_resp.json()
        air_data      = air_resp.json()
        forecast_data = forecast_resp.json()

        # ============================================================
        # THREE TABS
        # ============================================================
        tab1, tab2, tab3 = st.tabs([
            "🌤️ Current Weather",
            "🌫️ Air Quality",
            "📅 5-Day Forecast"
        ])

        # ============================================================
        # TAB 1 — CURRENT WEATHER
        # ============================================================
        with tab1:

            city        = weather_data["name"]
            temp        = round(weather_data["main"]["temp"] - 273.15, 2)
            max_temp    = round(weather_data["main"]["temp_max"] - 273.15, 2)
            min_temp    = round(weather_data["main"]["temp_min"] - 273.15, 2)
            humidity    = weather_data["main"]["humidity"]
            pressure    = weather_data["main"]["pressure"]
            wind_speed  = weather_data["wind"]["speed"]
            description = weather_data["weather"][0]["description"].title()

            st.markdown(f"### 📍 {city}")

            # Metric row
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

            # Data table
            st.subheader("📊 Weather Data Table")
            data = {
                "City": [city],
                "Latitude": [lat],
                "Longitude": [lon],
                "Temperature (°C)": [temp],
                "Max Temp (°C)": [max_temp],
                "Min Temp (°C)": [min_temp],
                "Humidity (%)": [humidity],
                "Pressure (hPa)": [pressure],
                "Wind Speed (m/s)": [wind_speed],
                "Condition": [description]
            }
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

            # Bar chart — temperature
            st.subheader("📈 Temperature Analysis")
            graph_df = pd.DataFrame({
                "Type": ["Current Temp", "Max Temp", "Min Temp"],
                "Temperature (°C)": [temp, max_temp, min_temp]
            })
            fig = px.bar(
                graph_df,
                x="Type",
                y="Temperature (°C)",
                text="Temperature (°C)",
                color="Type",
                title="Temperature Comparison (°C)",
                color_discrete_sequence=["#00BFFF", "#FF6347", "#32CD32"]
            )
            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Line chart — other params
            st.subheader("📉 Weather Parameters")
            line_df = pd.DataFrame({
                "Parameter": ["Humidity (%)", "Pressure (hPa)", "Wind Speed (m/s)"],
                "Value": [humidity, pressure, wind_speed]
            })
            line_fig = px.line(
                line_df,
                x="Parameter",
                y="Value",
                markers=True,
                title="Weather Parameter Overview"
            )
            st.plotly_chart(line_fig, use_container_width=True)

            # Pie chart
            st.subheader("🥧 Distribution Chart")
            pie_fig = px.pie(
                line_df,
                names="Parameter",
                values="Value",
                hole=0.5,
                title="Weather Distribution"
            )
            st.plotly_chart(pie_fig, use_container_width=True)

            # Raw JSON
            with st.expander("🔍 View Raw JSON"):
                st.json(weather_data)

        # ============================================================
        # TAB 2 — AIR QUALITY
        # ============================================================
        with tab2:

            components = air_data["list"][0]["components"]
            aqi_index  = air_data["list"][0]["main"]["aqi"]
            label, css = aqi_label(aqi_index)

            st.markdown(f"### 🌫️ Air Quality Index (AQI)")
            st.markdown(
                f'<p>Overall AQI: <span class="{css}">{label} (Level {aqi_index}/5)</span></p>',
                unsafe_allow_html=True
            )

            st.write("")

            # Pollutant metric cards
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("CO (μg/m³)",   f"{components.get('co', 0):.2f}")
            c2.metric("NO (μg/m³)",   f"{components.get('no', 0):.2f}")
            c3.metric("NO₂ (μg/m³)",  f"{components.get('no2', 0):.2f}")
            c4.metric("O₃ (μg/m³)",   f"{components.get('o3', 0):.2f}")

            c5, c6, c7, c8 = st.columns(4)
            c5.metric("SO₂ (μg/m³)",  f"{components.get('so2', 0):.2f}")
            c6.metric("PM2.5 (μg/m³)",f"{components.get('pm2_5', 0):.2f}")
            c7.metric("PM10 (μg/m³)", f"{components.get('pm10', 0):.2f}")
            c8.metric("NH₃ (μg/m³)",  f"{components.get('nh3', 0):.2f}")

            st.write("")

            # Data table
            st.subheader("📊 Pollutant Data Table")
            poll_df = pd.DataFrame([{
                "Pollutant": k.upper().replace("_", "."),
                "Concentration (μg/m³)": round(v, 4)
            } for k, v in components.items()])
            st.dataframe(poll_df, use_container_width=True)

            # Bar chart — all pollutants
            st.subheader("📈 Pollutant Concentration Comparison")
            bar_fig = px.bar(
                poll_df,
                x="Pollutant",
                y="Concentration (μg/m³)",
                text="Concentration (μg/m³)",
                color="Pollutant",
                title="Air Pollutant Levels (μg/m³)"
            )
            bar_fig.update_traces(textposition="outside")
            bar_fig.update_layout(showlegend=False)
            st.plotly_chart(bar_fig, use_container_width=True)

            # Focus: PM2.5 and PM10 gauge charts
            st.subheader("🎯 PM2.5 & PM10 Health Gauges")
            g1, g2 = st.columns(2)

            pm25_val = components.get("pm2_5", 0)
            pm10_val = components.get("pm10", 0)

            with g1:
                gauge_25 = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=pm25_val,
                    title={"text": "PM2.5 (μg/m³)"},
                    gauge={
                        "axis": {"range": [0, 250]},
                        "bar": {"color": "#00BFFF"},
                        "steps": [
                            {"range": [0, 12],    "color": "#00e400"},
                            {"range": [12, 35.4], "color": "#ffff00"},
                            {"range": [35.4, 55], "color": "#ff7e00"},
                            {"range": [55, 150],  "color": "#ff0000"},
                            {"range": [150, 250], "color": "#8f3f97"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": pm25_val
                        }
                    },
                    delta={"reference": 12, "increasing": {"color": "red"}}
                ))
                st.plotly_chart(gauge_25, use_container_width=True)

            with g2:
                gauge_10 = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=pm10_val,
                    title={"text": "PM10 (μg/m³)"},
                    gauge={
                        "axis": {"range": [0, 430]},
                        "bar": {"color": "#FF6347"},
                        "steps": [
                            {"range": [0, 54],    "color": "#00e400"},
                            {"range": [54, 154],  "color": "#ffff00"},
                            {"range": [154, 254], "color": "#ff7e00"},
                            {"range": [254, 354], "color": "#ff0000"},
                            {"range": [354, 430], "color": "#8f3f97"},
                        ],
                        "threshold": {
                            "line": {"color": "red", "width": 4},
                            "thickness": 0.75,
                            "value": pm10_val
                        }
                    },
                    delta={"reference": 54, "increasing": {"color": "red"}}
                ))
                st.plotly_chart(gauge_10, use_container_width=True)

            # AQI info legend
            with st.expander("ℹ️ AQI Level Guide"):
                st.markdown("""
| Level | Label      | What it means |
|-------|------------|----------------|
| 1     | 🟢 Good       | Air quality is satisfactory, little or no risk |
| 2     | 🟡 Fair       | Acceptable quality; some pollutants may affect very sensitive people |
| 3     | 🟠 Moderate   | Sensitive groups may experience health effects |
| 4     | 🔴 Poor       | Everyone may begin to experience health effects |
| 5     | 🟣 Very Poor  | Health alert: serious health effects for everyone |
""")

            with st.expander("🔍 View Raw Air Quality JSON"):
                st.json(air_data)

        # ============================================================
        # TAB 3 — 5-DAY FORECAST
        # ============================================================
        with tab3:

            city_name = forecast_data["city"]["name"]
            st.markdown(f"### 📅 5-Day / 3-Hour Forecast — {city_name}")

            # Parse forecast list
            rows = []
            for entry in forecast_data["list"]:
                dt     = datetime.fromtimestamp(entry["dt"])
                t      = round(entry["main"]["temp"] - 273.15, 2)
                t_max  = round(entry["main"]["temp_max"] - 273.15, 2)
                t_min  = round(entry["main"]["temp_min"] - 273.15, 2)
                hum    = entry["main"]["humidity"]
                pres   = entry["main"]["pressure"]
                wind   = entry["wind"]["speed"]
                desc   = entry["weather"][0]["description"].title()
                pop    = round(entry.get("pop", 0) * 100, 1)   # Probability of precipitation %
                rows.append({
                    "DateTime": dt,
                    "Date": dt.strftime("%d %b"),
                    "Time": dt.strftime("%H:%M"),
                    "Temp (°C)": t,
                    "Max Temp (°C)": t_max,
                    "Min Temp (°C)": t_min,
                    "Humidity (%)": hum,
                    "Pressure (hPa)": pres,
                    "Wind Speed (m/s)": wind,
                    "Condition": desc,
                    "Rain Prob (%)": pop
                })

            fc_df = pd.DataFrame(rows)

            # Summary metric cards — averages
            st.subheader("📊 5-Day Averages")
            a1, a2, a3, a4 = st.columns(4)
            a1.metric("🌡 Avg Temp",       f"{fc_df['Temp (°C)'].mean():.1f} °C")
            a2.metric("💧 Avg Humidity",   f"{fc_df['Humidity (%)'].mean():.1f} %")
            a3.metric("💨 Avg Wind Speed", f"{fc_df['Wind Speed (m/s)'].mean():.2f} m/s")
            a4.metric("🌧 Max Rain Prob",  f"{fc_df['Rain Prob (%)'].max()} %")

            st.write("")

            # Full data table (scrollable)
            st.subheader("🗓️ Full Forecast Table")
            display_cols = [
                "Date", "Time", "Temp (°C)", "Max Temp (°C)",
                "Min Temp (°C)", "Humidity (%)", "Wind Speed (m/s)",
                "Rain Prob (%)", "Condition"
            ]
            st.dataframe(fc_df[display_cols], use_container_width=True, height=300)

            # Temperature over time
            st.subheader("🌡️ Temperature Trend (5 Days)")
            temp_fig = px.line(
                fc_df,
                x="DateTime",
                y=["Temp (°C)", "Max Temp (°C)", "Min Temp (°C)"],
                markers=True,
                title="Temperature Over Next 5 Days",
                labels={"value": "Temperature (°C)", "variable": "Series", "DateTime": "Date & Time"},
                color_discrete_map={
                    "Temp (°C)":     "#00BFFF",
                    "Max Temp (°C)": "#FF6347",
                    "Min Temp (°C)": "#32CD32"
                }
            )
            temp_fig.update_xaxes(tickformat="%d %b\n%H:%M")
            st.plotly_chart(temp_fig, use_container_width=True)

            # Humidity over time
            st.subheader("💧 Humidity Trend (5 Days)")
            hum_fig = px.area(
                fc_df,
                x="DateTime",
                y="Humidity (%)",
                title="Humidity Over Next 5 Days",
                labels={"DateTime": "Date & Time"},
                color_discrete_sequence=["#1E90FF"]
            )
            hum_fig.update_xaxes(tickformat="%d %b\n%H:%M")
            st.plotly_chart(hum_fig, use_container_width=True)

            # Rain probability bar chart
            st.subheader("🌧️ Precipitation Probability (5 Days)")
            rain_fig = px.bar(
                fc_df,
                x="DateTime",
                y="Rain Prob (%)",
                title="Chance of Rain Over Next 5 Days",
                labels={"DateTime": "Date & Time"},
                color="Rain Prob (%)",
                color_continuous_scale="Blues"
            )
            rain_fig.update_xaxes(tickformat="%d %b\n%H:%M")
            st.plotly_chart(rain_fig, use_container_width=True)

            # Wind speed over time
            st.subheader("💨 Wind Speed Trend (5 Days)")
            wind_fig = px.line(
                fc_df,
                x="DateTime",
                y="Wind Speed (m/s)",
                markers=True,
                title="Wind Speed Over Next 5 Days",
                labels={"DateTime": "Date & Time"},
                color_discrete_sequence=["#FFD700"]
            )
            wind_fig.update_xaxes(tickformat="%d %b\n%H:%M")
            st.plotly_chart(wind_fig, use_container_width=True)

            # Daily summary (group by day, pick max/min)
            st.subheader("📆 Daily Summary")
            fc_df["Day"] = fc_df["DateTime"].dt.strftime("%A, %d %b")
            daily = (
                fc_df.groupby("Day")
                .agg(
                    Max_Temp=("Max Temp (°C)", "max"),
                    Min_Temp=("Min Temp (°C)", "min"),
                    Avg_Humidity=("Humidity (%)", "mean"),
                    Max_Wind=("Wind Speed (m/s)", "max"),
                    Max_Rain_Prob=("Rain Prob (%)", "max"),
                )
                .reset_index()
            )
            daily.columns = [
                "Day", "Max Temp (°C)", "Min Temp (°C)",
                "Avg Humidity (%)", "Max Wind (m/s)", "Max Rain Prob (%)"
            ]
            daily["Avg Humidity (%)"] = daily["Avg Humidity (%)"].round(1)
            st.dataframe(daily, use_container_width=True)

            with st.expander("🔍 View Raw Forecast JSON"):
                st.json(forecast_data)

        # ============================================================
        # FOOTER
        # ============================================================
        st.write("---")
        st.caption(
            f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )

    # -------- API ERROR HANDLING --------
    else:
        for label, resp in [
            ("Weather", weather_resp),
            ("Air Quality", air_resp),
            ("Forecast", forecast_resp)
        ]:
            if resp.status_code != 200:
                st.error(f"❌ Failed to fetch {label} data (Status {resp.status_code})")
                try:
                    st.json(resp.json())
                except Exception:
                    st.write(resp.text)
