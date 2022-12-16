from django.contrib import admin

from .models import Proyecto, Miembro, Historial
# Register your models here.


class MiembroInline(admin.TabularInline):
    model = Miembro


class ProyectoAdmin(admin.ModelAdmin):
    inlines = (MiembroInline,)


admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Historial)