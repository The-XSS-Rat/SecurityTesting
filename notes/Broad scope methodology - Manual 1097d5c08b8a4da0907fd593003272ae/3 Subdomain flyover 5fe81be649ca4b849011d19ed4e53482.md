# 3. Subdomain flyover

# Introduction

Now that we have a list of subdomains which we know are alive, we are going to want to investigate them more closely. We have several things we can do to these domains but we want to start by getting a good overview of what each domain might have to offer and then we move on to a more manual approach which will resemble a penester like approach (Numbered sections) In the other learning path (Lettered sections) we will be learning a more automated approach to vulnerability scanning. Both have to be done to be complete and one can not go withouth the other. We will miss a lot with automation but we can cover so much more ground than when we manually walk the application.

# What is it?

When we execute subdomain flyover, we are trying to get an overview of what targets we have. We need to see what this list actually contains and i mean the world 'See' literally, we are going to take screenshots. 

In subdomain flyover we are trying to take a screenshot of all of the alive domain we gathered in our previous steps 1 & 2. We have several tools we can use to do this, i personally use aquatone but i notice i am getting old and may not be as up to date as i was so i encourage you to do your own research a bit as well into which tools runs faster. They all basically do the same thing anyway. The endgame is the screenshots and maybe the HTML file but we can grab that by navigating to the page.

# Meet aquatone

[https://github.com/michenriksen/aquatone](https://github.com/michenriksen/aquatone)

1. Install [Google Chrome](https://www.google.com/chrome/) or [Chromium](https://www.chromium.org/getting-involved/download-chromium) browser -- **Note:** Google Chrome is currently giving unreliable results when running in *headless* mode, so it is recommended to install Chromium for the best results.
2. Download the [latest release](https://github.com/michenriksen/aquatone/releases/latest) of Aquatone for your operating system.
3. Uncompress the zip file and move the `aquatone` binary to your desired location. You probably want to move it to a location in your `$PATH` for easier use.
    1. You can also add the binary to your `$PATH` variable
    2. export $PATH='$PATH:/location/of/bin'

We want to use the chromium browser because what aquatone will do is it will open a headless session in a browser. A headless session basically means it starts up chromium like it normally would and has all the capabilities of controlling it (Such as to make HTTP GET requests so it can navigate to a page and take a screenshot) but we won't even see it as a user. To us, it will be like a background application running without user interaction. Aquatone does this to improve speed and since the operations it has to do are not very complex, it can easily perform them in a less stable headless browser.

We run aquatone but piping the output of our file into aquatone. This command will only work if the aquatone binary is in the `$PATH` as discussed before so if it's not working that's the first place i would look.

```jsx
$ cat targets.txt | aquatone
```

# Results

The output should be a folder structure that shows us a screenshot of all the domains that we had in our list so that we can nicely pick manually have a look and see what domains are of interest to us. So let's have a look at how to interpret these screenshots shall we.

## Custom made login portals

These always catch my eye, you know the login portal that has been made by the intern on a friday night that looks like it comes from the 80's? Yeah well, those always draw my eye. I may be taking a laugh at it but if a developer had to write it themselves that means that they also had to protect every single page behind the login portal properly. This is something that's very hard to do as it requires either a solution that will be general and automatically implemented on every page or they will have to pay close attention to every new page they create to make sure it has the proper authentication and authorization controls.

Practically this translates into me doing content discovery any of these login portals that i encounter on my hunts. I will usually use the content discovery engagement tool from burp suite but i realise this is a pro feature and easy enough to understand (just make sure to rate limit it properly) we will be talking about fuff in this course, though please note their are a whole host of tools available to do directory brute forcing.

Notice how i said content discovery in the previous paragraph? That's because we will be doing more than just directory brute forcing. We also want to check for files in those directories that resolve ofcourse like images or webpages or maybe even stuff we are not supposed to see like excel files?

### Fuff

[https://github.com/ffuf/ffuf](https://github.com/ffuf/ffuf)

- [Download](https://github.com/ffuf/ffuf/releases/latest) a prebuilt binary from [releases page](https://github.com/ffuf/ffuf/releases/latest), unpack and run!

    *or*

- If you have recent go compiler installed: `go get -u github.com/ffuf/ffuf` (the same command works for updating)

    *or*

- git clone [https://github.com/ffuf/ffuf](https://github.com/ffuf/ffuf) ; cd ffuf ; go get ; go build

If you go with the pre-built binary or if you install fuff from the go package or from scratch you will again need to make sure that it's in your path variable if you want to use it or that you in the directory where you have the binary. 

```jsx
export $PATH='$PATH:/location/of/bin'
```

When we use fuff, the quality of our results will depend on the quality of our wordlists, we will talk more about that later but first let's learn a bit about how to run fuff because you can two ways with the basic command. Wherever we put FUZZ in our attack string, fuff will replace that with the value from the wordlist we specify.

```jsx
ffuf -w /path/to/wordlist -u https://target/FUZZ
ffuf -w /path/to/wordlist -u https://target/FUZZ.php 
			(or .aspx or .html or nothing at all depening on the webserver our target uses)
```

As you can see in our running examples we can either try to fuzz a directory or a file itself. Depending on the configuration of our target, one or both might be desired as some targets use URL rerouting (not using a file extension in the URL to hide the webserver tech) in which case file fuzzing will not be useful,  or might just straight up display the file extension in which case file fuzzing will be very useful.

We can also use fuff to fuzz for parameters if we want.

```jsx
ffuf -w /path/to/wordlist -u https://target/index.php?FUZZ
```

### Wordlists

The quality of our wordlists will determine the quality of our results. Whenever we are working with wordlists this saying stands true. We have several options for creating wordlists, we can either take pre-built list like one from the expansive lists that Daniel Miessler provides over at [https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists) . Now you can just take the biggest wordlist you can find but as you can see we have quite a few options already. We can fuzz for either endpoints, files or parameters and usually we want to do this recursively as well. This can all take quite a while and the bigger the wordlists, the bigger of a time you will spend waiting and not hunting.

I can't recommend you a list for every single target out there as every target is different but here are some general pointers:

- Pick a list that's as small as possible but still relevant. There's no point in using a wordlist with just 3 values on it and also no point in using a list with 4 billion values.
- Pick a list that's specific to your target. Attacking an API? Pick an API list, not a CMS list! Attacking a CMS? Pick the correct CMS! Go as specific as possible.
- Pick a specific list for every target, don't just use the same list on all of the subdomains you found. You might be testing too much or too little otherwise.
- Not sure if your wordlist fits your target? Reach out to someone and ask some tips but make sure you don't disclose results you are not allowed to or even details such as the target name.

## Webshops

Whenever i see a screenshot of webshop, i will initiate my normal webshop strategy where i will

- Register for an account
    - Test the registration and forgot password system
- Actually buy a product
    - Try to find an IDOR on the invoices, on the cart system and anything that has an ID on it
- Return that product
    - Repeat my whole IDOR routine on the return process
- Try to passively look for XSS in the background (See my XSS Course [http://hackxpert.com/](http://hackxpert.com/))
- Maybe look for XXE or SSRF along the way
- Try for Blind XSS when i see a contact form

## Blogs

I will usually skip these as they don't contain a lot of functionality for me to test.

## Misc

Any strange thing i see, i will look deeper into.