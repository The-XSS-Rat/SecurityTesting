# 6. Security Misconfiguration

# Introduction

I believe this name was chosen to be as ambigious as possible. It can encompass anything and everything related to configurations but if we do some effort it is possible to define a general testing guide for security misconfigurations by looking at the common properties of all the vulnerabilities we can find in writeups and hacktivities. 

# Is my target vulnerable?

The following properties of a system will indicate a likely vulnerability though some of these properties are a bit more ambigious and harder to test. 

- Missing appropriate security hardening across any part of the application stack. Most applications these days consists of complete technical solutions and issues might arise in any of these components. To test for this properly we need to have a good overview of our system under test though.
- When our target uses cloud services, they need to make sure to configure the authentication and authorisation on those properly as well.
- If features are enabled that are not being used this can lead to some serious security impact in certain cases. An example we can think of is leaving a port open that is not needed while having vulnerable software running on there.
- Some admins are very lazy and they might leave passwords default or super easy to guess like test/test. This is also a security misconfiguration of course.
- Our target needs to keep it's systems and dependencies up to date. Besides keeping them up-to-date we need to make sure these components are enabled and configured properly.
- If any of the settings surrounding security is set to an insecure value.
- The server does not send security headers or directives or they are not set to secure values

To prevent these kinds of vulnerabilities, we can implement some mitigations. 

## Mitigations

- Automated systems need to be in place to easily deploy a new testing enviornment that is identical to the PRD enviornement in regards to security and configuration.
- The DTAP (Development, testing, acceptance and production) enviornments should ideally be identical with different credentials used in each enviornment.
- We need to have the minimum amount of functionality possible enabled. If we don't strictly need a component for our application, we should disable those components. This includes shadow-api's which are api's that are online but which nobody knows they exist off.
- We need to implement a process to do a periodic security review that focusses on cloud storage strategies (i. e. s3 buckets)
- A good seperation of components with attention to seperating tenants if they use the same hardware.
- Every components needs to have a very well defined security profile
- Our applications should always send security directives like headers
- We should automate the verification of our security settings as much as possible so we can pick up on issues before they make it to the production enviornment. Static code reviews can also help.

# What are we hunting for?

All of these best practices serve to cover a particular goal but we also need to know what these goals are so we can test with precision. 

- Cloud storage misconfigurations
- Test network infrastructure configuration
- Test Application Platform Configuration
- Testing alternative HTTP methods
- Test HTTP Strict Transport Security

## Test network infrastructure configuration

This can be anything from an exposed admin panel to known server vulnerabilities. Pretty much any attack that can be performed over the network and relies on configuration can be put into this category. 

## Cloud storage misconfigurations

Companies often use services like S3 buckets from amazon without properly understanding them. This might lead to misconfigurations happening which could allow things like unauthenticated access. 

## Testing alternative HTTP methods

Just like we already talked about in chapter 5 (Broken access control), we can use the OPTIONS http method to find out which http methods we are able to execute and sometimes this might concern http methods which are not fully implemeted on the server. 

## Test HTTP Strict Transport Security

This is not interesting at all for bug bounty hunters but pentesters should reports this as a best practice. A website should always force the user onto the https version of the website. 

# So how do we hunt for this?

Hunting for security misconfigurations requires some special conditions because you need to either have a confirmeable guess at a certain configuration or have access to how a system works by for example looking at it's source code on github. You will also need to confirm these findings though since an unconfirmed vulnerability isn't really one at all. 

We can start by doing some google dorking and looking for conf file or yaml or xml or anything related to configurations. 

```xml
filtype:cfg or filetype:yml or filetype:xml or intitle:"Config" or ...
```

besides google dorking we can do the exact same thing for github where we might have some more luck as usually developers will mask things like passwords by putting them into environment variables but they leave all the other settings in plain sight. 

whenever you come across a configuration file it is up to you to find out exactly what every setting is for and if that setting can be unsafe by simply googling around and even just reading the manuals of the components for which those config files serve.