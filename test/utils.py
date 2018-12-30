import json
import os

def admin_login(client):
    req = {'uid': os.getenv('ADMIN'), 'pass_hash': os.getenv('ADMIN_PASS')}
    res = client.post('/login/', data=req)
    data = json.loads(res.data.decode())
    return data['auth_token']

def post_registration(client, uid, pass_hash='asdf', name='EOH', phone='1234567890', society='EOH'):
    req = {'uid': uid, 'pass_hash': pass_hash, 'name': name, 'phone': phone, 'society': society}
    res = client.post('/register/', data=req)
    return json.loads(res.data.decode())

def post_login(client, uid, pass_hash):
    req = {'uid': uid, 'pass_hash': pass_hash}
    res = client.post('/login/', data=req)
    return json.loads(res.data.decode())

def post_position(client, admin_auth, position):
    req = {'auth_token': admin_auth, 'position': position}
    res = client.post('/admin_add_position/', data=req)
    return json.loads(res.data.decode())

def del_position(client, admin_auth, position):
    req = {'auth_token': admin_auth, 'position': position}
    res = client.post('/admin_del_position/', data=req)
    return json.loads(res.data.decode())

def post_timeslot(client, admin_auth, tsid, position, start, duration, cap):
    req = {'tsid': tsid, 'position': position, 'start': start, 'duration': duration, 
            'cap': cap, 'auth_token': admin_auth}
    res = client.post('/admin_add_timeslot/', data=req)
    return json.loads(res.data.decode())

def del_timeslot(client, admin_auth, tsid):
    req = {'auth_token': admin_auth, 'tsid': tsid}
    res = client.post('/admin_del_timeslot/', data=req)
    return json.loads(res.data.decode())