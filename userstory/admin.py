from django.contrib import admin
from userstory.models import UserStory, Tarea, Nota, TareaAux

# Register your models here.
admin.site.register(UserStory)
admin.site.register(Tarea)
admin.site.register(TareaAux)
admin.site.register(Nota)
