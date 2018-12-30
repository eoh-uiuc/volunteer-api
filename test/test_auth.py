import unittest
import json
import os

import src.app as app
import models.user as user

import utils as utils

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.db_client = app.client
        self.client = self.app.test_client()
        self.secret = os.getenv('SECRET')

    def test_register_user(self):
        uid = 'bmw4'
        data = utils.post_registration(self.client, uid)

        self.assertEqual(data['status'], 200)
        self.assertTrue(self.db_client.user_exists(uid))

        self.db_client.remove_user(uid)
        self.assertFalse(self.db_client.user_exists(uid))

    def test_failed_login_user(self):
        uid = 'bmw4'
        if self.db_client.user_exists(uid):
            self.db_client.remove_user(uid)
        data = utils.post_login(self.client, uid, 'asdf')

        self.assertEqual(data['status'], 400)
        self.assertEqual(data['auth_token'], '')
        self.assertFalse(self.db_client.user_exists(uid))

    def test_login_user(self):
        uid = 'bmw4'
        utils.post_registration(self.client, uid)
        data = utils.post_login(self.client, uid, 'asdf')

        self.assertEqual(data['status'], 200)
        self.assertTrue(data['auth_token'] != '')
        self.assertTrue(user.User.decode_auth_token(data['auth_token'], self.secret)[0])

        self.db_client.remove_user(uid)
        self.assertFalse(self.db_client.user_exists(uid))

