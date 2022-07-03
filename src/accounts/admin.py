from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomAccount

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_active', 'is_staff', )
    list_display_links = ('email', 'username',)
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)
    list_filter = ()
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(CustomAccount)