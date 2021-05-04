# 2. Processing Our List Of Subdomain

# Intro

Now that we have a (hopefully big) list of potential subdomains, a big part of the hard work is over. Yaaaay! But we don't have a vulnerability yet so we will have to keep digging deeper into our list of subdomains to find that hidden gem that hopefully others missed. That's why it's so important to have a really solid list of subdomains and why would should do our subdomain enumeration at such a high level.

We are going to process our list of subdomains with httprobe to see which subdomains are live and which don't even respond at all. We are going to take care to log all subdomains which return an answer. It doesn't matter if we get an error code because error codes also mean that the subdomain is live.

# HTTProbe

The description on the github page of HTTProbe is very simple.

> Take a list of domains and probe for working http and https servers.

We first need to install HTTProbe

```php
go get -u github.com/tomnomnom/httprobe

We also have to make sure the go/bin folder is added to $PATH variable because that's the location of httprobe
export PATH=$PATH:$HOME/go/bin
```

If we don't have go installed, we need to install that as well ofcourse

[https://golang.org/doc/install](https://golang.org/doc/install)

Since i use WSL and ubuntu i execute the following command but it can differ per OS ofcourse

```php
sudo apt install golang-go
```

Now we can start checking the massive list we gathered from the previous chapter.

```php
cat recon/example/domains.txt | httprobe >> working-domains-google.com.twt
```

This will create a new file with all the domains that returned an answer indicating they are alive. By default this will scan port 80 and port 443

We can set several flags but I usually use the default settings as they seem to be sufficient.

# Results

We should now be left with a file that contains nothing but subdomains that are alive but this still isn't going to lead us to any vulnerabilities. We need this list though to continue to the next step. 

This is where we can choose one of two paths:

- Further exploration of the alive domains (indicated by the numbers in front of the chapter titles)
- Vulnerability scanning of the alive domains (indicated by the letters in front of the chapter titles)