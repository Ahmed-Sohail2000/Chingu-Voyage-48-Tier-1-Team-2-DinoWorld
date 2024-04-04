
# lets plot the dinosaurs found in different countries on a map using choropleth - https://www.datacamp.com/tutorial/making-map-in-python-using-plotly-library-guide
!pip install geopy
from geopy.geocoders import Nominatim
import plotly.io as pio
import json, requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import plotly.express as px
import geopandas as gpd

# Load the GeoJSON file containing country boundaries
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# setup the json url
dino_url = 'https://raw.githubusercontent.com/chingu-voyages/voyage-project-tier1-dinosaurs/main/assets/dinosaurs.json'
response = requests.get(dino_url)

# open the file
dino_data = json.loads(response.text)

# create a dataframe
dino_data = pd.DataFrame(dino_data)

# create a function to get the latitude and longitude of the country
def get_lat_lon(country):
  geolocator = Nominatim(user_agent='dino_map')
  location = geolocator.geocode(country)

  if location:
    return location.latitude, location.longitude
  else:
    return None, None

# get latitude and longitude for each country and add it into the dino data
dino_data['Latitude'], dino_data['Longitude'] = zip(*dino_data['foundIn'].apply(get_lat_lon))

# Merge dino_data with the world GeoDataFrame on the country names
world_dino = world.merge(dino_data, left_on='name', right_on='foundIn')

# Plot the choropleth map
fig = px.choropleth(world_dino,
                    locations='iso_a3',
                    color='foundIn',
                    hover_name='foundIn',
                    title='Dinosaurs found around the world',
                    color_continuous_scale=[(0, 'yellow'), (0.5, 'orange'), (1, 'red')],
                    projection = 'natural earth')

# Change the background color and make the title bold
fig.update_layout(plot_bgcolor='lightgray', paper_bgcolor='lightgray')
fig.update_layout(title={'text': 'Dinosaurs found around the world', 'font': {'size': 20, 'family': 'Arial', 'color': 'black'}, 'x': 0.5, 'y': 0.95, 'xanchor': 'center', 'yanchor': 'top'})

# Show the plot
fig.show()

# export it as a html file
pio.write_html(fig, file = 'dinosaurs around the world.html', auto_open = True)
