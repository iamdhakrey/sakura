import discord
from discord.ext.commands.context import Context


def norm_to_emoji(guild:discord.Guild,arg:str):
    new_arg = []
    arg = str(arg).split(":")
    for i in arg:
        if discord.utils.get(guild.emojis,name=i):
            emoji = discord.utils.get(guild.emojis,name=i)
            new_arg.append(str(emoji))
        else:
            new_arg.append(str(i))
    wel = ""
    for i in new_arg:
        wel = wel + i 
    
    return wel