from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de proyectos. Es posible visualizar, crear proyectos, asi como
asignar, desasignar y administrar roles de los usuarios de un proyecto.
"""

app_name = 'proyectos'
urlpatterns = [
    path('', views.listar_proyectos, name='listar_proyectos'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('<int:id_proyecto>/asignar_usuarios/', views.asignar_usuarios, name='asignar_usuarios'),
    path('<int:id_proyecto>/asignar_usuarios_busqueda/', views.asignar_usuarios_busqueda, name='asignar_usuarios_busqueda'),
    path('<int:id_proyecto>/desasignar_usuarios/', views.desasignar_usuarios, name='desasignar_usuarios'),
    path('<int:id_proyecto>/administrar_roles/', views.administrar_roles, name='administrar_roles'),
]
'''path('create/', views.crear_rol, name='crear_rol'),
    path('<int:rol_id>/', views.modificar_rol, name='modificar_rol'),
    path('delete/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol'),'''