#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Built-in Modules
import pickle

# Third Party Modules
import discord
from discord import app_commands
from discord.ext import commands

# Custom Modules
from config import config

__author__ = "dr34d a.k.a. Tori"
__copyright__ = "Copyright 2023, dr34d"
__license__ = "MIT"
__version__ = "2.0.0"
__date__ = "2023-03-18"
__maintainer__ = "dr34d"
__status__ = "Production"

########################## Editable Defaults #########################
# NOTE: Changing these could affect execution in unpredictable ways! #
######################################################################
logging = True # Set startup state Enabled:True/Disabled:False

######################################################################
#############/ / / / DO NOT EDIT BELOW THIS LINE \ \ \ \##############
######################################################################
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

try:
    with open('excluded_users.conf', 'rb') as f:
        excludedUsers = pickle.load(f)
except:
    excludedUsers = []

@tree.command(name="excludeuser", description="Excludes specified user from logging.", guild=discord.Object(id=config.GUILD_ID))
async def log_exclude_user(interaction, user:discord.User):
    global excludedUsers
    if user.id in excludedUsers:
        await interaction.response.send_message("{displayName} already in Logging Ignore List".format(displayName=user.display_name), ephemeral=True)
    else:
        excludedUsers.append(user.id)
        with open('excluded_users.conf', 'wb') as f:
            pickle.dump(excludedUsers, f)
        await interaction.response.send_message("Adding {displayName} with ID: {userID} to Logging Ignore List".format(displayName=user.display_name, userID=user.id), ephemeral=True)

@tree.command(name="remexcludeuser", description="Removes specified user from logging exclusions.", guild=discord.Object(id=config.GUILD_ID))
async def log_rem_exclude_user(interaction, user:discord.User):
    global excludedUsers
    if user.id in excludedUsers:
        excludedUsers.remove(user.id)
        with open('excluded_users.conf', 'wb') as f:
            pickle.dump(excludedUsers, f)
        await interaction.response.send_message("Removed {displayName} with ID: {userID} from Logging Ignore List".format(displayName=user.display_name, userID=user.id), ephemeral=True)
    else:
        await interaction.response.send_message("{displayName} not in Logging Ignore List".format(displayName=user.display_name), ephemeral=True)

@tree.command(name="listexcludes", description="Lists users excluded from logging.", guild=discord.Object(id=config.GUILD_ID))
async def log_list_exclude_user(interaction):
    excludeListFriendly = []
    guild = client.get_guild(config.GUILD_ID)
    for id in excludedUsers:
        member = guild.get_member(id)
        excludeListFriendly.append(member.display_name)
    await interaction.response.send_message("The following list of users is excluded from logging: {excludes}".format(excludes=excludeListFriendly), ephemeral=True)

@tree.command(name="logrun", description="Enables Logging.", guild=discord.Object(id=config.GUILD_ID))
async def log_run(interaction):
    global logging
    logging = True
    await interaction.response.send_message("Logging Enabled", ephemeral=True)

@tree.command(name="logpause", description="Pauses Logging", guild=discord.Object(id=config.GUILD_ID))
async def log_pause(interaction):
    global logging
    logging = False
    await interaction.response.send_message("Logging Paused", ephemeral=True)

@tree.command(name="logstatus", description="Get logging status", guild=discord.Object(id=config.GUILD_ID))
async def log_status(interaction):
    if logging:
        await interaction.response.send_message("Logging Active", ephemeral=True)
    else:
        await interaction.response.send_message("Logging Paused", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=config.GUILD_ID))
    print("Ready!")

@client.event
async def on_message_edit(before, after):
    if logging:
        if before.author == client.user:
            # Ignore messages edited by the bot
            return
        elif before.author.id in excludedUsers:
            # Ignore excluded users
            return
        elif before.content == after.content:
            # Ignore messages with identical content. This is useful when messages contain gifs or URLs.
            return
        else:
            channel = client.get_channel(config.LOG_CHANNEL)
            embed = discord.Embed(title='Message Edited', color=0xffa500)
            embed.set_author(name=before.author.display_name, icon_url=before.author.avatar.url)
            embed.add_field(name='Before', value=before.content, inline=False)
            embed.add_field(name='After', value=after.content, inline=False)
            if before.attachments:
                attachment_urls = '\n'.join([attachment.url for attachment in before.attachments])
                embed.add_field(name='Attachments', value=attachment_urls, inline=False)
            embed.add_field(name='Jump URL', value=before.jump_url, inline=False)
            embed.set_footer(text=f'Message ID: {before.id} | Author ID: {before.author.id}')
            await channel.send(embed=embed)
    else:
        return

@client.event
async def on_message_delete(message):
    if logging:
        if message.author == client.user:
            # Ignore messages deleted by the bot
            return
        elif message.author.id in excludedUsers:
            # Ignore excluded users
            return
        else:
            channel = client.get_channel(config.LOG_CHANNEL)
            embed = discord.Embed(title='Message Deleted', color=0xff0000)
            embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
            embed.add_field(name='Content', value=message.content, inline=False)
            if message.attachments:
                attachment_urls = '\n'.join([attachment.url for attachment in message.attachments])
                embed.add_field(name='Attachments', value=attachment_urls, inline=False)
            embed.add_field(name='Jump URL', value=message.jump_url, inline=False)
            embed.set_footer(text=f'Message ID: {message.id} | Author ID: {message.author.id}')
            await channel.send(embed=embed)
    else:
        return

client.run(config.BOT_TOKEN)
