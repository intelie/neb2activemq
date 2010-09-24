import os


# PYTHON PACKAGES DEPENDENCIES INSTALLATION


packages = [{"stomp": "stomp.py-2.0.4"}, {"sysv_ipc": "sysv_ipc-0.6.1"}, {"chardet": "python2-chardet-2.0.1"}]


#TODO: check version


def install(package_name, file_version):
  try: 
    exec "import %s" % package_name
    print "[PACKAGE %s ALREADY INSTALLED]" % package_name
    return 
  except:
    print "[INSTALLING %s]" % package_name
    if os.path.isfile("../lib/%s.tar.gz" % file_version):
      os.system('tar -xzf ../lib/%s.tar.gz -C ../lib' % file_version)
    elif os.path.isfile("../lib/%s.tgz" % file_version):
      os.system('tar -xzf ../lib/%s.tgz -C ../lib' % file_version)
    else:
      print "[PACKAGE NOT FOUND FOR %s]" % package_name
      print "[ABORTING.]"
      exit(-1)
    os.chdir("../lib/%s" % file_version)
    os.system('sudo python2.6 setup.py install')
    os.system('sudo rm -rf ../lib/%s' % file_version)
    os.chdir("../../scripts")
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
