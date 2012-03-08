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
#include "./include/neb2ipc.h"

#define NAGIOS_CHECK_OUTPUT "HTTP OK: HTTP/1.1 200 OK - 454 bytes in 0.001 second response time |time=0.000758s;;;0.000000 size=454B;;;0"
#define NAGIOS_CHECK_HOST_NAME "localhost"

#define QUEUE_OK        0
#define QUEUE_NOT_EMPTY 1
#define MORE_THAN_ONE_MESSAGE_WAS_SENT 2

int neb_register_callback(int callback_type, void *mod_handle, int priority, int (*callback_func)(int,void *)) {
  return *(int *) mock();
}

int schedule_new_event(int event_type, int high_priority, time_t run_time, int recurring, unsigned long event_interval, void *timing_func, int compensate_for_time_change, void *event_data, void *event_args, int event_options) {

  return *(int *) mock();
}

int neb_set_module_info(void *handle, int type, char *data){
  return *(int *) mock();
}

int neb_deregister_callback(int callback_type, int (*callback_func)(int,void *)){
  return *(int *) mock();
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

int msqid;

struct my_msgbuf {
    long mtype;
    char mtext[512];
} buf;

struct host_struct hst;
struct service_struct svc;
int event_type;
char ExpectedMessage[500];

nebstruct_service_check_data scdata;
nebstruct_host_check_data hcdata;
int statusOfCurrentMessage;

struct eventType {
  int type;
  void *event;
};

struct eventType eventTypes[2];

void createNebEvent(int check, char *host_name, char *output) {

    msqid = msgget(123456, IPC_CREAT | 0600);
    event_type = check;

    scdata.type = NEBTYPE_SERVICECHECK_PROCESSED;
    scdata.command_name = "check_http";
    scdata.host_name = host_name;
    scdata.output = output;

    hcdata.type = NEBTYPE_HOSTCHECK_PROCESSED;
    hcdata.host_name = host_name;
    hcdata.output = output;
    
    hst.name = NAGIOS_CHECK_HOST_NAME;
    hst.scheduled_downtime_depth = 1;

    if (check == NEBCALLBACK_SERVICE_CHECK_DATA)
      sprintf(ExpectedMessage, "%s^%s^%i^%i^%s\0", scdata.host_name, scdata.command_name, scdata.state, ERROR_FIND_HOST,scdata.output);
    if (check == NEBCALLBACK_HOST_CHECK_DATA)
      sprintf(ExpectedMessage, "%s^%i^%i^%s\0", hcdata.host_name, hcdata.state, ERROR_FIND_HOST,hcdata.output);

  }

int receiveOnlyOneIPCMessage() {
  msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT);
  if (msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT) != -1)
    return MORE_THAN_ONE_MESSAGE_WAS_SENT;
  else
    return QUEUE_OK;
}

int checkIfQueueIsEmpty (int msqid) {
  if (msgrcv(msqid, &buf, sizeof buf, event_type, IPC_NOWAIT) == -1)
    return QUEUE_OK;
  else
    return QUEUE_NOT_EMPTY;
}

void eventTypeFill(void) {

    eventTypes[0].type = NEBCALLBACK_HOST_CHECK_DATA;
    eventTypes[0].event = (nebstruct_host_check_data *) &hcdata;
    eventTypes[1].type = NEBCALLBACK_SERVICE_CHECK_DATA;
    eventTypes[1].event = (nebstruct_service_check_data *) &scdata;
}

void unprocessCheck() {

    hcdata.type = 1; //random number other than 801, NEBTYPE_HOSTCHECK_PROCESSED
    scdata.type = 1; //random number other than 701, NEBTYPE_SERVICECHECK_PROCESSED
}

void setExpectedMessage(int type) {
  
  if (type == NEBCALLBACK_HOST_CHECK_DATA)
      snprintf(ExpectedMessage, sizeof (ExpectedMessage) - 1, "%s^%i^%i^%s\0",
          hcdata.host_name, hcdata.state, hst.scheduled_downtime_depth, hcdata.output);
  if (type == NEBCALLBACK_SERVICE_CHECK_DATA)
     snprintf(ExpectedMessage, sizeof (ExpectedMessage) - 1, "%s^%s^%i^%i^%s\0",
          scdata.host_name, scdata.command_name, scdata.state, hst.scheduled_downtime_depth, scdata.output);
}

void FillMessageQueue(void) {

  do
    msgsnd(msqid, ExpectedMessage, sizeof ExpectedMessage, IPC_NOWAIT);
  while
    (msgsnd(msqid, ExpectedMessage, sizeof ExpectedMessage, IPC_NOWAIT) != -1);

}

