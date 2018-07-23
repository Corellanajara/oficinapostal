import folium
m = folium.Map(
    location=[-34.9926116,-71.2527959],
    zoom_start=20,
    tiles='Stamen Terrain'
)

folium.Marker([-34.5926116,-71.5527959], popup='<i>1234724-6</i>').add_to(m)
folium.Marker([-34.6926116, -71.6527959], popup='<b>21253642-5</b>').add_to(m)

m.save("index.html")
