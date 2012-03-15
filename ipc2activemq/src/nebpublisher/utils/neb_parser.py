import time, logging
import re
import sys


NOT_IMPLEMENTED = 1
BAD_FORMAT = 2
SERVICE_CHECK_MAP = {0 : 'OK', 1 : 'WARNING', 2 : 'CRITICAL', 3 : 'UNKNOWN'}
HOST_CHECK_MAP = {0 : 'OK', 1 : 'CRITICAL', 2 : 'UNKNOWN'}

logger = logging.getLogger("nebpublisher.parser")

def count_not_none(groups) :
    i = 0
    for element in groups:
        if element != None:
            i = i + 1
    return i


class Parser():
    def __init__ (self, topics, parser_functions):
        self.load_types()
        self.topics = topics
        self.parser_functions = parser_functions
        # this code was made to compile the regexps only once

        # iterate over command names
        for key in self.topics.expressions:
            topic = self.topics.expressions[key]
            #iterate over items in command (labelFilter, eventtype level)
            for item in topic:
                # Append error regexps to each regexps array to catch known errors
                for errorRegexp in topics.errorRegexps:
                    item['regexps'].append(errorRegexp)
                    #iterate over subitems (properties and regexps)
                for subitem in item['regexps']:
                    #substitute text with compiled regexp
                    subitem['regexp'] = re.compile(subitem['regexp'])
            topics.expressions[key] = topic
        logger.debug("Compiled regexps structure: %s " % \
                     str(topics.expressions))

    def load_types(self):
        """This function loads the types and the functions responsible for
           parsing each message event
        """
        self.switch = {13: self.parse_service_check,
                       14: self.parse_host_check}

    def parse(self, type, message):
        try:
            return self.switch[type](message)
        except KeyError, e:
            self.not_implemented_type(type)
            return NOT_IMPLEMENTED
        except Exception, e:
            info = sys.exc_info()
            import traceback
            traceback.print_tb(info[2])
            logger.warn('Unknown exception %s' % str(info))
            exit(1) #Houston!

    def not_implemented_type(self, type):
        logger.warn("Type %i has no parser." % type)
        return

    def not_implemented_service(self, service):
        logger.warn("Service %s has no parser." % service)
        return

    def parse_service_check(self, message):
        logger.debug("Message %s - service check" % message)
        if message is None:
            return BAD_FORMAT
        data = []
        data = message.split('^')

        if len(data) < 5:
            return BAD_FORMAT
	
	if not data[0] or not data[1] or not data[2] or not data[3] or not data[4]:
            return BAD_FORMAT	
	
        host = data[0]
        command_name = data[1]
        state = data[2]
        downtime = data[3]
        message = data[4]

        logger.debug("Host %s - command_name %s - state %s - downtime %s - output %s" % \
                     (host, command_name, state, downtime, message))

        if command_name in self.topics.expressions:
            topic = self.topics.expressions[command_name]
            result = self.create_event_from_regexp(host, downtime,  message, topic)
            if result != BAD_FORMAT and result != NOT_IMPLEMENTED:
                result['state'] = SERVICE_CHECK_MAP[int(state)]
                return [result]
            return result
        elif command_name in self.parser_functions.commands:
            command_parser_functions = self.parser_functions.commands[command_name]
            events = self.create_events_from_parser_functions(host, message, command_parser_functions)
            for event in events:
                event['state'] = SERVICE_CHECK_MAP[int(state)]
            return events

        logger.warn("Event type %s not registered as a topic" % command_name)
        return BAD_FORMAT


    def parse_host_check(self, message):
        
	if not message:
        	return BAD_FORMAT

        logger.debug("Message %s - host check" % message)
        data = []
        data = message.split('^')
        if len(data) < 4:
            return BAD_FORMAT
        if not data[0] or not data[1] or not data[2] or not data[3]:
            return BAD_FORMAT
        host = data[0]
        state = data[1]
        downtime = data[2]
        output = data[3]
        #logger.debug("Host %s - state %s - downtime %i output %s" % (host, state, downtime, output) )
        topic = self.topics.expressions['host']
        event = self.create_event_from_regexp(host, downtime, output, topic)

        if event != BAD_FORMAT and event != NOT_IMPLEMENTED:
            event['state'] = HOST_CHECK_MAP[int(state)]
            return [event]
        return event


    def create_event_from_regexp(self, host, downtime, message, topic):
        event = {'host' : host}
        event['downtime'] = downtime
        event['description'] = message
        logger.debug('Message to be matched: %s \n Topic: %s' % (message, str(topic)))
        match = False
        #iterate over items in command (labelFilter, eventtype level)
        for item in topic:
            if match:
                break
            if item['labelFilter'] != None and \
               not message.startswith(item['labelFilter']):
                logger.debug("Does not match with label")
            else: 
                #iterate over subitems (properties and regexps)
                for subitem in item['regexps']:
                    r = subitem['regexp']
                    m = r.match(message)
                    if m != None: 
                        if count_not_none(m.groups()) != len(subitem['properties']):
                            logger.warn("Regexp has a different number of properties from expected")
                        else:
                            # if groups in regexp and the number of properties match consider it a match
                            match = True
                            event['eventtype'] = item['eventtype']

                            # if the regex contains an specific event type, override it
                            if 'eventtype' in subitem and subitem['eventtype'] != None:
                                event['eventtype'] = subitem['eventtype']

                            i = 1 # first match is the whole expression
                            for property in subitem['properties']:
                                if m.group(i) != None:
                                    event[property] = m.group(i)
                                    i = i + 1
                            
                            # stop iterating over subitem
                            break

        logger.debug('event: %s' % str(event))
        if match:
            return event
        else:
            logger.warn('No expression for: %s' %(message))
            return BAD_FORMAT


    def create_events_from_parser_functions(self, host, message,
                                            command_parser_functions):
        for parser_function_struct in command_parser_functions:
            #if not message.startswith(parser_function_struct['labelFilter'] or ''):
            if parser_function_struct['labelFilter'] == None or \
               not message.startswith(parser_function_struct['labelFilter']):
                logger.debug("Does not match with label")
                return []
            else:
                get_events = parser_function_struct['function']
                event_type = parser_function_struct['eventtype']
                label_filter = parser_function_struct['labelFilter']
                return get_events(host, message, event_type, label_filter)
