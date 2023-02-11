#!/bin/bash

# Check if the required parameters are provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <target_host>"
  exit 1
fi

# Define the target host
target_host=$1

# Define the current date and time
current_time=$(date +%s)

# Run Nmap
start_nmap=$(date +%s)
nmap_ports=$(nmap -sS $target_host | grep open | awk '{print $1}' | tr '\n' ',' | sed 's/,$//')
end_nmap=$(date +%s)
nmap_time=$((end_nmap - start_nmap))

# Run Masscan
start_masscan=$(date +%s)
masscan_ports=$(masscan $target_host | grep open | awk '{print $3}' | tr '\n' ',' | sed 's/,$//')
end_masscan=$(date +%s)
masscan_time=$((end_masscan - start_masscan))

# Run Recon-ng
start_recon=$(date +%s)
recon_ports=$(recon-ng --no-check -m scanner/portscan/tcp --workspace default -e RHOSTS=$target_host | grep open | awk '{print $2}' | tr '\n' ',' | sed 's/,$//')
end_recon=$(date +%s)
recon_time=$((end_recon - start_recon))

# Print the results
echo "Nmap took $nmap_time seconds to run and found the following open ports: $nmap_ports"
echo "Masscan took $masscan_time seconds to run and found the following open ports: $masscan_ports"
echo "Recon-ng took $recon_time seconds to run and found the following open ports: $recon_ports"
