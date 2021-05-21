from sakura.BotMics.bot_db import DbConnection
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import ast 
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot

class Moderation(commands.Cog):
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

    @commands.command()
    @has_permissions(administrator=True)
    async def add_admin(self,ctx:Context,member:discord.Member):
        lis =  []
        server = await DbConnection.fetch_server(ctx.guild)
        if server.admin:
            server_admin = ast.literal_eval(server.admin)
            if member.id not in server_admin:
                server_admin.append(member.id)
                await DbConnection.fetch_server(ctx.guild,admin=server_admin)
                ctx.reply("Admin Member list updated on sakura server")
            else:
                ctx.reply("Member Already added in list")
        else:
            lis.append(member.id)
            await DbConnection.fetch_server(ctx.guild,admin=lis)
            ctx.reply("Admin Member list updated on sakura server")

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

def setup(bot:Bot):
    bot.add_cog(Moderation(bot))