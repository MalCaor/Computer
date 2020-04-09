# Computer
---

Computer is a Discord Bot made in python for Technology Watch (or other) 
It search if there is new post in all the feed given
ps: first real project in python so it will *probably* be bad

---

**How to install :**
*Maybe i will make a install.sh once the bot is finished*

First you need those python library :
* os
* discord
* dotenv
* json
* feedparser
* time
* threading

Then create a config.json :

> { 
>   "token"  : "Your bot token here",
>   "prefix" : "the prefix to call the bot",
>   "Allrss" : [
>     {"url" : "http://FirstFeed/.rss"},
>     {"url" : "https://SecondFeed/.rss"},
>     {"url" : "https://etc.../.rss"}
>   ]
> }

Final step :
> python3 Computer.py

And now the bot should work... maybe?

**How to use it :**

1. test if ready with
> !hello
if the bot respond is ok... else i probably fucked up something
(sometime it take a litle time to be ready (5s max))

2. say to the bot where post the feed with
> !posthere

3. start the post with
> !startpost