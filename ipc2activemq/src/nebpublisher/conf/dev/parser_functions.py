class ParserFunctions:
    @staticmethod
    def parse_cameras (message, eventtype, labelFilter):
        cameras_not_formatted = message.split()[1:]
        cameras = []
        for camera in cameras_not_formatted:
            cameras_splitted = camera.split(':')
            cameras.append({'eventtype': eventtype, 
                            'label': cameras_splitted[0], 
                            'value': cameras_splitted[1]})
        return cameras
        
commands = {
    'check_passive':[{
        'labelFilter': 'cameras',
        'eventtype': 'FMS',
        'function': ParserFunctions.parse_cameras
    }]
}
