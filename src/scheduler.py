import json

import src.auth as auth
import src.utils as utils
from src.utils import TSID, STATUS, MESSAGE, SUCCESS, SUCCESS_CODE, ERROR_CODE

NOT_AUTHENTICATED = 'Not authenticated'
ALREADY_REGISTERED = 'User already registered for timeslot'
NOT_REGISTERED = 'User is not registered for this timeslot'

def check_auth(func):
    def wrapper(client, request, *args, **kwargs):
        status, uid = auth.verify(request)
        if not status:
            return json.dumps({STATUS: ERROR_CODE, MESSAGE: NOT_AUTHENTICATED, 'details': uid})
        return func(client, request, uid, *args, **kwargs)
    return wrapper

@check_auth
def get_all(client, request, uid=None):
    db_data = client.get_all_timeslots()

    resp_data = utils.generate_timeslot_list(db_data)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS, 'data': resp_data})

@check_auth
def add_timeslot(client, request, uid=None):
    tsid = request.form[TSID]

    if client.user_timeslot_pair_exists(uid, tsid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: ALREADY_REGISTERED})

    client.add_timeslot_to_user(uid, tsid)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

@check_auth
def get_registered_timeslots(client, request, uid=None):
    timeslots = client.get_user_timeslots(uid)

    resp_data = utils.generate_timeslot_list(timeslots)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS, 'data': resp_data})

@check_auth
def remove_timeslot(client, request, uid=None):
    tsid = request.form[TSID]

    if not client.user_timeslot_pair_exists(uid, tsid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NOT_REGISTERED})

    client.remove_timeslot_from_user(uid, tsid)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

@check_auth
def get_timeslot_details(client, request, uid=None):
    tsid = request.args[TSID]

    details = client.get_timeslot(tsid).construct_document()
    registered = details['registered']
    res = []
    for r in registered:
        res.append(client.get_user(r).basic_info())
    
    details['registered'] = res

    return json.dumps({STATUS: SUCCESS_CODE, 'data': details})
