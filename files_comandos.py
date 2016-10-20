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