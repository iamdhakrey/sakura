import discord
from asgiref.sync import sync_to_async
from sakura.config import MAIN_PREFIXES
from discord import Activity
from discord import ActivityType, Status
from discord.ext import commands
from discord import Intents

from sakura.BotEvents import event_setup
intents = discord.Intents.all()


class SakuraBot(commands.Bot):
    def __init__(self, help_command, description, **options):
        super().__init__(self.get_command_prefix,help_command=help_command, description=description, **options)

    def get_command_prefix(self, client, message):
        prefixes = MAIN_PREFIXES
        return commands.when_mentioned_or(*prefixes)(client,message)

bot = SakuraBot(
    help_command=None,
    description="Sakura: A Discord Bot",
    status = Status.online,
    intents = intents,
    activity = Activity(type=ActivityType.listening,name='y help')
)

event_setup(bot)

@bot.command()
async def hi(ctx):
    await ctx.send('hi')

@bot.command()
async def get_avatar_url(ctx,):
    user_id = ctx.author.id
    print(ctx.author.avatar_url)
    find_user = discord.utils.get(bot.get_all_members(),id=user_id)
    print(find_user)

def run(TOKEN):
    bot.run(TOKEN)