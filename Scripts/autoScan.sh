#!/bin/bash

# Check if the target argument was provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <target>"
  echo "       where target can be a single IP address, range of IP addresses, or a subnet in CIDR notation"
  exit 1
fi

target=$1

# Run Naabu scan on all TCP and UDP ports
naabu -h $target -p-u > naabu_output.txt

# Run Masscan scan on all TCP and UDP ports
masscan $target -p- --rate=10000 > masscan_output.txt

# Run Recon-ng scan
recon-ng -r $target > recon-ng_output.txt

# Run Nmap scan on all TCP and UDP ports
nmap -sS -sU -p- -A $target > nmap_output.txt

# Check if a web port was found
if grep -q "80/tcp" nmap_output.txt || grep -q "443/tcp" nmap_output.txt; then
  echo "Web port found, running additional web tools..."
  
    # Run Gobuster scan
  gobuster dir -u http://$target -w /usr/share/wordlists/dirb/common.txt > gobuster_output.txt

  # Run Eyewitness scan
  eyewitness --web --threads=10 --no-prompt --prepend-https $target > eyewitness_output.txt

  # Run Nuclei scan
  nuclei -t templates/web-content/all-vulns.yaml -t templates/web-content/common-dirs.yaml $target > nuclei_output.txt

  # Run Nikto scan
  nikto -h $target > nikto_output.txt
fi

