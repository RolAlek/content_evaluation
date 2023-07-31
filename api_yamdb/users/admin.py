from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser

UserAdmin.fieldsets += (
    ('Роль', {'fields': ('role',)}),
    ('Дополнительная информация', {'fields': ('bio',)}),
)

admin.site.register(CustomUser, UserAdmin)
