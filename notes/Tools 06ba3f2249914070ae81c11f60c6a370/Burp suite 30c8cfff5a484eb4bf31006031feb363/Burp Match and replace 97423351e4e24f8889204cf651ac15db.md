# Burp: Match and replace

# Introduction

Burp suite's proxy options have an option called "Match and replace" available. This option has many rich uses that can help us automate our testing process. With some smart uses of this amazing option, we can automatically test for CSRF, IDOR, command injection,.. by just clicking around in the application! Let's explore this magical tool and it's many options.

# Replacing authorization headers

Since authorize basically just matches the authorization headers and attempts to replace them with the ones the user supplied, we can set up a similar rule in the proxy.

![Burp%20Match%20and%20replace%2097423351e4e24f8889204cf651ac15db/Untitled.png](Burp%20Match%20and%20replace%2097423351e4e24f8889204cf651ac15db/Untitled.png)

![Burp%20Match%20and%20replace%2097423351e4e24f8889204cf651ac15db/Untitled%201.png](Burp%20Match%20and%20replace%2097423351e4e24f8889204cf651ac15db/Untitled%201.png)

1. Usually the request header will contain the authorization methods
2. Fill in the tokens of the logged in user
3. Fill in the tokens of a second user you want to use

Now, as long as this rule is active you can click around in the application. If you can open any information that should not be public, we have an IDOR on our hands.

To disable this rule, simple uncheck the checkbox in front of it.

 

![Burp%20Match%20and%20replace%2097423351e4e24f8889204cf651ac15db/Untitled%202.png](Burp%20Match%20and%20replace%2097423351e4e24f8889204cf651ac15db/Untitled%202.png)

# Automatically replacing CSRF tokens

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled.png)

Depending on if the CSRF token is in the HEADER or the BODY section of the request, we will need to pick one.

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled%201.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled%201.png)

Fill in the regex to indicate to burp how it can find the CSRF token in your request and replace it with a value of your own. Be careful, this is just an example, it may be different for your target.

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled%202.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled%202.png)

When this rule is active, click through the application and try to make changes. If you are able to make changes where a CSRF token is normally expected, investigate this further. It may be a vulnerability. To restore normal functionality, simply disable this rule.

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled%203.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/CSRF%209bfcc03c9ce246a58d4815982e85bc18/Untitled%203.png)

# The sky is the limit

You can change any value you want in either 

- The response
- The request

And in either

- The header
- The body
- Request Parameter names
- Request Parameter values
- Request first line

These give us an infinte amount of possibilites so the sky is the limit... Think outside the box!