import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

if os.path.exists("env.py"):
    import env

@app.route('/myapi', methods=['GET'])
def get_data():
    try:
        api_key = os.environ.get("API_KEY") 
        # Check if lat and lon parameters are provided
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if lat and lon:
            external_api_url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lon}&appid={api_key}'
        else:
            location = request.args.get('location')
            if not location:
                return jsonify({"error": "No location or coordinates provided"}), 400
            external_api_url = f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={location}&appid={api_key}'

        response = requests.get(external_api_url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from external API"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def get_info():
    try:
        sample_url1 = "https://weather-key-160275f00837.herokuapp.com/myapi?location=London"
        sample_url2 = "https://weather-key-160275f00837.herokuapp.com/myapi?lat=51.5074&lon=-0.1278"
        return f"Sample URL with location: <strong>{sample_url1}</strong><br><br>Sample URL with latitude and longitude: <strong>{sample_url2}</strong>"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)

# _____________________________________________________

# import os
# import requests

# from flask import Flask, request, jsonify

# if os.path.exists("env.py"):
#     import env

# app = Flask(__name__)

# @app.route("/mykey", methods=["GET"])
# def get_key():
#     apiKey = os.environ.get("API_KEY")
#     lat = request.args.get("lat")
#     lon = request.args.get("lon")
#     print(lat, lon)
#     if lat and lon:
#         url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&{lat}&lon={lon}&appid={apiKey}"
#     else:
#         location = request.args.get("location")
#         if not location:
#             return jsonify({"error": "Missing required parameter: location"}), 400
#         url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={location}&appid={apiKey}"
#     print(url)
#     response = requests.get(url)
#     print(response.status_code)
#     if response.status_code == 200:
#         print(response.json())
#         return jsonify(response.json()), 200
#     else:
#         return jsonify({"error": "Invalid API key"}), response.status_code
    
# @app.route("/", methods=["GET"])
# def get_home():
#     sample_url1 = "https://weather-key-160275f00837.herokuapp.com/mykey?location=London"
#     sample_url2 = "https://weather-key-160275f00837.herokuapp.com/mykey?lat=51.5074&lon=-0.1278"
#     print(sample_url1)
#     print(sample_url2)
#     return jsonify({"message": "Welcome to the Weather API!"}), 200

# if __name__ == "__main__":  
#     app.run(
#         host=os.environ.get("IP", "0.0.0.0"),
#         port=int(os.environ.get("PORT", 5000)),
#         debug=True)
