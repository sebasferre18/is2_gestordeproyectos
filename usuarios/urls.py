from django.urls import path
from . import views

"""
Definicion de URLs para la gestion de usuarios. Es posible visualizar, crear, modificar y eliminar usuarios.
"""

app_name = 'usuarios'
urlpatterns = [
    path('nuevo_usuario/', views.nuevo_usuario, name='nuevo_usuario'),
    path('listar_usuarios/', views.usuario_list, name='listar_usuarios'),
    path('<int:id_usuario>/modificar_usuario/', views.modificar_usuario, name='modificar_usuario'),
    path('<int:id_usuario>/eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),
]