import os


# PYTHON PACKAGES DEPENDENCIES INSTALLATION
# execute with sudo

packages = [{"stomp": "stomp.py-2.0.4"}, {"sysv_ipc": "sysv_ipc-0.5.2"}, {"chardet": "python2-chardet-2.0.1"}]


#TODO: install python2.6
#TODO: check version

def install(package_name, file_version):
  try: 
    exec "import %s" % package_name
    print "[PACKAGE %s ALREADY INSTALLED]" % package_name
    return 
  except:
    print "[INSTALLING %s]" % package_name
    if os.path.isfile("%s.tar.gz" % file_version):
      os.system('tar -xzvf %s.tar.gz' % file_version)
    elif os.path.isfile("%s.tgz" % file_version):
      os.system('tar -xzvf %s.tgz' % file_version)
    else:
      print "[PACKAGE NOT FOUND FOR %s]" % package_name
      print "[ABORTING.]"
      exit(-1)
    os.chdir(file_version)
    os.system('python2.6 setup.py install')
    os.system('rm -rf %s' % file_version)
    os.chdir("..")
    try:
      exec "import %s" % package_name
      print "[%s INSTALLED!]" % package_name
    except ImportError:
      print "[ERROR INSTALLING %s]" % package_name
      exit(-1)



if __name__ == "__main__":
  for package in packages:
      for k, v in package.items():
        install(k, v)
  print "[DEPENDENCIES INSTALLED WITH SUCCESS]"
  exit(0)
