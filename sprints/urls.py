from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de sprints.
"""

app_name = 'sprints'
urlpatterns = [
    path('proyectos/<int:proyecto_id>/', views.index, name='index'),
    path('<int:sprint_id>/proyectos/<int:proyecto_id>/', views.ver_detalles, name='ver_detalles'),
    path('proyectos/<int:proyecto_id>/create/', views.crear_sprint, name='crear_sprint'),
]
