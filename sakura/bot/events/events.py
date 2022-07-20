from discord.ext.commands import Bot
from sakura.utils import prBlue, prGreen


def event_setup(bot: Bot):
    pass

    @bot.event
    async def on_ready():
        prGreen("[Bot] - Logged in as {bot.user.name}")
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
        prBlue("[Bot] - Disconnected! ")
