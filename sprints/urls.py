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
    path('<int:sprint_id>/proyectos/<int:proyecto_id>/sprintbacklog', views.sprint_backlog, name='sprint_backlog'),
    path('<int:sprint_id>/proyectos/<int:proyecto_id>/sprintbacklog/add', views.agregar_us, name='agregar_us'),
    path('<int:sprint_id>/proyectos/<int:proyecto_id>/sprintbacklog/add/<int:us_id>', views.agregar_us_sprintbacklog, name='agregar_us_sprintbacklog'),
    path('<int:sprint_id>/proyectos/<int:proyecto_id>/sprintbacklog/remove/<int:us_id>', views.quitar_us, name='quitar_us'),
    path('<int:sprint_id>/proyectos/<int:proyecto_id>/sprintbacklog/approve/<int:us_id>', views.aprobar_us, name='aprobar_us'),
]
