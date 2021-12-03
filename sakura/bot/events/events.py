import discord
from discord.errors import ExtensionAlreadyLoaded, Forbidden

from discord.ext.commands import Bot
from sakura.utils import prBlue, prBold, prCyan, prGreen, prPurple, prRed, prYellow


from sakura.config import COGS_FOLDER,DEFINED_COGS

def event_setup(bot:Bot):
    pass
    @bot.event
    async def on_ready():
        prGreen(f"[Bot] - Logged in as {bot.user.name}")
        prGreen("[Bot] - Sakura Ready to Rock..")
        # for cogs in DEFINED_COGS:
        #     try:
        #         bot.load_extension(COGS_FOLDER+"."+cogs)
        #     except ExtensionAlreadyLoaded as e:
        #         prRed(e)
        #         pass
        # prBold(f"[Bot] - All Extension Loaded")


    @bot.event
    async def on_disconnect():
        prBlue(f"[Bot] - Disconnected! ")
