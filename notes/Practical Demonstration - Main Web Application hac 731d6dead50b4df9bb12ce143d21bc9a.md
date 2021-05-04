# Practical Demonstration - Main     Web Application hacking

# Introduction

Hello All 

Welcome to Practical Demonstration of Web Application Hacking here we are going to learn about  various web vulnerabilities and how to hunt  them on a target and how to exploit them .

Before we begin to hunt we should choose a target that is in scope here we are going to choose our target as OWASP (Open Web Application Security Project) Juice Shop Project which is an insecure web application.

When we hunt, it's important to look at every target in it's own right. We are going to look at the OWASP juice shop. In this demonstration you will be show all the topic we went over and which parameters we will be using to test. Not all of our tests will lead to existing issues but still we **Have** to do all these tests. We are no longer practicing right now, this is bug bounties. 

# OWASP Juice Shop

## Installation

In general if we want to hunt bugs on a target we  will search for the application, and then we will start hunting but here we are choosing our web target as OWASP Juice Shop which is an insecure application this website requires installation now we will see how to install this application.

Here I am choosing Heroku  for installing our Juice Shop as this is free  and easy to use, you can also choose other ways like installing  Docker Images.

Step 1: go to [https://www.heroku.com/](https://www.heroku.com/) and Sign up for an account if you are not having.

         If you are having an account then go to step 2

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Screenshot_from_2021-03-11_15-23-14.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Screenshot_from_2021-03-11_15-23-14.jpeg)

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Screenshot_from_2021-03-11_15-19-23.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Screenshot_from_2021-03-11_15-19-23.jpeg)

Then confirm your email, and you will be seeing a page for setting up your password like below 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Screenshot_from_2021-03-11_15-29-50.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Screenshot_from_2021-03-11_15-29-50.jpeg)

Enter your Password and Proceed by clicking on SET Password and Login In and you  will be seeing a 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/enter_to_procee.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/enter_to_procee.jpeg)

Now you will be seeing the terms of services of Heroku and accept by clicking the accept button

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/heroku_terms.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/heroku_terms.jpeg)

You are ready by one step and are seeing the dashboard 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/dashboard.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/dashboard.jpeg)

Step 2:

Now we are ready with our account, and we are going to create our juice shop on Heroku  Navigate to   [https://elements.heroku.com/buttons/bkimminich/juice-shop](https://elements.heroku.com/buttons/bkimminich/juice-shop) then click on  **"DEPLOY TO HEROKU"**  for deploying the application onto Heroku  

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/deploy.jpeg](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/deploy.jpeg)

Pick a unique name for your app, it doesn't matter which it is, but it has to be unique.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled.png)

Click the "Deploy app" button, the app will now start deploying. It will take a while before the app is deployed so give it some time, sit back and make yourself a good coffee or tea with a nice piece of cheese.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%201.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%201.png)

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%202.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%202.png)

We Successfully Deployed our App, and We can now view our app 😉

## Identifying Nature of our target

We identified  this target as a webshop, so we have to keenly observe our target for knowing how this website is processing the user requests, as this is a web target we need to test the website at least for the following Functions.

~~this target properly we will have to make a small investment. Since this is a webshop we want to test for at least the following functions:~~

- Registration
- Login
- Buying an item
- Possibly returning an item
- Our wallet functionality if exists
- Logic flaws
- XSS
    - Stored
    - Reflected
- Basket functionality
- Adresses
- IDORs
- CSRF
- Broken access control if we can get to admin functions

    This is an initial judgement and we might add to this as we explore the website and find more functionality.

## Exploring the Application

First of all we need to know what functionality exists before we can start attacking our target properly. We need to fill up our site map in burp and we need to be able to explore the parameterised requests. To do this, we need to set up burp properly first. This includes setting up our scope and setting the options that we need. In this course we will use burp suite but feel free to use any other MiTM proxy with the same functionality.

### Setting up Burp Suite

It really helps to have burp suite pro, you don't have to but the fact that you can save a project is a major plus for having the burp pro application. I can only hunt in bursts of 1 to 3 hours, so I have to revisit my target often. This means two things.

