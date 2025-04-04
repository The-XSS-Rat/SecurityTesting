# API Request Tool

This tool allows you to send HTTP requests to a specified API endpoint, perform fuzzing on request parameters, and save/load your session history. It also supports authentication, proxy configuration, and the ability to load Swagger/OpenAPI definitions.

## Features

- **Send API requests** with different HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
- **Authentication Support**: Basic, Bearer, and OAuth 2.0.
- **Fuzzing Parameters**: Allows you to fuzz request parameters by replacing `FUZZ` in the body with values from a list.
- **Session Management**: Save and load API request history.
- **Swagger/OpenAPI Import**: Import Swagger/OpenAPI definitions to automatically generate endpoints and request bodies.
- **Export History**: Export request history to a CSV file.
- **Proxy Support**: Support for setting up a proxy server (with Burp Suite certificate support).

## Installation

To install the required dependencies using Python 3 and `venv`, follow these steps:

1. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
Activate the virtual environment:
```

## On macOS/Linux:

```bash
Kopiëren
source venv/bin/activate
```
## On Windows:

```bash
Kopiëren
.\venv\Scripts\activate
```

## Install the required dependencies:

```
bash
Kopiëren
pip install -r requirements.txt
```

## Usage
- API Endpoint: Enter the API endpoint URL.
- Authentication: Select the type of authentication (Basic, Bearer, or OAuth 2.0). Enter the corresponding credentials or token.
- Method: Choose the HTTP method (GET, POST, PUT, DELETE).
- Request Body: For POST, PUT, and DELETE requests, enter the request body. You can use FUZZ as a placeholder to be replaced with fuzzing values.
- Fuzzing: You can select pre-populated fuzzing lists or manually enter fuzz values to test your API endpoints with multiple values.
- Proxy: Configure a proxy URL if needed.
- Response: After sending the request, the response (status code and body) will be shown in the response section.
- History: View a list of all previous requests and responses. You can select an entry to pre-populate the request fields.
- Save/Load Session: Save your session to a file or load a previously saved session to continue your work.

## Files
- requirements.txt: List of required Python packages.
- last_session.json: Stores the history of your API requests.
- preferences.json: Stores user preferences like proxy settings and Burp Suite certificate path.
- burp_cert.pem: Burp Suite certificate for proxying HTTPS requests.
- PREPOPLISTS: Folder containing pre-populated fuzzing lists.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
