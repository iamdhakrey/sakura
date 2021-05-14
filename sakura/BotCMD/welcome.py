from sakura.config import MEDIA_ROOT
from sakura.BotMics.image import save_image
from sakura.BotMics.bot_db import DbConnection
from discord import channel
from discord.ext.commands.context import Context
from sakura.utils import prBold, prYellow
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.bot import Bot
import ast
from sakura.BotMics.botutils import norm_to_emoji

class Welcome(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot    = bot
        self.color  = 0x232323
    
    @commands.command(
        name        = 'set_welcome',
        description = 'Set welcome message',
        help        = 'y_help set_welcome',
        usage       = 'y_set_welcome #channel_name welcome_msg',
        aliases     = ['swm']
    )
    @has_permissions(administrator=True)
    async def set_welcome_message(self,ctx:Context,set_channel,*,msg=None):
        if msg is None:
            msg = ""

        if set_channel is not None:
            if str(set_channel).startswith('<#'):
                channel_id = str(set_channel).split(">")[0].replace("<#",'')
            else:
                msg += set_channel

        msg = norm_to_emoji(ctx,msg)
        if discord.utils.get(self.bot.get_all_channels(),id = int(channel_id)):
            channel_id = channel_id
        else:
            data = DbConnection.fetch_welcome(ctx.guild)
            channel_id =  data.welcome_channel
        # convert msg to list
        msg = msg.replace('\n',"\n\nqwwq").split("\nqwwq")

        await DbConnection.fetch_welcome(ctx.guild,
            welcome_msg     = msg,
            welcome_channel = channel_id, 
            update_by       = ctx.author.id 
            )

        await ctx.send("welcome msg set successfully")

    @set_welcome_message.error
    async def swm_error(self,ctx,error):
        # if msg is not given
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Welcome Msg Requierd")
        # Role  not Found
        if isinstance(error,commands.RoleNotFound):
            await ctx.send(error)

        #channel not Found
        if isinstance(error,commands.ChannelNotFound):
            await ctx.send(error)

    @commands.command(
        name        = 'check_welcome',
        description = 'before set check welcome msg first how it look like',
        help        = 'y_help check_welcome',
        usage       = 'y_check_welcome welcome msg',
        aliases     =['welcome_check','cw']
    )
    @has_permissions(administrator=True)
    async def check_welcome(self,ctx:Context,*,msg:str):
        msg = norm_to_emoji(ctx,msg)
        embed = discord.Embed(
            description = msg,
        )
        await ctx.send(embed=embed)

    @commands.command(
        name        = 'get_welcome',
        description = 'get the exists welcome msg',
        help        = 'y_help get_welcome',
        usage       = 'y_get_welcome',
        aliases=['show_welcome','gw'])
    @has_permissions(administrator=True)
    async def get_welcome(self,ctx:Context):
        welcome = await DbConnection.fetch_welcome(ctx.guild)
        msg = ast.literal_eval(welcome.welcome_msg)
        embed = discord.Embed(
            title       = "Welcome Message",
            description = "".join(msg)
        )
        if welcome.welcome_channel is not None:
            welcome_channel = "<#"+str(welcome.welcome_channel)+'>'
        else:
            welcome_channel = None
        embed.add_field(name="is_enable",value=welcome.welcome_enable,inline=False)
        embed.add_field(name="welcome_channel",value=welcome_channel,inline=True)
        embed.add_field(name="self_role",value=welcome.self_role,inline=False)
        await ctx.send(embed=embed)

    @commands.command(
        name        = 'Enable Welcome Message',
        description = 'Enable OR Disable welcome message',
        help        = 'y_help welcome_enable',
        usage       = 'y_welcome_enable True/False',
        aliases     = ['enable_welcome'])
    @has_permissions(administrator=True)
    async def welcome_enable(self,ctx:Context,status):
        if status is None:
            await ctx.reply("Bro use on/off or enable/disable ") 
            return

        if str(status) == "on" or str(status) == "ON" or str(status) == "enable":
            enable = True
            # print(status)
        elif str(status) == "off" or str(status) == "OFF" or str(status) == "disable":
            enable = False
        else:
            await ctx.reply("Bro use on/off or enable/disable ") 
            return
        await DbConnection.fetch_welcome(ctx.guild,welcome_enable=enable)
        await ctx.reply("welcome status is set to  {}".format(status))

    @welcome_enable.error
    async def welcome_enable_error(self,ctx:Context,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.reply("Bro use on/off or enable/disable ")     

    @commands.command(aliases=["tw"])
    @has_permissions(administrator=True)
    async def test_welcome(self,ctx):
        """
        Send Original Set Msg
        """
        member_id = ctx.author.id
        member_name = ctx.author.name +"#"+ctx.author.discriminator
        member_tag = "<@"+str(member_id)+">"  

        welcome_data = await DbConnection.fetch_welcome(ctx.guild)
        
        if welcome_data.self_role is not None:
            role = discord.utils.get(ctx.guild.roles,id = int(welcome_data.self_role))
        else:
            role = None
        welcome_channel = discord.utils.get(ctx.guild.channels,id=int(welcome_data.welcome_channel))

        temp_welcome_msg = ast.literal_eval(welcome_data.welcome_msg)
        welcome_msg = []

        for msg in temp_welcome_msg:
            wlmsg = msg
            if "member.mention" in msg:
                wlmsg = str(msg).replace("{"+"member.mention"+"}",member_tag)
                # test.append(wlmsg)
            if "member.name" in msg:
                wlmsg = str(msg).replace("{"+"member.name"+"}",member_name)
                # test.append(wlmsg)
            if "member.count" in msg:
                wlmsg = str(msg).replace("{"+"member.count"+"}",str(ctx.gumsgld.member_count))
                # test.append(wlmsg)
            if "member.server_name" in msg:
                wlmsg = str(msg).replace("{"+"member.server_name"+"}",str(ctx.guild.name))
                # test.append(wlmsg)
            if role is not None:
                if "member.role" in msg:
                    wlmsg = str(msg).replace("{"+"member.role"+"}",str(role.mention))
                # test.append(wlmsg)
            welcome_msg.append(wlmsg)
        embed = discord.Embed(
            description = "".join(welcome_msg)
        )
        save_image(self.bot,ctx)
        file = discord.File(open(str(ctx.guild.id)+"_out_welcome.png", 'rb'))
        embed.set_image(url="attachment://"+str(ctx.guild.id)+"_out_welcome.png")
        await ctx.send(embed=embed,file=file)

def setup(bot:Bot):
    bot.add_cog(Welcome(bot))