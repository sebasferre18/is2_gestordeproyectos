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
        assert respuesta.status_code == 200, "Error, el usuario no cuenta con los permisos requeridos"

    @pytest.mark.django_db
    def test_listar_permisos_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permiso/')
        assert respuesta.status_code == 404, "Error, el usuario no cuenta con los permisos requeridos"

    @pytest.mark.django_db
    def test_crear_permisos(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permissions/create/')
        assert respuesta.status_code == 200, "Error, el usuario no tiene permitido crear Permisos"

    @pytest.mark.django_db
    def test_crear_permisos_fail(self, client, django_user_model):
        username = "usuario1"
        password = "pass"
        user = django_user_model.objects.create_user(username=username, password=password)

        client.force_login(user)
        respuesta = client.get('/roles/permiso/crear/')
        assert respuesta.status_code == 404, "Error, el usuario no tiene permitido crear Permisos"


class TestModelos:
    @pytest.mark.django_db
    def test_rol(self):
        rol = Rol(nombre='pruebarol', descripcion="si")

    @pytest.mark.django_db
    def test_rol_comparacion(self):
        rol = Rol(nombre='pruebarol', descripcion="si")
        assert rol.nombre == 'pruebarol', "Error, el nombre del rol no coincide con el establecido"

    @pytest.mark.django_db
    def test_rol_fallo(self):
        rol = Rol(nombre='pruebarol', descripcion="si")
        assert rol.nombre != 27, "Error, el nombre del rol no coincide con el establecido"

    @pytest.mark.django_db
    def test_permiso(self):
        permiso = Permiso(nombre='pruebapermiso', es_admin=True)

    @pytest.mark.django_db
    def test_permiso_comparacion(self):
        permiso = Permiso(nombre='pruebapermiso', es_admin=True)
        assert permiso.nombre == 'pruebapermiso', "Error, el nombre del permiso no coincide con el determinado"

    @pytest.mark.django_db
    def test_permiso_fallo(self):
        permiso = Permiso(nombre='pruebapermiso', es_admin=True)
        assert permiso.es_admin != 2, "Error, el nombre del permiso no coincide con el determinado"