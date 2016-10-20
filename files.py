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