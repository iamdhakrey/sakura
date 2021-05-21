from os import makedirs, mkdir
import os
import discord
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from sakura.utils import prBlue, prBold, prCyan, prGreen, prPurple, prRed, prYellow
from sakura.BotMics.bot_db import DbConnection

from django.conf import settings

from sakura.config import COGS_FOLDER,DEFINED_COGS,SAKURA_DEBUG

def event_setup(bot:Bot):
    @bot.event
    async def on_ready():
        prGreen(f"[Bot] - Logged in as {bot.user.name}")
        prGreen("[Bot] - Sakura Ready to Rock..")
        for cogs in DEFINED_COGS:
            try:
                bot.load_extension(COGS_FOLDER+"."+cogs)
            except commands.errors.ExtensionAlreadyLoaded:
                pass
        prBold(f"[Bot] - All Extension Loaded")

    @bot.event
    async def on_connect():
        prGreen(f"[Bot] - Connected! ")

    @bot.event
    async def on_disconnect():
        prBlue(f"[Bot] - Disconnected! ")

    @bot.event
    async def on_guild_join(guild):
        prCyan(f'[Bot] - Guild join -> {guild.name}')
        if os.path.exists(str(settings.MEDIA_ROOT)+'/images/'+str(guild.id)):
            pass
        else:
            makedirs(str(settings.MEDIA_ROOT)+'/images/'+str(guild.id))
        await DbConnection.fetch_server(guild)
        await DbConnection.fetch_welcome(guild)

    @bot.event 
    async def on_guild_remove(guild):
        prPurple(f'[Bot] - Guild Remove -> {guild.name}')
        await DbConnection.left_server(guild)

    @bot.event
    async def on_command(ctx:Context):
        cmd = str(ctx.command).replace(ctx.prefix,'').capitalize()
        if SAKURA_DEBUG:
            prBold(f"[CMD] - {cmd} used by {ctx.author.name}#{ctx.author.discriminator}")
        
    @bot.event
    async def on_command_error(ctx:Context,error):
        if SAKURA_DEBUG:
            if isinstance(error,commands.CommandError):
                if isinstance(error,commands.CommandNotFound):
                    cmd = str(ctx.message.content).replace(ctx.prefix,'').split()[0]
                    prYellow(f"[CMD_Not_Found] - {cmd} execute by {ctx.author.name}#{ctx.author.discriminator}")
                
                if isinstance(error, MissingRequiredArgument):
                    cmd = str(ctx.message.content).replace(ctx.prefix,'').split()[0]
                    prBlue(f'[CMD required Missing] - {cmd} {str(error).split()[0]} is missing')
                
                else:
                    prBlue(error)
            else:
                prBlue(error)
        else:
            prBlue(error)