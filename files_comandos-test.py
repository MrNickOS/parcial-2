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
