# bot.py
import os

import discord

from dotenv import load_dotenv

import json

import feedparser

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

# git depot
repoGit = "https://github.com/MalCaor/Computer"

feed = feedparser.parse(rssTest)
Allfeed = []
for rss in Allrss:
    Allfeed.append(feedparser.parse(rss['url']))

# message event
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    mess = message.content.lower()

    if mess.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
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


client.run(token)