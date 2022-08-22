from django.contrib import admin

# Register your models here.
from .models import WelcomeData

@admin.register(WelcomeData)
class WelcomeDataAdmin(admin.ModelAdmin):
    list_display = ('server_id', 'server_name', "welcome_enable", 'update_by',
                    'last_update')

