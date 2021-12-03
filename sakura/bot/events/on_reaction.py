import os
import discord
from random import randint
from sakura.BotMics.botutils import em_and_role_split
from sakura.BotMics.bot_db import DbConnection
from django.conf import settings
import django
from sakura.utils import prBold,  prPurple
from discord.ext.commands import Bot

def event_setup(bot:Bot):
    @bot.event
    async def on_raw_reaction_add(payload):
        reaction = str(payload.emoji)
        msg_id = payload.message_id
        ch_id = payload.channel_id
        username = payload.member
        user_id = payload.user_id
        guild_id = payload.guild_id

        try:
            reaction_data = await DbConnection.fetch_self_role(msg_id)
        except django.db.utils.IntegrityError:
            return
        max_role = reaction_data.max_role
        _,emoji_role_dict = em_and_role_split(eval(reaction_data.reaction),"%")

        emoji = reaction.split(":")[1].strip()
        member =  await payload.member.guild.fetch_member(user_id)
        roles_list = []
        for emoji_dict in emoji_role_dict:
            roles_list.append(int(str(emoji_role_dict[emoji_dict]).replace("<@&",'').replace(">",'')))
            if emoji == emoji_dict:
                role = payload.member.guild.get_role(int(str(emoji_role_dict[emoji_dict]).replace("<@&",'').replace(">",'')))
                await member.add_roles(role)
                prBold(f"[Bot] - {member} Role added -> {role}")
        
        if max_role is None:
            return
        member_roles_count = 1
        for list_roles in roles_list:
            for member_roles in member.roles:
                if int(list_roles) == int(member_roles.id):
                    member_roles_count += 1

        channel = discord.utils.get(payload.member.guild.channels,id = ch_id)        
        dis_msg = await channel.fetch_message(int(msg_id))
        while(member_roles_count > max_role):
            rand = randint(0,len(roles_list))
            role = payload.member.guild.get_role(int(roles_list[rand]))
            remove_emoji = None
            for key,values in emoji_role_dict.items():
                if int(str(values).replace('<@&','').replace('>','')) == int(role.id):
                    try:
                        if discord.utils.get(payload.member.guild.emojis,name=str(key).replace(":",'')):
                            key = discord.utils.get(payload.member.guild.emojis,name=str(key).replace(":",''))
                    except:
                        if discord.utils.get(payload.member.guild.emojis,name=key):
                            key = discord.utils.get(payload.member.guild.emojis,name=key)
                    remove_emoji = key
            await member.remove_roles(role)
            member_roles_count -= 1
            await dis_msg.remove_reaction(remove_emoji,member)
            roles_list.remove(roles_list[rand])
            prBold(f"[Bot] - {member} Role removed {role}")
                        
    @bot.event 
    async def on_raw_reaction_remove(payload):
        reaction = str(payload.emoji)
        msg_id = payload.message_id
        ch_id = payload.channel_id
        username = payload.member
        user_id = payload.user_id
        guild_id = payload.guild_id
        guild_name = bot.get_guild(guild_id)

        member = guild_name.get_member(user_id)
        try:
            reaction_data = await DbConnection.fetch_self_role(msg_id)
        except django.db.utils.IntegrityError:
            return
        max_role = reaction_data.max_role
        _,emoji_role_dict = em_and_role_split(eval(reaction_data.reaction),"%")

        emoji = reaction.split(":")[1].strip()
        roles_list = []
        for emoji_dict in emoji_role_dict:
            roles_list.append(int(str(emoji_role_dict[emoji_dict]).replace("<@&",'').replace(">",'')))
            if emoji == emoji_dict:
                role = member.guild.get_role(int(str(emoji_role_dict[emoji_dict]).replace("<@&",'').replace(">",'')))
                await member.remove_roles(role)
                prBold(f'[Bot] - {member} Role Remove -> {role}')