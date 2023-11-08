import discord
from discord import Activity, ActivityType, Status
from discord.ext import commands

from sakura.bot.events import event_setup
from sakura.bot.slash import setup
from sakura.bot.cmd import cmd_setup
from sakura.bot.config import COGS_FOLDER, DEFINED_COGS, MAIN_PREFIXES

intents = discord.Intents.all()


class SakuraBot(commands.Bot):

    def __init__(self, help_command, description, **options):
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
                activity=Activity(type=ActivityType.listening, name='y_ help'))

# connect to sakura slash_command
setup(bot)
# connect to sakura bot cmd
# cmd_setup(bot)
# connect to sakura event
event_setup(bot)


for cogs in DEFINED_COGS:
    # load all cogs from config
    bot.load_extension(COGS_FOLDER + "." + cogs)


def run(TOKEN):
    bot.run(TOKEN)
