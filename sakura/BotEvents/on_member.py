import os
from random import choice,randint
from sakura.BotMics.image import save_image
from sakura.BotMics.botutils import norm_to_emoji
from sakura.BotMics.bot_db import DbConnection
from django.conf import settings
from sakura.utils import prCyan, prPurple
from discord.ext.commands import Bot
import discord
import requests
from PIL import Image,ImageOps,ImageDraw,ImageFont
from io import BytesIO

ROOT_PATH = str(settings.MEDIA_ROOT)

def event_setup(bot:Bot):
    @bot.event
    async def on_member_join(member:discord.Member):
        member_id = member.id
        member_name = member.name +"#"+member.discriminator
        member_tag = "<@"+str(member_id)+">"  
        prCyan(f'[Bot] - Member join -> {member.name}')
        welcome_data = await DbConnection.fetch_welcome(member.guild)
        if welcome_data.welcome_enable is None and welcome_data.self_role is None:
            return
        
        if welcome_data.welcome_channel:
            w_channel = discord.utils.get(member.guild.channels,id=int(welcome_data.welcome_channel))
        
        if w_channel is None:
            return
        if welcome_data.self_role:
            role = discord.utils.get(member.guild.roles,id=int(welcome_data.self_role))
            await member.add_roles(role)
        
        w_msg = welcome_data.welcome_msg
        
        temp_welcome_msg = norm_to_emoji(member.guild,welcome_data.welcome_msg).split("\n")
        welcome_msg = []

        for msg in temp_welcome_msg:
            wlmsg = msg
            if "member.mention" in msg:
                wlmsg = str(msg).replace("{"+"member.mention"+"}",member_tag)

            if "member.name" in msg:
                wlmsg = str(msg).replace("{"+"member.name"+"}",member_name)

            if "member.count" in msg:
                wlmsg = str(msg).replace("{"+"member.count"+"}",str(member.guild.member_count))

            if "member.server_name" in msg:
                wlmsg = str(msg).replace("{"+"member.server_name"+"}",str(member.guild.name))
            
            welcome_msg.append(wlmsg)
        embed = discord.Embed(
            description = "".join(welcome_msg)
        )
        save_image(bot,member.guild,member)
        file = discord.File(open(str(member.guild.id)+"_out_welcome.png", 'rb'))
        embed.set_image(url="attachment://"+str(member.guild.id)+"_out_welcome.png")
        await w_channel.send(embed=embed,file=file)

    @bot.event 
    async def on_member_remove(guild):
        prPurple(f'[Bot] - Guild Remove -> {guild.name}')