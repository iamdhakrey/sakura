from discord.ext import commands
from discord.commands import slash_command


class Example(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[738037561712443493]
                   )  # Create a slash command for the supplied guilds.
    async def hello(self, ctx):
        await ctx.respond("Hi, this is a slash command from a cog!")

    @slash_command(guild_ids=[738037561712443493])
    async def hi(self, ctx):
        await ctx.respond("Hi, this is a global slash command from a cog!")


def setup(bot):
    bot.add_cog(Example(bot))
