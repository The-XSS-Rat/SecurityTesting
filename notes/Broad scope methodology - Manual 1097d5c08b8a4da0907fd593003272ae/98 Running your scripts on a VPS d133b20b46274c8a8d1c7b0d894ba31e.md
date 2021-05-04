# 98 Running your scripts on a VPS

# Introduction

Sometimes we want to hunt from our laptops, sometimes from our desktops and sometimes even from our phones. Sometimes we want to run a small quick command, sometimes we want to run a full network scan of all ports + TCP ports. Sometimes we want to make a reverse shell connection, sometimes we want to generate an exploit. Sometimes we hunt at home, sometimes we hunt at a friends house. Not everyone has the money to pay for a proper laptop, others do but prefer the comfort of the cloud.

Whatever your reason might be, i think a VPS is a great tool in the arsenal of any hunter. There are many use cases that we can think of to buy a VPS and i personally recommend linode because they take prepaid credit cards, but you also have digital ocean, aws and an army of VPS providers that can help you in your needs. 

Free 100$ credit on linode:

[https://linode.gvw92c.net/ELJZW](https://linode.gvw92c.net/ELJZW)

# Requirements

Let's start off with talking about what kind of VPS you need because a lot of people seem to wonder about this. Basically the cheapest VPS you can find will be more than sufficient, It's much better to scale vertically and add another VPS if you need to.

For reasons of keeping all your files and commands in one place you might want to consider getting a bigger VPS but most providers let you upgrade without any problem later down the line.

My linode configuration consists of 2 small nanodes.

![98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e/Untitled.png](98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e/Untitled.png)

Location is also very important, if you are located in the EU, you don't want a server in the USA because it will lag it a lot. You have to pick the location closest to you.

![98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e/Untitled%201.png](98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e/Untitled%201.png)

Backups also matter, if you are serious about putting scripts on your VPS, you should consider working with github but for the results and other configurations, you should consider enabling back-up settings. On linode, it's just 2$ a month extra.

![98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e/Untitled%202.png](98%20Running%20your%20scripts%20on%20a%20VPS%20d133b20b46274c8a8d1c7b0d894ba31e/Untitled%202.png)

Now that you have a VPS, you can set up some stuff.

# Cronjobs

We need two folders on our server, one that will hold our custom nuclei templates and one that will hold our files which have subdomains lists in them. We then need to create a bash script that will scan our folder to see if new files exist. We can easily do this by making an MD5 hash of the folder and seeing if it differs from the one we made last time. If even one bit is different, our whole MD5 hash will differ as well.

THIS IS PSEUDOCODE, FORM THIS INTO YOUR SCRIPTING LANGUAGE OF CHOICE!

```python
newSum=`ls domains | md5sum`
oldSum=`cat oldSum.txt`
echo "$value"
if Newsum!=oldSum{
		  StartNuclei(Templates);
			WriteNewHashToFile(oldSum.txt,newSum);
}
```

This will need to run every so often so we can set up a cronjob for this.

```bash
crontab -e
* */1 * * * checkDomains.sh
```

This cronjob will execute our checkDomain script every hour

We can do the same for a script which will check for new templates, that way we can simply upload them and check our results a few hours later without starting a nuclei command. This makes it so that we can 

- Add FTP to the template folder
- Easily upload new templates via FTP
- Automatic scanning of our domains when a new template exists

```bash
oldSum= 'cat oldSum.txt'
newSum= 'ls templates | md5sum'
lastScanDate=`cat lastScanDate.txt`
echo "$value"
	if Newsum!=oldSum{
		  StartNuclei(getTemplateDate(),lastScanDate);
			WriteNewHashToFile(oldSum.txt,newSum);
			updateLastScanDate()
}
```

This will again need to run every so often so we will put it in another cronjob

```bash
crontab -e
* */1 * * * checkDomains.sh
* */1 * * * checkTemplates.sh
```

We can also add a script that will regularly check for new subdomains

```bash
amass enum -d $1 >> domains-$1.com.txt &
python3 dnsrecon.py -d $1 -D 5000.txt -t brt >> domains-$1.com.txt &
...
sort -u domains-$1.com.txt
```

This script will run amass , dnsrecon , ... and any other script we set to it and send the output to a file which will contain the domain name. Afterwards sort -u will remove all duplicate entries. This will prevent our file size from exploding with duplicate entries.

And then we can again put this in a cronjob to make it run every now and again but we can enter a parameter since we used to $1 in the script. This will take the first parameter and get the value.

```bash
crontab -e
* */1 * * * checkDomains.sh
* */1 * * * checkTemplates.sh
* * * */1 * domainScan.sh google.com
* * * */1 * domainScan.sh tesla.com
* * * */1 * domainScan.sh yahoo.com
```

Now it's up to us to create new templates and put them in the templates folder or we can expand the scripts to add things like httprobe.

```bash
amass enum -d $1 >> domains-$1.com.txt &
python3 dnsrecon.py -d $1 -D 5000.txt -t brt >> domains-$1.com.txt &
...
sort -u domains-$1.com.txt
cat domains-$1.com.txt | httprobe >> live-domains-$1.com.txt
```

Ofcourse we need to take into account that the more we add, the longer these scripts will run so make sure you give them enough time in the crontab. If we would run them every hour and they take two hours to complete, we will get more and more scripts starting up which will crash your server pretty soon.