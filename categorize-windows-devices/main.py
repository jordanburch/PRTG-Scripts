import PRTG


def has_sensor_of_type(sensors, type):
    for sensor in sensors:
        if sensor['type_raw'] == type:
            return True

    return False


def add_to_new_prtg(device, group_id, autodiscovery_template):
    new_device = PRTG.clone_device(device['host'], device['device'], group_id)
    PRTG.auto_discover(new_device, autodiscovery_template)


for device in PRTG.get_all_paginated_devices():
    sensors = PRTG.get_all_sensors_for_device(device['objid'])

    if has_sensor_of_type(sensors, 'http'):
        print('Website - ', device['device'])
        add_to_new_prtg(device, '2453', '')
        continue
    if has_sensor_of_type(sensors, 'ftp'):
        print('FTP - ', device['device'])
        add_to_new_prtg(device, '2453', '')
        continue
    if has_sensor_of_type(sensors, 'ping'):
        print('Ping - ', device['device'])
        add_to_new_prtg(device, '2453', '')
        continue
