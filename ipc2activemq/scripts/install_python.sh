

#SMOKE TESTING FOR PYTHON 2.6
which python2.6 &>/dev/null
if [ $? -eq 0 ] 
then
  echo "[PYTHON 2.6 ALREADY INSTALLED]"
else
  echo "[PYTHON NOT FOUND]"
  #TODO:INSTALLING PYTHON
fi
