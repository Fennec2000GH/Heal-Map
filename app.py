import os
# try:
#     import mordecai
# except:
#     os.system(command='python3.9 -m spacy download en_core_web_lg')

import googlemaps, folium, numpy as np, pandas as pd, spacy, spacy_streamlit, streamlit as st, streamlit_folium
import plotly.express as px, plotly.graph_objects as go

from dotenv import load_dotenv
from pprint import pprint

#region
# environment variables
try:
    global API_KEY
    load_dotenv()
    API_KEY = os.getenv(key='API_KEY')
except:
    pass

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
'![google](https://img.shields.io/badge/google-Places-crimson?style=flat-square&logo=appveyor)' +
'![google](https://img.shields.io/badge/google-Distance%20Matrix-goldenrod?style=flat-square&logo=appveyor)' +
'[![Star](https://img.shields.io/github/stars/Fennec2000GH/Heal-Map.svg?logo=github&style=social)](https://gitHub.com/Fennec2000GH/Heal-Map)')
#endregion

# geocoding
gmaps = googlemaps.Client(key=API_KEY)
def geocode_to_coordinates(text: str):
    geocode_result = gmaps.geocode(text)
    lat, lng = tuple(geocode_result[0]['geometry']['location'].values())
    return lat, lng

st.header(body='Find locations near me')

location = st.text_input(label='Location', help='Input your address or identifiable location.')
category = st.selectbox(
    label='Category', 
    options=np.asarray(a=list([
        'Hospital',
        'Clinic',
        'Pharmacy',
        'Fitness'
    ])),
    help='Select the type of location e.g. hospital.'
    )

#region
if st.button(label='🔍'):
    
    # geocode results for given location
    lat, lng = geocode_to_coordinates(text=location)
    st.write(lat, lng)

    # found destinations

    destinations = gmaps.places(
        query=category,
        location=(lat, lng)
    )

    search_results = destinations['results']
    formatted_addresses = np.asarray(a=list([result['formatted_address'] for result in search_results]))
    lat_lng_pairs = np.asarray(a=list([tuple(result['geometry']['location'].values()) for result in search_results]))

    st.subheader(body='Found Destinations')
    st.write(formatted_addresses)

    # map 
    st.subheader(body='Map')
    map_df = df = pd.DataFrame(
        data=lat_lng_pairs,
        columns=['lat', 'lon']
    )

    st.map(
        data=map_df, 
        zoom=10,
        use_container_width=True
    )

    # distance comparisons
    st.subheader(body='Distance Radar')
    dist_matrix = gmaps.distance_matrix(
        origins=(lat, lng),
        destinations=lat_lng_pairs[:5]
    )
    distances = np.asarray(a=list([element['distance']['value'] for element in dist_matrix['rows'][0]['elements']]))
    durations = np.asarray(a=list([element['duration']['value'] for element in dist_matrix['rows'][0]['elements']]))

    radar_df = pd.DataFrame(data=dict(distances=distances, durations=durations, theta=formatted_addresses[:5]))

    # radar_fig = px.line_polar(
    #     data_frame=radar_df,
    #     r='r',
    #     theta='theta',
    #     line_close=True,
    # )

    radar_fig = go.Figure()
    radar_fig.add_trace(trace=go.Scatterpolar(
        r=distances,
        theta=formatted_addresses[:5],
        fill='toself',
        name='Distance'
    ))
    radar_fig.add_trace(trace=go.Scatterpolar(
        r=durations,
        theta=formatted_addresses[:5],
        fill='toself',
        name='Duration'
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    st.plotly_chart(figure_or_data=radar_fig, use_container_width=True)
#endregion

#region
# geoparsing
st.header(body='Parse places from text')
# geo = mordecai.Geoparser()

geo_text = st.text_input(label='Text', help='Input text here.')
nlp = spacy.load(name='en_core_web_lg')
colors = dict({
    'ORG': 'linear-gradient(90deg, red, blue)',
    'LOC': 'linear-gradient(90deg, green, yellow)',
})
options = dict({'ents': list(['ORG', 'LOC']), 'colors': colors})

if st.button(label='🌎'):
    
# geoparse_df = pd.DataFrame(data=geo.geoparse(geo_text))
# st.dataframe(data=geoparse_df)
    doc = nlp(text=geo_text)
    spacy_streamlit.visualize_ner(doc=doc, labels=options['ents'])
    lat, lng = geocode_to_coordinates(text=doc.ents[0][0])
    m = folium.Map(location=np.asarray(a=list([lat, lng])), zoom_start=15, tiles='Stamen Terrain')

    for location in list(filter(lambda x: x in set(options['ents']), doc.ents)):
        st.write(location)
        folium.Marker(
            location=geocode_to_coordinates(text=location),
            popup=location,
            icon=folium.Icon(color='green', icon="info-sign"),
        ).add_to(m)

    streamlit_folium.folium_static(fig=m)

#endregion