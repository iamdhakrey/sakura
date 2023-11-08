from sakura.bot.cmd.basic import setup as basic_setup
from sakura.bot.cmd.fun import setup as fun_setup
from sakura.bot.cmd.help import setup as help_setup
from sakura.bot.cmd.moderation import setup as mod_setup
from sakura.bot.cmd.music import setup as music_setup
from sakura.bot.cmd.welcome import setup as welcome_setup

def cmd_setup(bot):
    basic_setup(bot)
    fun_setup(bot)
    help_setup(bot)
    mod_setup(bot)
    music_setup(bot)
    welcome_setup(bot)
    