from sakura.bot.slash.basic import setup as basic_setup
from sakura.bot.slash.fun import setup as fun_setup
from sakura.bot.slash.moderation import setup as moderation_setup
from sakura.bot.slash.self_role import setup as self_role_setup
from sakura.bot.slash.music import setup as music_setup


def setup(bot):
    basic_setup(bot)
    fun_setup(bot)
    moderation_setup(bot)
    self_role_setup(bot)
    music_setup(bot)
