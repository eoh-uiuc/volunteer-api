from models.timeslot import Timeslot

SECRET = 'SECRET'
ADMIN = 'ADMIN'

UID = 'uid'
TSID = 'tsid'

AUTHORIZATION = 'Authorization'
PWD = 'pwd'
PASS_HASH = 'pass_hash'
AUTH_TOKEN = 'auth_token'
POSITION = 'position'

STATUS = 'status'
MESSAGE = 'message'

SUCCESS = 'Success'

SUCCESS_CODE = 200
ERROR_CODE = 400

def parse_timeslot(request):
    slot_data = {i: j for i, j in request.form.items()}
    return Timeslot(**slot_data)

def generate_timeslot_list(timeslots):
    resp_data = {}
    for slot in timeslots:
        position = slot.position
        if position not in resp_data:
            resp_data[position] = []
        resp_data[position].append(slot.construct_response())

    return resp_data
