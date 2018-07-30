import folium
import os
from folium import plugins
from folium import features
mapa = folium.Map(
    location=[-34.9926116,-71.2527959],
    zoom_start=13,
    tiles='Stamen Terrain'
    )
boldo = folium.Circle(
    location = [ -34.969672, -71.230373 ],
    radius=1000,
    color='black',
    fill=True,
    popup = '<h2>Mapa Clasico</h2>',
    fill_color='#07131d'
).add_to(mapa)


marker = folium.Marker(
    location=[-34.969672, -71.230373],
    icon=folium.Icon(color='red',icon='info-sign'),
    popup='19473993-1'
).add_to(mapa)

mapa.save("recursos/map.html")

##########################################################

from folium.plugins import Draw

m = folium.Map(
    location=[-34.9926116,-71.2527959],
    zoom_start=13)

draw = Draw()

draw.add_to(m)
plug = plugins.TimestampedGeoJson({
    'type': 'FeatureCollection',
}, period='PT1M', add_last_point=True)

plug.add_to(m)

m.save(os.path.join('recursos', 'dibujar.html'))



#######################################
import json
import numpy as np
import vincent

N = 100

multi_iter2 = {
    'x': [4,5,6],
    'y': [1,2,3],
}

scatter = vincent.Scatter(multi_iter2, iter_idx='x', height=100, width=200)
data = json.loads(scatter.to_json())

m = folium.Map([-34.969672, -71.230373], zoom_start=12)
mk = features.Marker([-34.969672, -71.230373])
p = folium.Popup('Hello')
v = features.Vega(data, width='100%', height='100%')

mk.add_child(p)
p.add_child(v)
m.add_child(mk)

m.save(os.path.join('recursos', 'mapaGrafico.html'))

#################################



mapaDatos = folium.Map(
    location=[-34.969672, -71.230373],
    zoom_start=16,

)
plug = plugins.TimestampedGeoJson({
    'type': 'FeatureCollection',
}, period='PT1M', add_last_point=True)

plug.add_to(mapaDatos)
####################################################


m = folium.Map(
    location=[-34.98159659061569, -71.16451516151428],
    zoom_start=16
)

# Lon, Lat order.
lines = [
    {
        'coordinates': [
            [-71.16451516151428, -34.98159659061569],
            [-71.15964426994324, -34.982590062684206],
        ],
        'dates': [
            '2017-06-02T00:00:00',
            '2017-06-02T00:10:00'
        ],
        'color': 'red'
    },
    {
        'coordinates': [
            [-71.15964426994324, -34.682590062684206],
            [-71.1575843334198, -34.679505030038506],
        ],
        'dates': [
            '2017-06-02T00:10:00',
            '2017-06-02T00:20:00'
        ],
        'color': 'blue'
    },
    {
        'coordinates': [
            [-71.1575843334198, -34.979505030038506],
            [-71.16337790489197, -34.978040905014065],
        ],
        'dates': [
            '2017-06-02T00:20:00',
            '2017-06-02T00:30:00'
        ],
        'color': 'green',
        'weight': 15,
    },
    {
        'coordinates': [
            [-71.16337790489197, -34.978040905014065],
            [-71.16451516151428, -34.98159659061569],
        ],
        'dates': [
            '2017-06-02T00:30:00',
            '2017-06-02T00:40:00'
        ],
        'color': '#FFFFFF',
    },
]


features = [
    {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': line['coordinates'],
        },
        'properties': {
            'times': line['dates'],
            'style': {
                'color': line['color'],
                'weight': line['weight'] if 'weight' in line else 5
            }
        }
    }
    for line in lines
]


plugins.TimestampedGeoJson({
    'type': 'FeatureCollection',
    'features': features,
}, period='PT1M', add_last_point=True).add_to(m)


m.save('recursos/Plugins_6.html')




mapaDatos.save("recursos/mapaDatos.html")


##########################

import json
import pandas as pd

us_states = os.path.join('data', 'us-states.json')
US_Unemployment_Oct2012 = os.path.join(
    'data', 'US_Unemployment_Oct2012.csv'
)

geo_json_data = json.load(open(us_states))
unemployment = pd.read_csv(US_Unemployment_Oct2012)

unemployment_dict = unemployment.set_index('State')['Unemployment']

def my_color_function(feature):
    """Maps low values to green and hugh values to red."""
    if unemployment_dict[feature['id']] > 6.5:
        return '#ff0000'
    else:
        return '#008000'

m = folium.Map([43, -100], tiles='cartodbpositron', zoom_start=4)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        'fillColor': my_color_function(feature),
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }
).add_to(m)

m.save(os.path.join('recursos/Colormaps_0.html'))
