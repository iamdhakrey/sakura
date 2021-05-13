from typing import no_type_check
from sakura.BotMics.bot_db import DbConnection
from discord import channel
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot
from sakura.BotMics.botutils import norm_to_emoji

class Welcome(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot    = bot
        self.color  = 0x232323
    
    @commands.command(aliases=['swm','set_welcome'])
    @has_permissions(administrator=True)
    async def set_welcome_message(self,ctx:Context,set_channel,*,msg=None):
        if msg is None:
            msg = ""

        if set_channel is not None:
            if str(set_channel).startswith('<#'):
                channel_id = str(set_channel).split(">")[0].replace("<#",'')
            else:
                msg += set_channel

        msg = norm_to_emoji(ctx,msg)
        if discord.utils.get(self.bot.get_all_channels(),id = int(channel_id)):
            channel_id = channel_id
        else:
            data = DbConnection.fetch_welcome(ctx.guild)
            channel_id =  data.welcome_channel
        await DbConnection.fetch_welcome(ctx.guild,
            welcome_msg = msg,
            welcome_channel = channel_id 
            )
    
    @commands.command(aliases=['welcome_check','cw'])
    @has_permissions(administrator=True)
    async def check_welcome(self,ctx:Context,*,msg:str):
        msg = norm_to_emoji(ctx,msg)
        embed = discord.Embed(
            description = msg,
        )
        await ctx.send(embed=embed)

def setup(bot:Bot):
    bot.add_cog(Welcome(bot))