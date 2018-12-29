from models.timeslot import Timeslot

def parse_timeslot(request):
    slot_data = {i: j for i, j in request.form.items()}
    return Timeslot(**slot_data)