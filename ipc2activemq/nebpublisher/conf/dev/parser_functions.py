import copy

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
