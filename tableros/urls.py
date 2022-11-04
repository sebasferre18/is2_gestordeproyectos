from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de tableros.
"""

app_name = 'tableros'
urlpatterns = [
    path('sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/', views.index, name='index'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/', views.tablero_detalles, name='tablero_detalles'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/us/<int:us_id>', views.tablero_us_detalles, name='tablero_us_detalles'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/us/<int:us_id>/actualizar', views.actualizar_estado, name='actualizar_estado'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/us/<int:us_id>/registrar', views.registrar_tarea, name='registrar_tarea'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/us/<int:us_id>/adjuntar', views.adjuntar_nota, name='adjuntar_nota'),
    path('<int:tablero_id>/sprints/<int:sprint_id>/proyectos/<int:proyecto_id>/us/<int:us_id>/aprobar', views.aprobar_us, name='aprobar_us'),
]

