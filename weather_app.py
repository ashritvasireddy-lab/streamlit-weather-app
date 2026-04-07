import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.title("🌍 Worldwide Weather App")

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"

# --- Sidebar city input
city_input = st.sidebar.text_input("Enter city (e.g., Dallas, US)")

lat = lon = city_name = None

# --- Get coordinates from city or map click
if city_input:
    resp = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_input}&limit=1&appid={API_KEY}").json()
    if resp:
        lat, lon = resp[0]['lat'], resp[0]['lon']
        city_name = f"{resp[0]['name']}, {resp[0]['country']}"
    else:
        st.warning("City not found. Use 'City, CountryCode'.")

# --- Map click fallback
m = folium.Map(location=[20, 0], zoom_start=2)
clicked = st_folium(m, width=700, height=500).get('last_clicked')
if lat is None and clicked:
    lat, lon = clicked['lat'], clicked['lng']
    rev = requests.get(f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}").json()
    city_name = f"{rev[0]['name']}, {rev[0]['country']}" if rev else f"Lat {lat:.2f}, Lon {lon:.2f}"

# --- Fetch and display weather
if lat and lon:
    w = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}").json()
    if w.get('main'):
        st.subheader(f"Weather in {city_name}")
        st.write(f"🌡 {w['main']['temp']}°C | 💨 {w['wind']['speed']} m/s | ☁ {w['weather'][0]['description'].title()} | 💧 {w['main']['humidity']}%")
        st.image(f"http://openweathermap.org/img/wn/{w['weather'][0]['icon']}@2x.png")
    else:
        st.error("Weather data not available.")
else:
    st.info("Type a city or click on the map to see weather.")
