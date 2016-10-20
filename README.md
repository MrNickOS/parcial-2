##Desarrollo de servicios web con Python 2.6.6 en MV Linux Centos 6.8<br>

###<b>Autor</b>: Nicolás Machado Sáenz<br>
###Universidad Icesi - Semestre 2016-2<br><br>

A continuación veremos cómo realizo la implementación de servicios Web sencillos mediante el lenguaje de programación<br>
Python y el ambiente Flask. En este caso, básicamente se manipularán algunos archivos pertenecientes al directorio raíz<br>
de un usuario, realizando peticiones desde un complemento de navegador Web.<br><br>

####Más especificamente, se realizan las siguientes operaciones sobre el directorio del usuario:<br>
* Creación de archivos con manejo de JSON.
* Obtencion de listado de archivos, tanto total como de recientemente creados.
* Eliminacion de un archivo o directorio de archivos.
      
Antes de proceder con el ejercicio, se crea una cuenta de usuario en Centos 6.8 con el nombre <i>filesystem_user</i> y una<br>
contraseña correspondiente. Una vez creada esta cuenta, se accede a ella y se instala el entorno <i>Flask</i>.<br>
Por otro lado también es necesario contar en el navegador Google Chrome con el complemento web Postman.<br>

###Desarrollo de los servicios<br>

Los servicios se dividen en scripts sobre el lenguaje Python 2.6.6. Para ejecutarlos, es necesario no solo instalar el entorno<br>
de Flask, si no tambien activarlo. Es necesario recordar que si existen otras cuentas de usuario con este entorno instalado, no<br>
implica que pueda omitirse el paso de la instalación para la nueva cuenta. Una vez activado, puede observarse <i>(flask)</i> en la<br>
línea de comandos, y ejecutar así el script principal ingresando al terminal de Centos el comando <i>python files.py</i>.<br><br>

El primer paso es crear el script files_comandos.py que manejará de manera interna los posibles comandos utilizables en la URL<br>
http://IP:puerto/files donde IP y puerto son la dirección IP y el puerto de escucha que utiliza la máquina virtual servidor de<br>
Linux. El código es el siguiente:

```python
from subprocess import Popen, PIPE

def create_file(filename, content):
   proceso1 = Popen(["touch",filename])
   proceso1 = Popen(["echo",content,">>",filename], stdout=PIPE, stderr=PIPE)
   proceso1.wait()
   return True if filename in get_all_files() else False

def get_all_files():
   proceso2 = Popen(["ls", "-l"], stdout=PIPE)
   lista_arch = Popen(["awk",'-F',' ','{print $9}'], stdin=proceso2.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None, lista_arch)

def remove_files():
   if "test-files" in get_all_files():
      proceso3 = Popen(["rm", "-r", "test-files"], stdout=PIPE)
      return True
   else:
      return False
```
Es imprescindible notar que en el método remove_files() se hace referencia a un fichero test-files. Este fichero DEBE crearse<br>
antes de continuar con este tutorial, para evitar confusiones con posibles problemas de funcionalidad del microservicio, y se<br>
ubicará en la misma carpeta donde se hayan creado los scripts, en lo posible, el directorio raiz del usuario.<br>

El siguiente paso es crear un script llamado files_recientes.py el cual gestionará la consulta de archivos recién creados por<br>
el usuario, es decir, durante el periodo inmediatamente anterior a la consulta. En este caso, el código consultará los ficheros<br>
recientes de los últimos 60 minutos y los retorna en una lista.

```python
from subprocess import Popen, PIPE

def get_all_recent():
   elProceso = Popen(["find","-type","f","-mmin","-60"], stdout=PIPE)
   rec_list = Popen(["awk",'-F','/','{print $NF}'],stdin=elProceso.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None,rec_list)
```
 
![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_delete.png)

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_get_files.png)

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_get_files_recent.png)

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_post_recent_404.png)
