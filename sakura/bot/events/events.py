from discord.ext.commands import Bot
from sakura.bot.utils import prBlue, prGreen


def event_setup(bot: Bot):
    """
    Setup the event loop for the bot.
    """
    @bot.event
    async def on_ready():
        prGreen(f"[Bot] - Logged in as {bot.user.name}#{bot.user.discriminator}")
        prGreen("[Bot] - Sakura Ready to Rock..")

    @bot.event
    async def on_disconnect():
        prBlue("[Bot] - Disconnected! ")
