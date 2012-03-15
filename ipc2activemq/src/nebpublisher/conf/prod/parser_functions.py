import copy
import re

class ParserFunctions:
    @staticmethod
    def parse_cameras (host, message, eventtype, labelFilter):
        cameras_not_formatted = message.split()[1:]
        cameras = []
        for camera in cameras_not_formatted:
            cameras_splitted = camera.split(':')
            cameras.append({'eventtype': eventtype, 
                            'label': cameras_splitted[0], 
                            'value': cameras_splitted[1]})
        return cameras


    @staticmethod
    def parse_unix_df(host, message, eventtype, labelFilter):
        partitions = message.split('[')
        split_by_space = message.split()

        basic_event = {'eventtype': eventtype, 'state': split_by_space[1],
                   'host': host}

        if len(partitions) <= 1:
            if 'DISK %s' % basic_event['state'] == message:
                return [basic_event]
            else:
                partitions = message.split(':')
                events = []
                for partition_info in partitions[1:]:
                    if not partition_info:
                        continue
                    #/ 7156 MB (77% inode=97%)
                    new_event = copy.copy(basic_event)
                    event_split = partition_info[1:].split('(')
                    new_event['free_percent'] = float(event_split[1].split('%')[0])
                    new_event['partition'] = ' '.join(event_split[0].split()[:-2])
                    events.append(new_event)
                return events
        
        events = []
        for partition_info in partitions[1:]:
            #1463088 kB (74%) free on /]
            partition_splitted = partition_info.split('%) free on ')
            if len(partition_splitted) < 2:
                if 'used on' in partition_info:
                    partition_splitted = partition_info.split('%) used on ')
                    new_event = copy.copy(basic_event)
                    new_event['partition'] = partition_splitted[1].split(']')[0]
                    new_event['free_percent'] = 100 - float(partition_splitted[0].split('(')[1])
                    events.append(new_event)
                continue
            percent = float(partition_splitted[0].split('(')[1])
            partition = partition_splitted[1].split(']')[0]
            new_event = copy.copy(basic_event)
            new_event['partition'] = partition
            new_event['free_percent'] = percent
            events.append(new_event)
        return events


re_partition = re.compile('(.+): ([0-9\.]+)% used \(([0-9\.]+)/([0-9\.]+)')
def check_disk_snmp(host, message, eventtype, label_filter):
    state = message.split(':')[0]
    basic_event = {'eventtype': eventtype, 'host': host, 'state': state}
    events = []
    for partition_data in message[len(state) + 2:].split('MB) ')[:-1]:
        results = re_partition.findall(partition_data)
        if len(results) != 1:
            continue
        if len(results[0]) != 4:
            continue

        event = copy.copy(basic_event)
        event['partition'] = results[0][0]
        event['percent_used'] = results[0][1]
        event['total_used_megabytes'] = results[0][2]
        event['total_megabytes'] = results[0][3]
        events.append(event)
    return events

  
commands = {
    'check_passive':[{
        'labelFilter': 'cameras',
        'eventtype': 'FMS',
        'function': ParserFunctions.parse_cameras
    }],

    'check_unix_df': [
        {'labelFilter': 'DISK',
         'eventtype': 'Disk',
         'function': ParserFunctions.parse_unix_df
        },
    ],
    'check_snmp_disk': [
        {'labelFilter': 'OK',
         'function': check_disk_snmp,
         'eventtype': 'DiskSNMP'
        },
        {'labelFilter': 'WARNING',
         'function': check_disk_snmp,
         'eventtype': 'DiskSNMP'
        },
        {'labelFilter': 'CRITICAL',
         'function': check_disk_snmp,
         'eventtype': 'DiskSNMP'
        },
    ],
}

commands['check_disk2'] = commands['check_unix_df']
commands['check_disk3'] = commands['check_unix_df']
commands['check_disk4'] = commands['check_unix_df']
commands['check_disk5'] = commands['check_unix_df']
commands['check_disk6'] = commands['check_unix_df']
commands['check_disk7'] = commands['check_unix_df']
commands['check_disk_stg1'] = commands['check_unix_df']
commands['check_disk_stg2'] = commands['check_unix_df']
commands['check_disk_stg3'] = commands['check_unix_df']
commands['check_disk_stg4'] = commands['check_unix_df']
commands['check_disk_stg5'] = commands['check_unix_df']
commands['check_disk_stg6'] = commands['check_unix_df']
commands['check_disk_stg7'] = commands['check_unix_df']
commands['check_disk_stg8'] = commands['check_unix_df']
