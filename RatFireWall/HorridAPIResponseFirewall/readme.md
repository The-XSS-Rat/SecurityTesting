# Outgoing API Firewall Proxy
This Python-Flask based outgoing API firewall proxy helps protect your application by inspecting JSON responses from an external API. It searches for specific forbidden keywords, such as "password" or "api-key", and blocks the response if it contains any of these words. The proxy supports GET, POST, PUT, and DELETE methods.

## Requirements
- Python 3.6 or higher
- Flask
- Installation
- Clone this repository:
- Create a virtual environment and install dependencies:

`python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt`

## Configuration
Edit the app.py file and replace the PROXY_API_BASE_URL variable with the base URL of the API you want to proxy:

`PROXY_API_BASE_URL = 'https://api.example.com'`

Modify the FORBIDDEN_KEYWORDS list to include the keywords you want to block in the JSON response:


`FORBIDDEN_KEYWORDS = ['password', 'api-key']`

## Running the proxy
- Start the Flask app by running:

`flask run --host=0.0.0.0 --port=8080`

This will start the proxy on port 8080. You can now send requests to http://localhost:8080 followed by the API path you want to access.

## Usage
Make requests to the proxy as you would to the actual API. For example, if the original API request is:

`GET https://api.example.com/some/endpoint?param=value`

You would make the same request to the proxy:

`GET http://localhost:8080/some/endpoint?param=value`

If the proxy detects any forbidden keywords in the JSON response, it will return a 403 Forbidden response with an error message.

## License
This project is released under the MIT License.

## Contributing
Pull requests and issues are welcome. Please feel free to contribute and help improve the project!




