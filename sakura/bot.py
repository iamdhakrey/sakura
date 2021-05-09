from discord.ext import commands

bot = commands.Bot(command_prefix='/')

@bot.command()
async def hi(ctx):
    await ctx.send('hi')

def run(TOKEN):
    bot.run(TOKEN)