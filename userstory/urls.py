from django.urls import path, include
from . import views

app_name = 'userstory'

urlpatterns = [
    path('listar_us/<int:proyecto_id>/', views.listar_us, name='listar_us'),
    path('crear_us/<int:proyecto_id>/', views.crear_us, name='crear_us'),
    path('modificar_us/<int:proyecto_id>/<int:us_id>/', views.modificar_us, name='modificar_us'),
]