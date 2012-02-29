/* include (minimum required) event broker header files */
#include "./include/nebmodules.h"
#include "./include/nebcallbacks.h"

/* include other event broker header files that we need for our work */
#include "./include/nebstructs.h"
#include "./include/broker.h"
/* include some Nagios stuff as well */
#include "./include/config.h"
#include "./include/common.h"
//#include "./include/nagios.h"
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



int neb_register_callback(int callback_type, void *mod_handle, int priority, int (*callback_func)(int,void *)) {
  return (int) mock();
}

int schedule_new_event(int event_type, int high_priority, time_t run_time, int recurring, unsigned long event_interval, void *timing_func, int compensate_for_time_change, void *event_data, void *event_args, int event_options) {

  return (int) mock();
}

int neb_set_module_info(void *handle, int type, char *data){
  return (int) mock();
}

int neb_deregister_callback(int callback_type, int (*callback_func)(int,void *)){
  return (int) mock();
}

int write_to_all_logs(char *string, unsigned long type) {
  return (int) mock();
}

host * find_host(char *name) {
  return (host *) mock();
}

service * find_service(char *host_name, char *svc_desc) {
  return (service *) mock();
}

void test_SERVICE_CHECK_NULL_HOST(void **state) {
  
  /*declaring variables*/
  struct host_struct hst;
  hst.scheduled_downtime_depth = 0;
  hst.name = NULL;
  will_return(write_to_all_logs, 0);
  will_return(find_host, &hst); 

  int msqid;
  msqid = msgget(123456, IPC_CREAT | 0600);

  struct my_msgbuf {
    long mtype;
    char mtext[512];
  } buf;

  struct service_struct svc;

  int event_type = NEBCALLBACK_SERVICE_CHECK_DATA;

  nebstruct_service_check_data scdata;
  scdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
  scdata.host_name = "localhost";
  scdata.command_name = "string ae";
  scdata.output = "Mensagem enviada para a fila do IPC";
  scdata.state = 1;
  neb2ipc_handle_data(event_type, &scdata);
  assert_int_equal(msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT), -1);

}

void test_HOST_CHECK_NULL_HOST(void **state) {
  
  /*declaring variables*/
  struct host_struct hst;
  hst.scheduled_downtime_depth = 0;
  hst.name = NULL;
  will_return(write_to_all_logs, 0);
  will_return(find_host, &hst); 

  int msqid;
  msqid = msgget(123456, IPC_CREAT | 0600);

  struct my_msgbuf {
    long mtype;
    char mtext[512];
  } buf;

  int event_type = NEBCALLBACK_HOST_CHECK_DATA;

  nebstruct_host_check_data hcdata;
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
  hcdata.host_name = "localhost";
  hcdata.output = "Mensagem enviada para a fila do IPC";
  
  neb2ipc_handle_data(event_type, &hcdata, msqid);
  msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT);
  assert_int_equal(msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT), - 1);

}

int main(int argc, char *argv[]) {
  const UnitTest tests[] = {
                            unit_test(test_SERVICE_CHECK_NULL_HOST),
                            unit_test(test_HOST_CHECK_NULL_HOST),
                           };
return run_tests(tests);
}
