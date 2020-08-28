**Strategy**

*Tips*
- First of all, get to know your application, spend some time on using it normally but keep burp open
- Start with XSS and SSTI as early as possible if in scope, insert them into every field you see
- Create your own fuzzing lists 
- Expand this list with your own findings
- VDP over paid if you want less competition
- PoC or GTFO
- Prove your impact

--------

**Sessions**

- Make a user with every role and check if he can directly access pages he should not be able to
- Take away a role and check if the user can still do the actions before logging out
- Look at the session token, does it change? If not, they might be useable for session fixation
- Delete a logged in user and check if he can still do actions before logging out

--------

**Stored XSS**

*Tips*
- For every input field
	- Try to get ```<a href=#>test</a>``` an entity in
	- Try to get an obfuscated entity in
	- If it catches on anything, go deeper

*video's*
- https://www.youtube.com/watch?v=uHy1x1NkwRU

--------
	
**Reflected XSS**

*Tips*
- Check the error pages (404,403,..) sometimes they contain reflected values
	- Trigger a 403 by trying to get the .htaccess file
- Try every reflected parameter

*video's*
- https://www.youtube.com/watch?v=wuyAY3vvd9s
- https://www.youtube.com/watch?v=GsyOuQBG2yM
- https://www.youtube.com/watch?v=5L_14F-uNGk
- https://www.youtube.com/watch?v=N3HfF6_3k94

--------

**DOM XSS**

*Tips*
- Would not recommend manually looking for DOM XSS
- Burp suite PRO scanner can find DOM XSS
- Tool: https://github.com/dpnishant/ra2-dom-xss-scanner

*video's*
- https://www.youtube.com/watch?v=gBqzzhgHoYg
- https://www.youtube.com/watch?v=WclmtS8Ftc4

--------

**Blind XSS**

*Tips*
- Use xsshunter
- Start hunting for blind XSS soon
- Copy every payload from your xsshunter payloads section and paste it into every field you see
- XSS hunter contains a payload for CSP bypass
- Generate some variations of your payloads (example replace < with &lt;)

--------

**XSS filter evasion tips**

*Tips*
- < and > can be replace with html entities &lt; and &gt;
- You can try an XSS polyglot
	- ```javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>```
	- https://gist.github.com/michenriksen/d729cd67736d750b3551876bbedbe626
	
	
--------

**Command injection**

*Tips*
- Create your own fuzzing list! (See video's)
- Blind command injection can happen so make sure you include a delay command in your fuzzing list
- Make sure you include windows and Linux commands on your fuzzing list

*Video's*
- https://youtu.be/GZyoEXdezZM
- https://youtu.be/B-aVRsaQTgo

-------

**CSRF**

*Tips*
- Check if there is a CSRF token
- Check if the token changes
- Check if the server still accepts the token if you give it a random token

*video's*
- https://www.youtube.com/watch?v=ImqLlFMQrwQ

--------

**Cookie**

*Tips*
- Httponly flag?
- Secure flag?
- Is the domain of the cookie checked? 
	- If not You can write a cookie to a subpath and it will append that to the request
- Is cookie reflected in URL GET parameter?

--------

**IDOR/broken access control**

*Tips*
- Try directly going to objects that you have no right to that are on the same level of authentication as the user
- Try directly going to objects that you have no right to that are on a higher level of authentication as the user
- Try directly going to objects that you have no right to that are from a different client in the system
- In Europe, Personal identifiable information is sensitive so bugs containing these can be of a higher severity

*video's*
- https://www.youtube.com/watch?v=hZ0xSRswN8M
- https://www.youtube.com/watch?v=mjrGOuFc1Kw
- https://www.youtube.com/watch?v=5vYhTik8_yU
- https://www.youtube.com/watch?v=HQUxXE1oaIE

--------

**LFI/RFI**

*Tips*
- If a file or image is being loaded from the local disk, try LFI/RFI (example file=test.jpg)
- Keep a VPS handy for when you need to do RFI

--------

**SSTI**

*Tips*
- Try to inject }}{{7*7}}
- Try to inject }}[[7*7]]

*video's*
- https://www.youtube.com/watch?v=iQ6FuL-DgX8
- https://www.youtube.com/watch?v=i8cvh0u-VXE

--------

**XXE**

*Tips*
- For every XML input you see, try XXE
- For every document upload, try to upload a docx file. Those can be vulnerable to XXE as well.
- For every picture upload, try to upload an SVG, you can do XXE via SVG as well

*video's*
- https://www.youtube.com/watch?v=AQUHzyzZXeA
- https://www.youtube.com/watch?v=unS3xGZj8xk
- https://www.youtube.com/watch?v=EwsW2WfUTmQ

--------

**SSRF**

*Video's*
- https://youtu.be/UpzXZcfYNNc
- https://youtu.be/unS3xGZj8xk

--------
**Chaining XSS**

*Tips*
- Maybe use XSS to steal non httpOnly cookie?
- Maybe use XSS to overwrite cookie on different path?
- Maybe use session that never changes togheter with xss to steal cookie for eternal account takeover (+ severity)
- Maybe use XSS to steal info displayed on the page (GDPR issue - PILL data)

*Videos*
- https://www.youtube.com/watch?v=5vYhTik8_yU
- https://www.youtube.com/watch?v=unS3xGZj8xk

--------

**Chaining CSRF**

*Tips*
- Maybe use a CSRF to make someone insert XSS on their own page?

--------

**Chaining IDOR**

*Tips*
- Sometimes, programs use UUID's (1213804129abc80823213214) and you find an IDOR on it. It will be low impact because you can't easily guess this id. maybe you can find an endpoint that displays all the UUID's? 

--------

**Finding hidden endpoints**

*Tips*
- Read the documenation. If there's an API, there might be API docs, google them!
- If there is a mobile app but it's not in scope, the app might communicate with a server that is in scope so think outside of the box
- GAU is a great tool to analyse JavaScript files
- Look in the settings if you can find some modules that are not active by default. Every hurdle you take is one that leaves a few other hackers behind
- If there is a paywall, invest. The more you have access to, the better
