import discord
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from sakura.bot.common.moderation import Moderation as Moderation_Common
from sakura.bot.utils import prBold


class Moderation(commands.Cog):
    """
    Moderation commands
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.color = 0x232323
        self.common = Moderation_Common()

    @commands.command(brief="Delete Messages",
                      description="Delete N number of amount messages",
                      aliases=["purge", "clean"],
                      help="y_help clear",
                      usage="y_clear 5")
    @has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        prBold(
            f"[Bot] - clear cmd used by {ctx.author} on {ctx.author.guild}" +
            " Discord Server")
        await self.common.clear(ctx, amount)

    @commands.command(brief="Add admin",
                      description="Add admin to the server",
                      aliases=["addadmin"],
                      help="y_help addadmin",
                      usage="y_addadmin @user")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def add_admin(self, ctx: Context, member: discord.Member):
        await ctx.reply(await self.common.add_admin(ctx, member))

    @commands.command(brief="Remove admin",
                      description="Remove admin from the server",
                      aliases=["removeadmin"],
                      help="y_help removeadmin",
                      usage="y_removeadmin @user")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def remove_admin(self, ctx: Context, member: discord.Member):
        await ctx.reply(await self.common.remove_admin(ctx, member))

    @commands.command(brief="Add mod",
                      description="Add mod to the server",
                      help="y_help add_admin_role",
                      usage="y_add_admin_role @role")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def add_admin_role(self, ctx: Context, role: discord.Role):
        await ctx.reply(await self.common.add_admin_role(ctx, role))

    @commands.command(brief="Remove admin role",
                      description="Remove admin role from the server",
                      help="y_help remove_admin_role",
                      usage="y_remove_admin_role @role")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def remove_admin_role(self, ctx: Context, role: discord.Role):
        await ctx.reply(await self.common.remove_admin_role(ctx, role))

    @commands.command(brief="Ban member",
                      description="Ban member to the server",
                      help="y_help ban",
                      usage="y_ban @user")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def ban(self, ctx: Context, member: discord.Member):
        await ctx.reply(await self.common.ban(ctx, member))

    @ban.error
    async def ban_error(self, ctx: Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Please mention the member to ban")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Please mention the member to ban")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You don't have permission to ban")
        elif isinstance(error, Forbidden):
            await ctx.reply("You don't have permission to ban")
        else:
            await ctx.reply("Something went wrong")

    @commands.command(brief="unban member",
                      description="""unban member to the server and
                                  sends invite link to the user
                                  invite link will be sent to the user's dm
                invite link is valid for 30 days
                """,
                      help="y_help unban",
                      usage='y_unban "member_full_name#1234"')
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def unban(self, ctx: Context, member):
        await ctx.reply(await self.common.unban(ctx, member))

    @unban.error
    async def unban_error(self, ctx: Context, error):
        if isinstance(error, Forbidden):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error,
                        discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.reply("You need to mention a member")
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.reply("Member not found")
        else:
            await ctx.reply("Something went wrong")

    @commands.command(brief="Kick member",
                      description="Kick member to the server",
                      help="y_help kick_user",
                      usage="y_kick_user @user")
    @commands.is_owner()
    @has_permissions(administrator=True)
    async def kick_user(self, ctx: Context, member: discord.Member):
        await ctx.reply(await self.common.kick_user(ctx, member))

    @kick_user.error
    async def kick_user_error(self, ctx: Context, error):
        if isinstance(error, Forbidden):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.reply("You don't have permission to unban")
        elif isinstance(error,
                        discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.reply("You need to mention a member")
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.reply("Member not found")
        else:
            await ctx.reply("Something went wrong")

    @commands.command(brief="clear all messages",
                      description="Clear all messages from the channel",
                      help="y_help nuke",
                      permission="manage_messages")
    @commands.is_owner()
    @has_permissions(manage_messages=True)
    async def nuke(self, ctx: Context):
        await ctx.reply(await self.common.nuke(ctx))

    @commands.command(brief="softban a user",
                      description="Soft ban a user for 7 days",
                      help="y_help softban",
                      permission="administator")
    @has_permissions(administrator=True)
    async def softban(self, ctx: Context, user: discord.Member):
        await ctx.reply(await self.common.softban(ctx, user))


def setup(bot: Bot):
    bot.add_cog(Moderation(bot))
