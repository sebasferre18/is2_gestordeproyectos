from django.contrib import admin
from userstory.models import UserStory, Tarea, Nota

# Register your models here.
admin.site.register(UserStory)
admin.site.register(Tarea)
admin.site.register(Nota)
