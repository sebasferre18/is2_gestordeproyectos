#!/bin/bash
echo "---Base de datos desarrollo para entorno de Desarrollo---"
echo "Borrando base de datos desarrollo existente..."
dropdb -i --if-exists desarrollo
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos desarrollo, verifique que no esté siendo usada."
    exit 1
fi
echo "Se ha borrado la base de datos desarrollo."
echo "Creando la base de datos desarrollo..."
createdb desarrollo
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear la base de datos desarrollo"
    exit 2
fi
echo "Se ha creado desarrollo"

psql -U postgres -d desarrollo < db.bak
echo "desarrollo se cargó exitosamente."