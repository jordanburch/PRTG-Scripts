import re
import PRTG

regex = '(?i)gaming'
group_id = '2078'

for device in PRTG.get_all_paginated_devices():
    if re.search(regex, device['device']) != None:
        PRTG.move_object(device['objid'], group_id)
