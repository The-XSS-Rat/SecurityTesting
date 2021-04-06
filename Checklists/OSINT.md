Target: finding api keys, secrets, source code, subdomains, anything usefull

# Resources
- Google - https://google.com
- Shodan - https://shodan.io
- Censys - https://censys.io
- Fofa - https://fofa.so
- Dogpile - http://www.dogpile.com
- Archives - https://archive.org
- Google hacking db

# Subdomain enum
- Aquatone - https://github.com/michenriksen/aquatone
- Sublister - https://github.com/aboul3la/Sublist3r
- DNS dumpster - https://dnsdumpster.com/
- Facebook - https://developers.facebook.com/tools/ct

# Email harvesting
- [Theharvester](https://github.com/laramies/theHarvester)
- [Prowl](https://github.com/nettitude/prowl)
- [Haveibeenpwned](https://haveibeenpwned.com/)

# Tips:
- You can use the following boolean logical operators to combine queries: AND, OR, + and -
- filetype: allows to search for specific file extensions
- site: will filter on a specific website
- intitle: and inurl: will filter on the title or the url
- link:: find webpages having a link to a specific url (deprecated in 2017, but still partially work)

## Some examples:
 1. NAME + CV + filetype:pdf can help you find someone CV
 2. DOMAIN - site:DOMAIN may help you find subdomains of a website
 3. SENTENCE - site:ORIGINDOMAIN may help you find website that plagiarized or copied an article

# Chrome plugins to help with OSINT:
- archive.is Button allows to quickly save a webpage in archive.is (more about this later)
- Wayback Machine to search for archived page in the archive.org Wayback machine
- OpenSource Intelligence gives a quick access to many OSINT tools
- EXIF Viewer allows to quickly view EXIF data in images
- FireShot to take screenshot quickly
