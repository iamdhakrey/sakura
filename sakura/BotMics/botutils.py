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

def em_and_role_split(msg,splitter):
    emoji_role_dict = {}
    emoji_list = []
    for em_and_role in msg:
        em_and_role = em_and_role.split(splitter)
        emoji_list.append(em_and_role[0].strip())
        emoji_role_dict[em_and_role[0].strip().replace(":","")] = em_and_role[1].strip()

    return emoji_list,emoji_role_dict