from sakura.config import MAIN_PREFIXES
from discord import Activity
from discord import ActivityType, Status
from discord.ext import commands


class SakuraBot(commands.Bot):
    def __init__(self, help_command, description, **options):
        super().__init__(self.get_command_prefix,help_command=help_command, description=description, **options)

    def get_command_prefix(self, client, message):
        prefixes = MAIN_PREFIXES
        return commands.when_mentioned_or(*prefixes)(client,message)

bot = SakuraBot(
    help_command=None,
    description="Sakura: A Discord Bot",
    status = Status.invisible,
    activity = Activity(type=ActivityType.listening,name='y help')
)

@bot.command()
async def hi(ctx):
    await ctx.send('hi')

def run(TOKEN):
    bot.run(TOKEN)