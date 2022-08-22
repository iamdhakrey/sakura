from __future__ import annotations

import discord
from discord.ext.commands.context import Context
from sakura.bot.BotMics.bot_db import DbConnection
from sakura.bot.BotMics.botutils import (eval_reaction_and_role, grep_emojis,
                                         norm_to_emoji)


class SelfRole:
    """
    Self-assignable roles
    """

    async def set_self_role(self, ctx: Context, unique: bool | int,
                            channel: discord.TextChannel, title: str,
                            message: str, emoji_and_role: str):
        """
        Age
        Are You An Adult or a Kid? React with :boy: for Kid and :man: for Adult
        """
        # #channel  unique title | desc | emoji % role | emoji % role

        # breakpoint |

        # check unique must be valid object

        if isinstance(unique, bool):
            if unique:
                maxrole = 1
            else:
                maxrole = 0
        elif isinstance(unique, int):
            maxrole = unique
        else:
            raise TypeError("Unique must be a True or False / Number")

        # created by
        created_by = ctx.author.id

        # channel id
        channel_id = channel.id

        desc = message
        reaction_and_roles = emoji_and_role.split("|")
        print(reaction_and_roles, "gw")

        reaction_and_roles_dict = {}
        for i in reaction_and_roles:
            emoji, role = i.split("%")
            reaction_and_roles_dict[emoji] = role

        print(reaction_and_roles_dict)

        desc = norm_to_emoji(ctx.guild, desc)

        send_emb = discord.Embed(title=title, description=desc, color=0x00ff00)

        emoji_list = grep_emojis(ctx.guild, reaction_and_roles, "%")
        reaction_and_roles = eval_reaction_and_role(ctx.guild,
                                                    reaction_and_roles, "%")

        send_msg = await channel.send(embed=send_emb)

        for i in emoji_list:
            try:
                if discord.utils.get(ctx.guild.emojis,
                                     name=str(i).replace(":", '')):
                    i = discord.utils.get(ctx.guild.emojis,
                                          name=str(i).replace(":", ''))
            except Exception:
                if discord.utils.get(ctx.guild.emojis, name=i):
                    i = discord.utils.get(ctx.guild.emojis, name=i)
            await send_msg.add_reaction(i)

        await DbConnection.fetch_self_role(send_msg.id,
                                           guild_id=ctx.guild.id,
                                           channel_id=channel_id,
                                           max_role=maxrole,
                                           reaction=reaction_and_roles,
                                           created_by=created_by)
        return "self role set Successfully"

    async def get_self_role(self, ctx: Context):
        """
        Get Self-assignable roles
        """
        # fetch all self-assignable roles from db
        selfdata = await DbConnection.fetch_self_role(guild=ctx.guild,
                                                      check_server=True)

        if not selfdata:
            return "No self-assignable roles found", None

        # Embed
        embed = discord.Embed(title="Self-assignable roles",
                              description="",
                              color=0x00ff00)

        # set thumbnails
        embed.set_thumbnail(url=ctx.guild.icon)

        # set footer
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=ctx.guild.icon)

        # set author
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)

        _count = 0

        format_raw = "| {0:<3} | {1:<10} | {2:<10} | {3:<10} | {4:<10} " \
                     "| {5:<10} |\n"
        data = f"""```{format_raw.format(
            "ID", "Title", "Channel   ",
            "Max Role", "Active", "Created_by")}"""
        data += """----------------------------------------------------- \n"""
        for i in selfdata:
            _count += 1
            # find channel
            channel = ctx.guild.get_channel(i.channel_id)
            data += format_raw.format(_count, i.title,
                                      channel.name, i.max_role, i.is_active,
                                      str(i.created_by))

        data = data + "```"
        return data, _count

    async def delete_self_role(self, ctx: Context, self_role_id: int):
        """
        Delete Self-assignable roles
        """
        # fetch all self-assignable roles from db
        selfdata = await DbConnection.fetch_self_role(guild=ctx.guild,
                                                      check_server=True)

        print(selfdata, self_role_id)
        reactionRole = selfdata.pop(self_role_id - 1)
        messageId = reactionRole.message_id
        channelId = reactionRole.channel_id
        print(messageId, channelId)
        await DbConnection.delete_self_role(message_id=messageId)
        return messageId, channelId

    async def edit_self_role(
        self,
        ctx: Context,
        self_role_id: int,
        unique: bool | int,
        title: str,
        message: str,
        emoji_and_role: str,
    ):
        """
        Edit Self-assignable roles
        """
        # fetch all self-assignable roles from db
        selfdata = await DbConnection.fetch_self_role(guild=ctx.guild)
        print(selfdata)

        reactionRole = selfdata.pop(self_role_id - 1)

        # check unique must be valid object
        if isinstance(unique, bool):
            if unique:
                maxrole = 1
            else:
                maxrole = 0
        elif isinstance(unique, int):
            maxrole = unique
        else:
            raise TypeError("Unique must be a True or False / Number")

        # get message object
        messageObj = await discord.utils.get(
            ctx.guild.text_channels,
            id=reactionRole.channel_id).fetch_message(reactionRole.message_id)

        if messageObj is None:
            return "Message not found"

        if reactionRole.max_role != maxrole:
            reactionRole.max_role = maxrole

        if title != reactionRole.title:
            reactionRole.title = title

        if emoji_and_role is None:
            return

        reaction_and_roles = emoji_and_role.replace("@", "").split("|")

        desc = norm_to_emoji(ctx.guild, message)

        embed = discord.Embed(title=title, description=desc, color=0x00ff00)

        emoji_list = grep_emojis(ctx.guild, reaction_and_roles, "%")
        reaction_and_roles = eval_reaction_and_role(ctx.guild,
                                                    reaction_and_roles, "%")

        send_msg = await messageObj.edit(embed=embed)

        for i in emoji_list:
            # print(i)
            try:
                if discord.utils.get(ctx.guild.emojis,
                                     name=str(i).replace(":", '')):
                    i = discord.utils.get(ctx.guild.emojis,
                                          name=str(i).replace(":", ""))
            except Exception:
                if discord.utils.get(ctx.guild.emojis, name=i):
                    i = discord.utils.get(ctx.guild.emojis, name=i)
            # s = '😀'
            # print('U+{:X}'.format(ord(i)))
            # print(i)
            # s = '😀'
            print(i.encode('unicode-escape'))
            print(i.encode('unicode-escape').decode('ASCII'))
            await send_msg.add_reaction(i)

            await DbConnection.update_self_role(
                reactionRole.id,
                guild_id=ctx.guild.id,
                channel_id=reactionRole.channel_id,
                max_role=maxrole,
                reaction=reaction_and_roles,
                updated_by=ctx.author.id)
        return "Reaction Role Update Successfully"
