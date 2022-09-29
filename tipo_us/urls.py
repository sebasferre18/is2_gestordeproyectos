from django.urls import path, include
from . import views

app_name = 'tipo_us'

urlpatterns = [
    path('<int:proyecto_id>/', views.listar_tipo_us, name='listar_tipo_us'),
    path('crear_tipo_us/<int:proyecto_id>/', views.crear_tipo_us, name='crear_tipo_us'),
    path('modificar_tipo_us/<int:proyecto_id>/<int:tipo_us_id>/', views.modificar_tipo_us, name='modificar_tipo_us'),
    path('eliminar_tipo_us/<int:proyecto_id>/<int:tipo_us_id>/', views.eliminar_tipo_us, name='eliminar_tipo_us'),
    path('importar_tipo_us/<int:proyecto_id>/', views.importar_tipo_us, name='importar_tipo_us'),
    path('importar_tipo_us/<int:proyecto_id>/<int:tipo_us_id>', views.agregar_tipo_us, name='agregar_tipo_us'),
]