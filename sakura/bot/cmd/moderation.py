from discord import channel
from discord.errors import Forbidden
from sakura.BotMics.bot_db import DbConnection
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import ast 
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot

class Moderation(commands.Cog):
    """
    Moderation commands
    """
    def __init__(self,bot) -> None:
        self.bot    = bot
        self.color  = 0x232323

    @commands.command(
        brief       = "Delete Messages",
        description = "Delete N number of amount messages",
        aliases     = ["purge","clean"],
        help        = "y_help clear",
        usage       = "y_clear 5")
    @has_permissions(administrator=True)
    async def clear(self,ctx,amount: int):
        await ctx.channel.purge(limit=amount+1)

    @commands.command(
        brief       = "Add admin",
        description = "Add admin to the server",
        aliases     = ["addadmin"],
        help        = "y_help addadmin",
        usage       = "y_addadmin @user"
        )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def add_admin(self,ctx:Context,member:discord.Member):
        lis =  []
        server = await DbConnection.fetch_server(ctx.guild)
        if server.admin:
            server_admin = ast.literal_eval(server.admin)
            if member.id not in server_admin:
                server_admin.append(member.id)
                await DbConnection.fetch_server(ctx.guild,admin=server_admin)
                await ctx.reply("Admin Member list updated on sakura server")
            else:
                await ctx.reply("Member Already added in list")
        else:
            lis.append(member.id)
            await DbConnection.fetch_server(ctx.guild,admin=lis)
            await ctx.reply("Admin Member list updated on sakura server")

    @commands.command(
        brief       = "Remove admin",
        description = "Remove admin from the server",
        aliases     = ["removeadmin"],
        help        = "y_help removeadmin",
        usage       = "y_removeadmin @user"
    )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def remove_admin(self,ctx:Context,member:discord.Member):
        lis =  []
        server = await DbConnection.fetch_server(ctx.guild)
        if server.admin:
            server_admin = ast.literal_eval(server.admin)
            server_admin.remove(member.id)
            await DbConnection.fetch_server(ctx.guild,admin=server_admin)

        else:
            lis.append(member.id)
            await DbConnection.fetch_server(ctx.guild,admin=lis)    

    @commands.command(
        brief       = "Add mod",
        description = "Add mod to the server",
        help        = "y_help add_admin_role",
        usage       = "y_add_admin_role @role"
    )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def add_admin_role(self,ctx:Context,role:discord.Role):
        lis =  []
        server = await DbConnection.fetch_server(ctx.guild)
        if server.admin_role:
            server_admin = ast.literal_eval(server.admin_role)
            if role.id not in server_admin:
                server_admin.append(role.id)
                await DbConnection.fetch_server(ctx.guild,admin_role=server_admin)
                await ctx.reply("Admin Role List updated on Sakura Server")
            else:
                await ctx.reply("Role already in added")
        else:
            lis.append(role.id)
            await DbConnection.fetch_server(ctx.guild,admin_role=lis)
            await ctx.reply("Admin Role List updated on Sakura Server")

    @commands.command(
        brief       = "Remove admin role",
        description = "Remove admin role from the server",
        help        = "y_help remove_admin_role",
        usage       = "y_remove_admin_role @role"
    )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def remove_admin_role(self,ctx:Context,role:discord.Role):
        lis =  []
        server = await DbConnection.fetch_server(ctx.guild)
        if server.admin_role:
            server_admin = ast.literal_eval(server.admin_role)
            if role.id in server_admin:
                server_admin.remove(role.id)
                await DbConnection.fetch_server(ctx.guild,admin_role=server_admin)
                await ctx.reply("Role Remove in list")
            else:
                await ctx.reply("Role not in list")
        else:
            await ctx.reply("No admin Role exists")

    @commands.command(
        brief       = "Ban member",
        description = "Ban member to the server",
        help        = "y_help ban",
        usage       = "y_ban @user"
    )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def ban(self,ctx:Context,member:discord.Member):
        name = member.name
        await member.ban()
        await ctx.reply(f"{name} has been banned")

    @ban.error
    async def ban_error(self,ctx:Context,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.reply("Please mention the member to ban")
        elif isinstance(error,commands.BadArgument):
            await ctx.reply("Please mention the member to ban")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.reply("You don't have permission to ban")
        elif isinstance(error,Forbidden):
            await ctx.reply("You don't have permission to ban")
        else:
            await ctx.reply("Something went wrong")

    @commands.command(
        brief       = "unban member",
        description = """unban member to the server and 
                sends invite link to the user
                invite link will be sent to the user's dm
                invite link is valid for 30 days
                """,
        help        = "y_help unban",
        usage       = 'y_unban "member_full_name#1234"'
    )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def unban(self,ctx:Context,member):
        # get banned users list
        banned_users = await ctx.guild.bans()
        # check if user is banned
        for ban_entry in banned_users:
            user = ban_entry.user
            if (f"{user.name}#{user.discriminator}" == member):
                # generate invite link
                invite = await ctx.channel.create_invite(max_age=30,max_uses=1)
                await user.send(f"You have been unbanned from {ctx.guild.name} \n now you can join again by click on this url: \n {invite}")
                await ctx.guild.unban(user)
                await ctx.reply(f"{user.name} has been unbanned")
                

        # prBold(member)
        # await ctx.guild.unban(member)
        # await ctx.reply(f"{member} has been unbanned")

    @unban.error
    async def unban_error(self,ctx:Context,error):
        if isinstance(error,Forbidden):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error,discord.ext.commands.errors.MissingPermissions):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error,discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.reply("You need to mention a member")
        elif isinstance(error,discord.ext.commands.errors.MemberNotFound):
            await ctx.reply("Member not found")
        else:
            await ctx.reply("Something went wrong")

            

    @commands.command(
        brief       = "Kick member",
        description = "Kick member to the server",
        help        = "y_help kick_user",
        usage       = "y_kick_user @user"
    )
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def kick_user(self,ctx:Context,member:discord.Member):
        await member.kick()
        await ctx.reply(f"{member.name} has been kicked")

    @kick_user.error
    async def kick_user_error(self,ctx:Context,error):
        if isinstance(error,Forbidden):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error,discord.ext.commands.errors.MissingPermissions):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error,discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.reply("You need to mention a member")
        elif isinstance(error,discord.ext.commands.errors.MemberNotFound):
            await ctx.reply("Member not found")
        else:
            await ctx.reply("Something went wrong")
            
            
    @commands.command(
        brief       = "clear all messages",
        description = "Clear all messages from the channel",
        help       = "y_help nuke",
        permission = "manage_messages"
    )
    @commands.is_owner()
    @has_permissions(manage_messages=True)
    async def nuke(self,ctx:Context):
        #  get message
        messages = await channel.history(limit=100).flatten()
        await channel.delete_messages(messages)
        await ctx.reply("Messages deleted")
        
        
    @commands.command(
        brief = "softban a user",
        description = "Soft ban a user for 7 days",
        help = "y_help softban",
        permission = "administator"
    )
    @has_permissions(administrator=True)
    async def softban(self,ctx:Context,user:discord.Member):
        user = user.name
        pass
        
def setup(bot:Bot):
    bot.add_cog(Moderation(bot))