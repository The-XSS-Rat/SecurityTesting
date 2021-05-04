# Broad scope methodology - Manual

# Introduction

Before we start running our tools, we need to know what they do in my opinion. Just running a script and expecting magic to happen is script kiddie behavior and we are far beyond that my friends. We are hackers.

I am not saying you should never use tools, mind that. Tools are very useful in automating our workflows but they miss so much. A tool only checks what you tell it to check while human eyes are unbeatable in detecting details that are odd or off. That's what it's all about my friends, we need to mind those details very much. We can't ignore them. 

The other reason i always recommend doing manual recon is that you can not possible program every single scenario into your automation. Life is diverse and so is software. We can't rely on automation to find all the bugs. That being said, i am a HEAVY proponent of nuclei from project discovery but not the default templates. More on that later.

Automation is good but automation combined with manual testing ensures we get the best results possible. We also need to know the processes to improve our automation because for me it's very important to keep improving. I don't know about you friend but i always have new ideas on how i can improve my workflow. If i can implement those into my test automation, i have a big advantage since i won't have to manually retest a target every time.

# Test objectives

We want to achieve the following test objects with our manual recon:

- Find an asset that is suiteable for our attack strategy
- Explore our target
- Execute our attack strategy

This may seem simple  but there is a lot of hidden truth in these simple words. First and foremost, we want to find an asset to execute our attack strategy on. This means that we need an attack strategy first. That's the exact reason we started with single scope applications in our course. We want to build a solid strategy before we even  begin thinking about recon, how else would we even recognize a suiteable target if we saw it?

We need to explore the assets we found thouroughly, we can either do this manually or automatically but both aim at different vulnerabilities. 

- The manual approach is actually semi automated as we've seen in the main app chapter but in general we need to explore our target's assets very thoroughly to actually find vulnerabilities.
- The automated approach aims at things like CVE's or misconfigurations.

Whichever approach we pick, we need to be aware that simply running a tool is not going to be enough. 

# Disadvantages of tools

I'm going to list the disadvantages of tools but again, i don't recommend against them. I recommend you first learn how to do it yourself.

- Everyone can run the same tool. It's not hard, there's usually instructions with the tool and it's free online. If everyone runs the same tool, everyone gets the same dupes.
- If you don't know what your tool does you are missing out on a lot of stuff
- Running a tool without knowing what it does is stupid. I'm not going to sugar coat it, it's just plain stupid. You could be testing very intrusively without even realising it and your target might not like that.

# How can we do manual recon?

Google dorking is very important in this process for me. Google indexes websites to a stunning degree and we query those websites if we use the correct syntax. In the following scenario i will be investigating Tesla as they have an excellent bug bounty program. I am making sure i am not showing you guys any vulnerabilities and if i would find them, believe me i would report them myself 😂. This being said, today we will explore how to find a target, not a bug. That will be taken up in other chapters.

# Google dorking

We will start with some good old google dorking. This is the first step in our process and we will try to emulate "subdomain" enumaration using this method. 

We will start with a basic dork

```jsx
site:google.com -www
```

This will show us all the subdomains from google except the main www subdomain.

![Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled.png](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled.png)

I will then take on the first subdomain that i see. This is where the testing begins. I explore the subdomain and try to find out what functionality is available via the website. I even go as far as to make a mindmap of all of the functionality so i'm sure i will remember later on.

After exploring the subdomain i will go to waybackmachine to find more hidden functionality and even read the javascript file if i like the functionality.

### Waybackmachine

We will use this website to emulate waybackurls. Waybackurls will grab all the URI's of a certain subdomain from waybackmachine but the waybackmachine has some pretty awesome functionality for us.

[http://web.archive.org/](http://web.archive.org/)

![Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled%201.png](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled%201.png)

I really like the summary tab. In here you will find a distribution by mimetype, if we only see images it might not be interesting to investigate if those images are public for example.

We can also explore all the URLs of our asset.

![Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled%202.png](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled%202.png)

Here we can filter by URL or by MIME type

![Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled%203.png](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/Untitled%203.png)

I also really like the site map as it shows all the URLs in a handy pie chart which allows us to explore the site in a birds-eye view.

### Moving on

If we are done with our target we can explore our next target. To get there, i simply remove my current asset from my search results by adepting the google DORK.

```jsx
site:google.com -www -news
```

## Other options

We can also use yahoo, duck duck go, bing, ... to explore our target more. This is basically what automated tools do. They look at as many sources as possible and try to gather all the subdomans.

# Show me your secrets

When i've seen all the subdomains i want to see, i move on to trying to find some more secrets. Github is perfect for that, sometimes there's things like API keys, secrets or even login data hidden in a repo. 

[https://securityonline.info/github-dorks/](https://securityonline.info/github-dorks/)

[0. Subdomain enumeration](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/0%20Subdomain%20enumeration%20b9ba6f298bf44f25845e4e0204c9027d.md)

[1. Creating our list of subdomains](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/1%20Creating%20our%20list%20of%20subdomains%20380c3bc8b56846108ce78f0062bed869.md)

[2. Processing Our List Of Subdomain](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/2%20Processing%20Our%20List%20Of%20Subdomain%206bf06bf770584289a8abd9e63c7bf2bd.md)

[3. Subdomain flyover](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/3%20Subdomain%20flyover%205fe81be649ca4b849011d19ed4e53482.md)

[4. Exploiting open ports](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/4%20Exploiting%20open%20ports%2028f4a661e49d42748c33b352ad34dc1a.md)

[A. Vulnerability scanning](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/A%20Vulnerability%20scanning%20713c913200be4fd98948a6d2d6d0f817.md)

[B. Vulnerability testing strategy](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/B%20Vulnerability%20testing%20strategy%20b4124e41647c49c49b11b70e1fb79cff.md)

[98 Running your scripts on a VPS](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e.md)

[99. List of tools for grabbing subdomains](Broad%20scope%20methodology%20-%20Manual%201097d5c08b8a4da0907fd593003272ae/99%20List%20of%20tools%20for%20grabbing%20subdomains%20788400d9c9d14a79b45c2fb1f6463692.md)