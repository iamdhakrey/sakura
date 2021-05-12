import discord
from discord.ext.commands import Bot
from discord.ext import commands
from sakura.utils import prBlue, prBold, prCyan, prGreen, prPurple, prRed, prYellow
from sakura.BotMics.bot_db import DbConnection

from sakura.config import COGS_FOLDER,DEFINED_COGS

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
        await DbConnection.fetch_server(guild)
        await DbConnection.fetch_welcome(guild)

    @bot.event 
    async def on_guild_remove(guild):
        prPurple(f'[Bot] - Guild Remove -> {guild.name}')
        await DbConnection.left_server(guild)