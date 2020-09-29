import re
import PRTG

scripts = dict()

for sensor in PRTG.get_all_paginated_sensors():
    if sensor['type_raw'] != 'exe' and sensor['type_raw'] != 'exexml':
        continue

    response = PRTG.prtg_request('getobjectproperty.htm?id=' + str(sensor['objid']) + '&name=exefilelabel&show=text')
    match = re.search('<result>.*<div>(.*)<\/div><\/div><\/result>', response.text)

    if not match.group(1) in scripts:
        scripts[match.group(1)] = 0
    scripts[match.group(1)] += 1

print(scripts)