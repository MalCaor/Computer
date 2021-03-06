# bot.py
import os

import discord

from dotenv import load_dotenv

import json

import feedparser

import time

import threading

# read file
with open('config.json', 'r') as myfile:
    data=myfile.read()

# parse file
conf = json.loads(data)

load_dotenv()
token = conf['token']

client = discord.Client()

# rss feed
rssTest = "http://www.reddit.com/r/python/.rss"
Allrss = conf['Allrss']

# list of post already posted
usedpost = []

# the chan where the post must print
chan = None

# git depot
repoGit = "https://github.com/MalCaor/Computer"

feed = feedparser.parse(rssTest)
Allfeed = []
for rss in Allrss:
    Allfeed.append(feedparser.parse(rss['url']))

update = False

# message event
@client.event
async def on_message(message):
    global update
    global Allfeed
    global chan

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    mess = message.content.lower()

    if mess.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if mess.startswith('!posthere'):
        chan = message.channel
        msg = 'ok, i will post here'
        await message.channel.send(msg)

    if mess.startswith('!num'):
        msg = "false"
        if any(char.isdigit() for char in mess):
            msg = "true"
        await message.channel.send(msg)

    if mess.startswith('!git'):
        msg = "Here is the github repo " + repoGit
        await message.channel.send(msg)

    # Name Feed Test
    if mess.startswith('!feedtestname'):
        msg = feed['feed']['title']
        await message.channel.send(msg)

    # Desc Feed Test
    if mess.startswith('!feedtestdesc'):
        msg = feed.feed.subtitle
        await message.channel.send(msg)

    if mess.startswith('!startpost'):
        update = True
        up.start()
        r = await up.update()
        await message.channel.send(msg)

    if mess.startswith('!sup'):
        if update:
            msg = 'True'
        else:
            msg = 'False'
        await message.channel.send(msg)

    if mess.startswith('!stoppost'):
        update = False
        msg = 'Iv stop posting'
        await message.channel.send(msg)

    # Link Feed Test
    if mess.startswith('!feedtestlink'):
        msg = feed['feed']['link']
        await message.channel.send(msg)

    if mess.startswith('!feedadd'):
        newfeedstr = mess.replace('!feedadd ', '')
        newfeed = feedparser.parse(newfeedstr)
        if('title' in newfeed.feed):
            Allfeed.append(newfeed)
            msg = 'feed have been add'
        else:
            msg = 'error feed incorect'
        await message.channel.send(msg)

    # Array Feed Top
    if mess.startswith('!feedtop'):
        y = len(Allfeed)
        if any(char.isdigit() for char in mess):
            y = ""
            for char in mess:
                if char.isdigit():
                    y = y + char
            y = int(y)
        if y > len(Allfeed):
            msg = "num too big, the current lenght is " + len(Allfeed)
        elif "desc" in mess :
            msg = ""
            for x in range(len(Allfeed) - (len(Allfeed)-y)):
                msg = msg + "* "+Allfeed[x]['feed']['subtitle'] + "\n"
        elif "name" in mess :
            msg = ""
            for x in range(len(Allfeed) - (len(Allfeed)-y)):
                msg = msg + "* "+Allfeed[x]['feed']['title'] + "\n"
        elif "link" in mess :
            msg = ""
            for x in range(len(Allfeed) - (len(Allfeed)-y)):
                msg = msg + "* "+Allfeed[x]['feed']['link'] + "\n"

        #msg = str(y)
        await message.channel.send(msg)


# UPDATE
class updatePost (threading.Thread):
    async def update(lol):
        print('update')
        global update
        global chan
        global usedpost
        while update:
            print('update is true')
            for feed in Allfeed:
                time.sleep(1)
                i = 0
                print('the feed')
                for post in feed.entries:
                    print('the post')
                    if post not in usedpost:
                        #enter it in use
                        usedpost.append(post)
                        # print the post
                        msg = '-----\n'
                        msg = msg + "+++ **" + post.title + "** +++" + "\n"
                        msg = msg + "+ *" + post.author + "* +" + "\n"
                        msg = msg + post.summary + "\n"
                        msg = msg + post.link + "\n"
                        msg = msg + '-----\n'
                        try :
                            await chan.send(msg)
                        except :
                            await chan.send("error")
                        time.sleep(5)
                        # only 5 post per time
                        i = i + 1
                        if(i>5):
                            break
            time.sleep(30)


    def stop(self):
        self._stop_event.set()

up = updatePost()

client.run(token)