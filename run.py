import os
import requests

from flask import Flask, request, jsonify

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

@app.route("/mykey", methods=["GET"])
def get_key():
    apiKey = os.environ.get("API_KEY")
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    print(lat, lon)
    if lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&{lat}&lon={lon}&appid={apiKey}"
    else:
        location = request.args.get("location")
        if not location:
            return jsonify({"error": "Missing required parameter: location"}), 400
        url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={location}&appid={apiKey}"
    print(url)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        print(response.json())
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": "Invalid API key"}), response.status_code
    
@app.route("/", methods=["GET"])
def get_home():
    sample_url1 = "https://weather-dh-d49c7aef68c1.herokuapp.com/mykey?location=London"
    sample_url2 = "https://weather-dh-d49c7aef68c1.herokuapp.com/mykey?lat=51.5074&lon=-0.1278"
    print(sample_url1)
    print(sample_url2)
    return jsonify({"message": "Welcome to the Weather API!"}), 200

if __name__ == "__main__":  
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=True)
