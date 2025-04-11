import requests
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import os
import csv
import time

# Constants
LAST_SESSION_FILE = "/tmp/last_session.json "
PREFERENCES_FILE = "/tmp/preferences.json"
BURP_CERT_PATH = "/tmp/burp_cert.pem"

# List to store full history entries
history_entries = []

# Constants for fuzzing rate limit
DEFAULT_RATE_LIMIT = 1  # 1 request per second
rate_limit = DEFAULT_RATE_LIMIT

# Load the pre-populated fuzzing lists from the PREPOPLISTS folder
def load_prepopulated_lists():
    prepopulated_lists = {}
    prepop_folder = "PREPOPLISTS"
    if not os.path.exists(prepop_folder):
        os.makedirs(prepop_folder)
        return prepopulated_lists

    for filename in os.listdir(prepop_folder):
        if filename.endswith(".txt"):
            with open(os.path.join(prepop_folder, filename), 'r') as f:
                fuzz_values = f.read().splitlines()
                prepopulated_lists[filename] = fuzz_values
    return prepopulated_lists

def update_fuzz_ui():
    prepopulated_lists = load_prepopulated_lists()

    # Clear the previous entries
    fuzz_text.delete("1.0", tk.END)
    fuzz_listbox.delete(0, tk.END)

    # Populate the Listbox with the names of the available pre-populated fuzzing lists
    for list_name in prepopulated_lists:
        fuzz_listbox.insert(tk.END, list_name)

    # Also provide an option to let users enter their own fuzz values
    fuzz_text.insert(tk.END, 'Enter custom fuzz values (one per line), or select a pre-populated list above.')

def use_prepopulated_fuzz_list():
    selected_index = fuzz_listbox.curselection()
    if not selected_index:
        return

    list_name = fuzz_listbox.get(selected_index[0])
    prepopulated_lists = load_prepopulated_lists()
    fuzz_values = prepopulated_lists.get(list_name, [])

    # Populate the fuzz input field with the selected list
    fuzz_text.delete("1.0", tk.END)
    for value in fuzz_values:
        fuzz_text.insert(tk.END, value + "\n")

def perform_request_with_rate_limit(fuzz_value=None):
    global rate_limit
    # Ensure there's a delay to meet the rate limit
    time.sleep(1 / rate_limit)
    
    # Perform the request as usual
    perform_request(fuzz_value)

def fuzz_parameters():
    values = fuzz_text.get("1.0", tk.END).strip().splitlines()
    for value in values:
        perform_request_with_rate_limit(fuzz_value=value)

def update_rate_limit():
    global rate_limit
    try:
        rate_limit = int(rate_limit_entry.get())
        if rate_limit <= 0:
            rate_limit = 1  # Minimum of 1 request per second
    except ValueError:
        rate_limit = 1  # Default to 1 request per second if invalid input

def load_preferences():
    """Load preferences if they exist."""
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, 'r') as f:
            prefs = json.load(f)
            proxy_entry.insert(0, prefs.get("default_proxy", ""))
            if os.path.exists(prefs.get("burp_cert_path", "")):
                global BURP_CERT_PATH
                BURP_CERT_PATH = prefs.get("burp_cert_path")

def save_preferences():
    prefs = {
        "default_proxy": proxy_entry.get(),
        "burp_cert_path": BURP_CERT_PATH
    }
    with open(PREFERENCES_FILE, 'w') as f:
        json.dump(prefs, f)

def import_burp_cert():
    global BURP_CERT_PATH
    cert_path = filedialog.askopenfilename(title="Select Burp Suite Certificate", filetypes=[("PEM files", "*.pem")])
    if cert_path:
        BURP_CERT_PATH = cert_path
        messagebox.showinfo("Certificate Imported", f"Burp Suite certificate imported from:\n{cert_path}")

