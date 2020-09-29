import csv
import PRTG

def get_sensors_for_device(device, sensors):
    results = set()

    for sensor in sensors:
        if sensor['parentid'] == device:
            results.add(sensor['type_raw'])

    return results

devices = list()
sensor_map = dict()
sensor_rows = list()
sensor_combinations = list()
known_sensors = set()

all_sensors = PRTG.get_all_paginated_sensors()
for sensor in all_sensors:
    if not sensor['type_raw'] in known_sensors:
        known_sensors.add(sensor['type_raw'])

for device in PRTG.get_all_paginated_devices():
    device_sensors = get_sensors_for_device(device['objid'], all_sensors)
    if device_sensors in sensor_combinations:
        continue

    sensor_combinations.append(device_sensors)
    id = len(devices) + 1
    devices.append({
        "Name": device['device'],
        "Host": device['host'],
        "ID": id
    })

    row = {
        "ID": id
    }

    for sensor in known_sensors:
        row[sensor] = int(sensor in device_sensors)

    sensor_rows.append(row)

try:
    with open('devices.csv', 'w') as devicecsv:
        writer = csv.DictWriter(devicecsv, fieldnames=['Name', 'Host', 'ID'])
        writer.writeheader()
        writer.writerows(devices)

    with open('sensors.csv', 'w') as sensorcsv:
        writer = csv.DictWriter(sensorcsv, fieldnames=['ID'] + list(known_sensors))
        writer.writeheader()
        writer.writerows(sensor_rows)
except IOError:
    print("I/O error")