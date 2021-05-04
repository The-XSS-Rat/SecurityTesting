# 1. Injection

# Introductions

When OWASP talks about injection flaws it's refering to flaws that allow for anything ranging from low impact issues (HTML injection) to critical bugs (SQLi allowing for dropping of table). Basically anything in between can also be mentioned here like LDAP injection, OS command injection, ... . These vulnerabilities all have one thing in common, their root cause. They all occur because developer pass unsanitised data from the user to an interpreter.  

# What is it?

If you are a developer you've probably written some queries by now, these queries might sometimes take user input as well, for example:

```bash
SELECT * FROM PRODUCTS WHERE TEXT LIKE '%" . $_GET['q'] . "%';
```

This innocent looking line of code can mess up a lot if we don't sanitize the user input properly. A malicious user might enter a quote here which would interrupt the SQL statement and allow for the execution of user submitted queries. As you can imagine this is not something desireable and we have many different types of injection. Today we will be going over several of them and we will be looking at the from different viewpoints. We also need to note SQL injection is just a small part of this puzzel and we will go over command injection as well.

# SQL injection

## Hacker's POV

As a hacker, my point of view is going to be one of trying to rely on the fact that the developer will need to sanitize all my data and if they forget to do that at even just 1 point i might have a possible entry point for attacks. This is why my strategy as a test will depend very heavily on testing every single parameter that i see and and even the ones i don't see directly. 

Since we can test for both SQLi and blind SQLi, this complicates matters. Blind SQLi is where the server will not return any values for us to process, we can only test this method by sending a query which is known to cause a delay but this has several issues that come along:

- Any lag can cause a delay in the response making it seem like the blind SQLi triggered while it did not
- You need to know what DB your target uses so you can specificy a command for that server
- Blind SQLi testing is harder on calls that are already slow by nature, you will have to implement a very long wait to see if it is applied correctly

With this in mind, we will try to test every single parameter we can find for SQLi if we have a suspiscion of database queries being executed which we can control. A typical practical example you will find out there is SQLi on login and while this may happen on a pentest, it never does on a bug bounty target. That would just be way too obvious, we will have to look for those hidden parameters in javascript files, hidden form fields, waybackmachine and whatever else we can think of.

We typically test with a single and double quote 

```bash
'"
```

When we see a SQL error, we will investigate further, either with tools like [SQLmap.py](http://sqlmap.py) or manually, though we have to note this does not work for blind SQLi.

## Developer's POV

A developer has a really tough job when it comes to SQLi protection, not only do they have to sanitize every parameter the user can control directly but they also have to think about indirect influence over their application. For example there might be batch jobs running that pick up files, the contents of those files often do need to be sanitized but that's not always easy. 

When third part applications start sending our application data, it becomes a total mess very easily and it's super easy to slip up and forget to sanitize one piece of information which could set off a chain reaction that you do not want to get deducted from your paycheque. 

As a developer you would do wise to follow some basic security principles to negate or avoid these kinds of attacks.

- Principle of least needed privilidges: If you have a query that needs to read from the database only, then maybe we don't need a user for that which can write or even delete data. If possible, we should always keep our users seperate wherever possible so that if we do get hacked, the hacker might have the least amount of priviledges possible
- Objection relationship mapping: What the developer can also do is create objects and then map those to certain database fields. When a query then needs to get executed, the query will happen on the collection of data objects and no longer on the database itself, taking away a big attack vector for SQLi
- Prepared statements: For places where you do need to interact with the database directly, it is always recommend to use prepared statements. They will be safer to use than to straight up create a database request.
- Whatever we decide to do, it is vital to sanitize user input wherever it interacts with our program

# OS Command injection

## What is it?

Command injection happens when we can control a parameter that gets passed into a shell. If that input is not handled safely and sanitised properly, we can insert a command into our input and have that executed by the shell. Depending on the capabilities and privilidges of that shell, we can execute various commands.

The theory sounds very simple however it's not simple at all to find this kind of vulnerability.

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/Command%20injection%20f3446f65fdc9437b9c16ef96b33edc36/Untitled.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/Command%20injection%20f3446f65fdc9437b9c16ef96b33edc36/Untitled.png)

## Attack strategy

The reason command injection is so hard to find is because we never really know which of our processes will trigger a back-end shell to execute. This means we will need to fuzz every parameter we find but you might be wondering what characters to fuzz with. To determine this, we first need to talk about which command separators can possibly be used and also which commands.

### Separators

The following command separators work on both Windows and Unix-based systems:

- `&`
- `&&`
- `|`
- `||`

The following command separators work only on Unix-based systems:

- `;`
- Newline (`0x0a` or `\n`)

On Unix-based systems, you can also use backticks or the dollar character to perform inline execution of an injected command within the original command:

- ``` injected command ```
- `$(` injected command `)`

### Commands

Below is a summary of some commands that are useful on Linux and Windows platforms:

[Copy of Linux and windows commands](1%20Injection%20299ca260cd4e4c5e9afcf191d2b8f1e9/Copy%20of%20Linux%20and%20windows%20commands%2000be2c96ca4a45b5adfad32224ecfcdf.csv)

## fuzzing list

Based on this, we can create a fuzzing list that contains all the seperators togheter with all the possible commands. I will leave this up to you as it should be a good exercise. Feel free to contact me on discord if you have issues with this however. 

Fuzz every single parameter you can find with this worldlist by using burp intruder.

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/Command%20injection%20f3446f65fdc9437b9c16ef96b33edc36/Untitled%201.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/Command%20injection%20f3446f65fdc9437b9c16ef96b33edc36/Untitled%201.png)

![../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/Command%20injection%20f3446f65fdc9437b9c16ef96b33edc36/Untitled%202.png](../../Vulnerability%20types%20d6487b7204244f159482be2dfb025fea/Command%20injection%20f3446f65fdc9437b9c16ef96b33edc36/Untitled%202.png)

As you can see in the screenshot, we load in our fuzzing list and mark the parameters we want to test.

## Blind command injection

We can test for blind command injection by launching a request that will execute a ping command to the loopback adress. 

```jsx
& ping -c 10 127.0.0.1 &
```

Again, add this to your fuzzing list and mind the response time for this attack vector. If it's longer than 10 seconds, we probably have a blind command injection but be mindful as lag might occur and give a false positive.