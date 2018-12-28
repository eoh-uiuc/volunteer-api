import json

from models.user import User

ID = 'uid'
PASS_HASH = 'pass_hash'

def register(db_client, request):
    uid = request.form[ID]
    if db_client.user_exists(uid):
        return json.dumps({'status': 400, 'message': 'User already exists', 'auth_token': ''})
    
    user_data = {i: j for i, j in request.form.items()}
    new_user = User(**user_data)
    db_client.add_user(new_user)
    auth_token = new_user.encode_auth_token()
    return json.dumps({'status': 200, 'message': 'Success', 'auth_token': auth_token.decode()})

def login(db_client, request):
    uid = request.form[ID]
    if not db_client.user_exists(uid):
        return json.dumps({'status': 400, 'message': 'User does not exists', 'auth_token': ''})

    user = db_client.get_user(uid)
    if request.form[PASS_HASH] != user.pass_hash:
        return json.dumps({'status': 400, 'message': 'Incorrect Password', 'auth_token': ''})

    auth_token = user.encode_auth_token()
    return json.dumps({'status': 200, 'message': 'Success', 'auth_token': auth_token.decode()})

def delete(db_client, request):
    uid = request.form[ID]
    if not db_client.user_exists(uid):
        return json.dumps({'status': 400, 'message': 'User does not exists'})

    user = db_client.get_user(uid)
    if request.form[PASS_HASH] != user.pass_hash:
        return json.dumps({'status': 400, 'message': 'Incorrect Password'})

    db_client.remove_user(uid)
    return json.dumps({'status': 200, 'message': 'Success'})