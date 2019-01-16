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

        self.uid = 'test'
        utils.post_registration(self.client, self.uid)
        data = utils.post_login(self.client, self.uid, 'asdf')
        self.auth_token = data['auth_token']

        self.tsid = 'safety_12'
        self.create_position(self.tsid, 'safety')

    def add_timeslot_to_user(self, auth, tsid):
        auth = {'Authorization': auth}
        req = {'tsid': tsid}
        return utils.post(self.client, '/add_timeslot/', req, auth)

    def get_user_timeslots(self, auth):
        auth = {'Authorization': auth}
        return utils.get(self.client, '/get_timeslots/', {}, auth)

    def remove_timeslot_from_user(self, auth, tsid):
        auth = {'Authorization': auth}
        req = {'tsid': tsid}
        return utils.post(self.client, '/del_timeslot/', req, auth)

    def create_position(self, tsid, position):
        utils.post_position(self.client, self.admin_auth, position)
        utils.post_timeslot(self.client, self.admin_auth, tsid, position, '01/01/2019 12:00A', 2, 5)

    def test_get_timeslots_empty(self):
        auth = {'Authorization': self.admin_auth}

        res = self.client.get('/get_all_timeslots/', headers=auth)
        res = json.loads(res.data.decode())
        self.assertEqual(res['status'], 200)

    def test_add_timeslot_to_user(self):
        res = self.add_timeslot_to_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        self.assertTrue(self.tsid in self.db_client.get_user(self.uid).timeslots)
        self.assertTrue(self.uid in self.db_client.get_timeslot(self.tsid).registered)

    def test_remove_user_also_removes_from_timeslots(self):
        uid = 'test1'
        utils.post_registration(self.client, uid)
        data = utils.post_login(self.client, uid, 'asdf')
        auth_token = data['auth_token']

        res = self.add_timeslot_to_user(auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        self.db_client.delete_user(uid)
        self.assertFalse(uid in self.db_client.get_timeslot(self.tsid).registered)

    def test_remove_timeslot_also_removes_from_users(self):

        res = self.add_timeslot_to_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        res = utils.del_timeslot(self.client, self.admin_auth, self.tsid)
        self.assertFalse(self.tsid in self.db_client.get_user(self.uid).timeslots)

    def test_get_registered_timeslots(self):
        timeslots = self.get_user_timeslots(self.auth_token)
        self.assertEqual(len(timeslots['data']), 0)

        res = self.add_timeslot_to_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        timeslots = self.get_user_timeslots(self.auth_token)
        self.assertEqual(len(timeslots['data']), 1)
        self.assertEqual(timeslots['data']['safety'][0]['tsid'], self.tsid)
        self.assertTrue(self.tsid in self.db_client.get_user(self.uid).timeslots)
        self.assertTrue(self.uid in self.db_client.get_timeslot(self.tsid).registered)

    def test_remove_invalid_timeslot_from_user(self):
        res = self.remove_timeslot_from_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 400)

    def test_remove_timeslot_from_user(self):
        res = self.add_timeslot_to_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        timeslots = self.get_user_timeslots(self.auth_token)
        self.assertEqual(len(timeslots['data']), 1)

        res = self.remove_timeslot_from_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        timeslots = self.get_user_timeslots(self.auth_token)
        self.assertEqual(len(timeslots['data']), 0)
        self.assertFalse(self.tsid in self.db_client.get_user(self.uid).timeslots)
        self.assertFalse(self.uid in self.db_client.get_timeslot(self.tsid).registered)

    def test_remove_timeslot_twice_from_user(self):
        res = self.add_timeslot_to_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        res = self.remove_timeslot_from_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 200)

        res = self.remove_timeslot_from_user(self.auth_token, self.tsid)
        self.assertEqual(res['status'], 400)

    def tearDown(self):
        self.db_client.delete_user(self.uid)
        self.clear_db()
        
    def clear_db(self):
        self.db_client.get_timeslot_posts().delete_many({})
        self.db_client.get_timeslot_position_posts().delete_many({})