- I have to take very dilligent notes so i don't retest things 10 times needlesly and so that i make sure i do test all of my functionality. Part of this documentation is the "Judging our target" section.
- If u can set up my project settings in burp suite, save them and reload them whenever you want, that is a major plus. The biggest part of any activity is getting yourself to do it and if you can skip part of the setup, that will help you get started. If you are doing something time seems to fly but if you are sitting in your sofa it takes tremendous power to get yourself up and go hunting. Anything you can do to make this easier is a major win.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/burpproject.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/burpproject.png)

First i like to setup my scope, make sure you add the proper URLs that are in scope. 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%203.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%203.png)

Hackerone has configuration files for burp you can download.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/h1.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/h1.png)

You can then import this file via the project options import functionality under "Project > Project options > Load Project options"

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%204.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%204.png)

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%205.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%205.png)

After setting up our scope we will move on to setting up our proxy options. I always configure several options to make it easier for myself to see things like hidden fields and to remove any javascript validation from my responses.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%206.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%206.png)

This will make any hidden fields easier to see as it will unhide them and draw a big red square around them. If you see this big red square you know you are looking at a hidden field.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%207.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%207.png)

Now that we have burp suite set up in the background we can start exploring our application.

### Manually Walking the Application

Just because we are manually walking the application does not mean we should not be hacking. This is the most important phase in bug bounties and most of you will know it as the recon phase.

In this phase we want to get to know our application. We want to start by exploring the functionality and as we do that we want to take note of our prvilidge levels. Even though it might not seem like it, since we don't have access to the admin functionality (yet), but there are different levels of priviledges. 

- Unauthenticated accounts (not logged in)
- Authenticated accounts

As we hack our application, there might be more levels we can add to this such as administrators.

I myself use excel to make a quick mindmap but you can use whatever tool suits you best.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%208.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%208.png)

When i register my account, I register using an attack vector that automatically tests for JS XSS, HTML injection and HTML tag attribute injection. 

```jsx
'"><u>THE XSS RAT WAS HERE
```

I use this attack vector wherever possible when attacking my target. 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%209.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%209.png)

This is the way, whenever the application uses my username anywhere, I am automatically testing for all the described attack vectors. If my username is reflected in the JS context anywhere, then I  will try to break out of the context it is being reflected into. If the username is reflected in a tag, like it is in the picture above. In this picture, when we save the username, we can see that we have broken out of the VALUE attribute of the input tag. From here, we can try to insert our own JavaScript. 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2010.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2010.png)

I will try this WHERE EVER I can, this includes addresses, nicknames, ... 

On the profile page however i can still see some more things i can test for. I see a profile picture so i can test for XXE via SVG here. 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2011.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2011.png)

I also see a link option here. This link will resolve to a picture which gives the option for SSRF. To test for this, i start my burp collaborator and grab a URL that i can insert into this field. Running a public burp collaborator server is a premium option and only available in the paid version of burp. If you don't have the paid version of burp you can use:

- Your own webserver
    - If you don't configure this properly, you can only capture HTTP requests
- A public burp collaborator
    - This may suffer from availability issues as it's shared between all users

        Whichever option we go for, we need to copy our payload to the clipboard and paste it in our URL field that the server tries to resolve.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2012.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2012.png)

We might need to put HTTP:// in front of our URL if the server checks for syntax.

http://[s5yf4ljmn9wgf95dcykd4iu7zy5otd.burpcollaborator.net](http://s5yf4ljmn9wgf95dcykd4iu7zy5otd.burpcollaborator.net/)

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2013.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2013.png)

If you are getting a lot of DNS requests coming into your burp collaborator but no HTTP requests, then there is  probably  no way to pull off SSRF, so  there is a possible egress filter in place. Egress filters can stop certain types of outgoing traffic. As of this writing OWASP juice shop does not have any SSRF vulnerabilities but if we would find one here, continue on our SSRF path. 

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2014.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2014.png)

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2015.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2015.png)

I will try the same XSS technique for adress any stored or reflected fields i can find. If i suspect a server side template engine is being used, i will add an SSTI attack vector. 

