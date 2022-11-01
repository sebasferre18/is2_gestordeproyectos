from django.contrib import admin

from .models import Sprint, Desarrollador
# Register your models here.


class DesarrolladorInline(admin.TabularInline):
    model = Desarrollador


class SprintAdmin(admin.ModelAdmin):
    inlines = (DesarrolladorInline,)


admin.site.register(Sprint, SprintAdmin)
