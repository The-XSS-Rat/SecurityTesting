## Table of contents
- [Burp collaborator alternatives](#burp-collaborator-alternatives)
- [I found website uses vulnerable version of JQuery, how do i exploit?](#i-found-website-uses-vulnerable-version-of-jquery-how-do-i-exploit)
- [I found a CSRF issue on the login/logout/change password/change email/...](#i-found-a-csrf-issue-on-the-loginlogoutchange-passwordchange-email)
- [How you find original IP and bypass the waf for port scanning ?](#how-you-find-original-ip-and-bypass-the-waf-for-port-scanning-)
- [FAQ how do i 403 bypass?](#faq-how-do-i-403-bypass)
- [why-test-for-idor-and-bac-by-replacing-the-jwt-token](#why-test-for-idor-and-bac-by-replacing-the-jwt-token)
- [i found key x while hunting, is it valid?](#i-found-key-x-while-hunting-is-it-valid)

-----

## Burp collaborator alternatives
- [Interactsh](https://t.co/nqFoFQxa8W?amp=1)
- [webhook.site](https://webhook.site)
- [Request bin](https://requestbin.com/)
- [DNSBin](https://github.com/ettic-team/dnsbin)

## I found website uses vulnerable version of JQuery, how do i exploit?

Great question!! 
- Understand what function is vulnerable in Jquery
- Developers have to use THAT function in user controlleable way
- Execute vulnerable function ENSURE developers did not apply filter

## I found a CSRF issue on the login/logout/change password/change email/... 

there is no CSRF token on the password reset/change password/login/logout

Don't look for CSRF on functionality that needs any form of control over the users account.
Pass change = you need current pass
pass reset = you need token from the email adress of the victim unless you can get the server to send the token to you but you don't need CSRF then.
Email change = pass required
login/logout = why even?  
 
Impact only :)<3

## How you find original IP and bypass the waf for port scanning ?
Cloudflare: https://blog.detectify.com/2019/07/31/bypassing-cloudflare-waf-with-the-origin-server-ip-address/

## FAQ how do i 403 bypass? 
https://github.com/Dheerajmadhukar/4-ZERO-3 !! <3 this is amazing!!

## Why test for IDOR and BAC by replacing the JWT token?
You can not automated replacing the object ID's because on one project it will be userID and on the other the same variable will named accountID. Object ID name's often differ from project to project, JWT does not.

I can show you the exact same impact from replacing the JWT by replacing the objectID and leaving the JWT alone BUTTTT

- You might be changing random people's data
- You might be testing in a production environment

Note: If you use automation, you can only delete an object ones

## i found key x while hunting, is it valid? 
[Check out this keyhacks repo](https://github.com/streaak/keyhacks)
