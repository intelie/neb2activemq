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
#include "./include/testing.h"

int statusOfCurrentMessage;

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
  return 0;
}

host * find_host(char *name) {
  return (host *) mock();
}

service * find_service(char *host_name, char *svc_desc) {
  return (service *) mock();
}

void test_service_check_null_host(void **state) {
  
  /*declaring variables*/
  struct host_struct hst;
  hst.scheduled_downtime_depth = 3;
  hst.name = NULL;
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
  scdata.command_name = "random string";
  scdata.output = "Message sent to IPC queue";
  scdata.state = 1;
  neb2ipc_handle_data(event_type, &scdata);
  char msg[100];
  sprintf(msg, "%s^%s^%i^%i^%s\0", scdata.host_name, scdata.command_name, scdata.state, hst.scheduled_downtime_depth, scdata.output);
  msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT);
  assert_string_equal(buf.mtext, msg);

}

void test_host_check_null_host (void **state) {
  
  /*declaring variables*/
  struct host_struct hst;
  hst.scheduled_downtime_depth = 3;
  hst.name = NULL;
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
  hcdata.output = "Message sent to IPC queue";
  
  neb2ipc_handle_data(event_type, &hcdata);
  msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT);
  char msg[100];
  sprintf(msg, "%s^%i^%i^%s\0", hcdata.host_name, hcdata.state, hst.scheduled_downtime_depth, hcdata.output);
  assert_string_equal(buf.mtext, msg); 

}

void test_event_type(void **state) {
  nebstruct_host_check_data hst;
  
  int event_type = 222; /*random number other than 13 and 14, which are , respectively,
                         NEBCALLBACK_SERVICE_CHECK_DATA and NEBCALLBACK_HOST_CHECK_DATA */
  neb2ipc_handle_data(event_type, &hst);
  assert_int_equal(statusOfCurrentMessage, EVENT_TYPE_UNKNOWN);
}


void test_host_check_processed (void **state) {
  
  nebstruct_host_check_data hst;
  hst.type = 1; //random number other than 801, NEBTYPE_HOSTCHECK_PROCESSED
  int event_type = NEBCALLBACK_HOST_CHECK_DATA;

  neb2ipc_handle_data(event_type, &hst);
  assert_int_equal(statusOfCurrentMessage, HOST_CHECK_N_PROCESSED);
}

void test_service_check_processed (void **state) {
  
  nebstruct_service_check_data svc;
  svc.type = 1; //random number other than 701, NEBTYPE_SERVICECHECK_PROCESSED
  int event_type = NEBCALLBACK_SERVICE_CHECK_DATA;

  neb2ipc_handle_data(event_type, &svc);
  assert_int_equal(statusOfCurrentMessage, SVC_CHECK_N_PROCESSED);
  
}

void test_host_name_NULL (void **state) {

  //host check
  int event_type = NEBCALLBACK_HOST_CHECK_DATA;

  nebstruct_host_check_data hcdata;
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
  
  //NEB2IPC checks output first, so we assign  anything to it
  hcdata.output = "any message just for testing";
  //test host_name for NULL
  neb2ipc_handle_data(event_type, &hcdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);
 
  //service check
  event_type = NEBCALLBACK_SERVICE_CHECK_DATA;
  nebstruct_service_check_data scdata;
  scdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
  
  scdata.command_name = "any command";
  //test host_name for NULL
  neb2ipc_handle_data(event_type, &scdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);

}

void test_host_name_empty (void **state) {
  //host check
  int event_type = NEBCALLBACK_HOST_CHECK_DATA;

  nebstruct_host_check_data hcdata;
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
  
  //NEB2IPC checks output first, so we assign  anything to it
  hcdata.output = "any message just for testing";

  //test host name for emptyness
  hcdata.host_name = "";
  neb2ipc_handle_data(event_type, &hcdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);
  
  //service check
  event_type = NEBCALLBACK_SERVICE_CHECK_DATA;

  nebstruct_service_check_data scdata;
  scdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
  
  scdata.command_name = "any command";
  //test host_name for emptyness
  scdata.host_name = "";
  neb2ipc_handle_data(event_type, &scdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);


}

void test_output_NULL (void **state) {

  //host check
  int event_type = NEBCALLBACK_HOST_CHECK_DATA;

  nebstruct_host_check_data hcdata;
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;

  //test output for NULL
  neb2ipc_handle_data(event_type, &hcdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);
  statusOfCurrentMessage = 0;

  //service check
  event_type = NEBCALLBACK_SERVICE_CHECK_DATA;

  nebstruct_service_check_data scdata;
  hcdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
  
  scdata.command_name = "any command";
  scdata.host_name = "any host";
  //test output for NULL
  neb2ipc_handle_data(event_type, &scdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);


}

void test_output_empty (void **state) {

  //host check
  int event_type = NEBCALLBACK_HOST_CHECK_DATA;
  
  nebstruct_host_check_data hcdata;
  hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
  
  //test for empty output
  hcdata.output = "";
  neb2ipc_handle_data(event_type, &hcdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);
  statusOfCurrentMessage = 0;

  //service check
  event_type = NEBCALLBACK_SERVICE_CHECK_DATA;
  nebstruct_service_check_data scdata;
  scdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
  
  scdata.command_name = "any command";
  scdata.host_name = "any host";
  //test output for emptyness
  scdata.output = "";
  neb2ipc_handle_data(event_type, &scdata);
  assert_int_equal(statusOfCurrentMessage, MISSING_PARAMETER);

}

int main(int argc, char *argv[]) {
  const UnitTest tests[] = {
                            unit_test(test_service_check_null_host),
                            unit_test(test_host_check_null_host),
                            unit_test(test_event_type),
                            unit_test(test_host_check_processed),
                            unit_test(test_service_check_processed),
                            unit_test(test_host_name_empty),
                            unit_test(test_host_name_NULL),
                            unit_test(test_output_empty),
                            unit_test(test_output_NULL),
                           };
return run_tests(tests);
}
