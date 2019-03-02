import unittest
import json

import src.app as app
import utils

class HourLoggerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.db_client = app.client
        self.client = self.app.test_client()

        self.uid = 'test'
        utils.post_registration(self.client, self.uid)

    def checkin(self, time='12:00 am'):
        args = {'uid': self.uid, 'time': time}
        return utils.post(self.client, '/checkin/', args)

    def checkout(self, time='12:00pm'):
        args = {'uid': self.uid, 'time': time}
        return utils.post(self.client, '/checkout/', args)

    def testSimpleCheckInOut(self):
        self.checkin()
        self.assertTrue(self.db_client.is_checked_in(self.uid))

        self.checkout()
        self.assertFalse(self.db_client.is_checked_in(self.uid))

    def testInvalidCheckIn(self):
        self.checkin()
        resp = self.checkin()
        self.assertTrue(resp['status'] == 400)

        self.checkout()

    def testInvalidCheckOut(self):
        resp = self.checkout()
        self.assertTrue(resp['status'] == 400)

    def testGetLoggedHours(self):
        args = {'uid': self.uid}
        data = utils.get(self.client, '/get_logged_hours/?uid={}'.format(self.uid))
        self.assertTrue(data['status'] == 200)

    def tearDown(self):
        self.db_client.delete_user(self.uid)
        self.db_client.get_hours_posts().delete_many({})
