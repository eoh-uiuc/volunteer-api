import json

import src.auth as auth
import src.utils as utils

TSID = 'tsid'

def check_admin(func):
    def wrapper(client, request, *args, **kwargs):
        if not auth.verify_admin(request):
            return json.dumps({'status': 400, 'message': 'Not Admin'})
        return func(client, request, *args, **kwargs)
    return wrapper

@check_admin
def admin_add(client, request):
    timeslot = utils.parse_timeslot(request)

    if client.timeslot_exists(timeslot.tsid):
        return json.dumps({'status': 400, 'message': 'Timeslot already exists'})

    if not client.timeslot_position_exists(timeslot.position):
        return json.dumps({'status': 400, 'message': 'Invalid timeslot position'})

    client.add_timeslot(timeslot)
    return json.dumps({'status': 200, 'message': 'Success'})

@check_admin
def admin_mod(client, request):
    timeslot = utils.parse_timeslot(request)

    if not client.timeslot_exists(timeslot.tsid):
        return json.dumps({'status': 400, 'message': 'Timeslot does not exists'})

    if not client.timeslot_position_exists(timeslot.position):
        return json.dumps({'status': 400, 'message': 'Invalid timeslot position'})

    client.update_timeslot(timeslot.tsid, timeslot)
    return json.dumps({'status': 200, 'message': 'Success'})

@check_admin
def admin_del(client, request):
    tsid = request.form[TSID]
    if not client.timeslot_exists(tsid):
        return json.dumps({'status': 400, 'message': 'Timeslot does not exist'})
    
    client.remove_timeslot(tsid)
    return json.dumps({'status': 200, 'message': 'Success'})

@check_admin
def admin_add_pos(client, request):
    new_position = request.form['position']

    if client.timeslot_position_exists(new_position):
        return json.dumps({'status': 400, 'message': 'Timeslot position already exists'})

    client.add_timeslot_position(new_position)
    return json.dumps({'status': 200, 'message': 'Success'})

@check_admin
def admin_del_pos(client, request):
    new_position = request.form['position']

    if not client.timeslot_position_exists(new_position):
        return json.dumps({'status': 400, 'message': 'Timeslot position does not exists'})
    
    client.remove_timeslot_position(new_position)
    return json.dumps({'status': 200, 'message': 'Success'})
