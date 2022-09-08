from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de proyectos. Es posible visualizar, crear proyectos, asi como
asignar, desasignar y administrar roles de los usuarios de un proyecto.
"""

app_name = 'proyectos'
urlpatterns = [
    path('', views.listar_proyectos, name='listar_proyectos'),
    path('create/', views.crear_proyecto, name='crear_proyecto'),
    path('assign/', views.asignar_usuarios, name='asignar_usuarios'),
    path('assign_search/', views.asignar_usuarios_busqueda, name='asignar_usuarios_busqueda'),
    path('unassign/', views.desasignar_usuarios, name='desasignar_usuarios'),
    path('roles/', views.administrar_roles, name='administrar_roles'),
]
'''path('create/', views.crear_rol, name='crear_rol'),
    path('<int:rol_id>/', views.modificar_rol, name='modificar_rol'),
    path('delete/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol'),'''