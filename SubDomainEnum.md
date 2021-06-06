- [Usage And flow](#usage-and-flow)
  * [Amass](#amass)
    + [Installation](#installation)
      - [Requirements](#requirements)
      - [Steps](#steps)
    + [Running amass](#running-amass)
  * [Other general tools](#other-general-tools)
- [List of Tools](#list-of-tools)
  * [General Tools](#general-tools)
  * [Dictionary attacks](#dictionary-attacks)
  * [Permutation Scanning](#permutation-scanning)
  * [DNS Databases](#dns-databases)
  * [Checking SubDomain Status Code](#checking-subdomain-status-code)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Usage And flow
## Amass
First off, i like to use Amass. It will give me a great amount of results and usually makes the other tools seem like nubs.
### Installation
#### Requirements
- Brew Needs to be installed
#### Steps
    brew tap caffix/amass
    brew install amass
### Running amass
    Simple Enum:
     amass enum -d example.com
    
    Intel:
     amass intel -org google
    This will result in CIDR records:
     amass intel -ip -src -cidr IP.IP.IP.IP
## Other general tools
We can run other tools like SubFinder, FinDomain, dnssearch,... to complete our list, for those see the github pages.

# List of Tools
## General Tools
1. [Amass](https://github.com/OWASP/Amass)
2. [SubFinder](https://github.com/projectdiscovery/subfinder)
3. [Findomain](https://github.com/Findomain/Findomain)
4. [Sublist3r](https://github.com/aboul3la/Sublist3r)
5. [dnssearch](https://github.com/evilsocket/dnssearch)
6. [Sudomy](https://github.com/Screetsec/Sudomy)


## Dictionary attacks
1. [knockPy](https://github.com/guelfoweb/knock)
2. [DNSRecon](https://github.com/darkoperator/dnsrecon)
3. [MassDNS](https://github.com/blechschmidt/massdns)

## Permutation Scanning
1. [AltDNS](https://github.com/infosec-au/altdns)

## DNS Databases
1. [DNS Dumpster](https://dnsdumpster.com/)
2. [Shodan](https://snippets.shodan.io/c/83ldc9nef1Tp2R8C)
3. [Pentest-tools](https://pentest-tools.com/information-gathering/find-subdomains-of-domain)
4. [Rapid7 Forward DNS (FDNS)](https://opendata.rapid7.com/sonar.fdns_v2/)

## Checking SubDomain Status Code
1. [URLChecker](https://github.com/evanRubinsteinIT/URLChecker)
2. [HTTProbe](https://github.com/tomnomnom/httprobe)
3. [httpx](https://github.com/projectdiscovery/httpx)
4. [dnsx](https://github.com/projectdiscovery/dnsx)
