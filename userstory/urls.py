from django.urls import path, include
from . import views

app_name = 'userstory'

urlpatterns = [
    path('listar_us/', views.listar_us, name='listar_us'),
    path('crear_us/', views.crear_us, name='crear_us'),
    path('modificar_us/<int:us_id>/', views.modificar_us, name='modificar_us'),
]