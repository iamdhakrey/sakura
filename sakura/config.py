from django.conf import settings
import os

SAKURA_DEBUG = True

MAIN_PREFIXES = ['y_']

MEDIA_ROOT = settings.MEDIA_ROOT

COGS_FOLDER = "sakura.BotCMD"

DEFINED_COGS = ['basic','moderation','welcome','anime','self_role']