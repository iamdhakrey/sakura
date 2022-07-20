import random
from random import randint
from discord.embeds import Embed
from discord.ext.commands.context import Context
import discord

ban_gif = "https://c.tenor.com/No6jBHMIF1wAAAAC/banned-anime.gif"
dont_know = "https://c.tenor.com/KbjWt386YfcAAAAC/jibaku" \
                  "-shounen-hanako-kun-yashiro-nene.gif"


class Fun:
    """
    Anime related commands
    """
    async def kick(self, ctx: Context, member: discord.Member = None):
        kick_gif = [
            "https://media1.tenor.com/images/862272da6f71b28b53ec" /
            "262bcca6763a/tenor.gif",
            "https://c.tenor.com/Lyqfq7_vJnsAAAAC/kick-funny.gif",
            "https://c.tenor.com/Gf6UTsRayw4AAAAC/kickers-caught.gif",
            "https://c.tenor.com/5iVv64OjO28AAAAC/milk-and-mocha" /
            "-bear-couple.gif",
            "https://c.tenor.com/Jv9L6Rrml9QAAAAd/cat-kick.gif",
            "https://c.tenor.com/lxd8SO_uRIYAAAAC/anime-kick.gif",
            "https://c.tenor.com/7te6q4wtcYoAAAAC/mad-angry.gif",
            "https://c.tenor.com/4F6aGlGwyrwAAAAd/sdf-avatar.gif",
            "https://c.tenor.com/wOCOTBGZJyEAAAAC/chikku-neesan-" /
            "girl-hit-wall.gif",
            "https://c.tenor.com/rmJesAJehbUAAAAd/kiryu-harkua.gif"
        ]
        msg = ["Aur bhai {} aa gya swaad"]
        if member is None:
            return kick_gif[randint(0, len(kick_gif) - 1)]

        else:
            embed = Embed()
            embed.set_image(url=kick_gif[randint(0, len(kick_gif) - 1)])
            msg = "or bhai {} aa gya swad".format(member.mention)
            return msg, embed

    async def hug(self, ctx: Context, member: discord.Member = None):
        hug_gif = [
            "https://c.tenor.com/eiIM4HOwGZMAAAAC/couple-hug.gif",
            "https://c.tenor.com/ve7O0fIRmN8AAAAC/cozy-kiss.gif",
            "https://c.tenor.com/2bWwi8DhDsAAAAAC/hugs-and-love.gif",
            "https://c.tenor.com/xIuXbMtA38sAAAAd/toilet-bound-hanakokun.gif",
            "https://c.tenor.com/jQ0FcfbsXqIAAAAC/hug-anime.gif",
            "https://c.tenor.com/6IW-RXj4IP4AAAAC/hugging-hug.gif",
            "https://c.tenor.com/rhM8Dnf-AyMAAAAC/caring-hug-caring-kiss.gif",
            "https://c.tenor.com/vBzOvBQ5MugAAAAC/citrus-harumi.gif",
            "https://c.tenor.com/eZ4J7M5ifPYAAAAd/kyokou-suiri-anime.gif",
            "https://c.tenor.com/nv1mdvZoF6gAAAAC/come-here-hugs.gif"
        ]
        if member is None:
            return hug_gif[randint(0, len(hug_gif) - 1)]
        else:
            embed = Embed()
            embed.set_image(url=hug_gif[randint(0, len(hug_gif) - 1)])
            msg = "{} hugs {}".format(ctx.author.mention, member.mention)
            return msg, embed

    async def punch(self, ctx: Context, member: discord.Member = None):
        punch_gif = [
            "https://c.tenor.com/EvBn8m3xR1cAAAAC/toradora-punch.gif",
            "https://c.tenor.com/Xcr8fHyf84gAAAAC/baka-anime.gif",
            "https://c.tenor.com/wYyB8BBA8fIAAAAd/some-guy-getting-" /
            "punch-anime-punching-some-guy-anime.gif",
            "https://c.tenor.com/xWqmJMePsqEAAAAS/weaboo-otaku.gif",
            "https://c.tenor.com/l_zcD2qX5M4AAAAC/double-punch-anime" /
            "-double-punch.gif",
            "https://c.tenor.com/7rV7sHfUW_AAAAAC/punch-fight.gif",
            "https://c.tenor.com/jy3svkjYYeIAAAAC/anime-punch.gif",
            "https://c.tenor.com/_llMSP8BqD8AAAAd/punch-oldman.gif",
            "https://c.tenor.com/9Ct49m1OETYAAAAC/manjiro-sano-sano" /
            "-manjiro.gif",
            "https://c.tenor.com/48t1WItOKIMAAAAd/jojos-bizarre-" /
            "adventure-stand.gif"
        ]
        if member is None:
            return punch_gif[randint(0, len(punch_gif) - 1)]
        else:
            embed = Embed()
            embed.set_image(url=punch_gif[randint(0, len(punch_gif) - 1)])
            msg = "{} punches {}".format(ctx.author.mention, member.mention)
            return msg, embed

    async def slap(self, ctx: Context, member: discord.Member = None):
        slap_gif = [
            "https://c.tenor.com/PeJyQRCSHHkAAAAS/saki-saki-mukai-naoya.gif",
            "https://c.tenor.com/Ws6Dm1ZW_vMAAAAC/girl-slap.gif",
            "https://c.tenor.com/9dhSIzaI4o4AAAAC/rascal-rascal-does-not" /
            "-dream-of-bunny-girl-senpai.gif",
            "https://c.tenor.com/E3OW-MYYum0AAAAC/no-angry.gif",
            "https://c.tenor.com/Sp7yE5UzqFMAAAAC/spank-slap.gif",
            "https://c.tenor.com/VlSXTbFcvDQAAAAC/naruto-anime.gif",
            "https://c.tenor.com/2R9-4O6jqEsAAAAC/slap-slapping.gif",
            "https://c.tenor.com/fKzRzEiQlPQAAAAC/anime-slap.gif",
            "https://c.tenor.com/5eI0koENMAAAAAAC/anime-hit.gif",
            "https://c.tenor.com/9PcmapMrg7MAAAAC/meliodas-slapped.gif"
        ]
        if member is None:
            return slap_gif[randint(0, len(slap_gif) - 1)]
        else:
            embed = Embed()
            embed.set_image(url=slap_gif[randint(0, len(slap_gif) - 1)])
            msg = "{} slaps {}".format(ctx.author.mention, member.mention)
            return msg, embed

    async def poke(self, ctx: Context, member: discord.Member = None):
        poke_gif = [
            "https://c.tenor.com/HPlp78w2otYAAAAC/poke-anime.gif",
            "https://c.tenor.com/y4R6rexNEJIAAAAC/boop-anime.gif",
            "https://c.tenor.com/gMqsQ1wwbhgAAAAC/anime-poke.gif",
            "https://c.tenor.com/OVrz7NPyL5wAAAAC/nisekoi-chitoge.gif",
            "https://c.tenor.com/sa1QuA9GFaoAAAAC/anime-tickle.gif",
            "https://c.tenor.com/jNx0V84WbqkAAAAC/anime-anime-poke.gif",
            "https://c.tenor.com/NjIdfk7i3bsAAAAC/poke-poke-poke.gif",
            "https://c.tenor.com/5j7eivfftw8AAAAC/poke.gif",
            "https://c.tenor.com/-8b1jKUBWhEAAAAC/greenarrow-arrow.gif",
            "https://c.tenor.com/59tRi3gEjzUAAAAC/caught-got-cha.gif"
        ]
        if member is None:
            return poke_gif[randint(0, len(poke_gif) - 1)]
        else:
            embed = Embed()
            embed.set_image(url=poke_gif[randint(0, len(poke_gif) - 1)])
            msg = "{} pokes {}".format(ctx.author.mention, member.mention)
            return msg, embed

    async def beer(self, ctx: Context, member: discord.Member = None):
        beer_gif = [
            "https://c.tenor.com/CPbn6ugwh00AAAAC/drink-chug.gif",
        ]
        if member is None:
            return beer_gif[randint(0, len(beer_gif) - 1)]
        else:
            embed = Embed()
            embed.set_image(url=beer_gif[randint(0, len(beer_gif) - 1)])
            msg = "{} gives a beer to {}".format(ctx.author.mention,
                                                 member.mention)
            return msg, embed

    async def howhot(self, ctx: Context, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        return f"**{user.name}** is **{hot:.2f}%** hot {emoji}"

    async def kiss(self, ctx: Context, user: discord.Member = None):
        # kiss_gif = []
        return "not implemented yet"
