import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PROXY_API_BASE_URL = 'https://api.example.com'  # Replace with the API you want to proxy
FORBIDDEN_KEYWORDS = ['password', 'api-key']


def inspect_response(json_data):
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in str(json_data).lower():
            return True
    return False


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_request(path):
    if request.method == 'GET':
        response = requests.get(f'{PROXY_API_BASE_URL}/{path}', params=request.args)
    elif request.method == 'POST':
        response = requests.post(f'{PROXY_API_BASE_URL}/{path}', json=request.json)
    elif request.method == 'PUT':
        response = requests.put(f'{PROXY_API_BASE_URL}/{path}', json=request.json)
    elif request.method == 'DELETE':
        response = requests.delete(f'{PROXY_API_BASE_URL}/{path}', params=request.args)
    
    if response.status_code == 200 and response.headers['Content-Type'] == 'application/json':
        json_data = response.json()
        if inspect_response(json_data):
            return jsonify({"error": "Forbidden content in response"}), 403
        else:
            return jsonify(json_data), 200

    return response.content, response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
