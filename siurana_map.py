import folium
import pandas as pd
from folium.features import GeoJsonTooltip

#create the map object without background
map = folium.Map(location=[41.263, 0.945], zoom_start=15.5, tiles=None)

#add a satellite tile layer to the map object
folium.TileLayer(tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
attr= 'Esri', name='Satellite').add_to(map)

#add a street map tile layer to the map object
folium.TileLayer(tiles = "OpenStreetMap", name='Street Map').add_to(map)

#create a feature group for parking location layer
fg_parking = folium.FeatureGroup(name="Parking Locations")

#read the data for the parking locations from a csv file using the pandas library
locations = pd.read_csv("Siurana_parking_locations.csv")

#create lists with data on the specific locations
lat = list(locations["Lat"])
lon = list(locations["Lon"])
no = list(locations["no"])
url = list(locations["url"])

#create html text string with link to google maps for the pop ups
html_link_text = """<a href=%s>Directions to parking no %s</a>
"""

#loop on elements in the lists with data on parking locations and add children (popup, tooltips, styled with links) to the parking locations feature group
for lt, ln, n, u in zip(lat, lon, no, url): 
    fg_parking.add_child(folium.CircleMarker(location=[lt, ln], radius=7, popup=folium.Popup(html=html_link_text % (u, str(n))), tooltip="Panking no " + str(n), color="darkgreen", fill_color="green", fill_opacity=0.7))

#create a feature group for the crags polygons
fg_crags = folium.FeatureGroup(name="Easy Crags")

#add polygons as childred to crags feature group from the geo json file, style them with style_funtion (lambda funtion as parameter), tooltip
fg_crags.add_child(folium.GeoJson(data=open("siurana_crags.geojson").read(), 
style_function=lambda x: {"color": "#E5460A", "fillColor": "#E5460A", "opacity": 1}, 
tooltip= GeoJsonTooltip(fields=["no", "name"], 
aliases=["Sector number: ", "Name: "]
)
))

#add the parking/crags feature groups as well as layer control panel as children to map object
map.add_child(fg_crags) 
map.add_child(fg_parking)
map.add_child(folium.LayerControl())

#save map object as html file
map.save("Siurana_climbing_31012022.html") 