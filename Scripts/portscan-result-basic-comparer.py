import subprocess

def run_scan(target_host, scan_tool):
    if scan_tool == "nmap":
        result = subprocess.run(["nmap", "-sS", target_host], capture_output=True, text=True)
        ports = []
        for line in result.stdout.split("\n"):
            if "open" in line:
                port = line.split("/")[0]
                ports.append(port)
        return ports
    elif scan_tool == "masscan":
        result = subprocess.run(["masscan", target_host], capture_output=True, text=True)
        ports = []
        for line in result.stdout.split("\n"):
            if "open" in line:
                port = line.split(" ")[3].split("/")[0]
                ports.append(port)
        return ports
    elif scan_tool == "recon-ng":
        result = subprocess.run(["recon-ng", "--no-check", "-m", "scanner/portscan/tcp", "--workspace", "default", "-e", f"RHOSTS={target_host}"], capture_output=True, text=True)
        ports = []
        for line in result.stdout.split("\n"):
            if "open" in line:
                port = line.split(" ")[2]
                ports.append(port)
        return ports
    else:
        return []

def compare_scans(target_host):
    nmap_ports = run_scan(target_host, "nmap")
    masscan_ports = run_scan(target_host, "masscan")
    recon_ports = run_scan(target_host, "recon-ng")
    print(f"Nmap found the following open ports: {nmap_ports}")
    print(f"Masscan found the following open ports: {masscan_ports}")
    print(f"Recon-ng found the following open ports: {recon_ports}")
    common_ports = set(nmap_ports) & set(masscan_ports) & set(recon_ports)
    if common_ports:
        print(f"The following ports were found open by all three tools: {list(common_ports)}")
    else:
        print("No common open ports were found by all three tools.")

if __name__ == "__main__":
    target_host = input("Enter the target host: ")
    compare_scans(target_host)
