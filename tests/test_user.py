import unittest

from app import db
from app.models import User

from base import BaseTestCase

class TestUserModel(BaseTestCase):
	
	def test_encode_auth_token(self):
		user = User.create_element('username', 'password','email')
		auth_token = user.encode_auth_token(user.id)
		self.assertTrue(isinstance(auth_token, bytes))
	
	def test_decode_atuh_token(self):
		user = User.create_element('username', 'password', 'email')
		auth_token = user.encode_auth_token(user.id)
		self.assertTrue(isinstance(auth_token, bytes))
		self.assertTrue(User.decode_auth_token(auth_token) == 1)