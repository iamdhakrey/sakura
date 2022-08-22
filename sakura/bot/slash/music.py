import discord
from discord.ext.commands import slash_command
from discord.ext import commands
from discord.ext.commands.context import Context
from sakura.bot.BotMics.botutils import JsonTask, Video
from discord import Option

from sakura.bot.utils import prBold


# from sakura.BotMics.botutils import MusicQueue
async def is_valid_url(ctx: Context, url: str):
    """
    Check if url is valid

    :param ctx: Context
    :type ctx: Context
    :param url: url
    :type url: str
    :return: bool
    """
    if not url.startswith("http"):
        # await ctx.send(f"{prBold('Error:')} {prBold('Invalid URL')}")
        return False
    return True


class MusicNode:

    def __init__(self, song: Video):
        self.song = song
        self.next = None


class MusicList:

    def __init__(self) -> None:
        self.head = None

    def push(self, song: MusicNode):
        """Insert a song at the beginning

        :param song: song to be insert
        :type song: Video
        """
        old_music_list = self.head
        self.head = song
        self.next = old_music_list

    def append(self, song: MusicNode):
        """
        inster a new music at the end

        :param song: song to be inserted
        :type song: MusicNode
        """

        # check head is none or not if it is none then set head to song
        # if head is not none then inset new node at the end
        if self.head is None:
            self.head = song
            return

        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = song

    def delete(self, index: int = 0):
        """
        delete a node at the given index

        :param index: index to be deleted
        :type index: int
        """
        # if index is greate then to linked list size
        # then delete at the beginning
        if self.size() <= index:
            print("Warning: index is greater then size", end=" ")
            print("deleting last node of the linked list")
            temp = self.head
            curr = self.head
            while curr.next.next is not None:
                curr = curr.next
            curr.next = None
            return temp

        # if index is 0 then delete at the beginning
        if index == 0:
            temp = self.head
            self.head = self.head.next
            return temp

        # if index is not 0 or less then to linked list size
        # then delete at the given index
        curr = self.head
        prev = self.head
        temp = self.head
        count = 0
        while curr:
            if index == count:
                temp = curr.next
                break
            prev = curr
            curr = curr.next
            count += 1
        prev.next = temp

    def size(self):
        """
        return the size of the linked list
        using Recursion or Iteration

        default using_recursion are use for count the size of the list

        if both iteration and recursion is True then by default it is
        using recursion method

        :param using_recursion: for using recursion method
        :type using_recursion: Bool
        :param using_iteration: for using iteration method
        :type using_iteration: Bool
        :return: size of the linked list
        :rtype: int
        """
        count = 0
        curr = self.head
        while curr:
            count += 1
            curr = curr.next
        return count

    def print(self):
        """
        print the linked list
        """
        # embed = discord.Embed(title="Queue")
        curr = self.head
        # print("Linked List: [", end="")
        count = 1
        while curr:
            if curr.next:
                # embed.add_field(name=curr.song.title,
                # value=curr.song.duration,
                # inline=True)
                yield curr.song
                print(f"{curr.song.title} ->", end=" ")
            else:
                yield curr.song
                # embed.add_field(name=curr.song.title,
                # value=curr.song.duration,
                # inline=True)
                # print(f"{curr.song.title}]")
            curr = curr.next
            count += 1


