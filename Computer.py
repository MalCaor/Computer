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

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!num'):
        msg = "false"
        if any(char.isdigit() for char in message.content):
            msg = "true"
        await message.channel.send(msg)

    if message.content.startswith('!git'):
        msg = "Here is the github repo " + repoGit
        await message.channel.send(msg)

    # Name Feed Test
    if message.content.startswith('!feedtestNAME'):
        msg = feed['feed']['title']
        await message.channel.send(msg)

    # Desc Feed Test
    if message.content.startswith('!feedtestDESC'):
        msg = feed.feed.subtitle
        await message.channel.send(msg)

    # Link Feed Test
    if message.content.startswith('!feedtestLINK'):
        msg = feed['feed']['link']
        await message.channel.send(msg)

    if message.content.startswith('!feedAdd'):
        newfeedstr = message.content.replace('!feedAdd ', '')
        newfeed = feedparser.parse(newfeedstr)
        if('title' in newfeed.feed):
            Allfeed.append(newfeed)
            msg = 'feed have been add'
        else:
            msg = 'error feed incorect'
        await message.channel.send(msg)

    # Array Feed Top
    if message.content.startswith('!feedTop'):
        y = len(Allfeed)
        if any(char.isdigit() for char in message.content):
            y = ""
            for char in message.content:
                if char.isdigit():
                    y = y + char
            y = int(y)
        if y > len(Allfeed):
            msg = "num too big, the current lenght is " + len(Allfeed)
        elif "Desc" in message.content :
            msg = ""
            for x in range(len(Allfeed) - (len(Allfeed)-y)):
                msg = msg + "* "+Allfeed[x]['feed']['subtitle'] + "\n"
        elif "Name" in message.content :
            msg = ""
            for x in range(len(Allfeed) - (len(Allfeed)-y)):
                msg = msg + "* "+Allfeed[x]['feed']['title'] + "\n"
        elif "Link" in message.content :
            msg = ""
            for x in range(len(Allfeed) - (len(Allfeed)-y)):
                msg = msg + "* "+Allfeed[x]['feed']['link'] + "\n"

        #msg = str(y)
        await message.channel.send(msg)


client.run(token)