# 3. Sensitive data exposure

# Introduction

I feel like a lot of mystery surrounds this topic. A lot of people seem to wonder which data is sensitive when exposed. Some people seem to think every single API key disclosed in a JS file is a vulnerability but ofcourse this is not the case! Some API keys are supposed to be used by XHR requests and they are supposed to be public. When it comes to information disclosers we always have to keep in mind that what we see should be private and even then it's not guaranteed to be a vulnerability. Depending on which viewpoint you take (Pentesters or Bug Bounty Hunters) you should be less or more careful with what you report. We will go much deeper into this when we talk what to report and what not to report. 

In this article we will talk about kinds of information disclosure going from debug information to admin passwords.

# How does it occur

There are several places we can go looking for sensitive information. let's start by listing all the ways sensitive data exposure can occur.

- A post-it on the monitor with a password. This one is pretty obvious.
- Debug information is very useful for both pentesters and bug bounty hunters.
- Github repository with either passwords directly committed into a public repo or other sensitive information. Github can also be used to get an overview of the application as it might contain the code that is being used.
- Twitter might contain some tweets with sensitive information by employees
- The webserver itself might contain configuration files which are visible to visitors of the webserver
- LinkedIn might contain information that it should not on the timelines of the employees
- Comments left by the developers
- Javascript files
- Directory listings are sometimes exposed to the public which allows attackers to view the internal structure of a website but even worse is when the directory listing is not secured at all and the attacker can just freely browse every file of the website.
- Directory listings can lead to backup files being exposed and if the attacker can download and analyse this, they can investigate the source code and get a better idea of how the application works and sometimes even find secrets.

## Physical threats

When it comes to pentesting, i think a lot of hackers forget the physical aspect of pentesting. I've worked with numerous clients that i offered a physical pentesting packages as well and i've been able to just walk in with employees by just pretending like i belonged there. I observed the dress code, bought a fluo vest and a helmet and walked right into a high security construction zone like nothing wrong was going on. I took one of their keyboards to show i was at the main frame and i turned in my assignment to get a hefty bonus. All of this would not have mattered if i would not have found the password to the mainframe on a physical post-it note on the server rack which i took a picture off. 

This is a cool story from my experiences but the point i am trying to make is that physical entry does need to be considered when creating a security plan. When a pentester is on an assignment but not assigned to do physical pentesting, he/she should report any infractions they see though as it's not part of the scope but as long as you do not do intrusive testing, an observed defect can be reported like a door that is always open. 

As a bug bounty hunter this is less useful to us but it can still have some consequences. An example i can give is when i found a post-it note in a picture of all the employees of my target in front of someone's desk. That note had the master password the back-end admin account on it. You can guess what happened from there. 

## Debug information

Developers have the option of enabling debug information when they create an application and add that into their code. This information can be used to find and fix any flaws that still exist in the application and they are very useful however when the developer forgets to disable them in production, we can use them to gather information from.

Sometimes this information might be very simple useless information for example

```bash
DEBUG Wrong email or password entered
```

Sometimes however, valuable things can be found in those debug messages. An example i found was when i tried to change my userType parameter from "user" to "administrator". This was the following message i got

```bash
DEBUG Unable to find enum value "administrator" in userTypes Enum. Possible values are
- Admin
- User
- Reporter
```

Ofcourse i fixed my mistake and collected my bounty. It is so nice when your targets tell you exactly what to do. Depending on the context you should report this as a bug bounty hunter but only if you can prove impact with this vulnerability. As a pentesters you should definitely report any information disclosure you find.

We can possibly also find the following information in debug messages

- Values for key session variables that can be manipulated via user input, for example the JWT encryption key allowing you to craft your own JWT
- Hostnames and credentials for back-end components, for example admin login credentials. The hostnames should be noted but the credentials should be reported by bug bounty hunters. Again pentesters should always report information disclosure but the hostnames will be a medium/low bug while the account data will be a high/critical, depending on how you can exploit them or low if there is no way to exploit them at all.
- File and directory names on the server. This should not always be reported by bug bounty hunters but for pentesters, this is something you should always report. It can help hunters find files for LFI for example.
- Keys used to encrypt data transmitted via the client. This can be used to decrypt data but it requires the attacker to already have access to that data so for bug bounty hunters this might help us understand things a little bit better by being able to decrypt our transmissions but this is not worthy of reporting in general. A pentester will probably report this as a medium/high vulnerability.

## Git Gud

Git is an amazing source for information disclosure and often people don't realise how big of a rabbit hole github can be. Often the developers that work at our target will create public repositories and without realising commit sensitive information. 

Usually config files are interesting as they might contain passwords and api keys to back-end services, however this is not always the case. Most developers these days are smarter than this and put their passwords in the CI/CD pipeline's enviornment variable. This means that we can't find it in the config file anymore but just a reference to it

Something else we might be able to find is source code which is always a good thing, source code is like a map to find our treasure and can help us understand the application on a while new level. 

A lot of hunters realise that github is a good source of information or maybe even privately hosted Git instances that are open to the public. What a lot of hunters miss though is that the commit history might be one of the best sources for information. A developer might have commited sensitive information and realised his mistake but if he commited a fix to remove that data, the commit history will still show the first version with sensitive information. 

