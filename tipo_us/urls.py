from django.urls import path, include
from . import views

app_name = 'tipo_us'

urlpatterns = [
    path('', views.listar_tipo_us, name='listar_tipo_us'),
    path('crear_tipo_us/', views.crear_tipo_us, name='crear_tipo_us'),
    path('modificar_tipo_us/<int:tipo_us_id>/', views.modificar_tipo_us, name='modificar_tipo_us'),
    path('eliminar_tipo_us/<int:tipo_us_id>/', views.eliminar_tipo_us, name='eliminar_tipo_us'),
]

'''path('create/', views.crear_proyecto, name='crear_proyecto'),
    path('<int:proyecto_id>/', views.ver_detalles, name='ver_detalles'),
    path('assign/<int:proyecto_id>/', views.asignar_usuarios, name='asignar_usuarios'),
    path('assign_search/', views.asignar_usuarios_busqueda, name='asignar_usuarios_busqueda'),
    path('unassign/<int:proyecto_id>/', views.desasignar_usuarios, name='desasignar_usuarios'),
    path('unassign/<int:proyecto_id>/<int:miembro_id>', views.eliminar_miembro, name='eliminar_miembro'),
    path('roles/', views.administrar_roles, name='administrar_roles'),
    path('start/<int:proyecto_id>/', views.iniciar_proyecto, name='iniciar_proyecto'),
    path('end/<int:proyecto_id>/', views.finalizar_proyecto, name='finalizar_proyecto'),
    path('cancel/<int:proyecto_id>/', views.cancelar_proyecto, name='cancelar_proyecto'),
    path('tipo_us/', include('tipo_us.urls')),'''