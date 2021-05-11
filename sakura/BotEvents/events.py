import discord
from discord.ext.commands import Bot
from sakura.utils import prGreen, prRed, prYellow

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
