##Primer Parcial Sistemas Operativos
##Desarrollo de servicios web con Python 2.6.6 en Linux Centos 6.8<br>

###<b>Autor</b>: Nicolás Machado Sáenz<br>
###Universidad Icesi - Semestre 2016-2<br><br>

En este ejercicio se realizo la implementación de servicios Web sencillos mediante el lenguaje de programación Python<br>
y el ambiente Flask. Estos servicios consisten básicamente en la manipulación de archivos pertenecientes a una sesión<br>
de usuario desde un navegador Web.<br><br>

Más especificamente, se realizan las siguientes operaciones sobre el directorio del usuario:<br>
      * Creación de archivos con manejo de JSON.<br>
      * Obtencion de listado de archivos, tanto total como de recientemente creados.<br>
      * Eliminacion de un archivo o directorio de archivos.<br>
      
Antes de proceder con el ejercicio, se crea una cuenta de usuario en Centos 6.8 con el nombre <i>filesystem_user</i> y una<br>
contraseña correspondiente. Una vez creada esta cuenta, se accede a ella y se instala el entorno <i>Flask</i>.<br><br>

###Desarrollo de los servicios<br>

Los servicios se dividen en scripts sobre el lenguaje Python 2.6.6. Para ejecutarlos, es necesario no solo instalar el entorno<br>
de Flask, si no tambien activarlo. Es necesario recordar que si existen otras cuentas de usuario con este entorno instalado, no<br>
implica que pueda omitirse el paso de la instalación para la nueva cuenta. Una vez activado, puede observarse <i>(flask)</i> en la<br>
línea de comandos, y ejecutar así el script principal ingresando al terminal de Centos el comando <i>python files.py</i>.<br><br>

Los scripts utilizados para la implementación de los servicios Web pueden consultarse en este mismo repositorio.<br>
