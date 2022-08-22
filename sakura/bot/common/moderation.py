import ast
import discord
from discord import channel
from discord.ext.commands.context import Context
from sakura.bot.BotMics.bot_db import DbConnection


class Moderation:
    """
    Moderation commands
    """

    async def clear(self, ctx, amount: int):
        """
        Delete Messages
        """
        await ctx.channel.purge(limit=amount + 1)

    async def add_admin(self, ctx: Context, member: discord.Member):
        """
        Add admin to the server
        """
        lis = []
        # fetching server from db
        server = await DbConnection.fetch_server(ctx.guild)
        # check if server admin list is not empty
        if server.admin:
            # if not empty then convert admin list to list
            server_admin = ast.literal_eval(server.admin)
            # check if member is already in admin list
            if member.id not in server_admin:
                # if not in admin list then add member to admin list
                server_admin.append(member.id)
                # update admin list in db
                await DbConnection.fetch_server(ctx.guild, admin=server_admin)
                # return message
                return f"{member} is now admin on {ctx.guild.name} server"
            else:
                # if member is already in admin list then return message
                return f"{member} is already admin on {ctx.guild.name} server"
        else:
            # if admin list is empty then add member to admin list
            lis.append(member.id)
            # update admin list in db
            await DbConnection.fetch_server(ctx.guild, admin=lis)
            # return message
            return f"{member} is now admin on {ctx.guild.name} server"

    async def remove_admin(self, ctx: Context, member: discord.Member):
        """
        remove admin from the server
        """
        # lis = []
        # fetching server from db
        server = await DbConnection.fetch_server(ctx.guild)
        # check if server admin list is not empty
        if server.admin:
            # if not empty then convert admin list to list
            server_admin = ast.literal_eval(server.admin)
            # check if member is already in admin list
            if member.id in server_admin:
                # if in admin list then remove member from admin list
                server_admin.remove(member.id)
                # update admin list in db
                await DbConnection.fetch_server(ctx.guild, admin=server_admin)
                # return message
                return f"{member} is now admin on {ctx.guild.name} server"
            else:
                # if member is not in admin list then return message
                return f"{member} is not admin on {ctx.guild.name} server"
        else:
            # if admin list is empty then return message
            return f"{member} is not admin on {ctx.guild.name} server"

    async def add_admin_role(self, ctx: Context, role: discord.Role):
        """
        add role to admin group
        """
        lis = []
        # fetching server from db
        server = await DbConnection.fetch_server(ctx.guild)
        # check if server admin role list is not empty
        if server.admin_role:
            # if not empty then convert admin role list to list
            server_admin = ast.literal_eval(server.admin_role)
            # check if role is already in admin role list
            if role.id not in server_admin:
                # if not in admin role list then add role to admin role list
                server_admin.append(role.id)
                # update admin role list in db
                await DbConnection.fetch_server(ctx.guild,
                                                admin_role=server_admin)
                # return message
                return f"{role} is now admin role on {ctx.guild.name} server"
            else:
                # if role is already in admin role list then return message
                return f"{role} is already admin role on {ctx.guild.name} " \
                        " server"
        else:
            # if admin role list is empty then add role to admin role list
            lis.append(role.id)
            # update admin role list in db
            await DbConnection.fetch_server(ctx.guild, admin_role=lis)
            # return message
            return f"{role} is now admin role on {ctx.guild.name} server"

    async def remove_admin_role(self, ctx: Context, role: discord.Role):
        """
        remove role from admin group
        """
        # fetching server from db
        server = await DbConnection.fetch_server(ctx.guild)
        # check if server admin role list is not empty
        if server.admin_role:
            # if not empty then convert admin role list to list
            server_admin = ast.literal_eval(server.admin_role)
            # check if role is already in admin role list
            # if role is in admin role list then remove
            # role from admin role list
            if role.id in server_admin:
                # if in admin role list then remove role from admin role list
                server_admin.remove(role.id)
                # update admin role list in db
                await DbConnection.fetch_server(ctx.guild,
                                                admin_role=server_admin)
                # return message
                return f"{role} is removed in admin role on " \
                       " {ctx.guild.name} server"
            else:
                # if role is not in admin role list then return message
                return f"{role} is not admin role on {ctx.guild.name} server"
        else:
            # if admin role list is empty then return message
            return f"{role} is not admin role on {ctx.guild.name} server"

    async def ban(self, ctx: Context, member: discord.Member):
        """
        ban member from the server
        """
        name = member.name
        # ban member from the server
        await member.ban()
        # return message
        return f"{name} is banned from {ctx.guild.name} server"

    async def unban(self, ctx: Context, member):
        """
        unban member from the server
        """
        # get banned users list
        banned_users = await ctx.guild.bans()
        # check if user is banned
        for ban_entry in banned_users:
            # if user is banned then unban user
            user = ban_entry.user
            if (f"{user.name}#{user.discriminator}" == member):
                # generate invite link for 30 days
                invite = await ctx.channel.create_invite(max_age=30,
                                                         max_uses=1)
                # send msg to user with invite link
                await user.send(
                    f"You have been unbanned from {ctx.guild.name} " +
                    f"now you can join again by click on this url: \n {invite}"
                )
                # unban user
                await ctx.guild.unban(user)
                # return message
                return f"{user} is unbanned from {ctx.guild.name} server"
        # if user is not banned then return message
        return f"{member} is not banned from {ctx.guild.name} server"

    async def kick_user(self, ctx: Context, member: discord.Member):
        """
        kick member from the server
        """
        name = member.name
        # kick member from the server
        await member.kick()
        # return message
        return f"{name} is kicked from {ctx.guild.name} server"

    async def nuke(self, ctx: Context):
        """
        nuke the server
        """
        #  get message
        messages = await channel.history(limit=100).flatten()
        # delete all messages
        await channel.delete_messages(messages)
        # return message
        return f"{ctx.guild.name} server is nuked"

    async def softban(self, ctx: Context, user: discord.Member):
        """
        softban member from the server
        """
        user = user.name
        return "Not implemented yet"
