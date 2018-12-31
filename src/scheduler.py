import json

import src.auth as auth
from src.utils import TSID, STATUS, MESSAGE, SUCCESS, SUCCESS_CODE, ERROR_CODE

NOT_AUTHENTICATED = 'Not authenticated'
ALREADY_REGISTERED = 'User already registered for timeslot'

def check_auth(func):
    def wrapper(client, request, *args, **kwargs):
        status, uid = auth.verify(request)
        if not status:
            return json.dumps({STATUS: ERROR_CODE, MESSAGE: NOT_AUTHENTICATED})
        return func(client, request, uid, *args, **kwargs)
    return wrapper

def generate_timeslot_list(timeslots):
    resp_data = {}
    for slot in timeslots:
        position = slot.position
        if position not in resp_data:
            resp_data[position] = []
        resp_data[position].append(slot.construct_response())

    return resp_data

@check_auth
def get_all(client, request, uid=None):
    db_data = client.get_all_timeslots()

    resp_data = generate_timeslot_list(db_data)
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

    resp_data = generate_timeslot_list(timeslots)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS, 'data': resp_data})
