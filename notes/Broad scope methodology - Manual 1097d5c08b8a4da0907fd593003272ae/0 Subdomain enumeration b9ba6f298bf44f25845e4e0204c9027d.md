# 0. Subdomain enumeration

# What is it?

![0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Subdomain_Enum.png](0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Subdomain_Enum.png)

When we talk about subdomain enumeration, we have several options to grab as many subdomains as possible. This is so that we can compose a list of subdomains for later investigations. 

We have several process available to us that help make this process easier and help us grab more subdomains.

# Search engine dorking

We have two options when we want to include dorking into our methdology. We can either do some manual dorking use that to increase our list of subdomains, but since that is not very effective, we can easily automate it as well. 

![0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled.png](0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled.png)

We can use many different search engines to execute this dorking process so automation is more than welcome. 

[https://github.com/OWASP/Amass](https://github.com/OWASP/Amass)

[https://github.com/fwaeytens/dnsenum/](https://github.com/fwaeytens/dnsenum/)

# Archiving website

There are 3 big players in the market of archiving the internet. These websites are set up so that we still enjoy the internet to a greater extend, even if the websites we love so much don't exist anymore. We can still visit them and even on existing websites we can grab that hint of nostalgia we all cherish. These websites take a snapshot of the target they are currently crawling if allowed and will index that in their databases. This is very useful for us as hackers since we can grab these snapshots and get the subdomains from them.

There is NO guarantee these subdomains are still online though and we will have to check them with the technique we will see in the httprobe chapter.

[https://archive.org/web/](https://archive.org/web/)

[https://archive-it.org/](https://archive-it.org/)

[https://archive.ph/](https://archive.ph/)

![0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled%201.png](0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled%201.png)

## Tools

- See search engine dorking

# DNS datasets

There are certain sources out there that gather subdomains. All of the have a different goal but they share one property. They all have a list of subdomains that we can use to query for new subdomains to add to our list.

We can again manually go through these datasets, but tools are much more recommended.

[https://dnsdumpster.com/](https://dnsdumpster.com/)

[https://otx.alienvault.com/](https://otx.alienvault.com/)

[https://github.com/jonluca/Anubis-DB](https://github.com/jonluca/Anubis-DB)

...

We can also use tools like amass again to gather subdomains from these passive sources.

# Certificate Transparency

Some certificate authorities (CA's) have made all the certificates they ever issues public. These certificates contain a goldmine of information, including domains, subdomains and email adresses.

![0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled%202.png](0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled%202.png)

We can again go through all these certificates ourselves, but there are perfectly valid solutions to check for this. 

1. [https://crt.sh/](https://crt.sh/)
2. [https://censys.io/](https://censys.io/)
3. [https://developers.facebook.com/tools/ct/](https://developers.facebook.com/tools/ct/)
4. [https://google.com/transparencyreport/https/ct/](https://www.google.com/transparencyreport/https/ct/)

![0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled%203.png](0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d/Untitled%203.png)

We can automate all this with scripts like [ct.py](http://ct.py) from massdns [https://github.com/blechschmidt/massdns](https://github.com/blechschmidt/massdns)

# DNS brute forcing

When we are going to try DNS brute forcing, we are trying to query a DNS server and see if our subdomains exist in the DNS. The results of this attack are very heavily dependant on the quality of the wordlists. DNS Recon is an amazing tool for this!

[https://github.com/darkoperator/dnsrecon](https://github.com/darkoperator/dnsrecon)

# Permutation scanning

Permutation scanning is a variation on DNS brute forcing. We are going to take our list of known subdomains and we are going to create a list with permutations on that original list.