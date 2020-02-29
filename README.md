# SecurityTesting

## How to use
- git clone https://github.com/heilla/SecurityTesting.git
- mkdir TARGETNAME
- cd TARGETNAME
- Copy the .sh files into the TARGETNAME folder

### Single run
sh initialScan.sh -h DOMAIN -o torfsNL -a true

### Running on a list of domains
sh scanMultipleDomains.sh -f domains.txt -a true

### Running a sqlmap scan on list of domains
NEEDED: sqlmap
../SecurityTesting/sqliList.sh -f paramUrlsStaging.txt 

### Running an XSS scan on list of domains
NEEDED: XSS
../SecurityTesting/xssList.sh -f paramUrls.txt
