"""Prueba de documentacion"""

def func(x):
    return x + 1


def test_answer():
    """Funcion de prueba.

    Retorna True si func(a) es igual a 5"""
    assert func(3) == 5


class TestClass(object):
    """Prueba de documentacion"""
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')