## Blue bird OSINT by chain linking - Twitter + LinkedIn

A lot of developers will possibly not even realise this but they might tweet sensitive information which is ofcourse an issue. This might include things like pictures with post-its that contain passwords or even just screenshots of source code that contains things things like credentials or api keys or maybe even just URLs which lead to new endpoints you did not know about.

Even if the developer realises their mistake, it can often be too late as waybackmachine might have already indexed that tweet. In this case the developer will also need to remove that snapshot from the waybackmachine but this is something that is often forgotten.

Any information about the company or the products that is posted on social media should be reported as a pentester as informative but we have to mention that if they want to remove it fully, they might have to remove the waybackmachine entry as well.

As a pentester, this is something you can use to further pivot other exploits but usually this is not something we report.

For linkedIn exactly the same behavior applies.

## configuRATion

Sometimes a misconfiguration can lead to information disclosure as well. An example of this can be when the phpinfo() page is displayed fully to anyone, even unauthenticated users. This can tell the attacker for example that the eval() function might not be allowed, giving the attacker an attack plan for free.

Another example can be when the developer leaves the HTTP method "trace" enabled. This HTTP method usually does not lead to much information disclosure but might occasionally lead to the leaking of security headers.

As a pentester, we will report any misconfiguration we see, depending on the severity we will rate the bug accordingly but often the defect will be 'informative' or 'low' unless we are able to exploit it to pivot further into more impactful issue like RCE but then the issue will be about the RCE and not about the information disclosure anymore.

As bug bounty hunters, this information will rarely lead to a report and can only be reported is we can actually exploit the information we found.

## JavaScript commentary

Comments left in by the developers are often a goldmine of information about how the application works. There are also times when a developer will even leave an API key or credentials in the comments and forget to remove them before committing them.

You can find these comments by inspecting the source code of a webpage or if you have burp suite professional, you can also use the engagement tools by simply right clicking our target in the site map and selecting 'Engagement tools > Find comments'. 

As a pentester, this is one of the few things that you will rarely report unless we are talking about secrets or credentials ofcourse.

As a bug bounty hunter, these comments can be very useful to us as they lay out how the application works. This map of our target should be used and appraised but instead a lot of hunters tend to ignore it because it's tedious work to check all the comments but i find that it's usually well worth it to gain insight in how my target works.

These comments can usually be found in HTML but also in the javascript files at times and much more. 

In the javascript files, we can also find things like API keys and credentials though we have to realise most API keys in javaScript files are actually supposed to be public like google maps API keys though if those keys to a third party exists, all is not lost.

If we a third party connection which chargers us per request, we need to rate limit the amount of requests a user can make, otherwise an attacker can make a lot of automated requests and racking up our bill. As a pentester and bug bounty hunter, we have to report issues like this but build a very clear PoC and case. 

The severity of this issue can be pretty devestating to a company. For example a company that is just starting up can not handle a 100 000$ bill out of nowhere.

## Building a list and checking it twice

Some webservers have a directory listing enabled by default. If this happens, an attacker can at least view the internal structure of a website, often allowing them to find new endpoints without doing much effort. 

As a pentester this should be reported as a best practice but as a bug bounty hunter we will have to find some decent impact to this before we can report it, if there is any at all. As a pentester ofcourse we also need to check if we can exploit the functionality to increase the severity.

## BACK UP! This is your last warning!

Directory listings can lead to backup files which can contain source code. This is a great source of information for both pentesters and bug bounty hunters though probably not directly be exploited. This information will give attackers a better overview of the inner workings of the application. Information is one of the most important things we can have in hacking.

As a pentester i would report this as a low/medium issue unless i would be able to elevate my severity. As a bug bounty hunter i would only report this if i would find a way to elevate the information disclosure.

# How to test for information disclosure

This is really hard to define, there are some general strategies you can follow which we will outline right here:

- It is generally important to not focus too much on one thing because you might not see some other obvious issues which have been hidden by drawing your attention into a rabbit hole.
- Look everywhere you can for sensitive data, do not just keep it to the topics covered in this article but if you can think of any other places to look for sensitive data, definitely add it to your methodology.
- Usually you will not find information when you are specifically looking for it but when you are doing other activities. This means that you need to pretty decent at recognising what sensitive data looks like. This requires some pretty deep understanding of the target you are attacking, otherwise you can't know what is supposed to be sensitive information

# Checklist

- [ ]  If possible check for physical threats
- [ ]  If the target disclosed debug information, explore it
- [ ]  Explore Git, both the company profiles and the employees
- [ ]  Explore social media such as twitter, facebook and linkedIn. both the company profiles and the employees
- [ ]  Check the comments of the HTML and javascript file
- [ ]  Check for directory listings
- [ ]  Check for backups, if possible by directory tree or by brute forcing and fuzzing looking for .bak files

# Conclusion

Sensitive information disclosure is one of the bugs that rarely leads to a report as a bug bounty hunter and rarely leads to a report with more than a medium/low severity rating. When it comes to the leaking of 

- Account information
- Credentials
- API keys

Usually information disclosure is used to pivot to a much more impactful vulnerability. Information in and off itself is useless if we can't use it after all.