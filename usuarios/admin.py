from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Usuario

# Register your models here.


class UsuarioInline(admin.StackedInline):
    """
    Se define la clase Inline del modelo Usuario que extiende al modelo User de Django
    """
    model = Usuario
    can_delete = False
    verbose_name_plural = 'usuarios'


class UserAdmin(BaseUserAdmin):
    """
    Se define la clase que logra extender el modelo User de Django
    """
    inlines = (UsuarioInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)