from flask import Flask, request

import src.auth as auth
import src.admin as admin
import src.scheduler as scheduler
from src.mongo import DBClient

from models.user import User

app = Flask(__name__)
client = DBClient()

@app.route('/', methods=['GET'])
def index():
    return 'EOH Volunteer API'

@app.route('/register/', methods=['POST'])
def register():
    return auth.register(client, request)

@app.route('/login/', methods=['POST'])
def login():
    return auth.login(client, request)

@app.route('/delete_user/', methods=['POST'])
def remove():
    return auth.delete(client, request)

@app.route('/admin_add_timeslot/', methods=['POST'])
def admin_add():
    return admin.admin_add(client, request)

@app.route('/admin_mod_timeslot/', methods=['POST'])
def admin_mod():
    return admin.admin_mod(client, request)

@app.route('/admin_del_timeslot/', methods=['POST'])
def admin_del():
    return admin.admin_del(client, request)

@app.route('/admin_add_position/', methods=['POST'])
def admin_add_pos():
    return admin.admin_add_pos(client, request)

@app.route('/admin_del_position/', methods=['POST'])
def admin_del_pos():
    return admin.admin_del_pos(client, request)

@app.route('/get_all_timeslots/', methods=['GET'])
def get_all():
    return scheduler.get_all(client, request)

@app.route('/add_timeslot/', methods=['POST'])
def add_timeslot():
    return scheduler.add_timeslot(client, request)
    
