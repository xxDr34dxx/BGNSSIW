#!/usr/bin/python3
# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

__author__ = "dr34d a.k.a. Tori"
__copyright__ = "Copyright 2023, dr34d"
__license__ = "MIT"
__version__ = "1.1.0"
__date__ = "2023-03-14"
__maintainer__ = "dr34d"
__status__ = "Production"

### Mandatory Variables ###
BOT_TOKEN = ''
LOG_CHANNEL = 123456

### Defaults ###
# NOTE: Changing these could affect execution in unpredictable ways!
MAGICCHAR = '!'

###########################################################
########/ / / / DO NOT EDIT BELOW THIS LINE \ \ \ \########
###########################################################
client = commands.Bot(MAGICCHAR,intents=discord.Intents.all())

@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        # Ignore messages edited by the bot
        return
    else:
        channel = client.get_channel(LOG_CHANNEL)
        embed = discord.Embed(title='Message Edited', color=0xffa500)
        embed.set_author(name=before.author.display_name)
        embed.add_field(name='Before', value=before.content, inline=False)
        embed.add_field(name='After', value=after.content, inline=False)
        if before.attachments:
            attachment_urls = '\n'.join([attachment.url for attachment in before.attachments])
            embed.add_field(name='Attachments', value=attachment_urls, inline=False)
        embed.add_field(name='Jump URL', value=before.jump_url, inline=False)
        embed.set_footer(text=f'Message ID: {before.id} | Author ID: {before.author.id}')
        await channel.send(embed=embed)

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        # Ignore messages deleted by the bot
        return
    else:
        channel = client.get_channel(LOG_CHANNEL)
        embed = discord.Embed(title='Message Deleted', color=0xff0000)
        embed.set_author(name=message.author.display_name)
        embed.add_field(name='Content', value=message.content, inline=False)
        if message.attachments:
            attachment_urls = '\n'.join([attachment.url for attachment in message.attachments])
            embed.add_field(name='Attachments', value=attachment_urls, inline=False)
        embed.add_field(name='Jump URL', value=message.jump_url, inline=False)
        embed.set_footer(text=f'Message ID: {message.id} | Author ID: {message.author.id}')
        await channel.send(embed=embed)

client.run(BOT_TOKEN)
