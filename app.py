
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def fetch_fb_data():
    data = request.get_json()
    access_token = data.get('accessToken')

    if not access_token:
        return jsonify({"error": "Access token is missing"}), 400

    fb_response = requests.get(f"https://graph.facebook.com/me?fields=id,name,email,birthday&access_token={access_token}")
    if fb_response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Facebook", "details": fb_response.text}), 500

    user_data = fb_response.json()

    # Ensure all requested fields are included
    response_data = {
        "id": user_data.get("id"),
        "name": user_data.get("name"),
        "email": user_data.get("email", "Not provided"),
        "birthday": user_data.get("birthday", "Not provided")
    }

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
