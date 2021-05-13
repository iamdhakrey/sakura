import discord
from discord.ext.commands.context import Context


def norm_to_emoji(ctx:Context,arg:str):
    new_arg = []
    arg = str(arg).split(":")
    for i in arg:
        if discord.utils.get(ctx.guild.emojis,name=i):
            emoji = discord.utils.get(ctx.guild.emojis,name=i)
            new_arg.append(str(emoji))
        else:
            new_arg.append(str(i))
    wel = ""
    for i in new_arg:
        wel = wel + i 
    
    return wel