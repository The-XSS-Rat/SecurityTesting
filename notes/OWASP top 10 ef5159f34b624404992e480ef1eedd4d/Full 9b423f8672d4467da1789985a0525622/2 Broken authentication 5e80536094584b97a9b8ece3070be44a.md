# 2. Broken authentication

# Introduction

The OWASP Definition of broken authentication goes very deep and while this is not usually a problem for pentesters as they are required to pretty much report anything and let the customer decide what course of action to take. If we talk about bug bounty hunting though, these vulnerabilties are all useful to us as well, but maybe not immediately.

What OWASP means with broken authentication might differ from the definition most people have in their heads so let's dive a bit deeper into what they actually mean. OWASP is basically talking about bad session management. It seems mostly about invalid session validation. Normally i would think of things like broken access control but these are classified under chapter 5 in their own chapter.

# Attack types

## Credential stuffing and weak passwords

When an attack has a list of passwords and usernames, the attacker might be able to try to them all due to the server permitting automated attacks. This is called credential stuffing and the server should prevent this by enabling captcha's after several failed login attempts.

Permitting of brute forcing or automated scripts is a security flaw and it might not get accepted in bug bounties but as pentesters we do need to report them and classify their severity properly.

We should also never be able to register with weak passwords like "admin/admin" or "Password1". This will make it easier to brute force the password of a lazy employee that did not want to create a proper password.

## Password recovery options

What can also happen is that our target uses weak password recovery options like knowledge based recovery. This is when the server asks you to set several security questions and answers to them. The problem with this system is that people often set and forget these questions. This allows an attacker to find out that question and simply ask the victim in a nonchallant conversation. If the victim forgot they had a security question asking for the name of their first dog, and attacker can start a conversation about pets and get to know the answer pretty easily.

A good way to solve this password recovery issues is to rely on secondary backup options like a backup email adress or phone number. This would increase the difficulty for the attacker as they would have to hack the secondary email adres or even phone of the victim.

## Weak or no encryption of passwords

Another fun thing i like to talk about is weak password encryption. Some beginning programmers don't know the sensitivity of a password and how bad it can be if they are leaked as these days people seem to use the same password for everything.

A fun example of this is a website i was testing where i clicked "forgot password", i filled in my email adres and i saw the email come in. The only problem was that they were able to me my password in plain text! Normal hashing can not be reversed easily, which is why most passwords are hashed and salted when entered into a database. If an application does not do this, that is a very bad sign. I would turn around and run as fast as you can. The big problem with this defect is that is really hard to notice. If the application does not treat your password correctly, normally you would never know this as you can not have access to the database. 

## Multi-factor authentication

We can also have a look at multi-factor authentication. If it's missing, as a pentester we can definitly reports this as a best practice. If however it is provided, we have to check if it works correctly. We can see if we can still make requests that require MFA (multi factor authentication) without entering the MFA parameter. We can leave it empty, change it to a random value or even remove the parameter completly. We need to try this on all the requests that require MFA and if any of them still works after messing with the parameter, we have a vulnerability on our hands. It's going to be somewhat lower in severity though since it does require the account under attack to already be compromised.

## Passing me that SessionID

It can happen at times that companies have two applications and sometimes you log into one and need to switch to the other. There are several ways to handle authentication when it comes to this scenario and the least safe way is to send the session ID as a GET parameter. Under normal situations, this is not going to pose much of a threat as the URL gets encrypted when using HTTPS traffic. However in case of using regular HTTP traffic or if the attacker was able to perform a MiTM (Man in the middle) attack, the account can get compromised in this way. As a pentester we can definitly report this as a best practice again but as bug bounty hunters, this issue will not be accepted due to the requirements of having a MiTM attack. 

## Sessions

We also need to talk a little bit about how sessions are handled by servers. Sometimes a developer will configure their session handling wrong which can lead to any of the following scenario's:

