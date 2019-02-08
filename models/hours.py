class Hours:
    def __init__(self, uid, checkin_times=[], checkout_times=[], **kwargs):
        self.uid = uid
        self.checkin_times = checkin_times
        self.checkout_times = checkout_times

    def checkin(self, time):
        self.checkin_times.append(time)

    def checkout(self, time):
        self.checkout_times.append(time)

    def checked_in(self):
        return len(self.checkin_times) == len(self.checkout_times) + 1

    def construct_document(self):
        return {'uid': self.uid, 'checkin_times': self.checkin_times, 'checkout_times': self.checkout_times}

    def construct_response(self):
        hours = [[i, j] for i, j in zip(self.checkin_times, self.checkout_times)]
        return {'logged_hours': hours}
