from __future__ import annotations

import discord
from discord.ext.commands.context import Context
from sakurabkp.BotMics.bot_db import DbConnection
from sakurabkp.BotMics.botutils import (eval_reaction_and_role, grep_emojis,
                                     norm_to_emoji)


class WelcomeCommon:
    """
    Self-assignable roles
    """

    async def set_welcome(self, ctx: Context, unique: bool | int,
                          channel: discord.TextChannel, title: str,
                          message: str, emoji_and_role: str):
        """
        Age
        Are You An Adult or a Kid? React
        """
        pass