- Sessions might not get invalidated after logging out which means that if an attacker is able grab the sessionID (For example by stealing it with XSS), the attacker is able to keep using the sessionID to log into the account without it invalidating. This is something bug bounty hunters should keep in mind but not report, pentesters on the other hand should report this. For bug bounty hunters this would elevate the severity of bugs like account takeover.
- Sessions not invalidating soon enough, this means almost the same as the previous example but the difference is that we don't have an eternal account takeover but a limited one, though still way too long. The session should invalidate the moment the user logs out and ideally sometimes during the session, where there is a call in the background after a while to the authentication server for a new sessionID. This is something bug bounty hunters should keep in mind but not report, pentesters on the other hand should report this. For bug bounty hunters this would elevate the severity of bugs like account takeover.
- SessionID's being too predicteable, we have certain techniques to find out how random a sample of sessionID's really is and if they are not random enough, we can guess the sessionID's. This is worthy of a report for bug bounties and for sure from pentesters.
- SessionID's not being invalidated after a period of inactivity, see the first bullet point for the severity and reporting guidelines.

# Defense mechanisms

There are several general tips we can give so you can skip the next chapter if you wish but i recommend you read through it as it contains some edge cases that you might not have thought of. 

- Wherever possible, implement multi-factor authentication and implement it well. As attackers it's our job to test if MFA is implemented in a correct manner every single time it occurs.
- Change any default password and never use weak credentials like admin/admin or test/test
- You should make sure the users can not enter a weak password. While enforcing these rules, keep in mind that it is much more secure to have a very long passphrase than to have a short password with strange characters. Some applications do not even allow you to enter a long passphrase which is shocking. If your application allows you to create a password like "test" you should definitly report it as a pentester but not really as a bug bounty hunter as it's a best practice. A full guide on recommended password requirements can be found at [https://pages.nist.gov/800-63-3/sp800-63b.html#memsecret](https://pages.nist.gov/800-63-3/sp800-63b.html#memsecret)
- Make sure that you never give a specific error message and that the message is the same for all outcomes. For example if you login and the username is correct but the password is not, your error message should never mention this and instead be something like "Your usersname/password was incorrect". If you give a unique response, it can lead to attackers enumerating usernames. For bug bounty hunters this is usually listed in the out of scope section while for pentesting this can be reported as a best practice.
- When an attacker fails to login, you should limit their login attempts by either implementing captcha and/or time limits by for example not allowing any more login attempts for 10 minutes after 5 failed attempts. A good practice is also to require a password change if several failed attempts have happened when the victim logs in the next time to kick off any possible invaders. As a bug bounty hunter this is not something you should report but as a pentester this can be suggested as a best practice again.
- You should implement a secure, server side session manager and make sure that the session ID's are random enough. As a bug bounty hunter this can be an area of interest since a compromise in this section would directly be of high impact. As a pentester this usually defects in this area can usually be reported as high-critical. Sometimes they are of low severity though, so judge each defect carefully.
- Make sure you invalidate you sessions after both logout and a period of inactivity. As a bug bounty hunter this can be interesting to keep in mind but it's not something i would report as most programs won't accept this best practice. As a pentester i would report this as a best practice.

## General

In general we should never allow accounts that can perform impactful or sensitive actions like administrators to log in via front-end systems. This will prevent an attacker from brute forcing the account but it is a best practice so this is generally only useful for pentesters. On that note, a developer should also make sure the back-end (internal) and front-end (external) login systems are not the same and that they use different authentication mechanisms.

When we talk about authentication it is super important we never give detailed error messages and we have to make sure that we always provide the same error message. For example if a user does not provide the correct password but does have an existing username, we should not inform them the password was incorrect but just inform them the password or username is incorrect. This keeps them guessing as to what account names are valid. 

## Password mechanisms

As for passwords you should require a minimum of 8 characters but a passphrase is by far the safest option as it will take a long time to brute force this. Knowing this, we should allow the user to enter at least 64 characters and allow them to use alphanumeric but also require 1 special character to make it even harder to brute force those passwords. It is really important to set a maximum password length as otherwise bug bounty hunters and pentesters alike might be able to launch an application level DoS attack by overfilling your database server with extermely long passwords.