```jsx
'"><u>THE XSS RAT WAS HERE${7'*7'}
```

If this resolves to 7777777 or 49 I will investigate further into SSTI (SERVER SIDE TEMPLATE INJECTION) or CSTI (CROSS SITE TEMPLATE INJECTION)attack techniques.

### SQLi (Structured Query Language Injection)

The previous attack vector also automically tests for SQLi as well

```jsx
'"
```

These special characters will also test for SQLi since these are special characters also used in SQL statements. If we get an SQL error, we usually run a tool like SQLMAP to better investigate what SQLi. Now we are having a Hands-on Session and  for any further doubts refer SQLi section.

### Testing for IDORs(Indirect Object Reference)

For testing IDOR's we require two accounts on the target, we are already having one so that we  have to create a second account at our Target so that we can find IDOR's. We can test IDOR's by changing the first user(first account) cookies or Authorization Tokens or Headers with the Second User(Second Account). This may seem confusing as you can't copy your victims cookie or headers in production, but ****this is not our goal. We just need that cookie or header to automate our IDOR search. How to do this has been demonstrated in the tools section.

### Testing for Vertical Privilege Escalation

When we want to test for vertical privilege escalation we do need accounts of different privilege levels. Since we don't have any admin accounts yet, we can't test for this yet. If we did have different privilege levels, we would create accounts of all different privilege levels and test for BAC. Example:

- Administrator
- Content editor
- hu/Customers

Again, how to test for this specifically has been illustrated in the tools section.

### The login section

In the login section we can play around with the requests a little bit. For example if we request a password reset link, and append our own email adress to the request, the server might send the password reset link of the victim to the email adress of the attacker.

```jsx
POST /api/resetPassword HTTP/1.1
Host: ferretshop.herokuapp.com
Connection: close
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="88"
Accept: application/json, text/plain, */*
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTcsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiMWFlZGI4ZDlkYzQ3NTFlMjI5YTMzNWUzNzFkYjgwNTgiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE2MTU0MDY1OTcsImV4cCI6MTYxNTQyNDU5N30.ZP57rD5SMMyXD87VceX57xF4TQqqMeqAIUm96XQY_wTghbPF8gRmGxIIJN1G_vZkuewH5VrIbZ8RJuAaj5LOR3kfUJvkMm5ibLaNpUZYlenjM1OXowMKeZVniJiLx3D-UBGauEvJf4wkX2x3UXs_SuudK57-2xACAadUYxTlWEU
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ferretshop.herokuapp.com/
Accept-Encoding: gzip, deflate
Accept-Language: nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: language=en; welcomebanner_status=dismiss; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTcsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiMWFlZGI4ZDlkYzQ3NTFlMjI5YTMzNWUzNzFkYjgwNTgiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE2MTU0MDY1OTcsImV4cCI6MTYxNTQyNDU5N30.ZP57rD5SMMyXD87VceX57xF4TQqqMeqAIUm96XQY_wTghbPF8gRmGxIIJN1G_vZkuewH5VrIbZ8RJuAaj5LOR3kfUJvkMm5ibLaNpUZYlenjM1OXowMKeZVniJiLx3D-UBGauEvJf4wkX2x3UXs_SuudK57-2xACAadUYxTlWEU; io=Mq1hqj7m93njsus2AAAF
Content-Length: 24

{email:"victim@gmail.com"}
```

Might turn into

