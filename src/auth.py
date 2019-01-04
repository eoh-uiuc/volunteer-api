import json
import os
import hashlib

from models.user import User
from src.utils import SECRET, ADMIN, UID, PWD, PASS_HASH, AUTH_TOKEN, STATUS, MESSAGE, SUCCESS, SUCCESS_CODE, ERROR_CODE

INCORRECT_PASSWORD = 'Incorrect Password'
NONEXISTENT_USER = 'User does not exist'
DUPLICATE_USER = 'User already exists'

def verify_admin(request):
    auth_token = request.form[AUTH_TOKEN]
    status, uid = User.decode_auth_token(auth_token, os.getenv(SECRET))

    return status and uid == os.getenv(ADMIN)

def verify(request):
    auth_token = request.form[AUTH_TOKEN]
    status, uid = User.decode_auth_token(auth_token, os.getenv(SECRET))

    return status, uid

def hash_pass(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def register(db_client, request):
    uid = request.form[UID]
    if db_client.user_exists(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: DUPLICATE_USER, AUTH_TOKEN: ''})
    
    user_data = {i: j for i, j in request.form.items()}
    user_data[PASS_HASH] = hash_pass(user_data[PWD])
    new_user = User(**user_data)
    db_client.add_user(new_user)
    auth_token = new_user.encode_auth_token(os.getenv(SECRET))
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS, AUTH_TOKEN: auth_token.decode()})

def login(db_client, request):
    uid = request.form[UID]
    if not db_client.user_exists(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_USER, AUTH_TOKEN: ''})

    user = db_client.get_user(uid)
    if hash_pass(request.form[PWD]) != user.pass_hash:
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: INCORRECT_PASSWORD, AUTH_TOKEN: ''})

    auth_token = user.encode_auth_token(os.getenv(SECRET))
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS, AUTH_TOKEN: auth_token.decode()})

def delete(db_client, request):
    uid = request.form[UID]
    if not db_client.user_exists(uid):
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: NONEXISTENT_USER})

    user = db_client.get_user(uid)
    if hash_pass(request.form[PWD]) != user.pass_hash:
        return json.dumps({STATUS: ERROR_CODE, MESSAGE: INCORRECT_PASSWORD})

    db_client.delete_user(uid)
    return json.dumps({STATUS: SUCCESS_CODE, MESSAGE: SUCCESS})