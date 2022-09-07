from django.urls import path
from . import views

app_name = 'usuarios'
urlpatterns = [
    path('nuevo_usuario/', views.nuevo_usuario, name='nuevo_usuario'),
    path('listar_usuarios/', views.usuario_list, name='listar_usuarios'),
    path('<int:id_usuario>/modificar_usuario/', views.modificar_usuario, name='modificar_usuario'),

]