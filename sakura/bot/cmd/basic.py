from discord.ext.commands.context import Context
from sakura.bot.utils import prBold
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from sakura.bot.common.basic import Basic as common_basic


class Basic(commands.Cog):
    """
    Basic commands
    """

    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.color = 0x232323
        self.common = common_basic()

    @commands.command(brief="Show Avatar",
                      description="Shows your or someone avatar",
                      aliases=['av', 'dp'],
                      help="y_help avatar",
                      usage="y_avatar @Dhakrey#6689")
    async def avatar(self, ctx, *, user: discord.Member = None):
        prBold(
            f"[Bot] - Avatar cmd used by {ctx.author} on {ctx.author.guild} " /
            " Discord Server"
        )
        user = user or ctx.author
        await ctx.send(embed=await self.common.avatar(ctx, user))

    @commands.command(brief="Check Ping",
                      description="Shows Sakura ping status",
                      aliases=[],
                      help="y_ping",
                      usage="")
    async def ping(self, ctx: Context):
        prBold(
            f"[Bot] - Ping cmd used by {ctx.author} on {ctx.author.guild} " /
            "Discord Server"
        )
        await ctx.send(embed=await self.common.ping(ctx))

    @commands.command(brief="say somethings",
                      description="saying somethings",
                      aliases=['says'],
                      help="y_help say",
                      usage="y_say Hello World")
    async def say(self, ctx: Context, text: str, *args):
        txt = " ".join((text, ) + args)
        await ctx.trigger_typing()
        await ctx.send(txt)

    @commands.command(brief="About User",
                      description="About User",
                      aliases=['about'],
                      help="y_help info",
                      usage="y_info @Dhakrey#6689")
    async def info(self, ctx: Context, *, user: discord.Member = None):
        user = user if user else ctx.author
        await ctx.send(embed=await self.common.info(ctx, user))


def setup(bot: Bot):
    bot.add_cog(Basic(bot))
