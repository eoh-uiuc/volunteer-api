import json

from src.utils import UID, TIME, STATUS, MESSAGE, SUCCESS, SUCCESS_CODE, ERROR_CODE

NONEXISTENT_USER = 'User does not exist'
ALREADY_CHECKED_IN = 'User is already checked in'
NOT_CHECKED_IN = 'User is not checked in'

def checkin(client, request):
    uid = request.form[UID]

    if not client.user_exists(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_USER})

    if client.is_checked_in(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: ALREADY_CHECKED_IN})

    time = request.form[TIME]
    client.checkin(uid, time)

    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

def checkout(client, request):
    uid = request.form[UID]

    if not client.user_exists(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_USER})

    if not client.is_checked_in(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NOT_CHECKED_IN})

    time = request.form[TIME]
    client.checkout(uid, time)

    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})

def get_hours(client, request):
    uid = request.args[UID]

    if not client.user_exists(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_USER})

    hours = client.get_hours(uid)
    data = hours.construct_response()

    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS_CODE, **data})