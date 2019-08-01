import unittest
from flask import current_app

from app import app, create_app

from config import config

class TestDevelopmentConfig(unittest.TestCase):
	
	def setUp(self):
		config_class = config['development']
		self.app = create_app(config_class)
	
	def test_app_is_development(self):
		self.assertFalse(self.app.config['SECRET_KEY'] is 'my_precious')
		self.assertTrue(self.app.config['DEBUG'] is True)
		self.assertFalse(current_app is None)
		self.assertTrue(
			self.app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://root:lol123@localhost/api_flask'
		)

class TestTestingConfig(unittest.TestCase):

	def setUp(self):
		config_class = config['test']
		self.app = create_app(config_class)

	
	def test_app_is_testing(self):
		self.assertFalse(self.app.config['SECRET_KEY'] is 'my_precious')
		self.assertTrue(self.app.config['DEBUG'])
		self.assertTrue(
			self.app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://root:lol123@localhost/api_flask_test'
		)
