import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load environment variables from 'env.py' if it exists
if os.path.exists("env.py"):
    import env

# Define a route for the endpoint '/myapi' with the HTTP method 'GET'
@app.route('/myapi', methods=['GET'])
def get_data():
    try:
         # Retrieve the API key from the environment variables
        api_key = os.environ.get("API_KEY") 

        # Check if lat and lon parameters are provided in the query string
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        
        # Added endpoint parameter with default value 'weather'
        endpoint = request.args.get('endpoint', 'weather') 
        
        if lat and lon:
             # If lat and lon are provided, construct the API URL with the provided coordinates
            if endpoint == 'forecast':
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&lat={lat}&lon={lon}&appid={api_key}'
            else:
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&lat={lat}&lon={lon}&appid={api_key}'
        else:
             # If 'lat' and 'lon' are not provided, check if 'location' is provided
            location = request.args.get('location')
            if not location:
                return jsonify({"error": "No location or coordinates provided"}), 400
            # Construct the API URL with the provided location
            if endpoint == 'forecast':
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&q={location}&appid={api_key}'
            else:
                external_api_url = f'https://api.openweathermap.org/data/2.5/{endpoint}?units=metric&q={location}&appid={api_key}'
        
        # Send a GET request to the external API
        response = requests.get(external_api_url)
        
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "Failed to fetch data from external API"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app if this script is executed directly
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)