void verifyIfACorrectMessageWillBeSentEvenIfFindHostReturnsNULL (void **state) {
  
  eventTypeFill();
  for (int i = 0; i < 2; i++) {
    will_return(find_host, NULL);
    createNebEvent(eventTypes[i].type, NAGIOS_CHECK_HOST_NAME, NAGIOS_CHECK_OUTPUT);
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, ERROR_FIND_HOST_NULL);
    assert_int_equal(receiveOnlyOneIPCMessage(msqid), QUEUE_OK); 
    assert_string_equal(buf.mtext, ExpectedMessage);
  }
}

void verifyThatNoMessageWasSentWhenEventTypeNotServiceNorHostCHeck (void **state) {
  
  int event_type = 222; /*random number other than 13 and 14, which are , respectively,
                         NEBCALLBACK_SERVICE_CHECK_DATA and NEBCALLBACK_HOST_CHECK_DATA */
  neb2ipc_handle_data(event_type, &hcdata);
  assert_int_equal(statusOfCurrentMessage, ERROR_EVENT_TYPE_UNKNOWN);
  assert_int_equal(checkIfQueueIsEmpty(msqid), QUEUE_OK);
}

void verifyThatNoMessageWasSentIfCheckNotProcessed (void **state) {
  
  eventTypeFill();
  for (int i = 0; i < 2; i++) {
    createNebEvent(eventTypes[i].type, NAGIOS_CHECK_HOST_NAME, NAGIOS_CHECK_OUTPUT);
    unprocessCheck();
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, ERROR_CHECK_NOT_PROCESSED);
    assert_int_equal(checkIfQueueIsEmpty(msqid), QUEUE_OK);
  }
}

void verifyThatNoMessageWasSentWhenHostNameNULL (void **state) {

  for (int i = 0; i < 2; i++) {
    createNebEvent(eventTypes[i].type, NULL, NAGIOS_CHECK_OUTPUT);
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, ERROR_MISSING_PARAMETER);
    assert_int_equal(checkIfQueueIsEmpty(msqid), QUEUE_OK);
  }
}

void verifyThatNoMessageWasSentWhenHostNameEmpty (void **state) {

  for (int i = 0; i < 2; i++) {
    createNebEvent(eventTypes[i].type, "", NAGIOS_CHECK_OUTPUT);
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, ERROR_MISSING_PARAMETER);
    assert_int_equal(checkIfQueueIsEmpty(msqid), QUEUE_OK);
  }
}

void verifyThatIfMessageIsNULLThenItWasNotSent (void **state) {

  for (int i = 0; i < 2; i++) {
    createNebEvent(eventTypes[i].type, NAGIOS_CHECK_HOST_NAME, NULL);
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, ERROR_MISSING_PARAMETER);
    assert_int_equal(checkIfQueueIsEmpty(msqid), QUEUE_OK);
  }
}

void verifyThatIfMessageIsEmptyThenItWasNotSent (void **state) {

  for (int i = 0; i < 2; i++) {
    createNebEvent(eventTypes[i].type, NAGIOS_CHECK_HOST_NAME, "");
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, ERROR_MISSING_PARAMETER);
    assert_int_equal(checkIfQueueIsEmpty(msqid), QUEUE_OK);
  }
}

void TestIfWorkingWithCorrectParameters (void **state) {
  
  for (int i = 0; i < 2; i++) {
    createNebEvent(eventTypes[i].type, NAGIOS_CHECK_HOST_NAME, NAGIOS_CHECK_OUTPUT);
    setExpectedMessage(eventTypes[i].type);
    will_return(find_host, &hst);
    neb2ipc_handle_data(eventTypes[i].type, eventTypes[i].event);
    assert_int_equal(statusOfCurrentMessage, INITIAL_VALUE);
    assert_int_equal(receiveOnlyOneIPCMessage(msqid), QUEUE_OK);
    assert_string_equal(buf.mtext, ExpectedMessage);
  }
}

int main(int argc, char *argv[]) {
  const UnitTest tests[] = {
                            unit_test(verifyIfACorrectMessageWillBeSentEvenIfFindHostReturnsNULL),
                            unit_test(verifyThatNoMessageWasSentWhenEventTypeNotServiceNorHostCHeck),
                            unit_test(verifyThatNoMessageWasSentIfCheckNotProcessed),
                            unit_test(verifyThatNoMessageWasSentWhenHostNameNULL),
                            unit_test(verifyThatNoMessageWasSentWhenHostNameEmpty),
                            unit_test(verifyThatIfMessageIsNULLThenItWasNotSent), 
                            unit_test(verifyThatIfMessageIsEmptyThenItWasNotSent),
                            unit_test(TestIfWorkingWithCorrectParameters),
                           };
return run_tests(tests);
}
