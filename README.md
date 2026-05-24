# 🌍 Weather Analytics Dashboard

A real-time weather analytics web application built with **Streamlit** and the **OpenWeatherMap API**. Enter any location's coordinates to instantly view current weather conditions, air quality data, and a 5-day forecast — all with interactive charts and visualizations.
link : https://api-miniproject-5cy7ews3hcyqtst9djekqs.streamlit.app/

---

## 📸 Features

### 🌤️ Current Weather
- Live temperature, wind speed, humidity, and condition metrics
- Temperature comparison bar chart (current / max / min)
- Weather parameters line chart
- Distribution pie chart
- Raw JSON data viewer

### 🌫️ Air Quality Index (AQI)
- AQI level badge with color-coded health rating (Good → Very Poor)
- 8 pollutant metric cards: CO, NO, NO₂, O₃, SO₂, PM2.5, PM10, NH₃
- Pollutant concentration bar chart
- PM2.5 & PM10 health gauges with WHO threshold zones
- AQI level legend guide

### 📅 5-Day / 3-Hour Forecast
- 5-day summary cards (avg temp, humidity, wind, max rain chance)
- Full 40-slot forecast table (scrollable)
- Temperature trend line chart (current / max / min)
- Humidity area chart
- Precipitation probability bar chart
- Wind speed trend chart
- Daily summary table (grouped by day)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web application framework |
| [OpenWeatherMap API](https://openweathermap.org/api) | Weather, air quality & forecast data |
| [Plotly Express](https://plotly.com/python/plotly-express/) | Interactive charts and graphs |
| [Pandas](https://pandas.pydata.org/) | Data manipulation |
| [Requests](https://requests.readthedocs.io/) | HTTP API calls |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/weather-dashboard.git
cd weather-dashboard
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get an OpenWeatherMap API Key

1. Sign up at [openweathermap.org](https://openweathermap.org/api)
2. Navigate to **API Keys** in your account dashboard
3. Copy your API key

### 4. Configure the API Key

Create a `.streamlit/secrets.toml` file in the project root:

```toml
OPENWEATHER_API_KEY = "your_api_key_here"
```

> ⚠️ Never commit your API key to version control. The `.streamlit/` folder is included in `.gitignore` by default.

### 5. Run the App

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📁 Project Structure

```
weather-dashboard/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API key (not committed to git)
├── .gitignore
└── README.md
```

---

## 📦 Requirements

Create a `requirements.txt` file with the following:

```
streamlit
requests
pandas
plotly
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 🌐 APIs Used

| API | Endpoint | Description |
|---|---|---|
| Current Weather | `/data/2.5/weather` | Live weather for a location |
| Air Pollution | `/data/2.5/air_pollution` | AQI and pollutant concentrations |
| 5-Day Forecast | `/data/2.5/forecast` | 3-hour interval forecast for 5 days |

All three APIs are called simultaneously when the user clicks **Get Weather**.

---

## 🗺️ How to Use

1. Open the app in your browser
2. In the **sidebar**, enter the **Latitude** and **Longitude** of your desired location
3. Click **🔍 Get Weather**
4. Browse the three tabs:
   - **🌤️ Current Weather** — live conditions and charts
   - **🌫️ Air Quality** — AQI level, pollutants, and health gauges
   - **📅 5-Day Forecast** — temperature trends, rain probability, wind, and daily summary

### Finding Coordinates

You can find lat/lon coordinates easily from:
- [Google Maps](https://maps.google.com) — right-click any location → "What's here?"
- [latlong.net](https://www.latlong.net/)

**Example coordinates:**

| City | Latitude | Longitude |
|---|---|---|
| Dubai, UAE | 25.276987 | 55.296249 |
| Mumbai, India | 19.076090 | 72.877426 |
| London, UK | 51.507351 | -0.127758 |
| New York, USA | 40.712776 | -74.005974 |
| Tokyo, Japan | 35.689487 | 139.691711 |

---

## 🎨 AQI Level Guide

| Level | Label | Health Impact |
|---|---|---|
| 1 | 🟢 Good | Satisfactory air quality, little or no risk |
| 2 | 🟡 Fair | Acceptable; some pollutants may affect sensitive people |
| 3 | 🟠 Moderate | Sensitive groups may experience health effects |
| 4 | 🔴 Poor | Everyone may begin to experience health effects |
| 5 | 🟣 Very Poor | Health alert — serious effects for everyone |

---

## 🔒 Security Notes

- API keys are stored in `secrets.toml` and accessed via `st.secrets` — they are never exposed in the frontend
- Do not hardcode your API key directly into `app.py`
- Add `.streamlit/secrets.toml` to your `.gitignore`

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to a GitHub repository (without the secrets file)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Under **Advanced Settings → Secrets**, add:
   ```toml
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```
5. Click **Deploy**

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for providing free-tier weather APIs
- [Streamlit](https://streamlit.io/) for making data apps incredibly easy to build
- [Plotly](https://plotly.com/) for beautiful interactive visualizations
