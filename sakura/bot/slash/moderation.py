import discord
from discord.ext.commands import slash_command
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.context import Context

from sakura.bot.common.moderation import Moderation as ModerationCommon
from sakura.bot.utils import prBold


class SlashModeration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.common = ModerationCommon()

    @slash_command(guild_ids=[738037561712443493],
                   brief="Delete messages",
                   description="Delete N number of messages")
    @has_permissions(administrator=True)
    async def delete(self, ctx: Context, number: int):
        prBold(f"[Bot] - /delete used by {ctx.author} on {ctx.author.guild}" +
               " Discord Server")
        await self.common.clear(ctx, number)
        await ctx.respond(f"{number} messages deleted")

    @slash_command(guild_ids=[738037561712443493],
                   brief="Add admin to sakura",
                   description="Add admin to the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def add_admin(self, ctx: Context, member: discord.Member):
        await ctx.respond(f"{await self.common.add_admin(ctx, member)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="Remove admin from sakura",
                   description="Remove admin from the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def remove_admin(self, ctx: Context, member: discord.Member):
        await ctx.respond(f"{await self.common.remove_admin(ctx, member)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="add admin role to sakura server",
                   description="add admin role to the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def add_admin_role(self, ctx: Context, role: discord.Role):
        await ctx.respond(f"{await self.common.add_admin_role(ctx, role)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="remove admin role from sakura server",
                   description="remove admin role from the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def remove_admin_role(self, ctx: Context, role: discord.Role):
        await ctx.respond(f"{await self.common.remove_admin_role(ctx, role)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="ban user from  server",
                   description="ban user from the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def ban(self, ctx: Context, member: discord.Member):
        await ctx.respond(f"{await self.common.ban(ctx, member)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="unban user from  server",
                   description="unban user from the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def unban(self, ctx: Context, member):
        await ctx.respond(f"{await self.common.unban(ctx, member)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="kick user from  server",
                   description="kick user from the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def kick_user(self, ctx: Context, member: discord.Member):
        await ctx.respond(f"{await self.common.kick_user(ctx, member)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="nuke the server",
                   description="nuke the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def nuke(self, ctx: Context):
        await ctx.respond(f"{await self.common.nuke(ctx)}")

    @slash_command(guild_ids=[738037561712443493],
                   brief="softban user from  server",
                   description="solfban user from the server")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def softban(self, ctx: Context, member: discord.Member):
        await ctx.respond(f"{await self.common.softban(ctx, member)}")


def setup(bot):
    bot.add_cog(SlashModeration(bot))
