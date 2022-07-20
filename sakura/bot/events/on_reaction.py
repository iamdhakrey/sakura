
import discord
import django
from discord.ext.commands import Bot
from sakura.BotMics.bot_db import DbConnection
from sakura.utils import prBold


def event_setup(bot: Bot):

    @bot.event
    async def on_raw_reaction_add(payload):
        reaction = payload.emoji
        msg_id = payload.message_id
        ch_id = payload.channel_id
        username = payload.member
        user_id = payload.user_id
        guild_id = payload.guild_id

        if user_id == bot.user.id:
            return

        try:
            reaction_data = await DbConnection.fetch_self_role(msg_id)
        except django.db.utils.IntegrityError:
            return

        # get maximum number of reactions or reactions per user
        max_role = reaction_data.max_role
        # get reaction and role dict
        emoji_role_dict = eval(reaction_data.reaction)

        # get guild object
        guild = bot.get_guild(guild_id)

        emoji = discord.utils.get(guild.emojis, name=reaction.name)

        if reaction.animated:
            emoji = reaction
        else:
            emoji = reaction

        if emoji.name in emoji_role_dict.keys():
            role_id = emoji_role_dict[emoji.name]
            # getting discord.Role object
            role = discord.utils.get(username.guild.roles, id=role_id)
            if role:
                await username.add_roles(role)
                await username.send(
                    f"{username.display_name} has been given {role.name}")

        # get discord.Channel object
        channel = discord.utils.get(username.guild.channels, id=ch_id)
        # get discord.Message object
        msg = await channel.fetch_message(msg_id)
        if max_role == 1:
            # remove reacted emoji in dict
            if emoji in emoji_role_dict.keys():
                del emoji_role_dict[emoji.name]
            # get member roles and store in list
            member_roles = [role.id for role in username.roles]
            for emoji, role in emoji_role_dict.items():
                if role in member_roles:
                    await msg.remove_reaction(emoji, username)

    @bot.event
    async def on_raw_reaction_remove(payload):
        reaction = payload.emoji
        msg_id = payload.message_id
        # ch_id = payload.channel_id
        username = payload.member
        user_id = payload.user_id
        guild_id = payload.guild_id
        guild_name = bot.get_guild(guild_id)

        if user_id == bot.user.id:
            return

        try:
            reaction_data = await DbConnection.fetch_self_role(msg_id)
        except django.db.utils.IntegrityError:
            return
        emoji_role_dict = eval(reaction_data.reaction)
        # get Discord.Emoji object
        print(guild_name.emojis, reaction.name)
        emoji = discord.utils.get(guild_name.emojis, name=reaction.name)
        prBold(emoji)
        if emoji.animated:
            emoji = emoji
        else:
            emoji = reaction

        # get discord.Guild object
        guild = bot.get_guild(guild_id)

        # get discord.User object
        username = guild.get_member(user_id)
        if emoji.name in emoji_role_dict.keys():
            role_id = emoji_role_dict[emoji.name]
            role = discord.utils.get(guild.roles, id=role_id)
            if role:
                await username.remove_roles(role)
                await username.send(
                    f"{username.display_name} has been removed {role.name}")
