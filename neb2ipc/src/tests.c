/* include (minimum required) event broker header files */
#include "./include/nebmodules.h"
#include "./include/nebcallbacks.h"

/* include other event broker header files that we need for our work */
#include "./include/nebstructs.h"
#include "./include/broker.h"
/* include some Nagios stuff as well */
#include "./include/config.h"
#include "./include/common.h"
#include "./include/nagios.h"
/* includes for IPC */
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/msg.h>

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <google/cmockery.h>

host * find_host(char *name) {
  return (host *) mock();
}

service * find_service(char *host_name, char *svc_desc) {
  return (service *) mock();
}


void test_OK_HOST_CHECK(void **state) {
  
  struct host_struct hst;
  hst.scheduled_downtime_depth = 0;
  hst.name = "localhost name";
  will_return(find_host, &hst); 
  
  int msqid;
  msqid = msgget(1219, IPC_CREAT | 0600);
  int event_type = NEBCALLBACK_HOST_CHECK_DATA ;

  struct my_msgbuf {
    long mtype;
    char mtext[512];
  } buf;
  nebstruct_host_check_data hcdata;
   
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
  hcdata.host_name = "localhost";
  hcdata.output = "Mensagem enviada para a fila do IPC";
  
  neb2ipc_handle_data(event_type, &hcdata, msqid);
  msgrcv(msqid, &buf, sizeof buf, event_type, 0);
  char msg[100];
  sprintf(msg, "%s^%i^%i^%s", hst.name, hcdata.state,hst.scheduled_downtime_depth, hcdata.output);
  assert_string_equal(buf.mtext, msg);
}

void test_SERVICE_CHECK_NULL_HOST(void **state) {
  
  struct host_struct hst;
  hst.scheduled_downtime_depth = 0;
  hst.name = "localhost name\0";
  will_return(find_host, &hst); 


  int msqid;
  msqid = msgget(1219, IPC_CREAT | 0600);
  int event_type = NEBCALLBACK_SERVICE_CHECK_DATA;

  struct my_msgbuf {
    long mtype;
    char mtext[512];
  } buf;
  nebstruct_service_check_data scdata;
  scdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
  scdata.host_name = "localhost\0";
  scdata.output = "Mensagem enviada para a fila do IPC\0";
  scdata.state = 1;
  neb2ipc_handle_data(event_type, &scdata, msqid);
  msgrcv(msqid, &buf, sizeof buf, event_type, 0);

  char msg[100];
  sprintf(msg, "%s^%s^%i^%i^%s", scdata.host_name, scdata.command_name, scdata.state, hst.scheduled_downtime_depth, scdata.output);
  assert_string_equal(buf.mtext, msg);

}

void test_NULL_HOST(void **state) {

  struct host_struct hst;
  hst.scheduled_downtime_depth = 0;
  hst.name = NULL;
  will_return(find_host, &hst); 
  int msqid;
  msqid = msgget(1219, IPC_CREAT | 0600);
  int event_type = NEBCALLBACK_HOST_CHECK_DATA;

  struct my_msgbuf {
    long mtype;
    char mtext[512];
  } buf;
  nebstruct_host_check_data hcdata;
   
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
  hcdata.host_name = "localhost";
  hcdata.output = "Mensagem enviada para a fila do IPC";
  
  neb2ipc_handle_data(event_type, &hcdata, msqid);
  msgrcv(msqid, &buf, sizeof buf, event_type, 0);
  char msg[100];
  sprintf(msg, "%s^%i^%i^%s", hcdata.host_name, hcdata.state, ERROR_FIND_HOST, hcdata.output);
  assert_string_equal(buf.mtext, msg);

}

int main(int argc, char *argv[]) {
  const UnitTest tests[] = {
                            unit_test(test_OK_HOST_CHECK),
                            unit_test(test_NULL_HOST),
                            unit_test(test_SERVICE_CHECK_NULL_HOST),
                           };
return run_tests(tests);
}
