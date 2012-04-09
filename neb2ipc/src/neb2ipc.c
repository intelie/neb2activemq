/*****************************************************************************
 *
 * neb2ipc.C - NEB Module to export data to a message queue
 *
 * Copyright (c) 2009 Intelie
 *
 *
 *****************************************************************************/

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

#include <string.h>

#include "./include/testing.h"

/* specify event broker API version (required) */
NEB_API_VERSION( CURRENT_NEB_API_VERSION);

int statusOfCurrentMessage;

/* variables for ipc */
#define KEY 123456
int msqid;
struct my_msgbuf {
	long mtype;
	char mtext[512];
} buf; 

/* used for logging*/
char temp_buffer[1024];

/* user for comand_name copy */
char command_name[1024];

void *neb2ipc_module_handle = NULL;

void neb2ipc_reminder_message(char *);
int neb2ipc_handle_data(int, void *);

/* this function gets called when the module is loaded by the event broker */
int nebmodule_init(int flags, char *args, nebmodule *handle) {
	char temp_buffer[1024];
	time_t current_time;
	unsigned long interval;

	/* save our handle */
	neb2ipc_module_handle = handle;

	/* set some info - this is completely optional, as Nagios doesn't do anything with this data */
	neb_set_module_info(neb2ipc_module_handle, NEBMODULE_MODINFO_TITLE,
			"neb2ipc");
	neb_set_module_info(neb2ipc_module_handle, NEBMODULE_MODINFO_AUTHOR,
			"Intelie");
	neb_set_module_info(neb2ipc_module_handle, NEBMODULE_MODINFO_TITLE,
			"neb2ipc");
	neb_set_module_info(neb2ipc_module_handle, NEBMODULE_MODINFO_VERSION,
			"noversion");
	neb_set_module_info(neb2ipc_module_handle, NEBMODULE_MODINFO_LICENSE,
			"GPL v3");
	neb_set_module_info(neb2ipc_module_handle, NEBMODULE_MODINFO_DESC,
			"A Nagios Event Broker (NEB) module to integrate with activemq.");

	/* log module info to the Nagios log file */
	write_to_all_logs("neb2ipc: Copyright (c) 2009 Intelie", NSLOG_INFO_MESSAGE);

	/* Example: log a message to the Nagios log file
	temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
	write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
	*/

	/* log a reminder message every 1 hour */
	time(&current_time);
	interval = 3600;
	schedule_new_event(EVENT_USER_FUNCTION, TRUE, current_time + interval,
			TRUE, interval, NULL, TRUE, (void *) neb2ipc_reminder_message,
			"Processing events to activemq", 0);

	/* register to be notified of check events */
	neb_register_callback(NEBCALLBACK_HOST_CHECK_DATA, neb2ipc_module_handle,
			0, neb2ipc_handle_data);
	neb_register_callback(NEBCALLBACK_SERVICE_CHECK_DATA,
			neb2ipc_module_handle, 0, neb2ipc_handle_data);

	/* create a message queue */
	/* the path and id are used just to create a unique key */
	/*    if ((key = ftok("/usr/local/nagios/var", 1)) == -1){
	 snprintf(temp_buffer,sizeof(temp_buffer)-1,"neb2ipc: System was unable to generate key for message queue.");
	 temp_buffer[sizeof(temp_buffer)-1]='\x0';
	 write_to_all_logs(temp_buffer, NSLOG_RUNTIME_ERROR);
	 return 1;
	 }*/

	if ((msqid = msgget(KEY, IPC_CREAT | 0600)) == -1) {
		snprintf(temp_buffer, sizeof(temp_buffer) - 1,
				"neb2ipc: System was unable to create message queue.");
		temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
		write_to_all_logs(temp_buffer, NSLOG_RUNTIME_ERROR);
		return 1;
	}

	snprintf(temp_buffer, sizeof(temp_buffer) - 1,
			"neb2ipc: Created message queue %i.", msqid);
	temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
	write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);

	return 0;
}

