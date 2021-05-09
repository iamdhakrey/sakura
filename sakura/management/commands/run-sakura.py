from django.core.management.base import BaseCommand,CommandError

from django.conf import settings

import os
import discord

from sakura import bot


def run(TOKEN):
    bot.run(TOKEN)
class Command(BaseCommand):
    help = 'run Sakura Bot'
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[Bot] - Bot Starting..."))

        # print(settings.TOKEN)
        if settings.TOKEN is not None:
            try:
                run(settings.TOKEN)
            except discord.errors.LoginFailure as e:
                self.stderr.write(self.style.ERROR('[Bot] - {0}'.format(e)))
        else:
            self.stderr.write(self.style.ERROR("[Bot] - Token Not Found "))
        # if 'TOKEN' in os.environ:
        #     run(os.environ.get('TOKEN'))
        # elif 'DISCORD_BOTTOKEN' in os.environ:
        #     run(os.environ.get('DISCORD_BOTTOKEN'))
        # else:
        #     print("[Bot] - No TOKEN found!")

        self.stdout.write(self.style.SUCCESS("[Bot] - Bot Stopped...."))