from flask import Flask, request
from flask_cors import CORS, cross_origin
import os

import src.auth as auth
import src.admin as admin
import src.scheduler as scheduler
import src.hour_logger as hour_logger
from src.mongo import DBClient

from models.user import User

application = Flask(__name__)
cors = CORS(application)
client = None
if os.environ['ENV'] == 'production':
  print('Connecting to production MongoDB instance specified by MONGO_URI')
  client = DBClient(os.environ['MONGO_URI'])
else:
  client = DBClient()

application.config['CORS_HEADERS'] = 'Content-Type'

@application.route('/', methods=['GET'])
@cross_origin()
def index():
    return 'EOH Volunteer API'

@application.route('/register/', methods=['POST'])
@cross_origin()
def register():
    return auth.register(client, request)

@application.route('/login/', methods=['POST'])
@cross_origin()
def login():
    return auth.login(client, request)

@application.route('/delete_user/', methods=['POST'])
@cross_origin()
def remove():
    return auth.delete(client, request)

@application.route('/admin_add_timeslot/', methods=['POST'])
def admin_add():
    return admin.admin_add(client, request)

@application.route('/admin_mod_timeslot/', methods=['POST'])
def admin_mod():
    return admin.admin_mod(client, request)

@application.route('/admin_del_timeslot/', methods=['POST'])
def admin_del():
    return admin.admin_del(client, request)

@application.route('/admin_add_position/', methods=['POST'])
def admin_add_pos():
    return admin.admin_add_pos(client, request)

@application.route('/admin_del_position/', methods=['POST'])
def admin_del_pos():
    return admin.admin_del_pos(client, request)


@application.route('/reset_password/', methods=['POST'])
def admin_reset_password():
    return admin.admin_reset_password(client, request)

@application.route('/get_all_timeslots/', methods=['GET'])
@cross_origin()
def get_all():
    return scheduler.get_all(client, request)

@application.route('/add_timeslot/', methods=['POST'])
@cross_origin()
def add_timeslot():
    return scheduler.add_timeslot(client, request)

@application.route('/get_timeslot_details/', methods=['GET'])
@cross_origin()
def get_timeslot_details():
    return scheduler.get_timeslot_details(client, request)

@application.route('/get_timeslots/', methods=['GET'])
@cross_origin()
def get_timeslots():
    return scheduler.get_registered_timeslots(client, request)

@application.route('/del_timeslot/', methods=['POST'])
@cross_origin()
def del_timeslot():
    return scheduler.remove_timeslot(client, request)

@application.route('/checkin/', methods=['POST'])
@cross_origin()
def checkin():
    return hour_logger.checkin(client, request)

@application.route('/checkout/', methods=['POST'])
@cross_origin()
def checkout():
    return hour_logger.checkout(client, request)

@application.route('/get_logged_hours/', methods=['GET'])
@cross_origin()
def get_logged_hours():
    return hour_logger.get_hours(client, request)
