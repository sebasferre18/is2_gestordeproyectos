from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de tableros.
"""

app_name = 'tableros'
urlpatterns = [
    path('sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/', views.index, name='index'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/', views.tablero_detalles, name='tablero_detalles'),
]
