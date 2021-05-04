# 5. Broken Access Control

# Introduction

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/BAC.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/BAC.png)

This vulnerability type involves a lot of logic and in it's most basic form it might not as you can see in the screenshot above but then again that situation almost never happens in real life so we have to be a bit more crafty. This basic understanding of Broken Access Control (BAC) is needed though get to the more advanced vulnerabilities though so that's why i included it. In it's most basic form you are talking having access to functionality that we should not have. 

## Types of BAC

In the first picture i represented vertical BAC since i am execute functionality that can not be executed by any user of my access level. I'd need a user of a higher privilege level than mine to be able to execute this functionality under normal operations. 

When we talk about horizontal BAC defects we are talking about functionality that we would normally be able to execute but simply not on that specific object. Depicted below is a horizontal BAC defect but many of you may recognize this as an IDOR (Insecure direct object reference), they are the same thing. 

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Horizontal_Bac.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Horizontal_Bac.png)

# Some background information

You might find it surprising that we have to give all this extra information for a topic that seems so simple at first sight but even as pentesters it will take a whole lot of concentration to test the correct things. 

Let's first imagine a hypothetical scenario where you have 10 different levels of users with 10 different functionalities that each progressively get more access to more functionality. If we want to test all functions we have to test 10 functions with 9 different functionality priviledge levels (Since we will not have to test the admin account). This is one the simplest scenario's possible where there is no overlap between different priviledge levels. 

In most production environments you will find a situation similar to what we have in the drawing below. 

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/BAC_example.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/BAC_example.png)

The reason most BAC defects happen in these functionalities is because the base functionality is built and only after some time do they start working on the expansions like importing or exporting objects. 

When we want to test for these types of vulnerabilities we can use several execution strategies but like with anything our attacks success will depend on our preparation to a big extend. We will have to take the time to map our target very carefully and even create a permissions matrix if our target has not done this for us. All of this is not as hard as it seems but you do have to be very diligent and know your target well. 

# Mindset over methodology

These types of vulnerabilities are all about testing every single piece of functionality with every single privilege level that you can find. For me this starts with taking good notes and ends with taking good notes. 

I usually take notes for this vulnerability type in excel since it's easier to create tables there but any note taking tool can be sufficient. On my X-axis i note down all the privilege levels (Columns) and on the Y-axis i will start noting down what functionality exists. I will then indicate if a user of that specified privilege level should be able to perform Create Read Update or Delete actions (CRUD actions)

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Untitled.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Untitled.png)

I can then use this later on to test my application with one of the testing techniques but first we need to talk about how these types of vulnerabilities can exist so we can better go into some of the testing techniques. 

## Passports please

When you want to cross over a border you are asked to show a passport to show you are authorised to do that action. We can sort of look at access control like we are checking if a user can cross a border we are executing a check for their passport and we can either check if the user is logged in (has a passport at all) or if he authorised to pass (Has an immigration passport). The keen eyed among you may have spotted a third option as well and that would be see if that passport isn't falsified or forged which we can also do by forging a JWT token for example if the encryption algorithm isn't set properly. 

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/BAC_at_server_level_(1).png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/BAC_at_server_level_(1).png)

## Our checklist so far

To summarise we can test for the following:

- BAC to see if the user is even logged in at all (Vertical)
- BAC defect in checking if usertype is supposed to be able to access objects (Horizontal)
- BAC defect in checking if usertype is supposed to be able to access functionality (vertical)
- BAC defect in the logic checking which user is logged in by for example using the none encryption algorithm on a JWT token. (Business logic flaw)
- BAC defect because user can access functionality which in return will grab other functionality or objects. The system might see that another component from itself is executing the calls and not check the originator or their privileges any further. (Can be vertical or horizontal)
- BAC on other methods than the ones used by the application. For example the application might be using a POST call which can be well secured but if we change that POST to a GET method we might not get the same strict checks for BAC defects.

# Prevention is better than curing

So as you might be able to see we do have quite a lot of things we can already test for and we are not even done yet. While it's hard to describe every situation into detail there are a few general we can give to prevent this vulnerability and we will go much deeper into the testing aspect. 

- Deny access to any resources by default and only allow access on resources where it should be accessible (White listing principle)
- Create a re-useable method for authorisation and implement it throughout the application so you can ensure authorisation controls are implemented consistently.
- There should be a matrix displaying which users are able to access what functionality and we should not assume everyone should be able to see any data.
- Make sure you disable directory listings on your webserver and that no metadata information like .git files are visible.
- Any failed login attempt or even failed attempt at accesing functionality that is not allowed should be logged and if appropriate an admin should be warned by mailing them for example.
- Rate limit any API's but make sure this does not interfere with normal operations to negate the threat of automated tools a little bit.
- Any authorisation headers should have a limited validity and should be disbaled upon logging out the user.

