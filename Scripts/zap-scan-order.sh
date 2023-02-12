#!/bin/bash

# Define the host to be scanned
host=<hostname/IP address>

# Define the location of the ZAP CLI installation
zap_cli_location=<location of ZAP CLI installation>

# Define the output file location
output_file=<output file location>

# Start ZAP
$zap_cli_location/zap-cli start

# Spidering the host
$zap_cli_location/zap-cli spider $host

# Running an AJAX spider
$zap_cli_location/zap-cli ajax-spider $host

# Wait for spidering to complete
$zap_cli_location/zap-cli wait -t 120

# Running a quick ZAP scan
$zap_cli_location/zap-cli quick-scan --spider --ajax --output-file $output_file/quick_scan_results.json $host

# Running a full ZAP scan
$zap_cli_location/zap-cli full-scan --spider --ajax --output-file $output_file/full_scan_results.json $host

# Stop ZAP
$zap_cli_location/zap-cli stop
