import discord
from discord.ext.commands import slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

from sakura.bot.common.basic import Basic as common_basic
from sakura.bot.utils import prBold


class SlashBasic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.common = common_basic()

    @slash_command(
        guild_ids=[738037561712443493],
        description="Say hi to me",
        brief="Say hi to me",
    )
    async def hello(self, ctx):
        prBold(
            f"[Bot] - /Hello used by {ctx.author} on {ctx.author.guild} " +
            " Discord Server"
        )
        await ctx.respond(f"Hi, {ctx.author.name}!")

    @slash_command(
        guild_ids=[738037561712443493],
        description="Show Your or Someone Avatar",
        brief="Show Avatar",
    )
    async def avatar(self, ctx: Context, *, user: discord.Member = None):
        prBold(
            f"[Bot] - /Avatar used by {ctx.author} on {ctx.author.guild}" +
            " Discord Server"
        )
        user = user or ctx.author
        await ctx.respond(embed=await self.common.avatar(ctx, user))

    @slash_command(
        guild_ids=[738037561712443493],
        description="Shows Sakura ping status",
        brief="Check Ping",
    )
    async def ping(self, ctx: Context):
        prBold(
            f"[Bot] - /Ping used by {ctx.author} on {ctx.author.guild} " +
            "Discord Server"
        )
        await ctx.respond(embed=await self.common.ping(ctx))

    @slash_command(
        guild_ids=[738037561712443493],
        aliases=["says"],
        description="saying somethings",
        brief="say somethings",
    )
    async def say(self, ctx: Context, *, text: str):
        prBold(
            f"[Bot] - /Say used by {ctx.author} on {ctx.author.guild} " +
            " Discord Server"
        )
        await ctx.trigger_typing()
        await ctx.respond(text)

    @slash_command(
        guild_ids=[738037561712443493],
        aliases=["about"],
        description="About User",
        brief="About User",
    )
    async def info(self, ctx: Context, *, user: discord.Member = None):
        prBold(
            f"[Bot] - /Info used by {ctx.author} on {ctx.author.guild} " +
            "Discord Server"
        )
        user = user if user else ctx.author
        await ctx.respond(embed=await self.common.info(ctx, user))


def setup(bot):
    bot.add_cog(SlashBasic(bot))
