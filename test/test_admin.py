import unittest
import json
import os

import src.app as app
import utils

class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.db_client = app.client
        self.client = self.app.test_client()
        self.auth_token = utils.admin_login(self.client)

    def test_add_position(self):
        res = utils.post_position(self.client, self.auth_token, 'safety')

        self.assertEqual(res['status'], 200)
        self.assertEqual(res['message'], 'Success')
        self.assertTrue(self.db_client.timeslot_position_exists('safety'))

    def test_del_position(self):
        utils.post_position(self.client, self.auth_token, 'safety')
        self.assertTrue(self.db_client.timeslot_position_exists('safety'))

        res = utils.del_position(self.client, self.auth_token, 'safety')

        self.assertEqual(res['status'], 200)
        self.assertEqual(res['message'], 'Success')
        self.assertFalse(self.db_client.timeslot_position_exists('safety'))

    def test_add_timeslot(self):
        tsid = 'safety_12'
        utils.post_position(self.client, self.auth_token, 'safety')
        res = utils.post_timeslot(self.client, self.auth_token, tsid, 'safety', '01/01/2019 12:00A', 2, 5)

        self.assertEqual(res['status'], 200)
        self.assertTrue(self.db_client.timeslot_exists(tsid))

    def test_remove_timeslot(self):
        tsid = 'safety_12'
        utils.post_position(self.client, self.auth_token, 'safety')
        utils.post_timeslot(self.client, self.auth_token, tsid, 'safety', '01/01/2019 12:00A', 2, 5)
        self.assertTrue(self.db_client.timeslot_exists(tsid))

        res = utils.del_timeslot(self.client, self.auth_token, tsid)

        self.assertEqual(res['status'], 200)
        self.assertFalse(self.db_client.timeslot_exists(tsid))

    def test_del_position_with_slots(self):
        utils.post_position(self.client, self.auth_token, 'safety')
        utils.post_timeslot(self.client, self.auth_token, 'safety_12', 'safety', '01/01/2019 12:00A', 2, 5)
        utils.post_timeslot(self.client, self.auth_token, 'safety_13', 'safety', '01/01/2019 01:00P', 2, 5)

        self.assertTrue(self.db_client.timeslot_exists('safety_12'))
        self.assertTrue(self.db_client.timeslot_exists('safety_13'))

        res = utils.del_position(self.client, self.auth_token, 'safety')

        self.assertEqual(res['status'], 200)
        self.assertFalse(self.db_client.timeslot_exists('safety_12'))
        self.assertFalse(self.db_client.timeslot_exists('safety_13'))

    def test_duplicate_timeslot(self):
        tsid = 'safety_12'
        utils.post_position(self.client, self.auth_token, 'safety')
        utils.post_timeslot(self.client, self.auth_token, tsid, 'safety', '01/01/2019 12:00A', 2, 5)
        self.assertTrue(self.db_client.timeslot_exists(tsid))
        res = utils.post_timeslot(self.client, self.auth_token, tsid, 'safety', '01/01/2019 12:00A', 2, 5)
        self.assertEqual(res['status'], 400)

        self.assertTrue(self.db_client.timeslot_exists(tsid))
        res = utils.del_timeslot(self.client, self.auth_token, tsid)
        self.assertFalse(self.db_client.timeslot_exists(tsid))

    def tearDown(self):
        self.clear_db()
        
    def clear_db(self):
        self.db_client.get_timeslot_posts().delete_many({})
        self.db_client.get_timeslot_position_posts().delete_many({})
