from sakura.bot.BotMics.botutils import norm_to_emoji
import time
from discord import channel, colour, emoji, member, message
from discord.ext import commands
import asyncio
import discord
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
from sakura.bot.BotMics.bot_db import DbConnection
import requests,random,os, json
from discord.ext.commands.context import Context

from discord.ext.commands import bot

class Self_Role(commands.Cog):
    """
    Self-assignable roles
    """
    def __init__(self,bot):
        self.bot = bot

    # @commands.command(
    #     brief="Set self Assign Role msg",
    #     description="Set self Assign Role msg",
    #     aliases=['ssm'],
    #     usage="y_set_self_role_msg <msg>",
    #     help="Set self Assign Role msg",
    # )
    # async def set_self_message(self,ctx:Context,unique,channel : discord.TextChannel = None ,*,msg):
    #     """
    #     Age
    #     Are You An Adult or a Kid? React with :boy: for Kid and :man: for Adult
    #     """
    #     # #channel  unique title | desc | emoji % role | emoji % role

    #     #breakpoint |

    #     if unique == "yes" or unique == 'Yes' or unique == 'YES':
    #         unique = 1
    #     elif unique == 'no' or unique == 'No' or unique == 'NO':
    #         unique = 0 
    #     elif int(unique) > 1:
    #         unique = unique
    #     else:
    #         msg = unique + " " + msg
    #         unique = 0
        

    #     split_msg = str(msg).split("|")

    #     msg = str(msg).split(':')

    #     # grep title and description
    #     title = split_msg.pop(0)
    #     desc =  split_msg.pop(0)
    #     reaction_and_roles = split_msg
        
    #     desc = norm_to_emoji(ctx.guild,desc)
        
    #     send_emb = discord.Embed(
    #         title=title,
    #         description = desc,
    #         color = 0x00ff00
    #     )
    #     send_emb.set_thumbnail(url=ctx.guild.icon_url)
    #     send_msg = await channel.send(embed=send_emb)

    #     emoji_list = em_and_role_split(ctx.guild,reaction_and_roles,"%")

    #     channel_id = channel.id
    #     for i in emoji_list:
    #         try:
    #             if discord.utils.get(ctx.guild.emojis,name=str(i).replace(":",'')):
    #                 i = discord.utils.get(ctx.guild.emojis,name=str(i).replace(":",''))
    #         except:
    #             if discord.utils.get(ctx.guild.emojis,name=i):
    #                 i = discord.utils.get(ctx.guild.emojis,name=i)
    #         await send_msg.add_reaction(i)
        
    #     await DbConnection.fetch_self_role(send_msg.id,guild_id=ctx.guild.id,max_role=unique,reaction=reaction_and_roles)
    #     await ctx.send("Self Role set Successfully")

def setup(bot):
    bot.add_cog(Self_Role(bot))