# Bug Bounty / Web Application Security Hunting Checklist

A practical checklist for web application security testing and bug bounty hunting. Work through each section methodically and expand the list with your own findings.

---

## Table of Contents

1. [Strategy](#strategy)
2. [Reconnaissance & Hidden Endpoints](#reconnaissance--hidden-endpoints)
3. [Session Management](#session-management)
4. [Cookies](#cookies)
5. [Authentication & Login](#authentication--login)
6. [SQL Injection](#sql-injection)
7. [Cross-Site Scripting (XSS)](#cross-site-scripting-xss)
   - [Stored XSS](#stored-xss)
   - [Reflected XSS](#reflected-xss)
   - [DOM XSS](#dom-xss)
   - [Blind XSS](#blind-xss)
   - [XSS Filter Evasion](#xss-filter-evasion)
8. [Server-Side Template Injection (SSTI)](#server-side-template-injection-ssti)
9. [Command Injection](#command-injection)
10. [CSRF (Cross-Site Request Forgery)](#csrf-cross-site-request-forgery)
11. [IDOR / Broken Access Control](#idor--broken-access-control)
12. [LFI / RFI (Local/Remote File Inclusion)](#lfi--rfi-localremote-file-inclusion)
13. [File Upload Vulnerabilities](#file-upload-vulnerabilities)
14. [XXE (XML External Entity)](#xxe-xml-external-entity)
15. [SSRF (Server-Side Request Forgery)](#ssrf-server-side-request-forgery)
16. [Open Redirects](#open-redirects)
17. [HTTP Security Headers](#http-security-headers)
18. [Chaining Vulnerabilities](#chaining-vulnerabilities)
    - [Chaining XSS](#chaining-xss)
    - [Chaining CSRF](#chaining-csrf)
    - [Chaining IDOR](#chaining-idor)

---

## Strategy

*Tips*
- First, get to know your target: spend time using the application normally with Burp Suite open to build a site map
- Start testing for XSS and SSTI as early as possible if they are in scope — insert payloads into every field you see
- Create your own fuzzing lists tailored to the target's technology stack
- Expand this checklist with your own findings as you go
- Consider VDP (Vulnerability Disclosure Programs) over paid programs if you want less competition
- PoC or GTFO — always have a working proof of concept before reporting
- Prove impact clearly in your report; a bug with no demonstrated impact is often dismissed

--------

## Reconnaissance & Hidden Endpoints

*Tips*
- Read the documentation. If there is an API, there are likely API docs — search Google for them (e.g., `site:target.com api docs`)
- If a mobile app is not in scope, the backend it communicates with might be — think outside the scope boundaries
- Use GAU (GetAllURLs) or `waybackurls` to find historical endpoints and JavaScript files
- Look in application settings for modules that are disabled by default — every extra feature is a potential attack surface fewer hunters have seen
- If there is a paywall, consider investing in access — the more you can access, the better your coverage
- Use Google Dorks: `site:target.com filetype:js`, `site:target.com inurl:api`, `site:target.com "internal use only"`
- Look for backup files: `.bak`, `.old`, `.zip`, `.tar.gz` on known file paths
- Check JavaScript files for hardcoded endpoints, API keys, and tokens
- Look for admin panels: `/admin`, `/administrator`, `/manage`, `/dashboard`, `/cp`
- Use directory brute-forcing tools (gobuster, feroxbuster, ffuf) with a solid wordlist

--------

## Session Management

*Tips*
- Create an account for every role in the application and test whether each role can directly access pages or actions it should not
- Remove a role from a user and verify the server enforces the change immediately (not just on next login)
- Inspect the session token: does it change after login? If not, it may be vulnerable to session fixation
- Delete a logged-in user's account and check whether the active session still works — the session should be invalidated server-side
- Check if the session token is present in the URL (GET parameter) — it should only be in cookies
- Verify that logout actually invalidates the session token on the server, not just in the browser
- Check that session tokens are long, random, and unpredictable (not sequential or time-based)
- Look for a hard session timeout — sessions should expire after a period of inactivity

--------

## Cookies

*Tips*
- Is the `HttpOnly` flag set on session cookies? Without it, XSS can steal the cookie via JavaScript
- Is the `Secure` flag set? Without it, the cookie can be sent over unencrypted HTTP
- Is the `SameSite` attribute set to `Strict` or `Lax`? Without it, CSRF may be easier to exploit
- Is the cookie domain scoped correctly? A wildcard domain (`.example.com`) allows subdomains to access the cookie
- Is the cookie path scoped correctly? An overly broad path allows more of the site to read the cookie
- Does the cookie have an appropriate expiry? Persistent cookies should not last forever
- Is the cookie value reflected in a URL GET parameter anywhere? That is a sensitive data leak
- Try writing a cookie to a subpath — if the domain is not validated, the cookie may be appended to requests to other paths

--------

## Authentication & Login

*Tips*
- Test for username enumeration: does the application return a different response for valid vs. invalid usernames?
- Check for weak lockout policies — can you brute-force login without being blocked?
- Test default credentials on admin panels and login pages
- Check if credentials are sent over HTTP (not HTTPS)
- Test the password reset flow:
    - Can you add a second email parameter to redirect the reset token to an attacker-controlled address?
    - Are reset tokens sent over HTTP?
    - Are reset tokens weak, short, or predictable?
    - Is the user forced to re-authenticate after a password reset?
- Are there alternative login methods (OAuth, magic links, mobile login) that may have weaker security?
- Test JWT tokens if present:
    - Try the `alg: none` signing algorithm
    - Check for weak HMAC keys (try cracking offline)
    - Test for HMAC vs. RSA algorithm confusion
- Verify that the session token changes after a successful login (prevents session fixation)

--------

## SQL Injection

*Tips*
- Test every input that gets passed to the database: URL parameters, POST body fields, HTTP headers (User-Agent, Referer, X-Forwarded-For), and cookies
- Start with a simple `'` (single quote) and observe whether the application throws an error or behaves differently
- Test for time-based blind SQLi using payloads like `' AND SLEEP(5)--` to confirm injection without visible output
- Use `sqlmap` to automate detection and exploitation once you suspect an injection point
- Test for second-order SQLi — data stored in the database may be used unsafely in a later query
- Check for NoSQL injection if the application uses MongoDB, CouchDB, or similar: try `{"$gt":""}` in JSON parameters
- Look for SQLi in search fields, login forms, order/sort parameters, and filter dropdowns

--------

## Cross-Site Scripting (XSS)

### Stored XSS

*Tips*
- For every input field, try to get a basic HTML tag stored: `<a href=#>test</a>`
- If the tag is rendered, try a simple script tag: `<script>alert(1)</script>`
- If basic tags are filtered, try obfuscated variants (see XSS Filter Evasion section)
- If anything gets through, dig deeper and escalate to a meaningful payload
- Check user profile fields, comments, product reviews, filenames, and anywhere user-supplied data is displayed to other users

*Videos*
- https://www.youtube.com/watch?v=uHy1x1NkwRU

--------

### Reflected XSS

*Tips*
- Check error pages (404, 403, 500) — they sometimes reflect URL parameters or request paths directly
    - Trigger a 403 by trying to access the `.htaccess` file
- Try every URL parameter and search query for reflection — even if the value appears in a JavaScript context
- Check the HTTP Referer header — some applications reflect it in the response

*Videos*
- https://www.youtube.com/watch?v=wuyAY3vvd9s
- https://www.youtube.com/watch?v=GsyOuQBG2yM
- https://www.youtube.com/watch?v=5L_14F-uNGk
- https://www.youtube.com/watch?v=N3HfF6_3k94

--------

### DOM XSS

*Tips*
- DOM XSS occurs entirely in the browser — the payload never hits the server, so server-side scanning will miss it
- Burp Suite PRO's scanner can detect DOM XSS automatically
- Manually look for dangerous JavaScript sinks: `document.write()`, `innerHTML`, `eval()`, `location.href`, `setTimeout()` with user-controlled input
- Tool: https://github.com/dpnishant/ra2-dom-xss-scanner

*Videos*
- https://www.youtube.com/watch?v=gBqzzhgHoYg
- https://www.youtube.com/watch?v=WclmtS8Ftc4

--------

### Blind XSS

*Tips*
- Use XSS Hunter (xsshunter.com) to receive out-of-band callbacks when your payloads fire in admin panels or backend systems
- Start injecting blind XSS payloads early — they may fire hours or days later
- Copy every payload from your XSS Hunter payloads section and insert it into every input field you encounter
- XSS Hunter provides a payload that also attempts CSP bypasses
- Generate variations of your payloads — for example, replace `<` with `&lt;` or use different event handlers

--------

### XSS Filter Evasion

*Tips*
- `<` and `>` can be replaced with HTML entities `&lt;` and `&gt;` to bypass naive filters
- Try an XSS polyglot that works across multiple contexts:
    - `` javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'> ``
    - https://gist.github.com/michenriksen/d729cd67736d750b3551876bbedbe626
- Try case variations: `<ScRiPt>`, `<SCRIPT>`, mixed case event handlers
- Try breaking up keywords: `<scr<script>ipt>alert(1)</scr</script>ipt>`
- Try encoding: URL encoding (`%3Cscript%3E`), double URL encoding, Unicode encoding
- If inside an HTML attribute, try breaking out: `" onmouseover="alert(1)` or `' autofocus onfocus='alert(1)`
- If inside a JavaScript string, try: `'; alert(1)//` or `\'; alert(1)//`

--------

## Server-Side Template Injection (SSTI)

*Tips*
- Inject `{{7*7}}` into every input field — if the application returns `49`, SSTI is confirmed (Jinja2/Twig)
- Try `}}{{7*7}}` and `}}[[7*7]]` to break out of existing template syntax
- Try `${7*7}` for FreeMarker, Velocity, or JavaScript template engines
- Try `<%= 7*7 %>` for ERB (Ruby) templates
- Once confirmed, use a tool like tplmap to automate exploitation
- SSTI can lead to Remote Code Execution (RCE) — escalate carefully and responsibly

*Videos*
- https://www.youtube.com/watch?v=iQ6FuL-DgX8
- https://www.youtube.com/watch?v=i8cvh0u-VXE

--------

## Command Injection

*Tips*
- Create a dedicated fuzzing list for command injection (see videos below for guidance)
- Include blind command injection payloads such as `; sleep 5` and `| ping -c 5 attacker.com` — these confirm injection without visible output
- Include both Linux and Windows command variants in your fuzzing list
- Test parameters that look like they interact with the OS: file names, IP addresses, hostnames, shell options
- Chain commands using: `;`, `&&`, `||`, `|`, backticks (`` ` ``), `$()`
- Use out-of-band techniques (Burp Collaborator, interactsh) to detect blind injection

*Videos*
- https://youtu.be/GZyoEXdezZM
- https://youtu.be/B-aVRsaQTgo

--------

## CSRF (Cross-Site Request Forgery)

*Tips*
- Check if a CSRF token is present on sensitive state-changing requests (password change, email change, account deletion)
- Check if the token changes with every request — a static token is a weaker protection
- Test whether the server still accepts the request if you submit a random/wrong CSRF token
- Test whether the server accepts the request with the CSRF token parameter removed entirely
- Check the `SameSite` cookie attribute — if it is `None` or absent, CSRF may be easier
- CSRF on login and logout pages is generally out of scope for most programs — focus on authenticated, sensitive actions

*Videos*
- https://www.youtube.com/watch?v=ImqLlFMQrwQ

--------

## IDOR / Broken Access Control

*Tips*
- Try accessing objects (user profiles, orders, documents, messages) that belong to another user at the same privilege level — replace numeric IDs, GUIDs, and usernames in requests
- Try accessing objects that require a higher privilege level than your account has (horizontal → vertical escalation)
- Try accessing objects that belong to a completely different tenant/client in a multi-tenant application
- Test API endpoints directly — the UI may hide options that the API still accepts
- In Europe, accessing another user's personally identifiable information (PII) is a GDPR issue and can significantly increase bug severity
- Test IDOR in indirect object references too: file paths, email addresses, order numbers, invoice numbers

*Videos*
- https://www.youtube.com/watch?v=hZ0xSRswN8M
- https://www.youtube.com/watch?v=mjrGOuFc1Kw
- https://www.youtube.com/watch?v=5vYhTik8_yU
- https://www.youtube.com/watch?v=HQUxXE1oaIE

--------

## LFI / RFI (Local/Remote File Inclusion)

*Tips*
- If a file or image is loaded via a parameter (e.g., `file=test.jpg`, `page=home`, `template=login`), test for LFI
- Classic LFI payload: `../../../../etc/passwd` (repeat `../` until you reach the root)
- On Windows targets try: `..\..\..\windows\win.ini`
- Try null byte injection to truncate file extensions: `../../../../etc/passwd%00` (older PHP versions)
- Try PHP wrappers: `php://filter/convert.base64-encode/resource=/etc/passwd` to read source code
- For RFI: keep a VPS ready with a simple HTTP server hosting a test file — include your server's URL in the parameter
- RFI requires `allow_url_include=On` in PHP — less common but still worth checking

--------

## File Upload Vulnerabilities

*Tips*
- Try uploading a file with a dangerous extension: `.php`, `.php5`, `.phtml`, `.asp`, `.aspx`, `.jsp`
- If the server restricts by file extension, try:
    - Changing the MIME type in the Content-Type header to `image/jpeg` while keeping the dangerous extension
    - Using a double extension: `shell.php.jpg`
    - Using null bytes: `shell.php%00.jpg` (older PHP versions)
    - Using alternative extensions: `.php5`, `.phtml`, `.phar`, `.shtml`
- If the server restricts by MIME type, try uploading a polyglot file (a valid image that also contains PHP/JS code)
- Check where uploaded files are stored — if they are served from a web-accessible directory, a web shell can be executed
- Try uploading an SVG file with embedded JavaScript or XXE payloads
- Try uploading a DOCX or XLSX file with XXE payloads embedded in its XML content

--------

## XXE (XML External Entity)

*Tips*
- Test every XML input for XXE — look for XML in request bodies, SOAP endpoints, and file uploads
- For every document upload (DOCX, XLSX, ODT), try uploading a crafted file containing an XXE payload — these formats are ZIP archives containing XML files
- For every picture upload field, try uploading an SVG file — SVG is XML-based and can carry XXE payloads
- Basic XXE payload to read local files:
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <root>&xxe;</root>
    ```
- If direct output is blocked, try blind XXE with an out-of-band callback to Burp Collaborator or interactsh

*Videos*
- https://www.youtube.com/watch?v=AQUHzyzZXeA
- https://www.youtube.com/watch?v=unS3xGZj8xk
- https://www.youtube.com/watch?v=EwsW2WfUTmQ

--------

## SSRF (Server-Side Request Forgery)

*Tips*
- Look for parameters that accept a URL or hostname: `url=`, `webhook=`, `redirect=`, `src=`, `dest=`, `feed=`, `load=`
- Try pointing the parameter to your Burp Collaborator or interactsh URL to detect blind SSRF
- Try internal IP ranges to access services not exposed to the internet:
    - `http://127.0.0.1/admin`
    - `http://169.254.169.254/latest/meta-data/` (AWS metadata endpoint)
    - `http://192.168.0.1/`
- Try different protocols: `file://`, `dict://`, `gopher://`, `ftp://`
- If the target uses cloud infrastructure, SSRF against the metadata endpoint can leak credentials and lead to full account compromise
- Use URL encoding, IPv6 notation (`http://[::1]/`), and decimal IP notation (`http://2130706433/`) to bypass naive SSRF filters

*Videos*
- https://youtu.be/UpzXZcfYNNc
- https://youtu.be/unS3xGZj8xk

--------

## Open Redirects

*Tips*
- Look for parameters that control redirection: `redirect=`, `url=`, `next=`, `return=`, `returnTo=`, `goto=`, `target=`
- Test with an external URL: `redirect=https://evil.com`
- Try bypasses if the server validates the domain:
    - Use `@`: `https://target.com@evil.com`
    - Use `//`: `//evil.com`
    - Use a subdomain of the target as a prefix: `https://target.com.evil.com`
    - URL encode the payload: `redirect=https%3A%2F%2Fevil.com`
- Open redirects can be chained with OAuth flows to steal authorization codes, or combined with phishing attacks
- Open redirects are generally low severity on their own — demonstrate a realistic chain for higher impact

--------

## HTTP Security Headers

*Tips*
- Check for the presence and correct configuration of the following security headers:
    - `Content-Security-Policy` (CSP) — prevents XSS; check for `unsafe-inline`, `unsafe-eval`, or wildcard sources
    - `X-Frame-Options` — prevents clickjacking; should be `DENY` or `SAMEORIGIN`
    - `Strict-Transport-Security` (HSTS) — enforces HTTPS; check for `includeSubDomains` and `preload`
    - `X-Content-Type-Options` — should be `nosniff` to prevent MIME sniffing
    - `Referrer-Policy` — controls how much referrer info is sent
    - `Permissions-Policy` — restricts browser features (camera, microphone, geolocation)
- Check that sensitive pages do not allow caching: `Cache-Control: no-store`
- A weak or missing CSP combined with a stored XSS is a great chain for a higher-severity finding

--------

## Chaining Vulnerabilities

### Chaining XSS

*Tips*
- Use XSS to steal a non-HttpOnly session cookie via `document.cookie` — combine with a session that never rotates for a persistent account takeover
- Use XSS to overwrite a cookie on a different path, then use that cookie in a CSRF attack
- Combine a session that never changes with XSS to steal the cookie for a permanent account takeover (significantly increases severity)
- Use XSS to exfiltrate PII displayed on the page — this creates a GDPR issue and raises severity
- Use XSS to perform actions on behalf of the victim user (CSRF-like impact, but bypasses CSRF tokens)
- Use XSS to redirect the victim to a phishing page or download a malicious file

*Videos*
- https://www.youtube.com/watch?v=5vYhTik8_yU
- https://www.youtube.com/watch?v=unS3xGZj8xk

--------

### Chaining CSRF

*Tips*
- Use a CSRF to trick a victim into storing a Stored XSS payload on their own page, which then affects other users who view it
- Chain CSRF with an open redirect to bypass `SameSite=Lax` restrictions in some browsers
- Use CSRF to change a victim's email address, then trigger a password reset to that new address (account takeover chain)

--------

### Chaining IDOR

*Tips*
- When programs use UUIDs as object identifiers and you find an IDOR, the impact may initially seem low because UUIDs are hard to guess — look for a separate endpoint that lists or exposes these UUIDs to elevate the severity
- Chain IDOR with a privilege escalation: use a low-privilege IDOR to read an admin's user ID, then attempt to perform admin actions using that ID
- Chain IDOR with information disclosure: first enumerate all user IDs via a leaky endpoint, then access each user's sensitive data