/* this function gets called when the module is unloaded by the event broker */
int nebmodule_deinit(int flags, int reason) {

	/* deregister for all events we previously registered for... */
	neb_deregister_callback(NEBCALLBACK_HOST_CHECK_DATA, neb2ipc_handle_data);
	neb_deregister_callback(NEBCALLBACK_SERVICE_CHECK_DATA, neb2ipc_handle_data);

	/* log a message to the Nagios log file */
	snprintf(temp_buffer, sizeof(temp_buffer) - 1, "neb2ipc: Goodbye!\n");
	temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
	write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);

	//	if (msgctl(msqid, IPC_RMID, NULL) == -1) {
	//		/* log a message to the Nagios log file */
	//			snprintf(temp_buffer,sizeof(temp_buffer)-1,"Could remove message queue id %i: %s",msqid, strerror(errno));
	//			temp_buffer[sizeof(temp_buffer)-1]='\x0';
	//			write_to_all_logs(temp_buffer,NSLOG_RUNTIME_ERROR);
	//	}

	return 0;
}

/* gets called every X minutes by an event in the scheduling queue */
void neb2ipc_reminder_message(char *message) {

	/* log a message to the Nagios log file */
	snprintf(temp_buffer, sizeof(temp_buffer) - 1,
			"neb2ipc: I'm still here! %s", message);
	temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
	write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);

	return;
}

