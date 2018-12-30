class Timeslot:
    def __init__(self, tsid, position, start, duration, cap, registered=[], **kwargs):
        self.tsid = tsid
        self.position = position
        self.start = start
        self.duration = int(duration)
        self.cap = int(cap)
        self.registered = registered

    def leftover(self):
        return self.cap - len(self.registered)

    def add_user(self, uid):
        self.registered.append(uid)

    def remove_user(self, uid):
        self.registered.remove(uid)

    def construct_document(self):
        return {'tsid': self.tsid, 'position': self.position, 'start': self.start, 
                'duration': self.duration, 'cap': self.cap, 'registered': self.registered}

    def construct_response(self):
        return {'tsid': self.tsid, 'position': self.position, 'start': self.start, 
                'duration': self.duration, 'cap': self.cap, 'taken': self.leftover()}

    def __str__(self):
        return '<Timeslot position: {} start: {}>'.format(self.position, self.start)