#!/bin/bash

# SCRIPT FOR PYTHON 2.6 INSTALLATION
# TODO: validate this script on CENTOS


#SMOKE TESTING FOR PYTHON 2.6
which python2.6 &>/dev/null
if [ $? = 0 ] 
then
  echo "[PYTHON 2.6 ALREADY INSTALLED]"
else
  echo "[PYTHON 2.6 NOT FOUND]"
  echo "do you want to install python2.6 from source? (y/n)"
  while [ "$answer" != "y" ] || [ "$answer" != "n"]; do
    read -n 1 answer
    case "$answer" in
      [Yy] ) 
        echo "[INSTALLING PYTHON 2.6]"
        cd ../lib
        tar -xzf Python-2.6.5.tar.gz
        cd Python-2.6.5
        ./configure
        make
        sudo make altinstall
        cd ../scripts
        if [ $? = 0 ]
        then
           which python2.6 &>/dev/null
           if [ $? = 0 ]
           then
             echo "[PYTHON2.6 INSTALLED SUCCESSFULLY!]"
             exit 0
           else
             exit -1
           fi
        fi

      break
      ;;
      [Nn] ) echo -e "\nno"
        echo "[PYTHON2.6 NOT INSTALLED]" 
        echo "do you want to continue the installation? (y/n)"
        read -n 1 answer2
        case "$answer2" in
          [Yy] )
            echo -e "\n[NEB2ACTIVEMQ INSTALLATION WILL CONTINUE]"
	    exit 0
            ;;
          [Nn] )
            echo -e "\n[NEB2ACTIVEMQ INSTALLATION STOPPED]"
            exit 1
            ;;
        esac
      ;; 
      * ) 
        echo "Please type y for yes or n for no"
      ;;
    esac
  done
    echo "[PYTHON2.6 NOT INSTALLED]"
fi
