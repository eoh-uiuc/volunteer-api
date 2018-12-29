import json

import src.auth as auth

def get_all(client, request):
    if not auth.verify(request):
        return json.dumps({'status': 400, 'message': 'Not authenticated'})

    resp_data = {}
    db_data = client.get_all_timeslots()
    for slot in db_data:
        position = slot.position
        if position not in resp_data:
            resp_data[position] = []
        resp_data[position].append(slot.construct_response())

    return json.dumps({'status': 200, 'message': 'Success', 'data': resp_data})