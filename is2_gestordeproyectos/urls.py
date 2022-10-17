from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('roles/', include('roles.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('accounts/profile/', views.home, name='home'),
    path('proyectos/', include('proyectos.urls')),
    path('tipo_us/', include('tipo_us.urls')),
    path('userstory/', include('userstory.urls')),
    path('sprints/', include('sprints.urls')),
]