```jsx
POST /api/resetPassword HTTP/1.1
Host: ferretshop.herokuapp.com
Connection: close
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="88"
Accept: application/json, text/plain, */*
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTcsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiMWFlZGI4ZDlkYzQ3NTFlMjI5YTMzNWUzNzFkYjgwNTgiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE2MTU0MDY1OTcsImV4cCI6MTYxNTQyNDU5N30.ZP57rD5SMMyXD87VceX57xF4TQqqMeqAIUm96XQY_wTghbPF8gRmGxIIJN1G_vZkuewH5VrIbZ8RJuAaj5LOR3kfUJvkMm5ibLaNpUZYlenjM1OXowMKeZVniJiLx3D-UBGauEvJf4wkX2x3UXs_SuudK57-2xACAadUYxTlWEU
sec-ch-ua-mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ferretshop.herokuapp.com/
Accept-Encoding: gzip, deflate
Accept-Language: nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: language=en; welcomebanner_status=dismiss; token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MTcsInVzZXJuYW1lIjoiIiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiMWFlZGI4ZDlkYzQ3NTFlMjI5YTMzNWUzNzFkYjgwNTgiLCJyb2xlIjoiY3VzdG9tZXIiLCJkZWx1eGVUb2tlbiI6IiIsImxhc3RMb2dpbklwIjoiMC4wLjAuMCIsInByb2ZpbGVJbWFnZSI6Ii9hc3NldHMvcHVibGljL2ltYWdlcy91cGxvYWRzL2RlZmF1bHQuc3ZnIiwidG90cFNlY3JldCI6IiIsImlzQWN0aXZlIjp0cnVlLCJjcmVhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDIxLTAzLTEwIDIwOjAzOjEyLjc5MiArMDA6MDAiLCJkZWxldGVkQXQiOm51bGx9LCJpYXQiOjE2MTU0MDY1OTcsImV4cCI6MTYxNTQyNDU5N30.ZP57rD5SMMyXD87VceX57xF4TQqqMeqAIUm96XQY_wTghbPF8gRmGxIIJN1G_vZkuewH5VrIbZ8RJuAaj5LOR3kfUJvkMm5ibLaNpUZYlenjM1OXowMKeZVniJiLx3D-UBGauEvJf4wkX2x3UXs_SuudK57-2xACAadUYxTlWEU; io=Mq1hqj7m93njsus2AAAF
Content-Length: 24

{email:"victim@gmail.com",
email:"attacker@gmail.com"}
```

This might prompt the "GenerateLink" server to generate a password reset link for the first email address but the "SendLink" server might send the link to the attacker.

### CSRF (Cross Site Request Forgery)

Whenever i see a CSRF token, i will try to replace it:

- with an empty parameter (CSRF=)
- with a parameter of the same restrictions (like same length and alphanumeric) (CSRF=2475455dfs1)
- CSRF=1
- A CSRF token that does not belong to that account

I can use the tools "Match and replace" or "Autorepeater" for this although the "Autorepeater" extensions seems to have broken with the latets burp update though this might get fixed later on.

See the tools section.

### Exploring the requests

Now comes the fun part, we are going to look at all the requests and parameters in their own right. To do this we need to go back to burp suite and look at our site map. This has been filling up in the background while we click around.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2016.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2016.png)

Now we can see the parameterised requests, we don't really care about the static requests.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2017.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2017.png)

I am going to look at all of these requests and see if i can find some parameters i can manipulate that i should not be able to manipulate such as:

- {userType:"User"} > {userType:"Admin"}
- {accountType:"Basic"} > {accountType:"Advanced"} (might be more expensive)
- {rating:5} > {rating:-5000} (might be able to negatively affect the rating of a video on youtube)
- ... Use your imagination

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2018.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2018.png)

In this case for example, we can change the author of a review which should not be possible.

### LFI/RFI

Whenever a parameters shows that it is grabbing a file from the local file system or whenever it seems to be from a remote location, i will try either LFI or RFI respectively. See those sections to learn more about them.

- GET /avatar.php?file=image1.png
- GET /avatar.php?file=s3.bucket.org/image1.png

LFI/RFI in and off- itself is usually not that impactful. If we find this issue we should try to find files on the system that we should not be able to access like private pictures of other users or we should try to include a file which executes remote code execution. This can cause use to create a reverse shell allowing us access on the server. If you ever achieve this, you should stop and report, don't explore a production server with the risk of seeing data you should not or crashing the production server.

### OS Command injection

This is the last vulnerability type i check for. The only way to check for this issue type is to fuzz all of those parameters with your fuzzing list that you created in the OS command injection section. To do this I use the intruder tool that's built into burp.

![Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2019.png](Practical%20Demonstration%20-%20Main%20Web%20Application%20hac%20731d6dead50b4df9bb12ce143d21bc9a/Untitled%2019.png)