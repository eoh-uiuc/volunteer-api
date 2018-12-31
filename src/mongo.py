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
        return self.get_user_posts().count_documents({UID: uid}) != 0

    def add_user(self, user):
        '''
        Assumes user does not exist. If user does exist, will add a duplicate document.
        '''
        self.get_user_posts().insert_one(user.construct_document())

    def get_user(self, uid):
        '''
        Returns None if user does not exist
        '''
        data = self.get_user_posts().find_one({UID: uid})
        return None if data == None else User(**data)

    def update_user(self, uid, user):
        '''
        Assumes user exists
        '''
        self.get_user_posts().update_one({UID: uid}, {'$set': user.construct_document()})

    def remove_user(self, uid):
        '''
        Removes user from database and removes it from its registered timeslots
        '''
        user = self.get_user(uid)
        tsids = user.timeslots
        for tsid in tsids:
            timeslot = self.get_timeslot(tsid)
            timeslot.remove_user(uid)
            self.update_timeslot(tsid, timeslot)
        self.get_user_posts().delete_one({UID: uid})

    def get_timeslot_posts(self):
        return self.client.times_db[SLOTS]

    def get_timeslot_position_posts(self):
        return self.client.times_db[POSITIONS]

    def add_timeslot_position(self, position):
        '''
        Assumes timeslot position does not exists. If it does, will insert a duplicate document
        '''
        self.get_timeslot_position_posts().insert_one({POS: position})

    def timeslot_position_exists(self, position):
        return self.get_timeslot_position_posts().count_documents({POS: position}) != 0

    def remove_timeslot_position(self, position):
        self.get_timeslot_position_posts().delete_one({POS: position})
        timeslots_to_delete = self.get_timeslot_posts().find({POS: position})
        for timeslot in timeslots_to_delete:
            self.remove_timeslot(timeslot[TSID])

    def timeslot_exists(self, tsid):
        return self.get_timeslot_posts().count_documents({TSID: tsid}) != 0

    def add_timeslot(self, timeslot):
        '''
        Assumes timeslot does not exist. If it does, will insert a duplicate document
        '''
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
        '''
        Removes timeslot from database and removes itself from its registered users
        Assumes user exists
        '''
        timeslot = self.get_timeslot(tsid)
        uids = timeslot.registered
        for uid in uids:
            user = self.get_user(uid)
            user.remove_timeslot(tsid)
            self.update_user(uid, user)
        self.get_timeslot_posts().delete_one({TSID: tsid})

    def user_timeslot_pair_exists(self, uid, tsid):
        data = self.get_user_posts().find_one({UID: uid})
        return tsid in data['timeslots']

    def add_timeslot_to_user(self, uid, tsid):
        '''
        Assumes uid and tsid exist, and that the uid has not previously registered for tsid
        '''
        user = self.get_user(uid)
        user.add_timeslot(tsid)
        self.update_user(uid, user)

        timeslot = self.get_timeslot(tsid)
        timeslot.add_user(uid)
        self.update_timeslot(tsid, timeslot)

    def get_user_timeslots(self, uid):
        user = self.get_user(uid)
        return [self.get_timeslot(tsid) for tsid in user.timeslots]
