import os
from os import makedirs

from discord.ext.commands import Bot
from django.conf import settings
from sakura.BotMics.bot_db import DbConnection
from sakura.utils import prCyan, prPurple


def event_setup(bot: Bot):

    @bot.event
    async def on_guild_join(guild):
        prCyan(f'[Bot] - Guild join -> {guild.name}')
        if os.path.exists(
                str(settings.MEDIA_ROOT) + '/images/' + str(guild.id)):
            pass
        else:
            makedirs(str(settings.MEDIA_ROOT) + '/images/' + str(guild.id))
        await DbConnection.fetch_server(guild)
        await DbConnection.fetch_welcome(guild)

    @bot.event
    async def on_guild_remove(guild):
        prPurple(f'[Bot] - Guild Remove -> {guild.name}')
        await DbConnection.left_server(guild)
