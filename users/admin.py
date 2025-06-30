from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_staff', 'display_groups')

    def display_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    display_groups.short_description = 'Grupos'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
