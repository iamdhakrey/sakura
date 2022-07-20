import os

import discord
import youtube_dl
from discord import utils
from discord.errors import ClientException
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from sakura.utils import prYellow


class Music(commands.Cog):
    """
    Music commands
    """

    def __init__(self, bot) -> None:
        self.bot = bot
        self.color = 0x232323

    @commands.command(brief="Play a song",
                      description="Play a song",
                      usage="play <song>",
                      aliases=["p"],
                      help="Play a song")
    async def play(self, ctx: Context, *, name: str):
        """
        Play Music from youtube
        """
        # TODO need to queue

        # voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        # check author is connected or not
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            await ctx.reply('You are not connected to any voice channel')
            return

        # TODO need to add youtube links
        print(name)
        # source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(name))
        # prBold(source)
        audio_dir = os.path.join('.', 'audio')
        audio_path = os.path.join(audio_dir, f'{ctx.guild.id}.mp3')
        # voice = utils.get(self.bot.voice_clients, guild=ctx.guild)

        # queue = self.music_queues.get(ctx.guild)
        ydl_opts = {
            'format':
            'bestaudio/best',
            'noplaylist':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl':
            audio_path
        }
        try:
            await channel.connect()
        except ClientException:
            pass
        # Path(audio_dir).mkdir(parents=True, exist_ok=True)
        prYellow(audio_path)
        # /home/user/mygit/Sakura/audio/738037561712443493.mp3
        source = discord.FFmpegPCMAudio(audio_path)
        # voice.play(source)

        print(source)
        # try:
        #     os.remove(audio_path)
        # except OSError:
        #     pass

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f'{name}'])
            except Exception:
                # await self.play_all_songs(guild)
                print('Error downloading song. Skipping.')
                return

        ctx.voice_client.play(source)

    @commands.command(brief="Pause the music",
                      description="Pause the music",
                      usage="pause",
                      aliases=["s"],
                      help="Pause the music")
    async def stop(self, ctx: Context):
        """
        Stop Music
        """

        voice = utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            ctx.message.author.voice.channel
            voice.stop()
            await voice.disconnect()
        except AttributeError:
            await ctx.reply('You are not connected to the same voice channel')
            return


def setup(bot: Bot):
    bot.add_cog(Music(bot))
