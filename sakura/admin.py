from django.contrib import admin

# Register your models here.

from .models import WelcomeData,Server,User

@admin.register(WelcomeData)
class WelcomeDataAdmin(admin.ModelAdmin):
    list_display = ('server_id','server_name',"welcome_enable",'update_by','last_update')

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('server_id','server_name','is_active')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('member_id','discord_tag')

