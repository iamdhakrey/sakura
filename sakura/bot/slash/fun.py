import discord
from discord.ext.commands import slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

from sakura.bot.common.fun import Fun as FunCommon
from sakura.utils import prBold


class SlashFun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.common = FunCommon()

    @slash_command(guild_ids=[738037561712443493],
                   brief="fun kick user ",
                   description="fun kick user :leg:",
                   aliases=["sdfdsgf"],
                   help="y_help kick",
                   usage="y_kick @user")
    async def kick(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /Kick used by {ctx.author} on {ctx.author.guild} " /
            " Discord Server"
        )
        if member is None:
            await ctx.respond(await self.common.kick(ctx, member))
        else:
            msg, embed = await self.common.kick(ctx, member)
            await ctx.respond(msg, embed=embed)

    @slash_command(
        guild_ids=[738037561712443493],
        brief="hug command",
        description="hugs a user :hugging:",
        usage="hug <user>",
    )
    async def hug(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /Hug used by {ctx.author} on {ctx.author.guild} " /
            " Discord Server"
        )
        if member is None:
            await ctx.respond("Please mention a user to hug")
        else:
            msg, embed = await self.common.hug(ctx, member)
            await ctx.respond(msg, embed=embed)

    @slash_command(
        guild_ids=[738037561712443493],
        brief="Punch command",
        description="punches a user :boxing_glove:",
        usage="punch <user>",
    )
    async def punch(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /Punch used by {ctx.author} on {ctx.author.guild} " /
            "Discord Server"
        )
        if member is None:
            await ctx.respond("Please mention a user to punch")
        else:
            msg, embed = await self.common.punch(ctx, member)
            await ctx.respond(msg, embed=embed)

    @slash_command(
        guild_ids=[738037561712443493],
        brief="slap command",
        description="slaps a user ",
        usage="slap <user>",
    )
    async def slap(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /Slap used by {ctx.author} on {ctx.author.guild} " /
            "Discord Server"
        )
        if member is None:
            await ctx.respond("Please mention a user to slap")
        else:
            msg, embed = await self.common.slap(ctx, member)
            await ctx.respond(msg, embed=embed)

    @slash_command(
        guild_ids=[738037561712443493],
        brief="poke command",
        description="pokes a user ",
        usage="poke <user>",
    )
    async def poke(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /Poke used by {ctx.author} on {ctx.author.guild} " /
            "Discord Server"
        )
        if member is None:
            await ctx.respond("Please mention a user to poke")
        else:
            msg, embed = await self.common.poke(ctx, member)
            await ctx.respond(msg, embed=embed)

    @slash_command(
        guild_ids=[738037561712443493],
        brief="How hot is discord user",
        description="How hot is discord user",
        usage="howhot <user>",
    )
    async def howhot(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /HowHot used by {ctx.author} on {ctx.author.guild}" /
            " Discord Server"
        )
        if member is None:
            await ctx.respond("Please mention a user to how hot is")
        else:
            msg = await self.common.howhot(ctx, member)
            await ctx.respond(msg)

    @slash_command(
        guild_ids=[738037561712443493],
        brief="kiss a discord user",
        description="kiss a discord user",
        usage="kiss <user>",
    )
    async def kiss(self, ctx: Context, member: discord.Member):
        prBold(
            f"[Bot] - Fun /Kiss used by {ctx.author} on {ctx.author.guild} " /
            "Discord Server"
        )
        if member is None:
            await ctx.respond("Please mention a user to kiss")
        else:
            msg, embed = await self.common.kiss(ctx, member)
            await ctx.respond(msg, embed=embed)


def setup(bot):
    bot.add_cog(SlashFun(bot))
