# 99. List of tools for grabbing subdomains

## General Tools

1. [SubFinder](https://github.com/projectdiscovery/subfinder)
2. [Findomain](https://github.com/Findomain/Findomain)
3. [Sublist3r](https://github.com/aboul3la/Sublist3r)
4. [dnssearch](https://github.com/evilsocket/dnssearch)
5. [Sudomy](https://github.com/Screetsec/Sudomy)
6. [Assetfinder](https://github.com/tomnomnom/assetfinder)
7. [Vita](https://github.com/junnlikestea/vita)
8. [PureDNS](https://github.com/d3mondev/puredns)
9. [GetAllUrls(GUA)](https://github.com/lc/gau)

## Frameworks

1. [Amass](https://github.com/OWASP/Amass)
2. [Sudomy](https://github.com/Screetsec/Sudomy)
3. [ReconFTW](https://github.com/six2dez/reconftw)
4. [DMitry](https://securitytrails.com/blog/dmitry-osint-tool) 

## Dictionary attacks

1. [knockPy](https://github.com/guelfoweb/knock)
2. [DNSRecon](https://github.com/darkoperator/dnsrecon)
3. [MassDNS](https://github.com/blechschmidt/massdns)

## Datasets

1. [crt.sh](https://crt.sh/)
2. [WaybackURLS](https://github.com/tomnomnom/waybackurls)

## Permutation Scanning

1. [AltDNS](https://github.com/infosec-au/altdns)

## DNS Databases

1. [DNS Dumpster](https://dnsdumpster.com/)
2. [Shodan](https://snippets.shodan.io/c/83ldc9nef1Tp2R8C)
3. [Pentest-tools](https://pentest-tools.com/information-gathering/find-subdomains-of-domain)
4. [Rapid7 Forward DNS (FDNS)](https://opendata.rapid7.com/sonar.fdns_v2/)
5. [Crobat](https://github.com/lnxcrew/crobat)
6. [Subdomain finder by c99.nl](https://subdomainfinder.c99.nl/)
7. [BufferOver](http://dns.bufferover.run/dns?q=)
8. [Spyse](https://spyse.com/)

## Checking SubDomain Status Code

1. [URLChecker](https://github.com/evanRubinsteinIT/URLChecker)
2. [HTTProbe](https://github.com/tomnomnom/httprobe)

## Bash Extra resources

```yaml
curl -s https://rapiddns.io/subdomain/example.com?full=1 | grep -oP '_blank">\K[^<]*' | grep -v http | sort -u
```

1. curl -s [https://rapiddns.io/subdomain/example.com?full=1](https://rapiddns.io/subdomain/example.com?full=1) >>>> Will download a list of all the domains from rapiddns
2. grep -oP '_blank">\K[^<]*' >>>> Will grep all the links that open in a new tab 
3. Will grep all URLs that start with http
4. Will then sort the list

- [https://gowthams.gitbook.io/bughunter-handbook/list-of-vulnerabilities-bugs/recon-and-osint/subdomain-enumeration](https://gowthams.gitbook.io/bughunter-handbook/list-of-vulnerabilities-bugs/recon-and-osint/subdomain-enumeration)
- [https://github.com/CristinaSolana/subdomain-recon](https://github.com/CristinaSolana/subdomain-recon)
- [https://github.com/ARPSyndicate/kenzer](https://github.com/ARPSyndicate/kenzer)
- [https://github.com/bing0o/SubEnum](https://github.com/bing0o/SubEnum)
- [https://github.com/gwen001/github-search/blob/master/github-subdomains.py](https://github.com/gwen001/github-search/blob/master/github-subdomains.py)