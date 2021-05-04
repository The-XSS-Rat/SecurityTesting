# Burp Suite: repeater

# Introduction

The burp suite repeater is a very usefull tool in our arsenal. This allows us to edit any request in various ways and resend them to the server. You probably all know the basics of how the repeater works so i'm not going to bore you too death with details but i will be showing you some really cool tricks. I bet you diden't know all of these. 

# Basics

![Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled.png](Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled.png)

1. The request, we can manipulate it here and change any parameters we want
2. The response, make sure you check it to see if there are parameters that are not in the request. They might be impactfull and if you copy them to the request, you might be able to change them
3. The controls, we can send a request, cancel it if it takes to long and go back & forth in our history
4. The tabs, here we can find all of the requests we have open

# The requests

If we right click the request, a couple of options become available to us. 

![Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled%201.png](Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled%201.png)

1. This will change the request from a POST to a GET and vica versa
2. This will change the request from a POST or GET to a PUT and from a PUT to a POST request
3. If you are filing a report, you often need to enter the URL. This option will enable you to copy the entire URL in one go and paste it into your report
4. If you want to mess with the request in CURL or add it to your report as a CURL call, this option will build that call for you
5. This will save the entire history of the request, including the ones we have sent before, edited and sent again, to a file.
6. If you edit the URL, you might want to add that specific endpoint to the site map

# Response

This context menu mostly has the same options as previously.

![Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled%202.png](Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled%202.png)

1. In here i want to highlight that we can render a page as well to see what it looks like. This sometimes beats reading 10000 lines of HTML code

# Tabs

![Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled%203.png](Burp%20Suite%20repeater%20d4bf73cf9c3146b48b75b24e6d0b797a/Untitled%203.png)

We can rename tabs by double clicking them.