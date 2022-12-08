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
    path('<int:proyecto_id>/', views.ver_detalles, name='ver_detalles'),
    path('assign/<int:proyecto_id>/', views.asignar_usuarios, name='asignar_usuarios'),
    path('unassign/<int:proyecto_id>/', views.desasignar_usuarios, name='desasignar_usuarios'),
    path('assign/<int:proyecto_id>/<int:user_id>', views.agregar_miembro, name='agregar_miembro'),
    path('unassign/<int:proyecto_id>/<int:miembro_id>', views.eliminar_miembro, name='eliminar_miembro'),
    path('start/<int:proyecto_id>/', views.iniciar_proyecto, name='iniciar_proyecto'),
    path('end/<int:proyecto_id>/', views.finalizar_proyecto, name='finalizar_proyecto'),
    path('cancel/<int:proyecto_id>/', views.cancelar_proyecto, name='cancelar_proyecto'),
    path('denied', views.acceso_denegado, name='acceso_denegado'),
    path('<int:proyecto_id>/decline', views.falta_de_permisos, name='falta_de_permisos'),
    path('members/<int:proyecto_id>/<int:miembro_id>', views.gestionar_roles, name='gestionar_roles'),
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('<int:proyecto_id>/historial', views.historial_modificaciones, name='historial_modificaciones')
]
