from sakura.utils import prBold, prYellow
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot

class Moderation(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot    = bot
        self.color  = 0x232323

    @commands.command(
        brief       = "Delete Messages",
        description = "Delete N number of amount messages",
        aliases     = ["purge","clean"],
        help        = "y_help clear",
        usage       = "y_clear 5")
    @has_permissions(administrator=True)
    async def clear(self,ctx,amount: int):
        await ctx.channel.purge(limit=amount+1)

def setup(bot:Bot):
    bot.add_cog(Moderation(bot))