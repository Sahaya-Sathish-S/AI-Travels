from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def receive_location():
    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")

    # Reverse Geocoding using Nominatim
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {
        "User-Agent": "AI-Travel-Safety-App"
    }

    response = requests.get(url, headers=headers)
    location_data = response.json()

    area_name = location_data.get("display_name", "Unknown Area")

    return jsonify({
        "area": area_name
    })

if __name__ == "_main_":
    app.run(debug=True)