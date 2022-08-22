import random
import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from sakurabkp.bot.common.fun import Fun as FunCommon

ban_gif = "https://c.tenor.com/No6jBHMIF1wAAAAC/banned-anime.gif"
dont_know = "https://c.tenor.com/KbjWt386YfcAAAAC/jibaku-" \
                  "shounen-hanako-kun-yashiro-nene.gif"


class Fun(commands.Cog):
    """
    Anime related commands
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.color = 0x232323
        self.common = FunCommon()

    @commands.command(brief="fun kick user ",
                      description="fun kick user :leg:",
                      aliases=["sdfdsgf"],
                      help="y_help kick",
                      usage="y_kick @user")
    async def kick(self, ctx: Context, member: discord.Member):
        if member is None:
            await ctx.reply(await self.common.kick(ctx, member))
        else:
            msg, embed = await self.common.kick(ctx, member)
            await ctx.reply(msg, embed=embed)

    @commands.command(
        brief="hug command",
        description="hugs a user :hugging:",
        usage="hug <user>",
    )
    async def hug(self, ctx: Context, member: discord.Member):
        if member is None:
            await ctx.reply("Please mention a user to hug")
        else:
            msg, embed = await self.common.hug(ctx, member)
            await ctx.reply(msg, embed=embed)

    @commands.command(
        brief="Punch command",
        description="punches a user :boxing_glove:",
        usage="punch <user>",
    )
    async def punch(self, ctx: Context, member: discord.Member):
        if member is None:
            await ctx.reply("Please mention a user to punch")
        else:
            msg, embed = await self.common.punch(ctx, member)
            await ctx.reply(msg, embed=embed)

    @commands.command(
        brief="slap command",
        description="slaps a user ",
        usage="slap <user>",
        # aliases = ["s"]
    )
    async def slap(self, ctx: Context, member: discord.Member):
        if member is None:
            await ctx.reply("Please mention a user to slap")
        else:
            msg, embed = await self.common.slap(ctx, member)
            await ctx.reply(msg, embed=embed)

    @commands.command(
        brief="poke command",
        description="pokes a user ",
        usage="poke <user>",
    )
    async def poke(self, ctx: Context, member: discord.Member):
        if member is None:
            await ctx.reply("Please mention a user to poke")
        else:
            msg, embed = await self.common.poke(ctx, member)
            await ctx.reply(msg, embed=embed)

    @commands.command(
        brief="Give someone a beer! 🍻",
        description="Give someone a beer! 🍻 ",
        usage="beer <user>",
        # aliases = ["h"]
    )
    async def beer(self, ctx: Context, member: discord.Member):
        if member is None:
            await ctx.reply("Please mention a user to give a beer")
        else:
            msg, embed = await self.common.beer(ctx, member)
            await ctx.reply(msg, embed=embed)

    @commands.command(brief="Random percent how hot is a discord user",
                      description="Random percent how hot is a discord user",
                      usage="hot <user>",
                      aliases=["howhot", "hot"])
    async def hotcalc(self, ctx: Context, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await ctx.reply(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(brief="kiss a discord user",
                      description="kiss a discord user",
                      usage="kiss <user>")
    async def kiss(self, ctx: Context, *, user: discord.Member):
        await ctx.reply(await self.common.kiss(ctx, user))


def setup(bot: Bot):
    bot.add_cog(Fun(bot))
