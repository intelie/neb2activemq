import os


# PYTHON PACKAGES DEPENDENCIES INSTALLATION


packages = [{"stomp": "stomp.py-2.0.4.tar.gz"}, {"sysv_ipc": "sysv_ipc-0.6.1.tar.gz"}, {"chardet": "python2-chardet-2.0.1.tar.gz"}]


#TODO: check version


def install(package_name, file_version):
  try: 
    exec "import %s" % package_name
    print "[PACKAGE %s ALREADY INSTALLED]" % package_name
    return 
  except:
    print "[INSTALLING %s]" % package_name
    if os.path.isfile("/opt/intelie/neb2activemq/ipc2activemq/lib/%s" % file_version):
      os.system('tar zxf /opt/intelie/neb2activemq/ipc2activemq/lib/%s -C /opt/intelie/neb2activemq/ipc2activemq/lib' % file_version)
    #elif os.path.isfile("/opt/intelie/neb2activemq/ipc2activemq/lib/%s.tgz" % file_version):
      #os.system('tar zxf /opt/intelie/neb2activemq/ipc2activemq/lib/%s.tgz -C /opt/intelie/neb2activemq/ipc2activemq/lib' % file_version)
    else:
      print "[PACKAGE NOT FOUND FOR %s]" % package_name
      print "[ABORTING.]"
      exit(-1)
    os.chdir("/opt/intelie/neb2activemq/ipc2activemq/lib/%s" % file_version)
    os.system('sudo python setup.py install')
    os.system('sudo rm -rf /opt/intelie/neb2activemq/ipc2activemq/lib/%s' % file_version)
    os.chdir("/opt/intelie/neb2activemq/scripts")
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
