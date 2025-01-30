from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
ZYLALABS_API_KEY = os.getenv("ZYLALABS_API_KEY")

app = Flask(__name__)

# API Endpoint
ZYLALABS_API_URL = "https://zylalabs.com/api/5921/zip+code+gas+prices+api/7816/get+prices"

def fetch_gas_prices(zip_code):
    headers = {
        "Authorization": f"Bearer {ZYLALABS_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {
        "zip": zip_code,
        "type": "regular"
    }

    response = requests.get(ZYLALABS_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search_gas():
    area_code = request.args.get("area_code")

    if not area_code:
        return jsonify({"error": "Area code is required"}), 400

    gas_data = fetch_gas_prices(area_code)

    if not gas_data or "gas_prices" not in gas_data:
        return jsonify({"error": "No gas price data found"}), 404

    return jsonify({"gas_prices": gas_data["gas_prices"]})

if __name__ == "__main__":
    app.run(debug=True)
