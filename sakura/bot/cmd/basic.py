import time
from discord import asset, guild
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot
from discord.app.commands import slash_command

class Basic(commands.Cog):
    """
    Basic commands
    """
    def __init__(self,bot:discord.Bot) -> None:
        self.bot    = bot
        self.color  = 0x232323
        self.bot.application_command(name='avatar',description="Show your or someone avatar",guild_ids=[738037561712443493],cls=discord.SlashCommand)(self.avatar_slash)

    @slash_command(guild_ids=[738037561712443493]) # Create a slash command for the supplied guilds.
    async def hello(self, ctx):
        await ctx.respond("Hi, this is a slash command from a cog!")
    

    @slash_command(guild_ids=[738037561712443493]) 
    async def hi(self, ctx):
        await ctx.respond(f"Hi, this is a global slash command from a cog!")
        
        
    async def common_avatar(self,ctx:Context,user:discord.Member):
        embed = discord.Embed(title="Avatar")
        embed.set_author(icon_url=user.avatar,name=user)
        embed.set_image(url=user.avatar)
        return embed
    
    @commands.command(
        brief       = "Show Avatar",
        description = "Shows your or someone avatar",
        aliases     = ['av','dp'],
        help        = "y_help avatar",
        usage       = "y_avatar @Lunatian#6689"
    )
    async def avatar(self,ctx,*,user:discord.Member = None):
        prBold(f"[Bot] - Avatar cmd used by {ctx.author} on {ctx.author.guild} Discord Server")
        user = user or ctx.author
        await ctx.send(embed=await self.common_avatar(ctx,user))
    
    async def avatar_slash(self, ctx:Context, user: discord.Member = None):
        prBold(f"[Bot Slash] - Avatar cmd used by {ctx.author} on {ctx.author.guild} Discord Server")
        user = user or ctx.author
        await ctx.respond(embed=await self.common_avatar(ctx,user))
        
    async def common_ping(self,ctx:Context):
        # embed = discord.Embed(title="Ping")
        ping = round(self.bot.latency,2)
        data = "Pong 🟢 {}ms ".format(ping)
        embed = discord.Embed(title=None, description=data, color=0x000000)
        return embed
    
    @commands.command(
        brief       = "Check Ping",
        description = "Shows Sakura ping status",
        aliases     = [],
        help        = "y_ping",
        usage       = ""
    )
    async def ping(self,ctx:Context):
        prBold(f"[Bot] - Ping cmd used by {ctx.author} on {ctx.author.guild} Discord Server")
        await ctx.send(embed=await self.common_ping(ctx))
        
    @slash_command(guild_ids=[738037561712443493],name='ping',description="Show Sakura ping status") # Create a slash command for the supplied guilds.
    async def ping_slash(self, ctx:Context):
        prBold(f"[Bot Slash] - Ping cmd used by {ctx.author} on {ctx.author.guild} Discord Server")
        await ctx.respond(embed=await self.common_ping(ctx))

    @commands.command(
        brief       = "say somethings",
        description = "saying somethings",
        aliases     = ['says'],
        help        = "y_say text ",
        usage       = ""
    )
    async def say(self,ctx:Context,text:str,*args):
        txt = " ".join((text,)+args)
        await ctx.trigger_typing()    
        await ctx.send(txt)
        
    @slash_command(
        guild_ids=[738037561712443493],
        name='say',
        description="say something"
        )
    async def say_slash(self, ctx:Context, text:str):
        txt = " ".join((text,))
        await ctx.trigger_typing()
        await ctx.respond(txt)    

def setup(bot:Bot):
    bot.add_cog(Basic(bot))