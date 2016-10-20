from subprocess import Popen, PIPE

def get_all_recent():
   elProceso = Popen(["find","-type","f","-mmin","-60"], stdout=PIPE)
   rec_list = Popen(["awk",'-F','/','{print $NF}'],stdin=elProceso.stdout, stdout=PIPE).communicate()[0].split('\n')
   return filter(None,rec_list)