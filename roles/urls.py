from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de roles. Es posible visualizar, crear, modificar y eliminar roles.
"""

app_name = 'roles'
urlpatterns = [
    path('proyectos/<int:proyecto_id>/', views.index, name='index'),
    path('proyectos/<int:proyecto_id>/create/', views.crear_rol, name='crear_rol'),
    path('<int:rol_id>/proyectos/<int:proyecto_id>/', views.modificar_rol, name='modificar_rol'),
    path('<int:rol_id>/proyectos/<int:proyecto_id>/delete/', views.eliminar_rol, name='eliminar_rol'),
    path('permissions/', views.permiso_index, name='permiso_index'),
    path('permissions/create/', views.crear_permiso, name='crear_permiso')
]