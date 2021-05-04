# Burp Suite: Do i need the profesional edition?

# Introduction

I often get asked this question and i can be very short about this, no. You don't need burp pro. That being said, it does have some very big advantages that will make life a lot easier on you. So while you don't need burp suite, you don't need it in a sense that you also don't need to eat fries every week but it sure does taste good. 🍟

What type of advantages you can gain from burp suite pro depends on the type of consumer you are. We will over some situations but in the end it's up to you decide since it is a lot of money for some people. I would see it as an investment.

# General advantages

While some of the advtanges are specific to the usage scenario's, some advtanges can also be good for everyone so we will list those here.

- The biggest advantage for me is that i can save my projects. As a full time QA team lead, full time dad, aspiring teacher and bug bounty hunter i have to divide my time VERY efficiently as you can imagine. Testing a target propperly in an hour is impossible and by far the biggest hurdle for me is getting set up. When i have to take 15 minutes to configure my burp suite every time i want to test my target that is going to stop me from even starting in the first place. Especially if i only have an hour to test my target i want to do it as efficiently as possible and not waste up to a quarter of my time every time i want to test.
- The intruder can used at full speed. When you have the community edition, portswigger limits the amount of requests you can make to 100 per attack and they severely rate limit the requests
    - We also have access to wordlists built by portswigger, these are really good.
- Content discovery is an amazing tool that's unlocked with burp suite proffesional edition. It's one of the best content discovery tools i've found out there and has multiple options available which we look into in detail in a later chapter.
- Besides the content discovery tool, we have access to a host of other usefull engagement tools such as a tool to identify all the javascript files and a tool to find references
- We can install a whole host of burp extensions that are very useful such as CSRF scanner. More about that later on in another chapter.
- We can search our whole project, this is not available in the CE
- Burp infiltrator and Collaborator client are available in the proffesional version.

# Small businesses

For a small business, there is one major advantage that i think bug bounty hunters won't profit very much from. You can perform automated scans on your target which can easily remove any low hanging fruit before you send those new features off into production. Please note that this version does not include any CI/CD integration.

The reason automated scans are not interesting for bug bounty hunters in my opinion is that bug bounties are insane and not like regular hacking at all. We are last to hack our target after pentesters and a range of other hackers after us. Besides that, most programs don't allow it and some WAFs might even IP ban you.

# Medium/Large businesses

If you have your development process down to an art and have your CI/CD pipelines set up, you might want to include a burp scan in your pipeline, this is possible but you need the enterprise version which costs a lot more but it also has some other features. Besides getting hacked costs a lot more.

[https://portswigger.net/burp/enterprise/features](https://portswigger.net/burp/enterprise/features)²