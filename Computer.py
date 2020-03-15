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
Allrss = ["http://www.reddit.com/r/python/.rss",
    "https://www.reddit.com/r/programming/.rss",
    "https://www.reddit.com/r/AskProgramming/.rss",
    "https://www.reddit.com/r/linux/.rss",
    "https://feeds.feedburner.com/TheHackersNews.rss"]

feed = feedparser.parse(rssTest)
Allfeed = []
for rss in Allrss:
    Allfeed.append(feedparser.parse(rss))

# message event
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
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

    # Array Feed Top
    if message.content.startswith('!feedTop'):
        y = len(Allrss)
        if "Desc" in message.content :
            msg = ""
            for x in range(len(Allrss) - (len(Allrss)-y)):
                msg = msg + Allfeed[x]['feed']['subtitle'] + "\n"
        elif "Name" in message.content :
            msg = ""
            for x in range(len(Allrss) - (len(Allrss)-y)):
                msg = msg + Allfeed[x]['feed']['title'] + "\n"
        elif "Link" in message.content :
            msg = ""
            for x in range(len(Allrss) - (len(Allrss)-y)):
                msg = msg + Allfeed[x]['feed']['link'] + "\n"

        await message.channel.send(msg)


client.run(token)