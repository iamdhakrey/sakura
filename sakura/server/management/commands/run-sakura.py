import discord
from django.conf import settings
from django.core.management.base import BaseCommand
from sakura.server import bot


def run(TOKEN):
    bot.run(TOKEN)


class Command(BaseCommand):
    help = 'run Sakura Bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("[Bot] - Bot Starting..."))

        if settings.TOKEN is not None:
            try:
                run(settings.TOKEN)
            except discord.errors.LoginFailure as e:
                self.stderr.write(self.style.ERROR('[Bot] - {0}'.format(e)))
        else:
            self.stderr.write(self.style.ERROR("[Bot] - Token Not Found "))

        self.stdout.write(self.style.SUCCESS("[Bot] - Bot Stopped...."))
