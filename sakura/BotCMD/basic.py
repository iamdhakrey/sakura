from discord import asset
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot

class Basic(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot    = bot
        self.color  = 0x232323

    @commands.command(
        brief       = "Show Avatar",
        description = "Shows your or someone avatar",
        aliases     = ['av','dp'],
        help        = "y_help avatar",
        usage       = "y_avatar \ny_avatar @Lunatian#6689"
    )
    async def avatar(self,ctx,*,user:discord.Member = None):
        prBold(f"[Bot] - Avatar cmd used by {ctx.author} on {ctx.author.guild} Discord Server")
        user = user or ctx.author
        embed = discord.Embed(title="Avatar")
        embed.set_author(icon_url=user.avatar_url,name=user)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command(
        brief       = "Check Ping",
        description = "Shows Sakura ping status",
        aliases     = [],
        help        = "y_ping",
        usage       = ""
    )
    async def ping(self,ctx:Context):
        ping = round(self.bot.latency,2)
        data = "Pong 🟢 {}ms ".format(ping)
        embed = discord.Embed(title=None, description=data, color=0x000000)
        await ctx.send(embed=embed)

    @commands.command(
        brief       = "say somethings",
        description = "",
        aliases     = ['says'],
        help        = "y_say text ",
        usage       = ""
    )
    async def say(self,ctx,text:str,*args):
        txt = " ".join((text,)+args)
        await ctx.send(txt)



def setup(bot:Bot):
    bot.add_cog(Basic(bot))