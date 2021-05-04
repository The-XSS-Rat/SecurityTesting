# Burp Suite: Comparer

# Introduction

![Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled.png](Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled.png)

Whenever we encounter 2 requests that might seem very similar, there is a chance that we want to see how they differ. This is where the amazing tool called "Comparer" comes into play.

# Sending requests to the comparer

We can either send a single request to the comparer or multiple requests. It doesn't matter very much besides the fact that if we send the requests individually we ofcourse need to send at least two of them to the comparer.

We have several options here, we can either send requests from the proxy > http history, target > site map, repeater, ... wherever we can right click on our requests/responses we can send them to the comparer from the context menu.

We can also paste a request from our clipboard or load it from a file.

![Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled%201.png](Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled%201.png)

## Comparing requests

![Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled%202.png](Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled%202.png)

We can compare requests by words or bytes. The most usefull option is going to be by text as we usually want to find differences that are visible in that way. Sometimes we are fuzzing on byte level, this is when we might want to compare on byte level.

![Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled%203.png](Burp%20Suite%20Comparer%20ac4f316bf2f542acbf7f0d77ddb33129/Untitled%203.png)

We have several interesting options here. 

1. Burp is going to highlight the differences in the requests or the responses.
2. It will either Highlight added, modified or deleted data
3. This option allows us to scroll through the requests synchronisly. This means that when we scoll in the request on the right, we will also scroll on the left.