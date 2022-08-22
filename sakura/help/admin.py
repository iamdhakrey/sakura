from django.contrib import admin

from .models import HelpCmd

# Register your models here.
@admin.register(HelpCmd)
class HelpCmdAdmin(admin.ModelAdmin):
    list_display = ('cmd', 'description', 'usage', 'brief', 'alias', 'category')