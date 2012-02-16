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


int write_to_all_logs(char *, unsigned long);

int write_to_all_logs(char *buffer, unsigned long data_type) {
  printf("%s\n", buffer);
return 0;
}

/* specify event broker API version (required) */
NEB_API_VERSION( CURRENT_NEB_API_VERSION);

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
int neb2ipc_handle_data(int, void *, int);

/* handle data from Nagios daemon */
int neb2ipc_handle_data(int event_type, void *data, int msqid) {

  
/*  if ((msqid = msgget(KEY, IPC_CREAT | 0600)) == -1) {
    snprintf(temp_buffer, sizeof(temp_buffer) - 1,
        "neb2ipc: System was unable to create message queue.");
    temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
    write_to_all_logs(temp_buffer, NSLOG_RUNTIME_ERROR);
    return 1;
  }
*/

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
				return 0;
			}

			if (hcdata->host_name == NULL || strlen(hcdata->host_name) == 0
					|| hcdata->output == NULL || strlen(hcdata->output) == 0) {

				snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Host check error: Missing one or more parameters:\n  host_name: %s\n  output: %s",
						hcdata->host_name, hcdata->output);
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);


				return 0;
			}
      
      host *hst;
      hst = find_host(hcdata->host_name);
      if (hst->name == NULL) {
        snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%i^%i^%s\0",
        hcdata->host_name, hcdata->state, ERROR_FIND_HOST, hcdata->output);
        if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT) == -1) {
          snprintf(temp_buffer, sizeof(temp_buffer) - 1,
                  "Error to send message to queue id %i: %s", msqid,
                   strerror(errno));
                   temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
                   write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
        }
      return 0;
      }

      if (hst->scheduled_downtime_depth == HOST_DOWN) {
       snprintf(temp_buffer, sizeof(temp_buffer) - 1, "Host '%s' is currently in scheduled downtime\0" ,hst->name);
       temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
       write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
      }
 

			/*send message to message queue */
			snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%i^%i^%s\0",
					hst->name, hcdata->state, hst->scheduled_downtime_depth, hcdata->output);
			if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT)
					== -1) {
				snprintf(temp_buffer, sizeof(temp_buffer) - 1,
						"Error to send message to queue id %i: %s", msqid,
						strerror(errno));
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
			}
		
		break;
    }

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
				sprintf(temp_buffer, "recebido: %s -- hostname: %s -- output: %s", svc->service_check_command, scdata->host_name, scdata->output);
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
				#endif
			}


			if (scdata->host_name == NULL || strlen(scdata->host_name) == 0
					|| command_name == NULL || strlen(command_name) == 0
					|| scdata->output == NULL || strlen(scdata->output) == 0) {

				snprintf(
						temp_buffer,
						sizeof(temp_buffer) - 1,
						"Service check error: Missing one or more parameters:\n  host_name: %s\n  command_name: %s\n  output: %s",
						scdata->host_name, command_name, scdata->output);
				temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
				write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);

				return 0;
			}
      
      host *hst;
      hst = find_host(scdata->host_name);

      if (hst->name == NULL) {
       snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%i^%i^%s\0",
                hcdata->host_name, hcdata->state, ERROR_FIND_HOST, hcdata->output);
                if (msgsnd(msqid, (struct buf *) &buf, sizeof(buf), IPC_NOWAIT) == -1) {
                           snprintf(temp_buffer, sizeof(temp_buffer) - 1,
                           "Error to send message to queue id %i: %s", msqid,
                           strerror(errno));
                  temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
                  write_to_all_logs(temp_buffer, NSLOG_RUNTIME_WARNING);
                }
      return 0;
      }

      if (hst->scheduled_downtime_depth == HOST_DOWN) {
        snprintf(temp_buffer, sizeof(temp_buffer) - 1, "Host '%s' is currently in scheduled downtime\0" ,scdata->host_name);
        temp_buffer[sizeof(temp_buffer) - 1] = '\x0';
        write_to_all_logs(temp_buffer, NSLOG_INFO_MESSAGE);
      }

			snprintf(buf.mtext, sizeof(buf.mtext) - 1, "%s^%s^%i^%i^%s\0",
					scdata->host_name, command_name, scdata->state,
					hst->scheduled_downtime_depth,scdata->output);

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
		

		break;
    }

	default:
		break;
    }
  }
	return 0;
}
