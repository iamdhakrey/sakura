import json
import os

import discord
import pytube
import youtube_dl as ytdl


unicode_emoji = {
    '0': '0️⃣',
    '1': '1️⃣',
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣'
}


def norm_to_emoji(guild: discord.Guild, arg: str):
    new_arg = []
    arg = str(arg).split(":")
    for i in arg:
        if discord.utils.get(guild.emojis, name=i):
            emoji = discord.utils.get(guild.emojis, name=i)
            new_arg.append(str(emoji))
        else:
            new_arg.append(str(i))
    wel = ""
    for i in new_arg:
        wel = wel + i

    return wel


def grep_emojis(guild: discord.guild, msg, splitter):
    """
    Split msg with given splitter
    """
    # emoji_role_dict = {}
    emoji_list = []
    for em_and_role in msg:
        em_and_role = em_and_role.split(splitter)
        emoji_list.append(em_and_role[0])
    return emoji_list


def to_dict(guild: discord.Guild, msg, splitter):
    """
    Split msg with given splitter
    """
    emoji_role_dict = {}
    for em_and_role in msg:
        em_and_role = em_and_role.split(splitter)
        emoji_role_dict[em_and_role[0].strguild()] = em_and_role[1].strguild()
    return emoji_role_dict


def eval_reaction_and_role(guild: discord.Guild, msg, splitter):
    """
    Split msg with given splitter

    :param guild: discord.Guild
    :type guild: discord.Guild
    :param msg: msg
    :type msg: list
    :param splitter: str
    :return: list
    """
    emoji_role_dict = {}
    for em_and_role in msg:
        em_and_role = em_and_role.split(splitter)
        role = em_and_role[1].strip().replace("<&", "").replace(">", "")
        # role = discord.utils.get(guild.roles,
        #                          id=em_and_role[1].replace("<&","").replace("<","")).id
        emoji_role_dict[em_and_role[0].strip()] = role
    # print(emoji_role_dict)

    return emoji_role_dict


def dict_to_list(dictionary: dict):
    """
    Convert dictionary to list and key and value
    join with "^"
    """
    list_ = []
    for key, value in dictionary.items():
        list_.append(str(key) + "^" + str(value))
    return list_


class Video:

    YTDL_OPTS = {
        "default_search": "ytsearch",
        "format": "bestaudio/best",
        "quiet": True,
        "extract_flat": "in_playlist"
    }

    def __init__(self, url, guild: discord.Guild):
        self.url = url
        self.guild = guild
        if self._is_valid_url():
            self.info = self._get_info()
        else:
            self.url = self.find_song()
            self.info = self._get_info()
            # print(self.info)
        self.title = self.info['title']
        self.duration = self._convert_duration(self.info['duration'])
        # print(json.dumps(self.info, indent=4))
        self.info_dict = self.info['formats'][0]
        self.thumbnail = self.info['thumbnail']
        self.stream_url = self.info_dict['url']

    def _convert_duration(self, duration):

        # format duration to hh:mm:ss
        duration = int(duration)
        hours = duration // 3600
        if hours < 0:
            final_hours = 00
        else:
            final_hours = str(hours).zfill(2)
        minutes = (duration - hours * 3600) // 60

        # convert to two digits
        if minutes < 10:
            final_minutes = f"0{minutes}"
        else:
            final_minutes = minutes

        seconds = duration - hours * 3600 - minutes * 60

        # convert to two digits
        if seconds < 10:
            final_seconds = f"0{seconds}"
        else:
            final_seconds = seconds

        return f"{final_hours}:{final_minutes}:{final_seconds}"

    def _get_info(self):
        with ytdl.YoutubeDL(self.YTDL_OPTS) as ydl:
            info = ydl.extract_info(self.url, download=False)
            return info

    def _is_valid_url(self):
        """
        Check if url is valid
        """
        return True if self.url.startswith("http") else False

    def get_embed(self):
        embed = discord.Embed(title=self.title,
                              description=f"Duration: {self.duration}")
        embed.set_image(url=self.thumbnail)
        return embed

    def find_song(self):
        """
        Find song in playlist
        from youtube search
        """
        with ytdl.YoutubeDL(self.YTDL_OPTS) as ydl:
            info = ydl.extract_info(f"ytsearch:{self.url}", download=False)
            # print(json.dumps(info, indent=4))
            self.url = "https://www.youtube.com/watch?v=" + info['entries'][0][
                'url']
            return self.url

    def download(self):
        """
        Download song from given self.url
        """
        path = "audio"
        yt = pytube.YouTube(self.url)
        stream = yt.streams.filter(only_audio=True, abr="128kbps").first()
        stream.download(output_path=path, filename=f"{self.guild.id}.mp3")
        return f"{path}/{self.guild.id}.mp3"


