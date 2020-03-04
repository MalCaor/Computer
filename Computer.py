# bot.py
import os

import discord

from dotenv import load_dotenv

import json

# read file
with open('config.json', 'r') as myfile:
    data=myfile.read()

# parse file
conf = json.loads(data)

load_dotenv()
token = conf['token']

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

client.run(token)