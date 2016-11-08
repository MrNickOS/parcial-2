from subprocess import Popen, PIPE
import pytest

def get_all_recent(tiempo):
   mmin = "-" + str(tiempo)
   elProceso = Popen(["find","-type","f","-mmin", mmin], stdout=PIPE)
   rec_list = Popen(["awk",'-F','/','{print $NF}'],stdin=elProceso.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None,rec_list)

def prueba_recent(n_arch, time):
   assert "nombres" in get_all_recent(time), "No se ha creado un archivo "+n_arch+" en los ultimos "+str(time)+" minutos"