If we follow all of these tips we already negate a lot of the attempts of abusing BAC defects but ofcourse these do not guarantee success. Sometimes even the smallest oversight might lead to a vulnerability and we should always test these requirements very well before deploying them to production. 

Despite it seeming like this is always tested very well before hitting a production environment I can assure you that this is often not the case. Because BAC issues seem so simple a lot of hackers underestimate how prevalent they are. 

# How to test for it?

Testing for Broken Access Control can happen in several ways and i do think it's important we test all off them. We will go over several methods and explain how and why they work. 

## Copy-pasting the URL

### Method

- Log in as an admin
- Open functionality only an admin can see
- Copy URL
- Log into incognito window as low priv user
- Paste URL in incognito windows

### What and why

We are copying the URLs from a browser where we are logged in as the highest privilege user to make it easier to see all the functionality. We only want to do this because need the URL to reach functionality which should include Access control. 

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/URL_copy.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/URL_copy.png)

This is the simplest way to test for broken access control but we have to take into account that we only test functions that should not be executed by low priv user but it's also important we try this with every type of user. 

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/URL_copy_(1).png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/URL_copy_(1).png)

To help aid with this type of testing we can use plugins like "pwnfox" to containerise our tabs. If we do that we can simple open a new tab and log in as another user in the same browser. This will also allow us to test a lot faster since we can test with more than 1 account type at a time. 

## Copy- and pasting JS methods

### Method

- Log in as an admin
- Look for a UI element that only admins can see and has a JS function
- Copy JS function
- Paste in developer console of low priv users

### What and why?

Sometimes one of our greatest allies in the battle for Broken Access Control is simple the developer console. We can apply the same principle but this time we copy javascript methods and paste those in the developer console of the low priv user. 

This works because sometimes developers will simply disable the UI elements but they might forget to do the same for the JS functions. 

You have to be careful though since for this you need to check out that you did not get a 403 status code response. 

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/JS_methods_copy.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/JS_methods_copy.png)

## Changing authorisation headers in repeater

### Method

- You should open a MiTM proxy such as burp suite
- You should login as a low privilege user
- You should copy their authorisation headers
- You should then login as an admin
- You should navigate to functionality that only high privilege users can access
- You should replace the authorisation header of the high priv user with the headers of the low priv user
    - This can be cookies
    - This can bearer header
    - This can be custom token
    - This can be sessionID

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Untitled_Diagram.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Untitled_Diagram.png)

### What and why?

This vulnerability is only possible because the server checks the authentication headers that we send along. A lot of you might be wondering "How can i get these cookies in a PRD enviornment? I can't steal others people's cookies unless i perform an XSS attack." and i want you to stop focussing on the headers. It's not about the headers but if we want to automate or even semi automate BAC defect hunting we will have to use the authorisation headers methods. 

What is important to remember is that we will execute functions with users that should not be able to execute those functions. This is the position an attacker will find themselves in as well but you have to remember that it's going to be hard for an attacker to know these URLs unless they are described in a JS document or something similar. This will significantly lower the impact as it will be much harder to perform a succesfull attack or even realise there is any weaknesses to be had. 

If we would be testing for IDORs for example we could also replace the identifiers but that would not be universal for our target since we could have an adressID, a userID, an invoiceID etc... and these would all need to be replaced if we want to test automatically. 

This method still requires a lot of manual interaction so we can just replace any identifiers as they pop up but make sure that you only try to access data that belongs to one of your accounts. It's definitly not ok to test on random production data. 

## Automation with match and replace/authorize/auto-repeater

### Method

- You should open a MiTM proxy such as burp suite
- You should login as a low privilege user
- You should copy their authorisation headers
- You should then login as an admin
- You should set up your tool to auto replace authorisation headers
- You can then start clicking around

### What and why?

We can use any of the tools in the title of this topic to automatically replace the authorisation headers. All we have to do is set it up properly before we can start clicking around and automatically test for IDORs/BAC defects. 

## Changing the request method

![5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Untitled%201.png](5%20Broken%20Access%20Control%20609e7d5fe10249f9a9288df639ac80f2/Untitled%201.png)

### Method

Perform the same method as in "Changing authorisation headers in repeater" but now add to also change the request method. Even though the server might never use the request method you are trying, it might be supported and possibly even less secure than the supported methods. 

### What and why?

This works because by default a webserver will accept all HTTP methods unless the developers turn that option off. This combined with the fact that developers will sometimes write general methods that support different types of operations within 1 algorithm leads to oversights in the access control of some features.