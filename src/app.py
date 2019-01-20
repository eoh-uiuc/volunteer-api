from flask import Flask, request
from flask_cors import CORS, cross_origin

import src.auth as auth
import src.admin as admin
import src.scheduler as scheduler
from src.mongo import DBClient

from models.user import User

app = Flask(__name__)
cors = CORS(app)
client = DBClient()
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return 'EOH Volunteer API'

@app.route('/register/', methods=['POST'])
@cross_origin()
def register():
    return auth.register(client, request)

@app.route('/login/', methods=['POST'])
@cross_origin()
def login():
    return auth.login(client, request)

@app.route('/delete_user/', methods=['POST'])
@cross_origin()
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
@cross_origin()
def get_all():
    return scheduler.get_all(client, request)

@app.route('/add_timeslot/', methods=['POST'])
@cross_origin()
def add_timeslot():
    return scheduler.add_timeslot(client, request)
    
@app.route('/get_timeslots/', methods=['GET'])
@cross_origin()
def get_timeslots():
    return scheduler.get_registered_timeslots(client, request)

@app.route('/del_timeslot/', methods=['POST'])
@cross_origin()
def del_timeslot():
    return scheduler.remove_timeslot(client, request)