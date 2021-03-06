import discord
import time
from discord.ext import commands
import datetime
import base64
import requests
import os
from pathlib import Path
from XSONotifications import XSOMessage, XSNotifier

# Intializes bot and it's options.
token = ''
def config():
    global token
    f_temp = Path('token.txt')
    f_temp.touch(exist_ok=True)  # will create file, if it exists will do nothing
    f = open("token.txt", "r+")
    token = f.readline()
    if token == None or token == '':
        token = input("Enter token: ")
        f.write(token)
        f.close()

config()

prefix = '*'
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, self_bot=True)

XSNotifier = XSNotifier()

@bot.event
async def on_ready():
    print(f"XSNotifications_discord is running.")

@bot.event
async def on_message(message):
    if (isinstance(message.channel, discord.channel.DMChannel) or bot.user in message.mentions) and message.author != bot.user: 
        msg = XSOMessage()
        msg.messageType = 1
        msg.sourceApp = "Discord"
        msg.opacity = 0.7
        msg.audioPath = ""
        msg.content = ""
        msg.useBase64Icon = True

        msg.title = str(message.author)

        if message.channel.type == discord.ChannelType.private:
            msg_type = "DM"
            msg.title += f"<space=1em><size=80%> {msg_type}"
        else:
            msg_type = message.guild.name
            msg.title += f"<space=1em><size=80%> {msg_type} - {message.channel.name}"

        msg.content += message.clean_content
        
        ava_url = str(message.author.avatar_url)
        ava_url = ava_url.rsplit(".", 1)[0] + ".jpg"
        icon = base64.b64encode(requests.get(ava_url).content)
        msg.icon = icon.decode('utf-8')
        
        XSNotifier.send_notification(msg)

bot.run(token, bot=False)