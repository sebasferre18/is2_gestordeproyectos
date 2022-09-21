from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Usuario

# Register your models here.


class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'usuarios'


class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
