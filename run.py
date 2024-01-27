import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


if os.path.exists("env.py"):
    import env

@app.route('/myapi', methods=['GET'])
def get_data():
    try:
        api_key = os.environ.get("API_KEY") 
        # Check if lat and lon parameters are provided
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        endpoint = request.args.get('endpoint', 'weather')  # Added endpoint parameter with default value 'weather'
        
        if lat and lon:
            if endpoint == 'forecast':
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&lat={lat}&lon={lon}&appid={api_key}'
            else:
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&lat={lat}&lon={lon}&appid={api_key}'
        else:
            location = request.args.get('location')
            if not location:
                return jsonify({"error": "No location or coordinates provided"}), 400
            if endpoint == 'forecast':
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&q={location}&appid={api_key}'
            else:
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&q={location}&appid={api_key}'

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
        sample_url3 = "https://weather-key-160275f00837.herokuapp.com/myapi?location=London&endpoint=forecast"
        return f"Sample URL with location: <strong>{sample_url1}</strong><br><br>Sample URL with latitude and longitude: <strong>{sample_url2}</strong> {sample_url3}"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)

# _____________________________________________________
# @app.route('/myapi', methods=['GET'])
# def get_data():
#     try:
#         api_key = os.environ.get("API_KEY") 
#         # Check if lat and lon parameters are provided
#         lat = request.args.get('lat')
#         lon = request.args.get('lon')
#         endpoint = request.args.get('endpoint', 'weather')  # Added endpoint parameter with default value 'weather'
        
#         if lat and lon:
#             # If lat and lon are provided, construct the API URL with the provided coordinates
#             external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&lat={lat}&lon={lon}&appid={api_key}'
#         else:
#             location = request.args.get('location')
#             if not location:
#                 # If neither lat and lon nor location are provided, return an error response
#                 return jsonify({"error": "No location or coordinates provided"}), 400
#             # If only location is provided, construct the API URL with the provided location
#             external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&q={location}&appid={api_key}'

#         # Send a GET request to the external API
#         response = requests.get(external_api_url)
#         if response.status_code == 200:
#             # If the request is successful (status code 200), return the JSON response
#             return jsonify(response.json())
#         else:
#             # If the request fails, return an error response with the corresponding status code
#             return jsonify({"error": "Failed to fetch data from external API"}), response.status_code
#     except Exception as e:
#         # If any exception occurs during the execution, return an error response with the exception message
#         return jsonify({"error": str(e)}), 500

# @app.route('/', methods=['GET'])
# def get_info():
#     try:
#         # Sample URLs for testing the '/myapi' endpoint
#         sample_url1 = "https://weather-key-160275f00837.herokuapp.com/myapi?location=London"
#         sample_url2 = "https://weather-key-160275f00837.herokuapp.com/myapi?lat=51.5074&lon=-0.1278"