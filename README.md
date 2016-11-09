##Pruebas unitarias de servicios con Pytest, Continuous Integration en Jenkins<br>

###<b>Autor</b>: Nicolás Machado Sáenz Cod. 13207014<br>
###Universidad Icesi - Semestre 2016-2<br><br>

Para esta actividad se realizaron pruebas unitarias a diferentes servicios en el lenguaje Python. Esto es, se verifica el funcionamiento de los mismos a través de una instrucción denominada assert, lo cual significa generar escenarios en los cuales la función ensayada puede devolver un resultado de error o de ejecución correcta. Las funciones a probar derivan de las utilizadas en el parcial 1.

####Más especificamente, se realizan las siguientes operaciones sobre el directorio del usuario:<br>
* Creación de archivos cualesquiera.
* Eliminación de archivos, a partir de la obtención de una lista.
* Comprobación de archivos recientes; comprueba si un archivo fue creado dentro de un tiempo determinado.
      
Para la plataforma Jenkins no se utilizaron credenciales, se trabajo sobre la cuenta de usuario <b>root</b> en Centos 6.8 Servidor y se utilizó el ambiente <b>testproject</b>.

###Implementación de los servicios y sus pruebas<br>

Los servicios generados en esta ocasión toman como base los scripts que proveen servicios Web correspondientes al I Parcial. Sobre estos se ejecutaron algunas modificaciones, incluyendo la eliminación de etiquetas a trafico web, la inclusión de metodos prueba en todos los scripts y el hecho de no trabajar más sobre lenguaje JSON.

Primeramente se trabaja sobre el script files_comandos-test.py, que define los servicios prestados como son la creación de ficheros (no incluye directorios), y la eliminación de archivos a partir de una lista obtenida de todos los ficheros presentes en el directorio donde se ejecuta la aplicación. Así mismo, se adicionan un par de métodos los cuales ejecutan la instrucción assert sobre un escenario basado en los parámetros de prueba ingresados en estas funciones. Esto se puede apreciar en la figura 1.

```python
from subprocess import Popen, PIPE
import pytest

def create_file(filename, content):
   if filename == '':
	print "No hay un nombre para el archivo"
	return False
   elif content == '':
	print "No se puede crear archivos vacios"
	return False
   else:
   	proceso1 = Popen(["touch",filename])
   	proceso1 = Popen(["echo",content,">>",filename], stdout=PIPE, stderr=PIPE)
   	proceso1.wait()
   	return True if filename in get_all_files() else False

def prueba_create_file(nom_arch, cont_arch):
   assert create_file(nom_arch, cont_arch), "Imposible generar el fichero "+nom_arch

def get_all_files():
   proceso2 = Popen(["ls", "-l"], stdout=PIPE)
   lista_arch = Popen(["awk",'-F',' ','{print $9}'], stdin=proceso2.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None, lista_arch)

def remove_files(file_remove):
   if file_remove in get_all_files():
      proceso3 = Popen(["rm", "-r", file_remove], stdout=PIPE)
      return True
   else:
      return False

def prueba_get_remove(arch_eliminar):
   assert remove_files(arch_eliminar), "Imposible eliminar "+arch_eliminar+": El fichero no existe!" 
```

La siguiente actividad es generar un script llamado <i>files_recientes-test.py</i> que accede a una lista de archivos recién creados por el usuario. En este caso, el código implementa el método de prueba, que consulta si un archivo cuyo nombre es pasado por parámetro hace parte de los ficheros generados durante los últimos X minutos (también como argumento) y, si no es así, devuelve un AssertionError.

```python
from subprocess import Popen, PIPE
import pytest

def get_all_recent(tiempo):
   mmin = "-" + str(tiempo)
   elProceso = Popen(["find","-type","f","-mmin", mmin], stdout=PIPE)
   rec_list = Popen(["awk",'-F','/','{print $NF}'],stdin=elProceso.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None,rec_list)

def prueba_recent(n_arch, time):
   assert "nombres" in get_all_recent(time), "No se ha creado un archivo "+n_arch+" en los ultimos "+str(time)+" minutos"
```

A continuación se escribe el código fuente de files-test.py. Este script es el main de la aplicación, accede a las funciones que proveen los códigos generados anteriormente y propone escenarios en donde las funciones principales pueden ejecutarse exitosamente o fallar si algún parámetro es incorrecto o no se puede acceder a un recurso específico.

```python
from flask import Flask, abort, request
import json

from files_comandos import create_file, prueba_create_file, get_all_files, remove_files, prueba_get_remove
from files_recientes import get_all_recent, prueba_recent

app = Flask(__name__)

def test_crear_archivo():
   prueba_create_file("primero", "Primer archivo de test")
   prueba_create_file("", "Fichero vacio")
   prueba_create_file("segundo", "Fichero de pruebas numero 2")
   prueba_create_file("5ntenido", "")

def test_lista_recientes():
   prueba_recent("primero", 20)
   prueba_recent("segundo", 15)
   prueba_recent("otro", 60)
   prueba_recent("5ntenido", 90)

def test_lista_eliminar_archivos():
   prueba_get_remove("segundo")
   prueba_get_remove("5ntenido")
   prueba_get_remove("tercero")
   prueba_get_remove("primero")

if __name__ == "__main__":
   app.run('0.0.0.0')
```

###Habilitación del ambiente<br>

Para poder ejecutar los scripts en Pytest, se debe habilitar el ambiente testproject. Esto se realiza en la consola de comandos de Linux Centos 6.8 Servidor tal como se muestra en la siguiente figura.

![alt tag](https://github.com/MrNickOS/parcial-2/blob/rama_01/activate_testproject.png)

Procedemos entonces a probar el script principal en Pytest. Como nos encontramos en el directorio raíz, el argumento del comando pytest incluye la ruta completa del script a testear. El resultado puede verse en el screenshot a continuación.

![alt tag](https://github.com/MrNickOS/parcial-2/blob/rama_01/pytest_prueba.png)

Nótese en esta parte de la actividad que no solo se ha probado las funciones del microservicio; también se han ejecutado, puede verse al final de la imagen un archivo "primero" creado durante el test (en la mitad de la imagen).

```json
{
	"filename":"carta",
	"content": "this is a file content"
}
```

Luego, reiniciar en la consola Linux el servicio Web files.py y reingresar a la URL con el método POST. Debe visualizar esto:

![alt tag] (https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_post_files.png)

Verificar que efectivamente el archivo ha sido creado, ingresando en la consola de comandos la instrucción <i>ls</i>. Debe ver un<br>
archivo denominado carta.<br>

Ahora pasaremos a visualizar los archivos recientemente creados, en un término de 60 minutos. Reinicie el servicio y en la barra
de URL de Postman ingrese la dirección http://IP:puerto/files/recently_created (reemplace IP:puerto por su IP y puerto escucha).<br>
Puede ver una lista de archivos recién creados como se muestra en la siguiente imagen.<br>

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_get_files_recent.png)

###Métodos no utilizados en el microservicio

En las URL existen solicitudes HTTP que no retornan ningún valor y por ende no ofrecen funcionalidades en el microservicio.
Es el caso de PUT para ambas URL utilizadas, o POST y DELETE para http://IP:puerto/files/recently_created. Pruebe el método
POST en la ruta anterior, deberá aparecer en Postman el siguiente mensaje.

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_post_recent_404.png)

Note el error 404 en Status. Este aparece porque el script principal (refiérase a files.py) definió la respuesta HTTP 404 para<br>
estos casos. Puede probar esto para los métodos especificados en esta sección y sus rutas respectivas.