def import_swagger():
    file_path = filedialog.askopenfilename(title="Select Swagger/OpenAPI JSON", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return
    try:
        with open(file_path, 'r') as f:
            swagger = json.load(f)
        endpoints = []
        endpoint_data = {}
        for path, methods in swagger.get("paths", {}).items():
            for method, details in methods.items():
                full_path = f"{method.upper()} {path}"
                endpoints.append(full_path)
                endpoint_data[full_path] = details
        if endpoints:
            top = tk.Toplevel(root)
            top.title("Swagger Endpoints")
            lb = tk.Listbox(top, width=80, height=20)
            lb.pack(padx=10, pady=10)
            for ep in endpoints:
                lb.insert(tk.END, ep)
            def use_selected():
                selected = lb.curselection()
                if selected:
                    key = lb.get(selected[0])
                    method, endpoint = key.split(" ", 1)
                    method_var.set(method)
                    url_entry.delete(0, tk.END)
                    url_entry.insert(0, endpoint)
                    if 'requestBody' in endpoint_data[key]:
                        content = endpoint_data[key]['requestBody'].get('content', {})
                        json_schema = content.get('application/json', {}).get('example')
                        if not json_schema:
                            json_schema = content.get('application/json', {}).get('schema')
                        if json_schema:
                            try:
                                if isinstance(json_schema, dict):
                                    formatted = json.dumps(json_schema, indent=2)
                                else:
                                    formatted = str(json_schema)
                                body_text.delete("1.0", tk.END)
                                body_text.insert(tk.END, formatted)
                            except Exception as e:
                                print("Schema parse error:", e)
            tk.Button(top, text="Use Selected", command=use_selected).pack(pady=5)
        else:
            messagebox.showinfo("No Endpoints", "No paths found in Swagger file.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse Swagger file:\n{e}")

def save_session():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if not file_path:
        return
    with open(file_path, 'w') as f:
        json.dump(history_entries, f)
    messagebox.showinfo("Saved", f"Session saved to {os.path.basename(file_path)}")

def load_session():
    """Load the last session file and populate the history."""
    if os.path.exists(LAST_SESSION_FILE):
        with open(LAST_SESSION_FILE, 'r') as f:
            try:
                loaded_entries = json.load(f)
                history_entries.clear()
                history_listbox.delete(0, tk.END)  # Clear the existing history list
                for entry in loaded_entries:
                    history_entries.append(entry)
                    history_listbox.insert(tk.END, f"{entry['method']} {entry['url']} [{entry['status_code']}]")
                if len(loaded_entries) > 0:
                    # Load the last entry into the UI fields
                    load_history_from_session(loaded_entries[-1])
            except json.JSONDecodeError:
                print("Error: Invalid session file format.")
                messagebox.showerror("Error", "Invalid session file format. Starting with a new session.")

def load_history_from_session(entry):
    """Populate the UI with data from a session entry."""
    # Split the full URL into baseURL and endpoint
    full_url = entry["url"]
    base_url = full_url.split('/')[0] + '//' + full_url.split('/')[2]  # Extract base URL (http://example.com)
    endpoint = '/'.join(full_url.split('/')[3:])  # The rest is the endpoint
    
    # Update the UI fields with the split base URL and endpoint
    base_url_entry.delete(0, tk.END)
    base_url_entry.insert(0, base_url)
    url_entry.delete(0, tk.END)
    url_entry.insert(0, endpoint)

    # Populate the other fields with the selected entry's data
    token_entry.delete(0, tk.END)
    token_entry.insert(0, entry["auth_token"])
    method_var.set(entry["method"])
    content_type_var.set(entry.get("content_type", "JSON"))
    proxy_entry.delete(0, tk.END)
    proxy_entry.insert(0, entry["proxy"])
    body_text.delete("1.0", tk.END)
    body_text.insert(tk.END, entry["body"])
    response_text.delete("1.0", tk.END)
    response_text.insert(tk.END, f"Status Code: {entry['status_code']}\n\n{entry['response']}")

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['method', 'url', 'status_code', 'body', 'response']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in history_entries:
            writer.writerow({k: entry.get(k, '') for k in fieldnames})
    messagebox.showinfo("Exported", "History exported to CSV")

def perform_request(fuzz_value=None):
    base_url = base_url_entry.get()
    endpoint = url_entry.get()
    full_url = base_url + endpoint  # Combine the baseURL and endpoint dynamically
    auth_token = token_entry.get()
    method = method_var.get()
    proxy_url = proxy_entry.get()
    body_input = body_text.get("1.0", tk.END).strip()
    content_type = content_type_var.get()

    proxies = None
    verify_cert = True
    if proxy_url:
        proxies = {"http": proxy_url, "https": proxy_url}
        if os.path.exists(BURP_CERT_PATH):
            verify_cert = BURP_CERT_PATH

    headers = {}
    data = None
    json_data = None

    # Handle different types of authentication
    if auth_type_var.get() == "Basic":
        username = username_entry.get()
        password = password_entry.get()
        headers["Authorization"] = f"{requests.auth._basic_auth_str(username, password)}"
    elif auth_type_var.get() == "Bearer":
        headers["Authorization"] = f"Bearer {auth_token}"
    elif auth_type_var.get() == "OAuth 2.0":
        # Handle OAuth 2.0 token input (or further implementation for OAuth flow)
        headers["Authorization"] = f"Bearer {auth_token}"

    if fuzz_value:
        body_input = body_input.replace("FUZZ", fuzz_value)

    if method in ['POST', 'PUT', 'DELETE']:
        if content_type == "JSON":
            headers["Content-Type"] = "application/json"
            try:
                json_data = json.loads(body_input)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format.")
                return
        else:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data = dict(item.split("=") for item in body_input.split("&") if "=" in item)

    try:
        response = requests.request(method, full_url, headers=headers, data=data, json=json_data, proxies=proxies, verify=verify_cert)
        history_data = {
            "url": full_url,
            "auth_token": auth_token,
            "method": method,
            "proxy": proxy_url,
            "body": body_input,
            "status_code": response.status_code,
            "response": response.text,
            "content_type": content_type
        }
        history_entries.append(history_data)
        history_listbox.insert(tk.END, f"{method} {full_url} [{response.status_code}]")

        # Save the session after the request
        with open(LAST_SESSION_FILE, 'w') as f:
            json.dump(history_entries, f)

        response_text.delete("1.0", tk.END)
        response_text.insert(tk.END, f"Status Code: {response.status_code}\n\n{response.text}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def fuzz_parameters():
    values = fuzz_text.get("1.0", tk.END).strip().splitlines()
    for value in values:
        perform_request(fuzz_value=value)

def load_history(event):
    selected_index = history_listbox.curselection()
    if not selected_index:
        return

    entry = history_entries[selected_index[0]]
    
    # Split the full URL into baseURL and endpoint
    full_url = entry["url"]
    base_url = full_url.split('/')[0] + '//' + full_url.split('/')[2]  # Extract base URL (http://example.com)
    endpoint = '/'.join(full_url.split('/')[3:])  # The rest is the endpoint
    
    # Ensure the endpoint starts with a slash if necessary
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint
    
    # Update the UI fields with the split base URL and endpoint
    base_url_entry.delete(0, tk.END)
    base_url_entry.insert(0, base_url)
    url_entry.delete(0, tk.END)
    url_entry.insert(0, endpoint)

    # Populate the other fields with the selected entry's data
    token_entry.delete(0, tk.END)
    token_entry.insert(0, entry["auth_token"])
    method_var.set(entry["method"])
    content_type_var.set(entry.get("content_type", "JSON"))
    proxy_entry.delete(0, tk.END)
    proxy_entry.insert(0, entry["proxy"])
    body_text.delete("1.0", tk.END)
    body_text.insert(tk.END, entry["body"])
    response_text.delete("1.0", tk.END)
    response_text.insert(tk.END, f"Status Code: {entry['status_code']}\n\n{entry['response']}")

# GUI setup
root = tk.Tk()
root.title("API Request Tool")

# Menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Session", command=save_session)
file_menu.add_command(label="Load Session", command=load_session)
file_menu.add_command(label="Export to CSV", command=export_to_csv)
file_menu.add_command(label="Import Burp Cert", command=import_burp_cert)
file_menu.add_command(label="Import Swagger", command=import_swagger)
file_menu.add_command(label="Save Preferences", command=save_preferences)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)
# Function to update the UI fields based on the selected authentication type
def update_auth_ui(*args):
    auth_type = auth_type_var.get()

    # Hide all authentication-related fields initially
    username_label.grid_forget()
    username_entry.grid_forget()
    password_label.grid_forget()
    password_entry.grid_forget()
    token_label.grid_forget()
    token_entry.grid_forget()

    # Show the appropriate fields based on the selected auth type
    if auth_type == "Basic":
        # Place the username and password on the same row (row 4)
        username_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        username_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        password_label.grid(row=4, column=2, sticky="w", padx=5, pady=5)
        password_entry.grid(row=4, column=3, sticky="ew", padx=5, pady=5)
    elif auth_type == "Bearer" or auth_type == "OAuth 2.0":
        token_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        token_entry.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=5)


