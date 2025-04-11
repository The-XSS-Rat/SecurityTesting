import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import json
import time
import threading
import requests

# Function to load OpenAPI specification from a local file
def load_openapi_spec(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the OpenAPI spec: {e}")
        return None

# Function to test an endpoint for SQL injection
def test_endpoint(base_url, path):
    url = base_url + path
    payloads = ["' OR '1'='1", '" OR "1"="1', "admin'--", 'admin"--']
    for payload in payloads:
        test_url = f"{url}?param={payload}"
        try:
            response = requests.get(test_url)
            if "error" in response.text.lower():  # Simplified check for SQL error
                result_text.insert(tk.END, f"Potential SQLi detected at {test_url}\n")
            time.sleep(1)  # To avoid overwhelming the server
        except Exception as e:
            result_text.insert(tk.END, f"Error testing {test_url}: {e}\n")

# Function to start testing all endpoints
def start_testing():
    base_url = baseurl_entry.get()
    if not base_url:
        messagebox.showerror("Input Error", "Please enter the Base URL.")
        return

    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror("Input Error", "Please load a valid OpenAPI file.")
        return

    spec = load_openapi_spec(file_path)
    if spec:
        paths = spec.get('paths', {})
        for path in paths:
            threading.Thread(target=test_endpoint, args=(base_url, path)).start()
    else:
        messagebox.showerror("Error", "Invalid OpenAPI specification.")

# Function to browse and load the OpenAPI file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

# Set up the GUI
root = tk.Tk()
root.title("API SQL Injection Tester")

# Base URL input
tk.Label(root, text="Base URL:").pack(pady=5)
baseurl_entry = tk.Entry(root, width=80)
baseurl_entry.pack(pady=5)

# File path input
tk.Label(root, text="OpenAPI File:").pack(pady=5)
file_entry = tk.Entry(root, width=80)
file_entry.pack(pady=5)

# Browse button for file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start Testing", command=start_testing)
start_button.pack(pady=20)

# Results display
result_text = scrolledtext.ScrolledText(root, height=20, width=80)
result_text.pack(pady=5)

root.mainloop()
