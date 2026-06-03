from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from src.config import webapp_mongo_uri
from src.job import update_locations
from folium.plugins import MarkerCluster
import folium

app = Flask(__name__)
app.config["MONGO_URI"] = webapp_mongo_uri
mongo = PyMongo(app)

@app.route("/")
def index():

    devices = list(mongo.db["Location_Sync_06/02/2026"].find())

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
        map_html=map_html, total_devices=len(devices), updated_devices=sum(len(device["Previous Locations"]) for device in devices if "Previous Locations" in device))
@app.route("/devices")
def devices():
    devices = list(mongo.db["Location_Sync_06/02/2026"].find())
    return render_template("devices.html", devices=devices)

@app.route("/update")
def update():
    # Implementation for updating device data
    update_locations()
    devices = list(mongo.db["Location_Sync_06/02/2026"].find())
    return redirect(url_for("index"))

@app.route("/edit/<int:device_id>", methods=["GET", "POST"])
def edit_device(device_id):
    device = mongo.db["Location_Sync_06/02/2026"].find_one({"deviceid": device_id})
    if not device:
        return "Device not found", 404

    if request.method == "POST":
        new_latitude = request.form.get("latitude")
        new_longitude = request.form.get("longitude")

        if new_latitude or new_longitude:
            mongo.db["Location_Sync_06/02/2026"].update_one(
                {"deviceid": device_id},
                {"$set": {"latitude": float(new_latitude), "longitude": float(new_longitude)}}
            )
            return redirect(url_for("devices"))

    return render_template("edit_device.html", device=device)

@app.route("/history/<int:device_id>")
def history(device_id):
    device = mongo.db["Location_Sync_06/02/2026"].find_one({"deviceid": device_id})
    if not device:
        return "Device not found", 404

    history = device.get("Previous Locations", [])
    return render_template("location_history.html", device=device, history=history)

if __name__ == "__main__":
    app.run(debug=True)