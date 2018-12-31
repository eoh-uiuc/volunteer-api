import unittest
import json
import os

import src.app as app
import utils

class SchedulerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.db_client = app.client
        self.client = self.app.test_client()
        self.admin_auth = utils.admin_login(self.client)

    def post_timeslot_to_user(self, auth, tsid):
        req = {'auth_token': auth, 'tsid': tsid}
        return utils.post(self.client, '/add_timeslot/', req)

    def get_user_timeslots(self, auth):
        req = {'auth_token': auth}
        return utils.get(self.client, '/get_timeslots/', req)

    def test_get_timeslots_empty(self):
        req = {'auth_token': self.admin_auth}

        res = self.client.get('/get_all_timeslots/', data=req)
        res = json.loads(res.data.decode())
        self.assertEqual(res['status'], 200)

    def test_add_timeslot_to_user(self):
        uid = 'bmw4'
        utils.post_registration(self.client, uid)
        data = utils.post_login(self.client, uid, 'asdf')
        auth_token = data['auth_token']

        tsid = 'safety_12'
        utils.post_position(self.client, self.admin_auth, 'safety')
        utils.post_timeslot(self.client, self.admin_auth, tsid, 'safety', '01/01/2019 12:00A', 2, 5)

        res = self.post_timeslot_to_user(auth_token, tsid)
        self.assertEqual(res['status'], 200)

        self.assertTrue(tsid in self.db_client.get_user(uid).timeslots)
        self.assertTrue(uid in self.db_client.get_timeslot(tsid).registered)
        self.db_client.remove_user(uid)

    def test_remove_user_also_removes_from_timeslots(self):
        uid = 'bmw4'
        utils.post_registration(self.client, uid)
        data = utils.post_login(self.client, uid, 'asdf')
        auth_token = data['auth_token']

        tsid = 'safety_12'
        utils.post_position(self.client, self.admin_auth, 'safety')
        utils.post_timeslot(self.client, self.admin_auth, tsid, 'safety', '01/01/2019 12:00A', 2, 5)

        res = self.post_timeslot_to_user(auth_token, tsid)
        self.assertEqual(res['status'], 200)

        self.db_client.remove_user(uid)
        self.assertFalse(uid in self.db_client.get_timeslot(tsid).registered)

    def test_remove_timeslot_also_removes_from_users(self):
        uid = 'bmw4'
        utils.post_registration(self.client, uid)
        data = utils.post_login(self.client, uid, 'asdf')
        auth_token = data['auth_token']

        tsid = 'safety_12'
        utils.post_position(self.client, self.admin_auth, 'safety')
        utils.post_timeslot(self.client, self.admin_auth, tsid, 'safety', '01/01/2019 12:00A', 2, 5)

        res = self.post_timeslot_to_user(auth_token, tsid)
        self.assertEqual(res['status'], 200)

        res = utils.del_timeslot(self.client, self.admin_auth, tsid)
        self.assertFalse(tsid in self.db_client.get_user(uid).timeslots)
        self.db_client.remove_user(uid)

    def test_get_registered_timeslots(self):
        uid = 'bmw4'
        utils.post_registration(self.client, uid)
        data = utils.post_login(self.client, uid, 'asdf')
        auth_token = data['auth_token']

        timeslots = self.get_user_timeslots(auth_token)
        self.assertEqual(len(timeslots['data']), 0)

        tsid = 'safety_12'
        utils.post_position(self.client, self.admin_auth, 'safety')
        utils.post_timeslot(self.client, self.admin_auth, tsid, 'safety', '01/01/2019 12:00A', 2, 5)

        res = self.post_timeslot_to_user(auth_token, tsid)
        self.assertEqual(res['status'], 200)

        timeslots = self.get_user_timeslots(auth_token)
        self.assertEqual(len(timeslots['data']), 1)
        self.assertEqual(timeslots['data']['safety'][0]['tsid'], tsid)
        self.db_client.remove_user(uid)

    def tearDown(self):
        self.clear_db()
        
    def clear_db(self):
        self.db_client.get_timeslot_posts().delete_many({})
        self.db_client.get_timeslot_position_posts().delete_many({})