# UI fields
tk.Label(root, text="API Endpoint:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
url_entry = tk.Entry(root, width=80)
url_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)


# UI fields
tk.Label(root, text="Base URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
base_url_entry = tk.Entry(root, width=80)
base_url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

tk.Label(root, text="API Endpoint:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
url_entry = tk.Entry(root, width=80)
url_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)


tk.Label(root, text="Authentication Type:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
auth_type_var = tk.StringVar(value="Bearer")
auth_type_var.trace_add("write", update_auth_ui)  # Update UI when authentication type changes
tk.OptionMenu(root, auth_type_var, "Basic", "Bearer", "OAuth 2.0").grid(row=2, column=1, sticky="ew", padx=5, pady=5)

# Labels and entries for different authentication types
username_label = tk.Label(root, text="Username:")
username_entry = tk.Entry(root, width=80)

password_label = tk.Label(root, text="Password:")
password_entry = tk.Entry(root, width=80, show="*")

token_label = tk.Label(root, text="Auth Token:")
token_entry = tk.Entry(root, width=80, show="*")

# Initially show fields for Bearer/OAuth 2.0 authentication
update_auth_ui()

tk.Label(root, text="Method:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
method_var = tk.StringVar(value="GET")
tk.OptionMenu(root, method_var, "GET", "POST", "PUT", "DELETE").grid(row=5, column=1, sticky="ew", padx=5, pady=5)

tk.Label(root, text="Content Type:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
content_type_var = tk.StringVar(value="JSON")
tk.OptionMenu(root, content_type_var, "JSON", "Form Data").grid(row=6, column=1, sticky="ew", padx=5, pady=5)

tk.Label(root, text="Proxy URL:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
proxy_entry = tk.Entry(root, width=80)
proxy_entry.grid(row=7, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

tk.Label(root, text="Request Body:").grid(row=8, column=0, sticky="nw", padx=5, pady=5)
body_text = scrolledtext.ScrolledText(root, height=5, width=60)
body_text.grid(row=8, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

tk.Button(root, text="Send Request", command=perform_request).grid(row=9, column=1, pady=5, sticky="ew", padx=5)

tk.Label(root, text="Fuzz Values (use 'FUZZ' in body):").grid(row=11, column=0, sticky="nw", padx=5, pady=5)
fuzz_text = scrolledtext.ScrolledText(root, height=5, width=30)
fuzz_text.grid(row=11, column=1, sticky="nw", padx=5, pady=5)
tk.Button(root, text="Fuzz Parameters", command=fuzz_parameters).grid(row=11, column=2, pady=5, sticky="n", padx=5)

tk.Label(root, text="History:").grid(row=12, column=0, sticky="nw", padx=5, pady=5)
history_listbox = tk.Listbox(root, height=10, width=50)
history_listbox.grid(row=12, column=1, sticky="nw", padx=5, pady=5)
history_listbox.bind('<<ListboxSelect>>', load_history)

tk.Label(root, text="Response:").grid(row=12, column=2, sticky="nw", padx=5, pady=5)
response_text = scrolledtext.ScrolledText(root, height=10, width=50)
response_text.grid(row=12, column=2, sticky="ne", padx=5, pady=5)

# Make columns responsive to resizing
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Load preferences and previous session
load_preferences()
load_session()  # Load the session on startup

for entry in history_entries:
    history_listbox.insert(tk.END, f"{entry['method']} {entry['url']} [{entry['status_code']}]")

root.mainloop()
