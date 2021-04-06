- Avoid using text files when creating lists with links. Use Markdown instead which makes the links clickable on GitHub.
- Avoid writing the same functions across multiple shell files. For instance, I would recommend writing a single helper function (for -h) which you can import into every script and configure.
- Whenever applicable, try to run things concurrently vs linearly. This is particularly relevant for http://scanMultipleDomains.sh. Now since I have mentioned http://scanMultipleDomains.sh, let me just add I would avoid writing single shell scripts for scanning several hosts vs a single host. You are better off writing you script so that it can process one or many hosts depending on the input. It makes it more user friendly.
- Clean user input instead of expecting the user to know what the input should look like. For example, where the protocol is required, your tool should add the protocol if it's missing. Write a single function for this purpose that can be called everywhere.
- Write the scripts in such a way that a user can add them to their /usr/bin/ or $PATH instead of having to create a copy in every target directory. There is no real need to have multiple copies of the same script everywhere on your machine.

There is more that I would personally change, but this should be enough for you to play around with for now.
