import unittest

from flask_testing import TestCase

from app import app, db, create_app
from config import config

class BaseTestCase(TestCase):
	""" Base Test """

	def create_app(self):
		app.config.from_object(config['test'])
		return app;

	def setUp(self):
		db.create_all()
		db.session.commit()
	
	def tearDown(self):
		db.session.remove()
		db.drop_all()
