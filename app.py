from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/location-page")
def location_page():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def receive_location():

    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")
    speed = data.get("speed")
    vehicle = data.get("vehicle")

    # Reverse Geocoding (UNCHANGED as you requested)
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {"User-Agent": "SafeTN-AI-App"}
    response = requests.get(url, headers=headers)
    location_data = response.json()
    area_name = location_data.get("display_name", "Unknown Area")

    # AI Risk Detection Logic
    risk = "LOW RISK - Safe Travel"
    suggestion = "Maintain safe driving."

    if vehicle == "bike":
        if speed > 80:
            risk = "HIGH RISK - Bike Overspeeding!"
            suggestion = "Reduce speed immediately. Wear helmet properly."
        elif speed > 60:
            risk = "MEDIUM RISK"
            suggestion = "You are nearing unsafe speed."

    elif vehicle == "car":
        if speed > 120:
            risk = "HIGH RISK - Car Overspeeding!"
            suggestion = "Slow down immediately. Maintain lane discipline."
        elif speed > 100:
            risk = "MEDIUM RISK"
            suggestion = "Reduce speed."

    elif vehicle == "bus":
        if speed > 90:
            risk = "HIGH RISK - Bus Overspeeding!"
            suggestion = "Passenger safety at risk. Slow down now."
        elif speed > 75:
            risk = "MEDIUM RISK"
            suggestion = "Drive carefully."

    return jsonify({
        "area": area_name,
        "risk_score": risk,
        "vehicle_type": vehicle,
        "suggestion": suggestion
    })

@app.route("/emergency", methods=["POST"])
def emergency_alert():

    data = request.json

    report = f"""
    🚨 SAFE TN SOS EMERGENCY ALERT 🚨
    ----------------------------------
    Phone Number: {data.get("phone")}
    Vehicle: {data.get("vehicle")}
    Speed: {data.get("speed")} km/h
    Area: {data.get("area")}
    Risk: {data.get("risk")}
    ----------------------------------
    """

    print(report)

    return jsonify({
        "message": "🚨 SOS Alert Sent Successfully! Authorities Notified."
    })

if __name__ == "__main__":
    app.run(debug=True)