from django.contrib import admin

# Register your models here.
from .models import SelfRole

@admin.register(SelfRole)
class SelfRoleAdmin(admin.ModelAdmin):
    list_display = ('server', 'message_id', 'max_role', "last_update")
