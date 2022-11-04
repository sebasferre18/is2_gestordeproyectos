#!/bin/bash
echo "---Base de datos produccion para entorno de Produccion---"
echo "Borrando base de datos produccion existente..."
dropdb -i --if-exists produccion
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo borrar la base de datos produccion, verifique que no esté siendo usada."
    exit 1
fi
echo "Se ha borrado la base de datos produccion."
echo "Creando la base de datos produccion..."
createdb produccion
if [ "$?" -ne 0 ]
then
    echo -e "No se pudo crear la base de datos produccion"
    exit 2
fi
echo "Se ha creado produccion"

psql -U postgres -d produccion < db.bak
echo "produccion se cargó exitosamente."