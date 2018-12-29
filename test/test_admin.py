import unittest
import json

import src.app as app
import key

class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client
        self.auth_token = self.admin_login()

    def admin_login(self):
        data = {'uid': key.ADMIN, 'pass_hash': key.ADMIN_PASS}
        res = self.client().post('/login/', data=data)
        data = json.loads(res.data.decode())
        return data['auth_token']

    def test_add_position(self):
        data = {'auth_token': self.auth_token, 'position': 'safety'}
        
        res = self.client().post('/admin_add_position/', data=data)
        res = json.loads(res.data.decode())
        self.assertEqual(res['status'], 200)
        self.assertEqual(res['message'], 'Success')
