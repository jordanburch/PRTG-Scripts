import requests
import json
import re
import constants
import time

C = constants.get_constants()

prtg_url = C['PRTG_URL']
prtg_un = C['PRTG_USER']
prtg_passhash = C['PRTG_PASSHASH']
prtg_clone_device = C['PRTG_CLONE_DEVICE']
prtg_clone_group = C['PRTG_CLONE_GROUP']
prtg_automation_group = C['PRTG_AUTOMATION_GROUP']

def prtg_request_json(request):
    r = requests.get(prtg_url + request + '&username=' + prtg_un + '&passhash=' + prtg_passhash + '&output=json', verify = False)
    return r.json()

def prtg_request(request):
    r = requests.get(prtg_url + request + '&username=' + prtg_un + '&passhash=' + prtg_passhash + '&output=json', verify = False)
    return r

def prtg_paginate_request(request, count, start):
    r = prtg_request_json(request + '&count=' + str(count) + '&start=' + str(start))

    numItems = r['treesize']
    return (numItems, r)

def prtg_post_request(request,args):
    args['username'] = prtg_un
    args['passhash'] = prtg_passhash
    encoded = quote(args)
    r = requests.get(prtg_url + request + '&username=' + prtg_un + '&passhash=' + prtg_passhash + '&output=json&'+encoded, verify = False)
    return r

def get_all_devices():
    r = prtg_request_json('table.json?content=devices&columns=objid,probe,group,parentid,device,host,downsens,partialdownsens,downacksens,upsens,warnsens,pausedsens,unusualsens,undefinedsens')
    return r['devices']

def get_all_paginated_devices():
    devices = list()
    num_items = 0
    page_size = 500
    start = 0

    while (num_items >= start):
        val = prtg_paginate_request('table.json?content=devices&columns=objid,probe,group,parentid,device,host,downsens,partialdownsens,downacksens,upsens,warnsens,pausedsens,unusualsens,undefinedsens', page_size, start)
        num_items = val[0]
        start += page_size
        devices += val[1]['devices']

    return devices

def get_all_sensors():
    r = prtg_request_json('table.json?content=sensors&columns=objid,type,probe,group,parentid,device,sensor,status,message,lastvalue,priority,favorite')
    return r['sensors']

def get_all_paginated_sensors():
    sensors = list()
    num_items = 0
    page_size = 500
    start = 0
    
    while (num_items >= start):
        val = prtg_paginate_request('table.json?content=sensors&columns=objid,probe,group,parentid,device,sensor,status,message,lastvalue,priority,favorite', page_size, start)
        num_items = val[0]
        start += page_size
        sensors += val[1]['sensors']

    return sensors

def get_all_sensors_for_device(device_id):
    r = prtg_request_json('table.json?content=sensors&columns=objid,type,probe,group,parentid,device,sensor,status,message,lastvalue,priority,favorite&filter_parentid=' + str(device_id))

    return r['sensors']

def get_all_groups():
    r = prtg_request_json('table.json?content=groups&columns=objid,group,name,parentid')
    return r['groups']

def get_sub_groups(gid):
    r = prtg_request_json('table.json?content=groups&columns=objid,group,name,parentid&id=' + gid)
    return r['groups']
    
def clone_gs_device(id,ip,name,group_id):
    req = 'duplicateobject.htm?id='+str(id)+'&name='+name+'&host='+ip+'&targetid='+str(group_id)
    r = prtg_request(req)
    data = r.content
    new_id = re.search("id=(\d+)",str(data))
    time.sleep(1)
    return new_id.group()[3:]

def clone_device(ip,name,group_id):
    req = 'duplicateobject.htm?id='+prtg_clone_device+'&name='+name+'&host='+ip+'&targetid='+str(group_id)
    r = prtg_request(req)
    data = r.content
    new_id = re.search("id=(\d+)",str(data))
    time.sleep(1)
    return new_id.group()[3:]

def rename(prtg_id,name):
    req = 'rename.htm?id='+str(prtg_id)+'&value=' + name 
    print(req)   
    r = prtg_request(req)
    print(str(r))
    set_object_property(prtg_id,'host',name)
    
def delete(prtgid):
    req = 'deleteobject?id='+str(prtgid)+'&approve=1' 
    print(req)   
    r = prtg_request(req)
    print(str(r))

def set_object_property(prtgid,prop,value):
    req = 'setobjectproperty.htm?id='+str(prtgid)+'&name='+str(prop)+'&value=' + str(value)
    print(req)   
    r = prtg_request(req)
    print(str(r))

def move_object(prtgid,targetid):
    req = 'moveobject.htm?id='+str(prtgid)+'&targetid='+str(targetid)
    print(req)   
    r = prtg_request(req)
    print(str(r))

def auto_discover(prtgid,template):
    if(prtgid != 0):
        req = 'discovernow.htm?id='+str(prtgid)+'&template=' + template + '.odt' 
        print(req)   
        r = prtg_request(req)
        print(str(r))
        time.sleep(20)

def resume(prtgid):
    req = 'pause.htm?id='+str(prtgid)+'&action=1'    
    r = prtg_request(req)
    print(str(r))
    time.sleep(1)

def get_automated_probe_groups():
    data = prtg_request_json('table.json?content=groups&columns=probe,objid,group,name,parentid')
    groups = data['groups']
    probe_groups = dict()

    group_map = dict()
    for p in groups:
        group_map[p['objid']] = p['name']
    for p in groups:
        parent_name = ''
        if(p['parentid'] in group_map.keys()):
            parent_name = group_map[p['parentid']]

        if(p['probe'] not in probe_groups.keys()):
            probe_groups[p['probe']] = dict()
        if(p['name'] == 'Root'):
            next
        elif(parent_name == 'Automated' or p['name'] == 'Automated'):
            probe_groups[p['probe']][p['group']] = p['objid']
        ##if(p['group'] == 'Automated'):
        ##    probe_groups[p['probe']] = p['objid']
    return probe_groups
    
def clone_group(name,group_id):
    req = 'duplicateobject.htm?name=' + name + '&targetid='+str(group_id)+'&id='+prtg_clone_group
    
    r = prtg_request(req)
    data = r.content
    new_id = re.search("id=(\d+)",str(data))
    return_id =  new_id.group()[3:]
    resume(return_id)
    return return_id
