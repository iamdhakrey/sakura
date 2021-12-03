from django.conf import settings
import os

SAKURA_DEBUG = True

MAIN_PREFIXES = ['y_']

MEDIA_ROOT = settings.MEDIA_ROOT

COGS_FOLDER = "sakura.bot.cmd"

DEFINED_COGS = ['basic','moderation','welcome','fun','self_role','music','help']