To make the passwords extra secure, you can require the user to switch passwords every so often, it is important to not do this too often however as it might annoy the users and work adversely and the user might enter a weak password to remember it better. 

If you have a sensitive feature such as changing the email adres or confirming a buy action, it is generally a best practice to ask the user for their password again. This would stop any attacker who wants to execute sensitive functions on an account that someone left logged in when they left their computer unattended.

### Password recovery mechanisms

It is very important to implement proper password recovery mechanisms as we've already discussed before. A simple recovery questions mechanisms is usually not sufficient as user often do not remember their own security questions and can thus be easily manipulated into revealing the answers to those questions. Ideally a back phone or e-mail adres is set so that the user can recover their passwords from there and if they do not have access to their backup accounts it would be a good idea to require they contact customer support.

### Storing our passwords.

We need to make sure that we store our users password securely, they put a huge amount of trust in us and we have to make sure to fill in the customers expectations. We should store their passwords in a secure fashion which can only executed one way, meaning we should not be able to decrypt the password once it has been encrypted. To later on check the passwords, you need to make encrypt the password the user provides and check that encrypted password with the one you have stored in the database. 

This often happens by hashing the passwords, however if we hash something, we always get the same value for hasing the same thing. This means that hackers can build what's called rainbow tables. These tables will contain a list of passwords and their hashed values. To combat this, companies can add a "salt" to your password. This is basically a random string that the developers store in the database along the hashed password. They will add this value to your password whenever they encrypt it to make sure the password can not easily be found in a rainbow table. 

Some general tips from OWASP to make sure the password:

- Has a maximum input length, to protect against denial of service attacks with very long inputs.
- Explicitly sets the type of both variable, to protect against type confusion attacks such as [Magic Hashes](https://www.whitehatsec.com/blog/magic-hashes/) in PHP.
- Returns in constant time, to protect against timing attacks.

# TLS

For security reasons it's very important to always transport any traffic over HTTPS/TLS. This will prevent an attacker from analysing the traffic between your web application and the victim if they should ever be able execute a MiTM attack. This is also becoming much more likely in recent times due to a lot of coffeeshops popping up with free wifi that is not very secure.

# Protection against automated attacks

It is really important to implement a few security measures that will foil a very big part of the automated scripts that exist out there. 

- We need to limit the amount of requests a user can make. For example if they make more than 2 requests per second at any time they can be put in a timeout or if they make a certain amount of requests, they can also be ip banned if the defensive mechanisms have to be extreme.
- We need to implement multi-factor authentication properly everywhere that a password is required. This will increase the complexity of the application but also the security.
- If a user attempts to login too often with an incorrect password, the account might not be able to login from that specific ip adress or at all but be careful because if you disable the account from logging in, you need to make sure the account name is never disclosed. If someone knows the account name of the victim, they can keep disabling the victims account effectively locking them out forever.
- We can implement a captcha mechanism that either triggers directly or after a few failed login attempts, this will make it a lot harder for scripts to auto test passwords

# Keeping track of the attack

It is very important that we log and investigate every failed login attempt. Some will just be honest mistakes by the owner of the account but some might be attacks that might have to lead to certain measures being taken against the attackers. 

# Passwords on a post-it are so 2015

All jokes aside, after using a secure password, you might find it's both hard to remember all of the passwords and to keep track of all the software that requires a password as you should always use a different password per application. To combat this you can use a password manager. Password managers can store and generate passwords and it's well worth investing in a password manager as it will help you manager the heap of password immensely

# Other authentication mechanisms

Depending on the implementation of the authentication types such as oAuth, SAML or LDAP we can have several other security flaws. To combat those it is highly recommended to fully read the documentation as it will often contain sections on security issues that might arise but it's better to invest in an expert to investigate your security mechanisms as this is not something you want to get wrong. This can be done by either hiring a pentester or entering a bug bounty program.