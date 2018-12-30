import json

import src.auth as auth
import src.utils as utils
from src.utils import TSID, STATUS, MESSAGE, POSITION, SUCCESS, SUCCESS_CODE, ERROR_CODE

ADMIN_REQUIRED = 'Admin privileges required'
NONEXISTENT_TIMESLOT = 'Timeslot does not exists'
DUPLICATE_TIMESLOT = 'Timeslot already exists'
INVALID_POSITION = 'Invalid timeslot position'
DUPLICATE_POSITION = 'Timeslot position already exists'

def check_admin(func):
    def wrapper(client, request, *args, **kwargs):
        if not auth.verify_admin(request):
            return json.dumps({STATUS: ERROR_CODE, MESSAGE: ADMIN_REQUIRED})
        return func(client, request, *args, **kwargs)
    return wrapper

@check_admin
def admin_add(client, request):
    timeslot = utils.parse_timeslot(request)

    if client.timeslot_exists(timeslot.tsid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: DUPLICATE_TIMESLOT})

    if not client.timeslot_position_exists(timeslot.position):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: INVALID_POSITION})

    client.add_timeslot(timeslot)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

@check_admin
def admin_mod(client, request):
    timeslot = utils.parse_timeslot(request)

    if not client.timeslot_exists(timeslot.tsid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_TIMESLOT})

    if not client.timeslot_position_exists(timeslot.position):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: INVALID_POSITION})

    client.update_timeslot(timeslot.tsid, timeslot)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

@check_admin
def admin_del(client, request):
    tsid = request.form[TSID]
    if not client.timeslot_exists(tsid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_TIMESLOT})
    
    client.remove_timeslot(tsid)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

@check_admin
def admin_add_pos(client, request):
    new_position = request.form[POSITION]

    if client.timeslot_position_exists(new_position):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: DUPLICATE_POSITION})

    client.add_timeslot_position(new_position)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

@check_admin
def admin_del_pos(client, request):
    new_position = request.form[POSITION]

    if not client.timeslot_position_exists(new_position):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: INVALID_POSITION})
    
    client.remove_timeslot_position(new_position)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})
