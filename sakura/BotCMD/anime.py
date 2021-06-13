from discord import asset, colour
from discord.embeds import Embed
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot


class Anime(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot    = bot
        self.color  = 0x232323

    @commands.command()
    async def kick(self,ctx:Context,member:discord.Member=None):
        kick_gif = "https://media1.tenor.com/images/862272da6f71b28b53ec262bcca6763a/tenor.gif"
        if member is None:
            await ctx.send(kick_gif)
        else:
            embed = Embed()
            embed.set_image(url=kick_gif)
            msg = "or bhai {} aa gya swad".format(member.mention)
            await ctx.send(msg,embed=embed)

def setup(bot:Bot):
    bot.add_cog(Anime(bot))