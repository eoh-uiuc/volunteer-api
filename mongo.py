from pymongo import MongoClient

from models.user import User

class DBClient:
    def __init__(self, host='localhost', port=27017):
        self.client = None
        self.connect(host, port)

    def connect(self, host, port):
        self.client = MongoClient(host, port)

    def get_user_posts(self):
        return self.client.users_db.users

    def user_exists(self, uid):
        return self.get_user(uid) != None

    def add_user(self, user):
        if not self.user_exists(user.uid):
            self.get_user_posts().insert_one(user.construct_document())

    def get_user(self, uid):
        data = self.get_user_posts().find_one({'uid': uid})
        if data == None:
            return None
        return User(**data)

    def update_user(self, uid, user):
        self.get_user_posts().update_one({'uid': uid}, {"$set": user.construct_document()})

    def remove_user(self, uid):
        if self.user_exists(uid):
            self.get_user_posts().remove({'uid': uid})
