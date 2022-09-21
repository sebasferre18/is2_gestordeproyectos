import os
import django
import pydoc

__author__="Grupo 06"

os.environ['DJANGO_SETTINGS_MODULE'] = 'is2_gestordeproyectos.settings'
django.setup()

pydoc.cli()
