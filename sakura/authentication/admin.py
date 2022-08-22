from django.contrib import admin

# Register your models here.

from .models import  DiscordUser

@admin.register(DiscordUser)
class DiscordUserModel(admin.ModelAdmin):
    list_display = ('id','discord_tag','last_login','avatar')
    search_fields = ('id','discord_tag')