/* handle data from Nagios daemon */
int neb2ipc_handle_data(int event_type, void *data) {

/*external variable for testing, declared in testing.h */
  statusOfCurrentMessage = INITIAL_VALUE;

	char CHECK_NRPE[] = "check_nrpe!";
	int INDEX_AFTER_CHECK_NRPE = strlen(CHECK_NRPE);

	nebstruct_host_check_data *hcdata = NULL;
	nebstruct_service_check_data *scdata = NULL;
  
	buf.mtype = event_type;
  
	/* what type of event/data do we have? */
	switch (event_type) {

	case NEBCALLBACK_HOST_CHECK_DATA:

		if ((hcdata = (nebstruct_host_check_data *) data)) {
			if (hcdata->type != NEBTYPE_HOSTCHECK_PROCESSED) {
				// Check not processed yet
        statusOfCurrentMessage = ERROR_CHECK_NOT_PROCESSED;

				return 0;
			}

 if (hcdata->output == NULL || strlen(hcdata->output) == 0) {
        snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Host check error: Missing output parameter");
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
        statusOfCurrentMessage = ERROR_MISSING_PARAMETER;

				return 0;
      }

      if (hcdata->host_name == NULL || strlen(hcdata->host_name) == 0) {
        snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Host check error: Missing host_name parameter");
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
        statusOfCurrentMessage = ERROR_MISSING_PARAMETER;
				return 0;
      }
      
			host *hst;
			hst = find_host(hcdata->host_name);
			if (hst == NULL) {
       	snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%i^%i^%s\0",
		  	hcdata->host_name, hcdata->state, ERROR_FIND_HOST,hcdata->output);

        if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT) == -1) {
				  snprintf(temp_buffer, sizeof(temp_buffer) - 1,
					  	"Error to send message to queue id %i: %s", msqid,
						  strerror(errno));
				  temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				  write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
          statusOfCurrentMessage = ERROR_MESSAGE_NOT_SENT_AND_FIND_HOST_NULL;

          return 0;
			  }

        snprintf(temp_buffer, sizeof(temp_buffer) - 1, "find_host() returned null, sent anyway");
     	  write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);

        statusOfCurrentMessage = ERROR_FIND_HOST_NULL;
        return 0;
      }

			#ifdef DEBUG
			if (hst->scheduled_downtime_depth == HOST_DOWN) {
		  	  snprintf(temp_buffer, sizeof(temp_buffer) - 1, "Host '%s' is currently in scheduled downtime\0" ,hst->name);
		          temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
        		  write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
       			}
			#endif
      
			/* send message to message queue */
			snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%i^%i^%s\0",
			hcdata->host_name, hcdata->state, hst->scheduled_downtime_depth, hcdata->output);

			if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT)
					== -1) {
				snprintf(temp_buffer, sizeof(temp_buffer) - 1,
						"Error to send message to queue id %i: %s", msqid,
						strerror(errno));
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
        statusOfCurrentMessage = ERROR_MESSAGE_NOT_SENT;
			}
		}
		break;

	case NEBCALLBACK_SERVICE_CHECK_DATA:

		if ((scdata = (nebstruct_service_check_data *) data)) {
			if (scdata->type != NEBTYPE_SERVICECHECK_PROCESSED) {
				// Check not processed yet
				/* log debug */
				#ifdef DEBUG
				snprintf(temp_buffer,sizeof(temp_buffer) - 1," Check not processed yet");
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
				#endif
        statusOfCurrentMessage = ERROR_CHECK_NOT_PROCESSED;

				return 0;
			}
			
			// If command_name comes null, search on service struct
			if (scdata->command_name != NULL && strlen(scdata->command_name)
					> 0) {
				strcpy(command_name,scdata->command_name);
			} else {
				service *svc;
				if ((svc = find_service(scdata->host_name,
						scdata->service_description)) == NULL) {
					snprintf(temp_buffer, sizeof(temp_buffer) - 1,
							"Could not find service %s for host %s",
							scdata->service_description, scdata->host_name);
					temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
					write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
          statusOfCurrentMessage = ERROR_NO_SVC_IN_HOST;

					return 0;
				}
			
				if (svc->service_check_command != NULL) {
					/* Checks if received by NRPE and remove "check_nrpe!" at the beggining */
					if (strstr(svc->service_check_command, CHECK_NRPE) > 0) {
						int i = 0;
						while (svc->service_check_command[i + INDEX_AFTER_CHECK_NRPE] != '\0') {
							if (svc->service_check_command[INDEX_AFTER_CHECK_NRPE] == '!') {
								break;
							}
							command_name[i] = svc->service_check_command[i + INDEX_AFTER_CHECK_NRPE];
							i++;
						}
						command_name[i] = '\0';
					}
					else {
						int cmd_len = strcspn(svc->service_check_command, "!");
						strncpy(command_name, svc->service_check_command, cmd_len);
						command_name[cmd_len] = '\x0';
					}

					/* log debug */
					#ifdef DEBUG
					snprintf(temp_buffer,sizeof(temp_buffer) - 1," Command name is %s", command_name );
					temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
					write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
					#endif
				}
				
				#ifdef DEBUG
				sprintf(temp_buffer, "recebido: %s -- hostname: %s -- output: %s -- downtime_depth: %i", svc->service_check_command, scdata->host_name, scdata->output, svc->scheduled_downtime_depth);
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
				#endif
			}

      if (scdata->host_name == NULL || strlen(scdata->host_name) == 0) {
        snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Service check error: Missing host_name parameter");
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
        statusOfCurrentMessage = ERROR_MISSING_PARAMETER;

				return 0;
			}

      if (command_name == NULL || strlen(command_name) == 0) {
        snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Service check error: Missing command_name parameter");
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
        statusOfCurrentMessage = ERROR_MISSING_PARAMETER;

				return 0;
			}

      if (scdata->output == NULL || strlen(scdata->output) == 0) {
         snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Service check error: Missing output parameter");
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
        statusOfCurrentMessage = ERROR_MISSING_PARAMETER;

				return 0;
			}

			host *hst;
			hst = find_host(scdata->host_name);
			if (hst == NULL) {
        snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%s^%i^%i^%s\0",
				scdata->host_name, command_name, scdata->state,ERROR_FIND_HOST, scdata->output);
        if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT) == -1) {
				  snprintf(temp_buffer, sizeof(temp_buffer) - 1,
						      "Error to send message to queue id %i: %s", msqid,
						      strerror(errno));
				  temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				  write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
          statusOfCurrentMessage = ERROR_MESSAGE_NOT_SENT_AND_FIND_HOST_NULL;

          return 0;
			  }

        snprintf(temp_buffer, sizeof(temp_buffer) - 1, "find_host() returned null, sent anyway");
     	  write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);

        statusOfCurrentMessage = ERROR_FIND_HOST_NULL;
        return 0;

			}
			#ifdef DEBUG
			if (hst->scheduled_downtime_depth == HOST_DOWN) {
			  snprintf(temp_buffer, sizeof(temp_buffer) - 1, "Host '%s' is currently in scheduled downtime\0" ,scdata->host_name);
			  temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
			  write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
			}
			#endif
			snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%s^%i^%i^%s\0",
					scdata->host_name, command_name, scdata->state, hst->scheduled_downtime_depth, scdata->output);

			/* debug log*/
			#ifdef DEBUG
			snprintf(temp_buffer, sizeof(temp_buffer) - 1,
					"service name> %s description> %s for> host %s",
					command_name, scdata->service_description,
					scdata->host_name);
			temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
			write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
			#endif

			if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT)
					== -1) {
				snprintf(temp_buffer, sizeof(temp_buffer) - 1,
						" Error to send message to queue id %i: %s", msqid,
						strerror(errno));
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
        statusOfCurrentMessage = ERROR_MESSAGE_NOT_SENT;
			}

		}

		break;

	default:
    statusOfCurrentMessage = ERROR_EVENT_TYPE_UNKNOWN;
		break;
	}

	return 0;
}

