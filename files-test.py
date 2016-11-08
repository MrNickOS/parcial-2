from flask import Flask, abort, request
import json

from files_comandos import create_file, prueba_create_file, get_all_files, remove_files, prueba_get_remove
from files_recientes import get_all_recent, prueba_recent

app = Flask(__name__)

def test_crear_archivo():
   #cont_json = request.get_json(silent=False, force=True)
   #filename = cont_json['filename']
   #content = cont_json['content']
   #if not filename:
   #   return 'No ha asignado un nombre al archivo!'
   #if create_file(filename, content):
   #   return 'Se ha creado exitosamente el archivo'
   #else:
   #   return 'No se pudo crear el archivo'
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
