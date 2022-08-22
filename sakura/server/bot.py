import discord
from discord import Activity, ActivityType, Status
from discord.ext import commands

from sakura.bot.events import event_setup
from sakura.bot.slash import setup
from sakura.bot.config import COGS_FOLDER, DEFINED_COGS, MAIN_PREFIXES

intents = discord.Intents.all()


class SakuraBot(commands.Bot):

    def __init__(self, help_command, description, **options):
        # super().__init__(self,help_command=help_command)
        # print(self.slash_command())
        super().__init__(self.get_command_prefix,
                         help_command=help_command,
                         description=description,
                         **options)

    def get_command_prefix(self, client, message):
        prefixes = MAIN_PREFIXES
        return commands.when_mentioned_or(*prefixes)(client, message)


bot = SakuraBot(help_command=None,
                description="Sakura: A Discord Bot",
                status=Status.online,
                intents=intents,
                activity=Activity(type=ActivityType.listening, name='y help'))

setup(bot)
event_setup(bot)

for cogs in DEFINED_COGS:
    # try:
    bot.load_extension(COGS_FOLDER + "." + cogs)
    # except discord.errors.ExtensionAlreadyLoaded:
    # prRed(f"{cogs} Extension already loaded")
# @bot.command()
# async def hi(ctx):
#     await ctx.send('hi')

# @bot.command()
# async def get_avatar_url(ctx,):
#     user_id = ctx.author.id
#     print(ctx.author.avatar_url)
#     find_user = discord.utils.get(bot.get_all_members(),id=user_id)
#     print(find_user)


def run(TOKEN):
    bot.run(TOKEN)
