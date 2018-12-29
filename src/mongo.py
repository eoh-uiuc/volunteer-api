from pymongo import MongoClient

from models.user import User
from models.timeslot import Timeslot

UID = 'uid'
TSID = 'tsid'
POSITIONS = 'positions'
POS = 'position'
SLOTS = 'slots'

class DBClient:
    def __init__(self, host='localhost', port=27017):
        self.client = None
        self.connect(host, port)

    def connect(self, host, port):
        self.client = MongoClient(host, port)

    def get_user_posts(self):
        return self.client.users_db.users

    def user_exists(self, uid):
        return self.get_user_posts().count({UID: uid}) != 0

    def add_user(self, user):
        self.get_user_posts().insert_one(user.construct_document())

    def get_user(self, uid):
        data = self.get_user_posts().find_one({UID: uid})
        return None if data == None else User(**data)

    def update_user(self, uid, user):
        self.get_user_posts().update_one({UID: uid}, {'$set': user.construct_document()})

    def remove_user(self, uid):
        self.get_user_posts().remove({UID: uid})

    def get_timeslot_posts(self):
        return self.client.times_db[SLOTS]

    def get_timeslot_position_posts(self):
        return self.client.times_db[POSITIONS]

    def add_timeslot_position(self, position):
        self.get_timeslot_position_posts().insert_one({POS: position})

    def timeslot_position_exists(self, position):
        return self.get_timeslot_position_posts().count({POS: position}) != 0

    def remove_timeslot_position(self, position):
        self.get_timeslot_position_posts().remove({POS: position})
        self.get_timeslot_posts().remove({POS: position})

    def timeslot_exists(self, tsid):
        return self.get_timeslot_posts().count({TSID: tsid}) != 0

    def add_timeslot(self, timeslot):
        self.get_timeslot_posts().insert_one(timeslot.construct_document())

    def get_timeslot(self, tsid):
        data = self.get_timeslot_posts().find_one({TSID: tsid})
        return None if data == None else Timeslot(**data)

    def get_all_timeslots(self):
        data = self.get_timeslot_posts().find()
        return None if data == None else [Timeslot(**i) for i in data]

    def update_timeslot(self, tsid, timeslot):
        self.get_timeslot_posts().update_one({TSID: tsid}, {'$set': timeslot.construct_document()})

    def remove_timeslot(self, tsid):
        self.get_timeslot_posts().remove({TSID: tsid})