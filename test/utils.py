import json
import os

def get(client, path, req={}, headers={}):
    res = client.get(path, data=req, headers=headers)
    return json.loads(res.data.decode())

def post(client, path, req={}, headers={}):
    res = client.post(path, data=req, headers=headers)
    return json.loads(res.data.decode())

def admin_register(client):
    post_registration(client, os.getenv('ADMIN'), os.getenv('ADMIN_PASS'))

def admin_login(client):
    req = {'uid': os.getenv('ADMIN'), 'pwd': os.getenv('ADMIN_PASS')}
    data = post(client, '/login/', req=req)
    if data['status'] == 400:
        admin_register(client)
        req = {'uid': os.getenv('ADMIN'), 'pwd': os.getenv('ADMIN_PASS')}
        data = post(client, '/login/', req=req)
    return data['auth_token']

def post_registration(client, uid, pwd='asdf', name='EOH', phone='1234567890', society='EOH'):
    req = {'uid': uid, 'pwd': pwd, 'name': name, 'phone': phone, 'society': society}
    return post(client, '/register/', req=req)

def post_login(client, uid, pwd):
    req = {'uid': uid, 'pwd': pwd}
    return post(client, '/login/', req=req)

def post_position(client, admin_auth, position):
    auth = {'Authorization': admin_auth}
    req = {'position': position}
    return post(client, '/admin_add_position/', req=req, headers=auth)

def del_position(client, admin_auth, position):
    auth = {'Authorization': admin_auth}
    req = {'position': position}
    return post(client, '/admin_del_position/', req=req, headers=auth)

def post_timeslot(client, admin_auth, tsid, position, start, duration, cap):
    auth = {'Authorization': admin_auth}
    req = {'tsid': tsid, 'position': position, 'start': start, 'duration': duration, 
            'cap': cap}
    return post(client, '/admin_add_timeslot/', req=req, headers=auth)

def del_timeslot(client, admin_auth, tsid):
    auth = {'Authorization': admin_auth}
    req = {'tsid': tsid}
    return post(client, '/admin_del_timeslot/', req=req, headers=auth)