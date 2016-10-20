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
de Flask, si no tambien activarlo. Es necesario recordar que si existen otras cuentas de usuario con este entorno instalado, no
implica que pueda omitirse el paso de la instalación para la nueva cuenta. Una vez activado, puede observarse <i>(flask)</i> en la
línea de comandos, y ejecutar así el script principal ingresando al terminal de Centos el comando <i>python files.py</i>.<br><br>

El primer paso es crear el script files_comandos.py que manejará de manera interna los posibles comandos utilizables en la URL
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
Es imprescindible notar que en el método <i>remove_files()</i> se hace referencia a un fichero <i>test-files</i>. Este fichero DEBE crearse<br>
antes de continuar con este tutorial, para evitar confusiones con posibles problemas de funcionalidad del microservicio, y<br>
se ubicará en la misma carpeta donde se hayan creado los scripts; en lo posible, el directorio raiz del usuario.<br>

El siguiente paso es crear un script llamado <i>files_recientes.py</i> el cual gestionará la consulta de archivos recién creados por<br>
el usuario, es decir, durante el periodo inmediatamente anterior a la consulta. En este caso, el código consultará los ficheros<br>
recientes de los últimos 60 minutos y los retorna en una lista.

```python
from subprocess import Popen, PIPE

def get_all_recent():
   elProceso = Popen(["find","-type","f","-mmin","-60"], stdout=PIPE)
   rec_list = Popen(["awk",'-F','/','{print $NF}'],stdin=elProceso.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None,rec_list)
```

El tercer paso es crear el script files.py. Este actúa como código main, es decir, invoca métodos de los scripts previos y<br>
los ejecuta de manera que quedan enlazados con la URL deseada. En este código fuente, pueden observarse las @app.route que
definen la URL a la que se accederá según la función solicitada al microservicio.<br>
```python
from flask import Flask, abort, request
import json

from files_comandos import create_file, get_all_files, remove_files
from files_recientes import get_all_recent

app = Flask(__name__)

@app.route('/files', methods=['POST'])
def crear_archivo():
   cont_json = request.get_json(silent=False, force=True)
   filename = cont_json['filename']
   content = cont_json['content']
   if not filename:
      return 'No ha asignado un nombre al archivo!',400
   if create_file(filename, content):
      return 'Se ha creado exitosamente el archivo',200
   else:
      return 'No se pudo crear el archivo',400

@app.route('/files', methods=['GET'])
def lista_archivos():
   miLista = {}
   miLista["files"] = get_all_files()
   return json.dumps(miLista)

@app.route('/files', methods=['DELETE'])
def eliminar_archivos():
   if not remove_files():
      return 'No se pudo eliminar exitosamente todos los archivos :(', 400
   else:
      return 'Los archivos fueron eliminados con exito del directorio :)', 200

@app.route('/files', methods=['PUT'])
def colocar_archivos():
   abort(404)

@app.route('/files/recently_created', methods=['GET'])
def lista_recientes():
   recent_list = {}
   recent_list["recent"] = get_all_recent()
   return json.dumps(recent_list)

@app.route('/files/recently_created', methods=['POST'])
def crear_recientes():
   abort(404)

@app.route('/files/recently_created', methods=['DELETE'])
def eliminar_recientes():
   abort(404)

@app.route('/files/recently_created', methods=['PUT'])
def colocar_recientes():
   abort(404)

if __name__ == "__main__":
   app.run(host='0.0.0.0',port=8084,debug='True')
```

###Ejecución del microservicio<br>

Para apreciar la ejecución del servicio Web creado a partir del código fuente presentado, debe activarse el entorno Flask<br>
y escribir en el terminal de comandos la instrucción <i>python files.py</i>. Luego, abrir Postman y acceder a http://IP:puerto/files<br> con IP y puerto como su dirección IP y puerto de escucha. Debe configurarse la solicitud en GET al lado de la URL. Se espera
que Postman despliegue lo que aparece en la figura.<br>

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_get_files.png)

Procedemos luego a cambiar la solicitud HTTP, de GET a DELETE. Debe ocurrir esto en el complemento Postman.<br>

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_delete.png)

En este punto puede notar que la carpeta <i>test-files</i> dejó de existir, compruébelo presionando en la consola CTRL+C seguido<br>
del comando <i>ls</i>. Ahora pasamos de eliminar archivos a crearlos. Para ello, dirigirse a Postman, cambiar la orden DELETE a<br>
POST, dirigirse a la pestaña BODY y seleccionar la opción raw. En el menú desplegable, cambiar a JSON y escribir en el campo de
texto el siguiente fragmento de código.

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

Ahora pasaremos a visualizar los archivos recientemente creados, en un término de 60 minutos. Reinicie el servicio y en la barra<br>
de URL de Postman ingrese la dirección http://IP:puerto/files/recently_created (reemplace IP:puerto por su IP y puerto escucha).<br>
Puede ver una lista de archivos recién creados como se muestra en la siguiente imagen.<br>

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_get_files_recent.png)

###Métodos no utilizados en el microservicio

En las URL existen solicitudes HTTP que no retornan ningún valor y por ende no ofrecen funcionalidades en el microservicio.<br>
Es el caso de PUT para ambas URL utilizadas, o POST y DELETE para http://IP:puerto/files/recently_created. Pruebe el método<br>
POST en la ruta anterior, deberá aparecer en Postman el siguiente mensaje.

![alt tag](https://github.com/MrNickOS/parcial-1/blob/rama_01/postman_post_recent_404.png)

Note el error 404 en Status. Este aparece porque el script principal (refiérase a files.py) definió la respuesta HTTP 404 para<br>
estos casos. Puede probar esto para los métodos especificados en esta sección y sus rutas respectivas.
