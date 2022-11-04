import pytest
from django.urls import reverse
from usuarios.models import Usuario
from roles.models import Rol, Permiso

class TestVistas:
    @pytest.mark.django_db
    def test_listar_permisos(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permissions/')
        assert respuesta.status_code == 200,"Enlace incorrecto"

    @pytest.mark.django_db
    def test_listar_permisos_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permiso/')
        assert respuesta.status_code == 404,"Enlace incorrecto"

    @pytest.mark.django_db
    def test_crear_permisos(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permissions/create/')
        assert respuesta.status_code == 200 ,"Fallo al crear usuario"

    @pytest.mark.django_db
    def test_crear_permisos_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permiso/crear/')
        assert respuesta.status_code == 404 ,"Página no encontrada"


class TestModelos:
    @pytest.mark.django_db
    def test_rol(self):
        rol = Rol(nombre='pruebarol', descripcion="si")

    @pytest.mark.django_db
    def test_rol_comparacion(self):
        rol = Rol(nombre='pruebarol', descripcion="si")
        assert rol.nombre == 'pruebarol'

    @pytest.mark.django_db
    def test_rol_fallo(self):
        rol = Rol(nombre='pruebarol', descripcion="si")
        assert rol.nombre != 27 ,"Rol incorrecto"

    @pytest.mark.django_db
    def test_permiso(self):
        permiso = Permiso(nombre='pruebapermiso', es_admin=True)

    @pytest.mark.django_db
    def test_permiso_comparacion(self):
        permiso = Permiso(nombre='pruebapermiso', es_admin=True)
        assert permiso.nombre == 'pruebapermiso',"Nombre de permiso incorrecto"

    @pytest.mark.django_db
    def test_permiso_fallo(self):
        permiso = Permiso(nombre='pruebapermiso', es_admin=False)
        assert permiso.es_admin != False, "El permiso no es administrativo"