class JsonTask:
    """
    Json Related Functions
    """

    def __init__(self, filename) -> None:
        self.json = json
        self.file = f"{filename}"

    def open_file(self):
        """
        open json file
        """
        if not os.path.isfile(self.file):
            with open(self.file, 'w') as file:
                dummy = {}
                file.write(self.json.dumps(dummy, indent=4))
        with open(self.file, 'r+') as file:
            self._json = self.json.load(file)

    def close_file(self):
        """
        close json file
        """
        with open(self.file, 'w') as file:
            file.write(self.json.dumps(self._json, indent=4))

    def __str__(self):
        return self.json.dumps(self._json, indent=4)

    def __repr__(self) -> str:
        return f"<{self.__class__.__qualname__}({self.file}>)"

    def _has(self, key: str):
        """
        check key is exist or not if exist
        return True else return False

        Agrs:
            key {str}

        Return:
            bool

        """
        if key in self._json:
            return True
        else:
            return False

    # def _compare(self, guild: str = None, args):
    #     """
    #     check values present or not
    #     if values not present then it will return

    #     """:
    #         for key, value in kwargs.items():
    #             if self._json[key] != value:
    #                 return False
    #     return True

    def _add(self, guild, args):
        """
        add data in json file

        Args:
            guild {str}
            args ()
            kwargs {dict}


        """
        try:
            data = self._json[guild]
            data.append(args)
        except KeyError:
            self._json[guild] = [args]
        with open(self.file, 'w') as file:
            file.write(self.json.dumps(self._json, indent=4))

    def _save(self):
        """
        save data in json file
        """
        with open(self.file, 'w') as file:
            file.write(self.json.dumps(self._json, indent=4))

    def pop(self, guild):
        """
        pop data from json file
        """
        self.open_file()
        _guild = self._json[guild]
        _url = _guild.pop(0)
        with open(self.file, 'w') as file:
            file.write(self.json.dumps(self._json, indent=4))
        self._save()
        self.close_file()
        return _url

    def append(self, guild, args):
        """
        append data in json file
        """
        self.open_file()
        print(self._has(guild))
        if self._has(guild):
            self._json[guild].append(args)
        else:
            self._json[guild] = [args]
        self._save()
        self.close_file()

    def size(self, guild):
        """
        return size of json file
        """
        self.open_file()
        if self._has(str(guild)):
            self.close_file()
            return len(self._json[guild])
        else:
            self.close_file()
            return 0

    def delete(self, guild):
        self.open_file()
        if self._has(guild):
            del self._json[guild]

    def fetch_data(self, guild, args):
        """
        fetch_data and push data in json file


        :param guild: guild of the server
        :param kwargs: key value pair of data
        :type guild: str
        :type kwargs: dict
        :return: data of guild
        :rtype: dict

        """
        self.open_file()
        if self._has(guild):
            # if self._compare(guild, args):
            # return self._json[guild]
            # else:
            self._add(guild, args)
        else:
            self._add(guild, args)
        self._save()
        self.close_file()
        return self._json[guild]
