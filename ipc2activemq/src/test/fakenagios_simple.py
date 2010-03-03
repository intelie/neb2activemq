
testes = {'diskOk' : 'Disk space OK - 8899052 kB free ( 39 % used)',
        'diskWarning' : 'Disk space WARNING - 6647236 kB free ( *61* % used)',
        'diskCritical' : 'Disk space CRITICAL - 6647224 kB free ( *61* % used)',
        'cpuOk' : 'CPU usage (%user %system %idle) OK - 0 0 99',
        'cpuWarning' : 'CPU usage (%user %system %idle) WARNING - 0 0 *99*',
        'cpuCritical' : 'CPU usage (%user %system %idle) CRITICAL - 0 0 *99*',
        'loadOk' : 'Load average OK - 0 0 0',
        'loadWarning' : 'Load average WARNING - 0 0 *2*',
        'loadCritical' : 'Load average CRITICAL - 0 0 *5*',
        'memoryOk' : 'Memory RAM OK - 81808 kB free ( 2088564 kB used)',
        'memoryWarning' : 'Memory RAM WARNING - *185900* kB free ( 2182264 kB used)',
        'memoryCritical' : 'Memory RAM CRITICAL - *185060* kB free ( 2181424 kB used)',
        'swapOk' : 'Swap OK - 2097144 kB total size ( 2097144 kB available space)',
        'swapWarning' : 'Swap WARNING - 2104504 kB total size ( *1996364* kB available space)',
        'swapCritical' : 'Swap CRITICAL - 2104504 kB total size ( *1996364* kB available space)',
        'queryOk' :"QUERY OK: 'select count(*) from nagios_hosts' returned 53.000000",
        'queryWarning' : "QUERY WARNING: 'select count(*) from nagios_hosts' returned 53.000000",
        'queryCritical' : "QUERY CRITICAL: 'select count(*) from nagios_hosts' returned 53.000000",
        'smtpOk' : 'SMTP OK - 0.010 sec. response time',
        'smtpWarning' : 'SMTP WARNING - 0.016 sec. response time',
        'smtpCritical' : 'SMTP CRITICAL - 0.550 sec. response time',        
        'srvvld48Ok' : 'FPING OK - srvvld48.test.com (loss=0%, rta=1.010000 ms)',
        'srvvld48Warning' : 'FPING WARNING - srvvld48.globoi.com (loss=0%, rta=0.560000 ms)',
        'srvvld48Critical' : 'FPING CRITICAL - srvvld48.test.com (loss=100% )'
        
}


import sysv_ipc
import re
import time

def main():      
  
  DAT = open("fakenagios.dat", "w")

  scale_list = [100.0]
 
  period = 60*10
  
  mq = sysv_ipc.MessageQueue(123456, flags = sysv_ipc.IPC_CREAT , mode = 0644)
  
  for scale in scale_list:
    check = True
    msg_counter = 0
    init_time = time.time()
    print("Init scale %s" % scale)
    sleep_delta = 1 / scale
    print("Delta %s" % sleep_delta)
    print("Period %s" % period)
    
    while check: 
      msg_init_time = time.time()
      try:    
        DAT.write("%d %d\n" % (time.time(), scale))
        DAT.flush()        
        # Manda mensagem
        send_message(mq, msg_counter % 6)
        # calcula o tempo que deveria dormir descontando o tempo de envio
        msg_counter = msg_counter + 1
        now = time.time()
        sleep_time = sleep_delta - (now - msg_init_time)
         
        
        if sleep_time > 0:
          time.sleep(sleep_time) 
        if  (now > init_time + period ):
          print(">>>>> Sent %s messages. Average of %s per sec" %(msg_counter,str(msg_counter/(now-init_time))))
          check = False
      except KeyboardInterrupt:
        DAT.close()
        print("User interrupted. Shutting down.")
        exit(0)
      except sysv_ipc.ExistentialError:
        print("Message queue does not exist for key"  )
        exit(1)
        
  DAT.close() 
  
  
def send_message(mq,option):
  if option == 0 :
    message = str('hostname^check_disk^0^%s' %testes['diskOk'])
    mq.send(message, type = 13)
  elif option == 1:
    message = str('hostname^check_disk^1^%s' %testes['diskWarning'])
    mq.send(message, type = 13)
  elif option == 2:
    message = str('hostname^check_disk^2^%s' %testes['diskCritical'])
    mq.send(message, type = 13)
  elif option == 3:
    message = str('srvvld58^%s' %testes['srvvld48Ok'])
    mq.send(message, type = 14)
  elif option == 4:
    message = str('srvvld58^%s' %testes['srvvld48Warning'])
    mq.send(message, type = 14)
  elif option == 5:
    message = str('srvvld58^%s' %testes['srvvld48Critical'])
    mq.send(message, type = 14)
    
    
  
  
if __name__ == "__main__":
  main()

