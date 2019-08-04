import unittest

from app import db
from app.models import User, Post

from base import BaseTestCase

class TestePostModel(BaseTestCase):

	def test_create_post_model(self):
		""" Test for create a post """
		user = User.create_element('username', 'password', 'alan@gmail.com')
		post = Post.create_element('title', 'description', user.id)
		self.assertTrue(isinstance(post, Post))
	
	def test_get_post_id(self):
		""" Test for get a post by id """
		user = User.create_element('username', 'password', 'alan@gmail.com')
		post = Post.create_element('title', 'description', user.id)
		post_id = Post.get_by_id(post.id)
		self.assertTrue(isinstance(post_id, Post))

	def test_update_post_model(self):
		user = User.create_element('username', 'password', 'alan@gmail.com')
		post = Post.create_element('title', 'description', user.id)
		post_update = Post.update_element('title', 'description', post.id)
		self.assertTrue(isinstance(post_update, Post))
	
	def test_delete_post_model(self):
		user = User.create_element('username', 'password', 'alan@gmail.com')
		post = Post.create_element('title', 'description', user.id)
		post_delete = Post.delete_element(post.id)
		self.assertTrue(post_delete)