class Hours:
    def __init__(self, uid, checkin_times=None, checkout_times=None, **kwargs):
        if checkin_times is None:
            checkin_times = []
        if checkout_times is None:
            checkout_times = []

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
    
    def __str__(self):
        return f'<{self.uid}, {str(self.checkin_times)}, {str(self.checkout_times)}>'