class SlashMusic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.playlist = JsonTask("playlist.json")
        # self.guild = None
        # self.guild.music_list = MusicList()
        # self.guild.next = None
        self.current = None
        # self.bot.add_listener(self.on_reaction_add, "on_reaction_add")

    @slash_command(
        guild_ids=[738037561712443493, 794612239972958260],

        # guild_ids=[738037561712443493],
        description="Volume Control",
        brief="Volume Control",
    )
    async def volume(self, ctx: Context, volume: int):
        prBold(f"[Bot] - /Volume used by {ctx.author} on {ctx.author.guild}" +
               "Discord Server")
        await ctx.trigger_typing()
        if volume < 0:
            volume = 0
        if volume > 100:
            volume = 100

        # ToDO - Set max volume for specific guild

        client = ctx.guild.voice_client

        if client is None:
            await ctx.respond("I'm not connected to any voice channel.")
            return

        client.source.volume = volume / 100
        await ctx.respond(f"Volume set to {volume}%")

    @slash_command(
        # guild_ids=[738037561712443493],
        guild_ids=[738037561712443493, 794612239972958260],
        description="stop",
    )
    async def stop(self, ctx: Context):
        prBold(f"[Bot] - /Stop used by {ctx.author} on {ctx.author.guild}" +
               " Discord Server")
        await ctx.trigger_typing()
        client = ctx.guild.voice_client
        self.guild = ctx.guild

        # delete playlist in json file
        self.playlist.delete(str(ctx.guild.id))

        if client is None:
            await ctx.respond("I'm not connected to any voice channel.")
            return

        await client.disconnect()
        await ctx.respond("Disconnected from voice channel.")

    def _play(self, client, guild, song=None):
        if song:
            self.current = song
        else:
            # print(self.music_list.print())
            self.current = self.playlist.pop(str(guild.id))
            # print(song)
        path = Video(self.current, guild).download()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(path))

        def after_playing(err):
            print(err, "Err")
            if self.playlist.size(str(guild.id)) > 0:
                next_song = self.playlist.pop(str(guild.id))
                self._play(client, guild, next_song)
            else:
                print("No more songs in the playlist")
                client.disconnect()

        # check client is connected to guild voice channel
        if client.is_connected():
            client.play(source, after=after_playing)

    @slash_command(
        guild_ids=[738037561712443493, 794612239972958260],
        aliases=["play"],
        description="play music",
        brief="play music",
    )
    async def play(self, ctx: Context, *,
                   url: Option(str, "The url of the song to play")):
        prBold(f"[Bot] - /play used by {ctx.author} on {ctx.author.guild} " +
               "Discord Server")

        self.guild = ctx.guild
        # get voice client
        client = ctx.guild.voice_client

        # connect to voice channel
        if client is None:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.respond("You are not connected to any voice channel."
                                  )
            await channel.connect()
            client = ctx.guild.voice_client

        if client is None:
            await ctx.respond("I'm not connected to any voice channel.")
            return

        # check if the user is connected to a voice channel
        if not client.is_connected():
            await ctx.respond("I'm not connected to any voice channel.")
            return

        # check if the user is connected to the same voice channel as the bot
        if not client.channel == ctx.author.voice.channel:
            await ctx.respond("You're not in my voice channel.")
            return

        guild_id = str(ctx.guild.id)

        msg = await ctx.respond("Searching for song...")

        video = Video(url, ctx.guild)
        # check if the bot is playing anything
        if client.is_playing():
            self.playlist.append(guild_id, video.url)
            # self.music_list.append(MusicNode(video))
            await msg.edit_original_message(
                content=f"{video.title} Added in Queue.")
            return

        self.playlist.append(guild_id, video.url)
        # self.music_list.append(MusicNode(Video(url, ctx.guild)))
        try:
            video = Video(url, ctx.guild)
        except Exception:
            await ctx.respond(
                "Now it's not my fault, but I can't play this song.")
            return
        try:
            await msg.edit_original_message(content="",
                                            embed=video.get_embed())
        except discord.errors.NotFound:
            await ctx.send(embed=video.get_embed())

        self._play(client, ctx.guild)

    @slash_command(guild_ids=[738037561712443493, 794612239972958260],
                   description='show music queue')
    async def queue(self, ctx: Context):
        if self.current:
            embed = discord.Embed()
            embed.add_field(name="Now Playing",
                            value=self.guild.current.song.title,
                            inline=False)
            # embed.set_footer(text=f"Now Playing")
            # await ctx.respond(embed=embed)
        if self.music_list.size() > 0:
            count = 1
            rep = ""
            for _song in self.guild.music_list.print():
                rep += f"{count}. {_song.title} \n"

                count += 1
            embed.add_field(name="Queue", value=rep, inline=False)
            # print(i.title)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("No song in Queue")


def setup(bot):
    bot.add_cog(SlashMusic(bot))
