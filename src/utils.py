from models.timeslot import Timeslot

SECRET = 'SECRET'
ADMIN = 'ADMIN'

UID = 'uid'
TSID = 'tsid'

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