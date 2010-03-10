import sys
import sysv_ipc
import time
import datetime

test_service = {
        'check_cpu' : 'usage (%user %system %idle) OK - 0 0 99 | iso.3.6.1.4.1.2021.11.9.0=0 iso.3.6.1.4.1.2021.11.10.0=0 iso.3.6.1.4.1.2021.11.11.0=99',
        'check_disk' : 'Disk space OK - 64031408 kB free ( 3 % used) | iso.3.6.1.4.1.2021.9.1.7.1=64031408 iso.3.6.1.4.1.2021.9.1.9.1=3',
        'check_load' : 'Load average OK - 0 0 0 | iso.3.6.1.4.1.2021.10.1.3.1=0 iso.3.6.1.4.1.2021.10.1.3.2=0 iso.3.6.1.4.1.2021.10.1.3.3=0',
        'check_swap' : 'Swap OK - 16780208 kB total size ( 16780112 kB available space) | iso.3.6.1.4.1.2021.4.3.0=16780208 iso.3.6.1.4.1.2021.4.4.0=16780112',
        'check_http' : 'HTTP OK HTTP/1.1 200 OK - 0.001 second response time |time=0.001378s;;;0.000000 size=259B;;;00',
        'check_fping' : 'FPING OK - riosf109.globoi.com (loss=0%, rta=0.560000 ms)|loss=0%;;;0;100 rta=0.000560s;;;0.000000',
        'check_tcp' : 'TCP OK - 0.092 second response time on port 3737',
        'check_memcached_hit' : 'MEMCACHED OK - OK, Hit checked: OK - at 10.10.48.4:11211',
        'check_memcached_size' : 'MEMCACHED OK - OK, Size checked: OK - at 10.10.245.10:11211',
        'check_mysql_health_connection_time' : 'OK - 0.04 seconds to connect as usr_nagios',
        'check_mysql_health_slow_queries' : 'OK - 0 slow queries in 1024 seconds (0.00/sec)',
        'check_mysql_health_slave-lag' : 'Slave is 10 seconds behind master',
        'check_mysql_health_threads_connected' : 'OK - 3 client connection threads',
        'check_mysql_health_slave-io-running' : 'OK - Slave io is running',
        'check_mysql_health_slave-sql-running' : 'OK - Slave sql is running',
        'check_memory' :"Memory RAM OK - 9005560 kB free ( 17198668 kB used) | iso.3.6.1.4.1.2021.4.6.0=9005560 iso.3.6.1.4.1.2021.4.11.0=17198668",
        'check_passive' : "cameras gcom/live:1 gnews/live:34 gsat/live1:0 gsat/live2:0 gsat/live3:0 g1rj1/live:0 g1sp1/live:89 bbb/pgma:569 bbb/pgmb:478 bbb/cam1:2 bbb/cam2:10 bbb/cam3:5 bbb/cam4:8 bbb/cam5:19 chat/dwt:0 chat/pjc:3 chat/ber1:1 chat/ber2:0 chat/cgj:0",
        
        'check_mysql_health_slave' : "CRITICAL - cannot connect to information_schema. Can't connect to MySQL server on '10.10.138.49' (111)"
}

def main():
  
  DAT = open("fakenagios.dat", "w")

  scale_list = [1.0] #, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0]
 
  period = 600
  
  mq = sysv_ipc.MessageQueue(123456, flags = sysv_ipc.IPC_CREAT, mode = 0644)
  
  for scale in scale_list:
    check = True
    msg_counter = 0
    service_counter = status_counter = 0
    init_time = time.time()
    sleep_delta = 1 / scale
    
    print("Init scale %s" % scale)
    print("Delta %s" % sleep_delta)
    print("Period %s" % period)
    
    while check:
      msg_init_time = time.time()
      try:
        now = datetime.datetime.fromtimestamp(time.time())
        messages_on_queue = mq.current_messages
        DAT.write("%s %d %d\n" % (now.strftime("%H:%M:%S"), scale, messages_on_queue))
        DAT.flush()

        # Manda mensagem
        send_messages(mq, service_counter, status_counter)
        status_counter = (status_counter + 1) % 4
        if status_counter == 0:
            service_counter = (service_counter + 1) % 8

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
        print("Message queue does not exist for key")
        exit(1)
        
  DAT.close()


def send_messages(mq, service_counter, status_counter):
    try:
        for key, item in test_service.iteritems():
            message = 'riold122^%s^%s^%s\0' % (key, status_counter, item)
            print message
            try:
                mq.send(message, block=False, type=13)
            except sysv_ipc.BusyError:
                print "Queue is full, ignoring"
    except:
        print "Something happened. Ignoring."
        pass

if __name__ == "__main__":
    main()
