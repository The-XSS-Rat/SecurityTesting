import subprocess
import json
import sys

# Function to enumerate subdomains using subfinder
def enumerate_subdomains(domain):
    try:
        print(f"Enumerating subdomains for {domain} using subfinder...")
        subfinder_command = ["subfinder", "-d", domain, "-silent"]
        result = subprocess.run(subfinder_command, capture_output=True, text=True, check=True)
        
        subdomains = result.stdout.strip().split("\n")
        if not subdomains or subdomains == [""]:
            print(f"No subdomains found for {domain}.")
            return []
        return subdomains
    
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Subfinder failed: {e}")
        return []

# Function to run FFUF with recursion on each subdomain
def run_ffuf(target_url, wordlist):
    try:
        print(f"Running FFUF recursively on {target_url}...")
        ffuf_command = [
            "ffuf",
            "-u", f"{target_url}/FUZZ",  # Fuzz for directories/files
            "-w", wordlist,              # Wordlist for discovery
            "-t", "50",                  # Number of threads (adjust as needed)
            "-recursion",                # Enable recursive fuzzing
            "-recursion-depth", "2",     # Set recursion depth
            "-o", "ffuf_output.json",    # Output results to JSON
            "-of", "json"                # Ensure output is in JSON format
        ]
        subprocess.run(ffuf_command, check=True)
        print("FFUF recursive scan completed. Results saved in ffuf_output.json")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFUF failed on {target_url}: {e}")

# Function to extract URLs from FFUF output
def extract_urls_from_ffuf():
    try:
        with open("ffuf_output.json", "r") as file:
            data = json.load(file)
            urls = [entry["url"] for entry in data["results"] if "url" in entry]
            return urls
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[ERROR] Could not read FFUF output: {e}")
        return []

# Function to run Dalfox on extracted URLs
def run_dalfox(urls):
    for url in urls:
        try:
            print(f"Running Dalfox for XSS testing on {url}...")
            dalfox_command = ["dalfox", "url", url, "--param", "--auto"]
            subprocess.run(dalfox_command, check=True)
            print(f"Dalfox scan completed for {url}")

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Dalfox failed on {url}: {e}")

# Main function to orchestrate subdomain enumeration, FFUF, and Dalfox
def main():
    domain = input("Enter the target domain (e.g., example.com): ")
    wordlist = input("Enter the path to your wordlist (e.g., /path/to/wordlist.txt): ")

    # Step 1: Enumerate subdomains
    subdomains = enumerate_subdomains(domain)
    
    if not subdomains:
        print("No subdomains found. Continuing without subdomain enumeration.")

    print(f"Found {len(subdomains)} subdomains. Starting FFUF scans...")

    # Step 2: Run FFUF on each subdomain
    all_urls = []
    for subdomain in subdomains:
        full_url = f"https://{subdomain}"  # Assuming HTTPS
        run_ffuf(full_url, wordlist)

        # Step 3: Extract discovered URLs from FFUF output
        urls = extract_urls_from_ffuf()
        all_urls.extend(urls)

    if all_urls:
        print(f"Found {len(all_urls)} URLs from FFUF. Running Dalfox on them...")
        # Step 4: Run Dalfox on discovered URLs
        run_dalfox(all_urls)
    else:
        print("No URLs found in FFUF output. Skipping Dalfox step.")

    print("Scanning process completed.")

if __name__ == "__main__":
    main()
