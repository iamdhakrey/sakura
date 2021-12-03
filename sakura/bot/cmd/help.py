import discord
from discord import embeds
from discord.ext import commands
from discord.errors import Forbidden

from sakura.BotMics.bot_db import DbConnection

"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.

Original concept by Jared Newsom (AKA Jared M.F.)
[Deleted] https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b
Rewritten and optimized by github.com/nonchris
https://gist.github.com/nonchris/1c7060a14a9d94e7929aa2ef14c41bc2

You need to set three variables to make that cog run.
Have a look at line 51 to 57
"""


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot:discord.ext.commands.Bot):
        self.bot = bot
        self.color = 0xc9a0dc

    @commands.command(
        brief="Shows this help message",
        description="Shows this help message",
        usage="help",
        aliases =  ['h']
    )
    async def help(self, ctx, *input):
        """ Shows all modules of that bot"""
	
        prefix = "y_" 
        version = "0.0.1" 

        owner = "Dhakrey" 
        owner_name = "Dhakrey#6689"

        if not input:
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            emb = discord.Embed(title='Commands and modules', color=self.color,
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':smiley:\n')

            for cog in self.bot.cogs:
                emb.add_field(name=f"`{cog}`", value=self.bot.cogs[cog].__doc__, inline=True)

            emb.add_field(name="About", value=f"The Bots is developed by `Dhakrey#6689`, based on discord.py.\n\
                                    This version of it is maintained by {owner}\n", inline=False)
            emb.set_footer(text=f"Bot is running v{version}")

        elif len(input) == 1:

            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():

                    emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        print(command)
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=f" {command.description} ", inline=False)
                    break
                else:
                    for command in self.bot.get_cog(cog).get_commands():
                        # print(command.name.lower() == input[0].lower(),command.hidden)
                        # if not command.hidden:
                        if command.name.lower() == input[0].lower():
                            # print(command.name.lower() == input[0].lower())
                            emb = discord.Embed(title=f' Help Command :- {command.name}',
                                                # description=command.description,
                                                color=ctx.author.color)
                            emb.add_field(name = f"`{command.name}`" ,value=f"{command.name} : {command.description} ", inline=False)
                            # emb.add_field(name="Usage", value=f"`{command.signature}`", inline=False)
                            emb.add_field(name="Aliases", value=f"`{command.aliases}`", inline=False)
                            emb.add_field(name="Example", value=f"`{command.usage}`", inline=False)
                            emb.add_field(name="Category", value=f"`{command.cog_name}`", inline=False)
                            break
            # else:
            #     emb = discord.Embed(title="What's that?!",
            #                         description=f"I've never heard from a module called `{input[0]}` before :scream:",
            #                         color=discord.Color.orange())

        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())
        emb.set_author(name=f"Help - {self.bot.user.name}", icon_url=self.bot.user.avatar)

        await send_embed(ctx, emb)

    @commands.command(
        hidden=True,
        
    )
    @commands.is_owner()
    async def help_db(self, ctx):
        """
        Sync the help database with the help command
        """
        for cog in self.bot.cogs:
            for cmd in self.bot.get_cog(cog).get_commands():
                if not cmd.hidden:
                    await DbConnection.fetch_help(cmd)
        await ctx.send("Done")
def setup(bot):
    bot.add_cog(Help(bot))