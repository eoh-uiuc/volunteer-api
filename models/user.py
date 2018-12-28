import jwt
import datetime

import key

class User:
    def __init__(self, uid, pass_hash, name, phone, society, timeslots=[], **kwargs):
        self.uid = uid
        self.pass_hash = pass_hash
        self.name = name
        self.phone = phone
        self.society = society
        self.timeslots = timeslots

    def construct_document(self):
        return {'uid': self.uid, 'pass_hash': self.pass_hash, 'name': self.name,
                'phone': self.phone, 'society': self.society, 'timeslots': self.timeslots}

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': self.uid
            }
            return jwt.encode(
                payload,
                key.SECRET,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key.SECRET)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __str__(self):
        return '<User id: {}>'.format(self.uid)