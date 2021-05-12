import discord
from discord.ext.commands import Bot
from sakura.utils import prGreen, prPurple, prRed, prYellow
from sakura.BotMics.bot_db import DbConnection

def event_setup(bot:Bot):
    @bot.event
    async def on_ready():
        prGreen(f"[Bot] - Logged in as {bot.user.name}")
        prGreen("[Bot] - Sakura Ready to Rock..")

    @bot.event
    async def on_connect():
        prGreen(f"[Bot] - Connected! ")

    @bot.event
    async def on_disconnect():
        prRed(f"[Bot] - Disconnected! ")

    @bot.event
    async def on_guild_join(guild):
        prYellow(f'[Bot] - Guild join -> {guild.name}')
        await DbConnection.fetch_server(guild)
        await DbConnection.fetch_welcome(guild)

    @bot.event 
    async def on_guild_remove(guild):
        prPurple(f'[Bot] - Guild Remove -> {guild.name}')
        await DbConnection.left_server(guild)