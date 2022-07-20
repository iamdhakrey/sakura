# from __future__ import annotations
import asyncio
import discord
from discord.ext.commands import slash_command
from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ui import Select

from sakura.BotMics.botutils import unicode_emoji
from sakura.bot.common.self_role import SelfRole
from sakura.utils import prBold

# from discord.ext.commands import Option
from discord import Option


class SlashSelfRole(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.self_role = SelfRole()

    @slash_command(guild_ids=[738037561712443493],
                   name="selfrole",
                   brief="Add self role to sakura",
                   description="Add self role to the server")
    @commands.is_owner()
    async def set_self_role(
        self,
        ctx: Context,
        unique: Option(bool or int,
                       default=True,
                       description="number of role to add") = True,
        channel: Option(discord.TextChannel,
                        description="channel to send message") = None,
        title: Option(str, description="title of message") = None,
        message: Option(str, description="message to send") = None,
        emoji_and_role: Option(
            str, description="emoji '%' role **|** emoji '%' role ") = None,
    ):

        _self_response = await self.self_role.set_self_role(
            ctx, unique, channel, title, message, emoji_and_role)

        await ctx.respond(_self_response)

    @slash_command(guild_ids=[738037561712443493],
                   name="get-selfrole",
                   brief="Get self role from sakura",
                   description="Get self role from the server")
    @commands.is_owner()
    async def get_self_role(
        self,
        ctx: Context,
    ):
        embed, count = await self.self_role.get_self_role(ctx)
        await ctx.respond(embed)

    @slash_command(guild_ids=[738037561712443493],
                   name="del-selfrole",
                   brief="Delete self role from sakura",
                   description="Delete self role from the server")
    @commands.is_owner()
    async def del_self_role(
        self,
        ctx: Context,
        id: Option(
            int,
            description="id of self role. For id use get_selfrole") = None,
    ):
        if id is None:
            await ctx.respond("Fetching self role...")
            id = await self.get_roles_and_send_reaction(ctx)
        if id is None:
            return await ctx.respond(
                f"{prBold('Error')} : {prBold('No reaction')}")

        id = int(id)
        message_id, channelId = await self.self_role.delete_self_role(ctx, id)

        try:
            message = await discord.utils.get(
                ctx.guild.text_channels,
                id=channelId).fetch_message(message_id)

        except discord.errors.NotFound:
            return await ctx.send("Error: No message")

        await message.delete()
        return await ctx.send("Self Role Successfunlly removed")
        # get message objec

    @slash_command(guild_ids=[738037561712443493],
                   name="edit-selfrole",
                   brief="Edit self role from sakura",
                   description="Edit self role from the server")
    @commands.is_owner()
    async def edit_self_role(
        self,
        ctx: Context,
        id: Option(int,
                   description="id of self role. For id use get_selfrole"),
        unique: Option(bool or int,
                       description="number of role to add") = True,
        title: Option(str, description="title of message") = None,
        message: Option(str, description="message to send") = None,
        emoji_and_role: Option(
            str, description="emoji '%' role **|** emoji '%' role ") = None,
        # color: Option(discord.Colour,description="color of embed") = None,
    ):
        _edit_response = await self.self_role.edit_self_role(
            ctx, id, unique, title, message, emoji_and_role)
        await ctx.respond(_edit_response)

    async def get_roles_and_send_reaction(self, ctx: Context):
        embed, count = await self.self_role.get_self_role(ctx)
        await ctx.send(embed)
        if count == 0 or count is None:
            return None
        select = Select()
        for i in range(count):
            await select.add_option(f"{i+1}", f"{i+1}")
            # await mes.add_reaction(unicode_emoji.get(f"{i + 1 }"))

        def check(reaction, user):
            return user == ctx.author and str(
                reaction.emoji) in unicode_emoji.values()

        # get reaction
        # wait 30 sec for reaction and return id
        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     timeout=30,
                                                     check=check)
        except asyncio.TimeoutError:
            return
        else:
            # return unicode emoji key which matching with reaction emoji
            if reaction.emoji in unicode_emoji.values():
                for key, value in unicode_emoji.items():
                    if value == str(reaction.emoji):
                        return key
            else:
                return None


def setup(bot):
    bot.add_cog(SlashSelfRole(bot))
