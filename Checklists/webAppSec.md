# Information gathering

- Search engine recon
    - Google dorking/yahoo dorking/...
        - Site:target.com -www -xxx...
        - We work exclusively, not inclusively. This means we start at the base site:target.com and exclude results we viewed. This ensures we don't miss things. We ALSO work inclusively, but it's only after working exclusively
- Webserver fingerprint
- Source code investigations
- Asset discovery
- User emulation ( Keep MiTM proxy open for site map population )
- Endpoint discovery
- Enumerate any admin interfaces
- Enumeration of errors and stack traces
- Repository recon
    - github dorking
- Fingerprint the application
- Map the application architecture
- Map out integration points
- Find
    - Data flows
    - Paths
    - Race's

# Exploits

## Login system

- Test the JWT token
    - Signature Verification
        - The none signing algorithm sometimes is accepted
        - Weak HMAC Keys
        - HMAC vs Public Key Confusion
        - [https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing_JSON_Web_Tokens](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing_JSON_Web_Tokens)
- Login bypass
    - Directory brute force
    - SQLi
    - Session ID prediction
- Username enumeration
- Credentials transported over HTTP
- Default credentials
- Issues in the registration process
    - Tokens sent over plaintext?
    - DoS by entering too many characters
    - Register a user with XSS attack vector in every input field, use for further testing
- Weak password systems
- Test password reset systems
    - Add second email parameter with email of attacker
    - Any tokens sent over HTTP
    - Weak predictable tokens
    - Is the user forced to reauthenticate
- SessionID in URL
- Logout should invalidate session tokens
- Validate that a hard session timeout exists.
- Weak lockout
- Is there any alternative login system
    - Oauth
    - Mobile login
    - Token login with weak tokens
- Testing for session puzzling
    - [https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/08-Testing_for_Session_Puzzling](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/08-Testing_for_Session_Puzzling)
- Session hijacking
    - Request from attackers website to victims bank for example to login. The bank will possibly return session vars if bad config. This leads to attackers owning session vars now.
    - [https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/09-Testing_for_Session_Hijacking](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/09-Testing_for_Session_Hijacking)

## Input validation

- XSS
    - Reflected XSS
    - Stored XSS
    - Blind XSS
    - DOM XSS
- SQLi
- XXE
- Command injection
- SSTI/CSTI
    - Insert ${7*7} into every field you see, if it resolves, investigate further
- SSRF
    - Add burp collaborator URL in everywhere that URL resolves
- HTTP parameter polution
    - [https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/04-Testing_for_HTTP_Parameter_Pollution)
- LDAP injection
- SSI (server side includes injection)
- XPath injection
- Clickjacking
- GraphQL testing

## General exploits

- RFI/LFI
- Insecure session management
- Subdomain takeover
- Check if user role is user controllable (Can you make yourself admin)
- Test the cookies attributes
    - Sensitive cookies should have secure and httponly flag
    - Domain and path need to be set right
    - Expires in timely manner
    - SameSite Attribute
- CSRF testing
    - Only on sensitive functions, not on login/logout
- File upload testing
    - Uploading of malicious content
    - File upload restrictions
        - Changing mimetype
        - Using nullbytes
- Test integration points for overextended priviledges
- Test if the browser caches sensitive information
    - Use the back button after logout timer
    - Click around after login timer
    - Check cache headers on sensitive pages
- There should not be any weak encryption used anywhere
    - Search for the following keywords to identify use of weak algorithms: MD4, MD5, RC4, RC2, DES, Blowfish, SHA-1, ECB

## Business logic flaws

- Data validation
    - example may be if I use my credit card at multiple locations very quickly it may be possible to exceed my limit if the systems are basing decisions on last night’s data.
    - Identify data injection points.
    - Validate that all checks are occurring on the back end and can’t be bypassed.
    - Attempt to break the format of the expected data and analyze how the application is handling it.
- Test for hidden parameters that you can change with impact.
    - For example changing account type from consumer to business
- Check for things that are only hidden in the front-end
- Check for disabled fields that are only front-end disabled
- Integrity checks
    - Review the project documentation for components of the system that move, store, or handle data.
    - Determine what type of data is logically acceptable by the component and what types the system should guard against.
    - Determine who should be allowed to modify or read that data in each component.
    - Attempt to insert, update, or delete data values used by each component that should not be allowed per the business logic workflow.
- Test functions that can only be used a limited amount of times
    - For example a coupon code that you should only be applying one time but that's just a front-end check
- If something gets added to account and should be withdrawn again, check if it is.
    - For example if you order an item but cancel the order, your loyatee points should go down as well.
