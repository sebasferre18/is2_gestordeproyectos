from django.urls import path
from . import views

app_name = 'roles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.crear_rol, name='crear_rol'),
    path('<int:rol_id>/', views.modificar_rol, name='modificar_rol'),
    path('delete/<int:rol_id>/', views.eliminar_rol, name='eliminar_rol')
]

