import os
import requests

from flask import Flask, request, jsonify
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

@app.route("/key", methods=["GET"])
def get_key():
    api_key = os.environ.get("API_KEY")

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly&appid={api_key}"
    else:
        location = request.args.get("location")
        if not location:
            return jsonify({"error": "Missing required parameter: location"}), 400
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    
    response = requests.get(url)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Invalid API key"}), response.status_code
    
@app.route("/", methods=["GET"])
def get_home():
    return jsonify({"message": "Welcome to the Weather API!"}), 200

if __name__ == "__main__":  
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=True)
