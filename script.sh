#!/bin/bash
mkdir -p media
chmod 777 media
mkdir -p static
echo "¡Bienvenido al Sistema Gestor de Proyectos del Grupo 6!"
echo "Seleccione uno de los siguientes entornos de despliegue:"
PS3='Por favor, ingrese una opción: '
options=("Desarrollo" "Producción" "Pruebas Unitarias" "Documentacion" "Salir")
select opt in "${options[@]}"
do
    case $opt in
        "Desarrollo")
            echo "Elegió desplegar el ambiente de desarrollo..."
            echo
            pip install -r requirements.txt
            echo
            chmod +x desarrolloconf.sh
            sudo -u postgres ./desarrolloconf.sh
            echo "El ambiente de desarrollo fue desplegado correctamente."
            break
            ;;
        "Producción")
            echo "Eligió desplegar el ambiente de producción..."
            echo
            pip install -r requirements.txt
            echo
            chmod +x produccionconf.sh
            sudo -u postgres ./produccionconf.sh
            cd ..
            path=$(pwd)
            cd is2_gestordeproyectos
            echo "Configurando servidor httpd..."
            echo "# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf

Listen 8080

<IfModule ssl_module>
	Listen 443
</IfModule>

<IfModule mod_gnutls.c>
	Listen 443
</IfModule>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet" | sudo tee /etc/apache2/ports.conf
            echo "<VirtualHost *:8080>

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog $path/logs/error.log
        CustomLog $path/logs/access.log combined

</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet

WSGIScriptAlias / $path/is2_gestordeproyectos/is2_gestordeproyectos/wsgi.py
# WSGIPythonHome /usr/bin/python3.10
WSGIPythonPath $path/is2_gestordeproyectos

<Directory $path/is2_gestordeproyectos/is2_gestordeproyectos>
<Files wsgi.py>
	Require all granted
</Files>
</Directory>" | sudo tee /etc/apache2/sites-available/000-default.conf
            service apache2 restart
            echo "El ambiente de produccion fue desplegado correctamente."
            break
            ;;
        "Pruebas Unitarias")
            echo "Eligio desplegar las pruebas unitarias."
            pytest --tb=short
            break
            ;;
        "Documentacion")
            echo "Eligio desplegar la documentacion."
            python django_pydoc.py -p 1234
            break
            ;;
        "Salir")
            break
            ;;
        *) echo "Opción inválida";;
    esac
done