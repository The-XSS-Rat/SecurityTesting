
# 🐍 API Fuzzer GUI Tool

A Python-based GUI tool for sending customized HTTP requests with fuzzing capabilities. It supports Swagger/OpenAPI JSON import, Burp Suite integration, custom and pre-populated wordlists, session saving/loading, and more.

<br>

## ✨ Features

- ✅ GUI interface using `Tkinter`
- ✅ Support for different authentication methods: Bearer, Basic, OAuth 2.0
- ✅ Load and manage **pre-populated fuzz lists** from the `PREPOPLISTS/` directory
- ✅ Swagger/OpenAPI JSON parser and endpoint loader
- ✅ Request fuzzing with delay/rate limiting
- ✅ History viewer with session save/load
- ✅ Burp Suite proxy and certificate support
- ✅ Export history to CSV
- ✅ Import and parse Swagger/OpenAPI files

<br>  

## 📁 Folder Structure
```

├── main.py # Main GUI app
├── PREPOPLISTS/         # Directory for pre-built wordlists
│ ├── sqli.txt
│ ├── xss.txt
│ └── ...                # Add more .txt wordlists
├── /tmp/
│ ├── last_session.json  # Saved session history
│ └── preferences.json   # Saved proxy/cert preferences

```
<br>

## 🚀 Getting Started

  

### Prerequisites

- Python 3.x
- Required packages: `requests` , `tkinter`

### Installation

- To install the required dependencies using Python 3 and venv follow these steps:

```bash
git clone https://github.com/The-XSS-Rat/SecurityTesting/tree/master/Scripts/RatAPIChat

```

- Set up a virtual environment:
````bash
python3 -m venv venv
````

### Activate the virtual environment:

- On macOS/Linux:

````bash
source venv/bin/activate
````

- On Windows:

````bash
.\venv\Scripts\activate
````
- Install the required dependencies:
````bash
pip install -r requirements.txt
````
### Install library seperately

- Installing `requests` (Python library for HTTP)
````bash
pip3 install requests

````

- Installing `tkinter` (GUI library)
````bash
sudo apt update
sudo apt install python3-tk
````

<br>

## 🧠 Usage 

### 1. Set Up 

- Enter **Base URL**, **Endpoint**, and select **Method** (GET, POST, etc.)
- Choose content type: `JSON` or `Form URL Encoded`
- Optionally input auth tokens, username/password (for Basic), or use OAuth 2.0

### 2. Fuzzing

- Either type custom fuzzing values in the fuzz box, or
- Load from `PREPOPLISTS/` by selecting a list from the GUI
- Press **"Fuzz"** to execute requests with each value

### 3. Swagger Import

- Click `Import Swagger` to load `.json` Swagger/OpenAPI
- Pick an endpoint → auto-fills method, URL, and request body
 
### 4. Proxy (Burp Suite)
 
- Input proxy URL (e.g. `http://127.0.0.1:8080`)
- Import Burp's certificate (PEM format) via GUI
 
### 5. Session & History

- View request history in the side panel
- Save/load session to/from `.json`
- Export all request/response history as `.csv`

<br>

## 📂 Pre-Populated Wordlists

Place `.txt` files in the `PREPOPLISTS/` folder. Each line should be a separate fuzzing value.

Example:
**xss.txt**

```
<script>alert(1)</script>
"><svg/onload=alert(1)>
'><img src=x onerror=alert(1)>
```
<br>

## 🧪 Sample Use Case

- Test for SQLi: load `sqli.txt` from PREPOPLISTS, click fuzz
- Use `FUZZ` keyword in body/URL to dynamically inject each value
- Monitor results and status codes for anomalies

<br>  

## 🛠 Tech Stack

- Python 3
- `Tkinter` for GUI
- `Requests` for HTTP handling
- JSON for Swagger parsing and data exchange
 
 <br>
 
## 🧑‍💻 Author

Developed by **THE XSSRAT**

<br>

## 📜 License

MIT License – feel free to use and modify with credit.
