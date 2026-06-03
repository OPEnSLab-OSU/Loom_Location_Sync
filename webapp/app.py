from flask import Flask, render_template
from flask_pymongo import PyMongo
from src.config import loom_mongo_uri
from folium.plugins import MarkerCluster
import folium

app = Flask(__name__)
app.config["MONGO_URI"] = loom_mongo_uri
mongo = PyMongo(app)

@app.route("/")
def index():

    devices = list(mongo.db["Location_Sync_04/23/2026"].find())
    print(len(devices))

    m = folium.Map(location=[39.5, -98.35], zoom_start=4)

    marker_cluster = MarkerCluster().add_to(m)

    for device in devices:
        folium.Marker(
            location=[device["latitude"], device["longitude"]],
            popup=device.get("name", "Unknown")
        ).add_to(marker_cluster)

    map_html = m._repr_html_()

    return render_template(
        "index.html",
        map_html=map_html
    )

if __name__ == "__main__":
    app.run(debug=True)