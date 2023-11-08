import os
import signal
import time

import discord
from django.conf import settings
from django.core.management.base import BaseCommand

from sakura.server import bot


def run(TOKEN):
    bot.run(TOKEN)


class Command(BaseCommand):
    help = 'run Sakura Bot'

    # def handle(self, *args, **options):
    #     self.stdout.write(self.style.SUCCESS("[Bot] - Bot Starting..."))

    #     if settings.TOKEN is not None:
    #         try:
    #             run(settings.TOKEN)
    #         except discord.errors.LoginFailure as e:
    #             self.stderr.write(self.style.ERROR('[Bot] - {0}'.format(e)))
    #     else:
    #         self.stderr.write(self.style.ERROR("[Bot] - Token Not Found "))

    #     self.stdout.write(self.style.SUCCESS("[Bot] - Bot Stopped...."))


    def handle(self, *args, **options):
        pid = os.getpid()
        mtime = 0
        while True:
            new_mtime = self.get_last_modified_time()
            if new_mtime > mtime:
                mtime = new_mtime
                self.stdout.write(self.style.SUCCESS("Restarting server..."))
                self.stdout.write(self.style.SUCCESS("[Bot] - Bot Starting..."))

                if settings.TOKEN is not None:
                    try:
                        run(settings.TOKEN)
                    except discord.errors.LoginFailure as e:
                        self.stderr.write(self.style.ERROR('[Bot] - {0}'.format(e)))
                else:
                    self.stderr.write(self.style.ERROR("[Bot] - Token Not Found "))

                self.stdout.write(self.style.SUCCESS("[Bot] - Bot Stopped...."))
                # run(settings.TOKEN)

                os.kill(pid, signal.SIGTERM)
            time.sleep(1)

    def get_last_modified_time(self):
        mtime = 0
        for dirpath, dirnames, filenames in os.walk("."):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if path.endswith(".py"):
                    file_mtime = os.path.getmtime(path)
                    if file_mtime > mtime:
                        mtime = file_mtime
        return mtime