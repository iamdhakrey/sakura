import discord
from discord.ext import commands
from discord.errors import Forbidden
from discord.ext.commands import Bot
from sakura.bot.BotMics.bot_db import DbConnection

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
            await ctx.send(
                "Hey, seems like I can't send embeds. Please check" +
                " my permissions :)")
        except Forbidden:
            await ctx.author.send(
                "Hey, seems like I can't send any message in " +
                f" {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this " +
                " issue? :slight_smile: ",
                embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.color = 0xc9a0dc

    @commands.command(brief="Shows this help message",
                      description="Shows this help message",
                      usage="help",
                      aliases=['h'])
    async def help(self, ctx, *input):
        """ Shows all modules of that bot"""

        prefix = "y_"
        version = "0.0.1"

        owner = "Dhakrey"
        # owner = "Dhakrey#6689"

        if not input:
            try:
                owner = ctx.guild.get_member(owner).mention
            except AttributeError:
                owner = owner

            emb = discord.Embed(
                title='Commands and modules',
                color=self.color,
                description=f'Use `{prefix}help <module>` to gain more' +
                ' information about that module ' + ':smiley:\n')

            for cog in self.bot.cogs:
                print(cog.startswith('Slash'))
                if cog.startswith('Slash'):
                    pass
                else:
                    emb.add_field(name=f"`{cog}`",
                              value=self.bot.cogs[cog].__doc__,
                              inline=True)

            emb.add_field(name="About",
                          value="The Bots is developed by `Dhakrey#6689`, " +
                          "based on py-cord.\n This version of it" +
                          f" is maintained by {owner}\n",
                          inline=False)
            emb.set_footer(text=f"Bot is running v{version}")

        elif len(input) == 1:

            for cog in self.bot.cogs:
                print("{}".format(cog))
                if cog.lower() == input[0].lower():

                    emb = discord.Embed(title=f'{cog} - Commands',
                                        description=self.bot.cogs[cog].__doc__,
                                        color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        print(command)
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`",
                                          value=f" {command.description} ",
                                          inline=False)
                    break
                else:
                    try:
                        for command in self.bot.get_cog(cog).get_commands():
                            if command.name.lower() == input[0].lower():
                                emb = discord.Embed(
                                    title=f' Help Command :- {command.name}',
                                    color=ctx.author.color)
                                _value = "{}: {}"
                                emb.add_field(name=f"`{command.name}`",
                                              value=_value.format(
                                                  "Description",
                                                  command.description),
                                              inline=False)
                                emb.add_field(name="Aliases",
                                              value=f"`{command.aliases}`",
                                              inline=False)
                                emb.add_field(name="Example",
                                              value=f"`{command.usage}`",
                                              inline=False)
                                emb.add_field(name="Category",
                                              value=f"`{command.cog_name}`",
                                              inline=False)
                                break
                    except AttributeError:
                        pass

        elif len(input) > 1:
            emb = discord.Embed(
                title="That's too much.",
                description="Please request only one module at " +
                " once :sweat_smile:",
                color=discord.Color.orange())
        emb.set_author(name=f"Help - {self.bot.user.name}",
                       icon_url=self.bot.user.avatar)

        embed = discord.Embed(title="Bot Help", color=0x00ff00)

        embed.set_footer(text=f"Bot version {version}")
        for cog_name, cog in self.bot.cogs.items():
            cog_help_str = ""
            for cmd in cog.get_commands():
                if isinstance(cmd, commands.Command):
                    cog_help_str += f"\n{cmd.name}: {cmd.help}"
                if cog_help_str:
                    embed.add_field(name=cog_name, value=cog_help_str, inline=False)
        embed.set_author(name=owner)
        await ctx.send(embed=embed)

        # await send_embed(ctx, emb)

    @commands.command(
        hidden=True, )
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
