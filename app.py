import datetime, googlemaps, numpy as np, pandas as pd, os, streamlit as st
from dotenv import load_dotenv
from pprint import pprint

# environment variables
load_dotenv()
API_KEY = os.getenv(key='API_KEY')

# page configuration
st.set_page_config(
    page_title='Heal Map',
    page_icon='❤️‍🩹',
    layout='centered',
    initial_sidebar_state='expanded'
)

st.image(image='logo.gif')
st.title(body='Heal Map')

st.write('![language](https://img.shields.io/badge/language-python-yellow?style=plastic&logo=appveyor)' +
'![ML/AI](https://img.shields.io/badge/ML/AI-mlxtend-darkblue)' +
'![google](https://img.shields.io/badge/google-Geocoding-blue?style=flat-square&logo=appveyor)' +
'![google](https://img.shields.io/badge/google-Directions-crimson?style=flat-square&logo=appveyor)' +
'![google](https://img.shields.io/badge/google-Places-goldenrod?style=flat-square&logo=appveyor)' +
'[![Star](https://img.shields.io/github/stars/Fennec2000GH/Heal-Map.svg?logo=github&style=social)](https://gitHub.com/Fennec2000GH/IntelliVision)')

# geocoding
st.header(body='Find locations near me')

st.write(API_KEY)
gmaps = googlemaps.Client(key=API_KEY)
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# request directions via public transit
now = datetime.datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

st.write(directions_result)