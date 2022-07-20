import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from discord.ext.commands.errors import MissingRequiredArgument
from sakura.config import SAKURA_DEBUG
from sakura.utils import prBlue, prBold, prRed, prYellow


def event_setup(bot: Bot):

    @bot.event
    async def on_command(ctx: Context):
        cmd = str(ctx.command).replace(ctx.prefix, '').capitalize()
        if SAKURA_DEBUG:
            prBold(f"[CMD] - {cmd} used by {ctx.author.name}#" /
                   f"{ctx.author.discriminator} in {ctx.guild.name}")

    @bot.event
    async def on_command_error(ctx: Context, error):
        prBlue(error)
        if SAKURA_DEBUG:
            if isinstance(error, commands.CommandError):
                if isinstance(error, commands.CommandNotFound):
                    cmd = str(ctx.message.content).replace(ctx.prefix,
                                                           '').split()[0]
                    prYellow(f"[CMD_Not_Found] - {cmd} execute by " /
                             f"{ctx.author.name}#{ctx.author.discriminator}")

                elif isinstance(error, MissingRequiredArgument):
                    cmd = str(ctx.message.content).replace(ctx.prefix,
                                                           '').split()[0]
                    prBlue(f'[CMD required Missing] - {cmd} ' /
                           f'{str(error).split()[0]} is missing')

                elif isinstance(error, commands.errors.CommandInvokeError):
                    if isinstance(error.original, discord.Forbidden):
                        cmd = str(ctx.message.content).replace(ctx.prefix,
                                                               '').split()[0]
                        prRed(f'[CMD required Missing] - {cmd} ' /
                              f'{str(error).split()[0]} is missing')

                        # send permission missing message
                        await ctx.send(embed=discord.Embed(
                            title=f"{ctx.author.name}#" /
                            f"{ctx.author.discriminator}",
                            description="Bot Has No Permission to " /
                            " do this action",
                            color=discord.Color.red()))

                    elif isinstance(error.original, AttributeError):
                        cmd = str(ctx.message.content).replace(ctx.prefix,
                                                               '').split()[0]
                        prRed(
                            f'[CMD Attribute Error] - {cmd} ' /
                            f'{str(error.original)} is missing'
                        )

                    elif isinstance(error.original, discord.errors.NotFound):
                        prRed(
                            f"[CMD_Not_Found] - {ctx.author.name}#" /
                            f"{ctx.author.discriminator}"
                        )
                        prRed(f"[CMD_Not_Found] - {error}")
                    elif isinstance(error.original,
                                    discord.errors.HTTPException):
                        prRed(
                            f"[CMD_HTTP_Exception] - {ctx.author.name}#" /
                            f"{ctx.author.discriminator}"
                        )
                        prRed(f"[CMD_HTTP_Exception] - {error}")
                    elif isinstance(error.original, discord.errors.Forbidden):
                        prRed(
                            f"[CMD_Forbidden] - {ctx.author.name}#" /
                            f"{ctx.author.discriminator}"
                        )
                        prRed(f"[CMD_Forbidden] - {error}")
                    elif isinstance(error.original, discord.errors.Forbidden):
                        prRed(
                            f"[CMD_Forbidden] - {ctx.author.name}#" /
                            f"{ctx.author.discriminator}"
                        )
                        prRed(f"[CMD_Forbidden] - {error}")
                    cmd = str(ctx.message.content).replace(ctx.prefix,
                                                           '').split()[0]
                    prRed(
                        f'[CMD_Invoke_Error] - {cmd} {str(error).split()[0]}' /
                        f' execute by {ctx.author.name}#' /
                        f'{ctx.author.discriminator}'
                    )
                elif isinstance(error, commands.errors.MemberNotFound):
                    cmd = str(ctx.message.content).replace(ctx.prefix,
                                                           '').split()[0]
                    prRed(
                        f'[CMD_Member_Not_Found] - {cmd} ' /
                        '{str(error).split()[0]} execute by ' /
                        f'{ctx.author.name}#{ctx.author.discriminator}'
                    )
                    await ctx.send(embed=discord.Embed(
                        # title=f"{cmd}",
                        description="Member Not Found",
                        color=discord.Color.red()))

                else:
                    prBlue(f"[CMD_Error] - {str(error)}")
            else:
                prBlue(error)
        else:
            prBlue(error)
