from flask import Blueprint
from flask import jsonify, make_response, abort, request

from .models import User, Post


page = Blueprint('page', __name__)

def auth_token_user():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_token = auth_header.split(" ")[1]
	else:
		auth_token = ''
	if auth_token:
		resp = User.decode_auth_token(auth_token)
		if not isinstance(resp, str):
			user = User.query.filter_by(id=resp).first()
			return user
		else:
			response_object = {
				'status': 'Fail',
				'message': resp
			}
			return response_object
	else:
		response_object = {
			'status': 'Fail',
			'message': 'Provide invalid auth token'
		}
		return response_object
		

@page.app_errorhandler(404)
def not_found(error):
	return make_response(jsonify({ 'status': 'Fail', 'message': 'Not found' }), 400)


@page.route('/api/v1/users/<username>', methods=['GET'])
def get_user(username):
	user = User.get_by_username(username)
	if not user:
		abort(404)
	return send_json(user)

@page.route('/api/v1/auth/register', methods=['POST'])
def register_user():
	""" Register user """

	#Check if request is a json
	if not request.json or not 'email' or not 'password' in request.json:
		abort(404)
	#get the post data
	post_data = request.get_json()
	#Check if user already exists
	user = User.query.filter_by(email=post_data.get('email')).first()
	if not user:
		try:
			#Create user
			user = User.create_element(post_data.get('username'), post_data.get('password'), post_data.get('email'))
			#generate the auth token
			auth_token = user.encode_auth_token(user.id)
			response_object = {
				'status': 'success',
				'message': 'Successfully registered.',
				'auth_token': auth_token.decode()
			}
			return make_response(jsonify(response_object)), 201
		except Exception as e:
			response_object = {
				'status': 'Fail',
				'message': 'Some error ocurred. Please try again'
			}
			return make_response(jsonify(response_object)), 401
	else:
		response_object = {
			'status': 'Fail',
			'message': 'User already exists. Please Log in.'
		}
		return make_response(jsonify(response_object)), 202

@page.route('/api/v1/auth/login', methods=['POST'])
def login_user():
	""" Login resource """
	if not request.json or not 'email' or not 'password' in request.json:
		abort(404)

	#get the post data
	post_data = request.get_json()
	try:
		# get user data for email
		user = User.get_by_email(post_data.get('email'))
		if user and user.verify_password(post_data.get('password')):
			auth_token = user.encode_auth_token(user.id)
			if auth_token:
				response_object = {
					'status': 'success',
					'message': 'Successfully logged in.',
					'auth_token': auth_token.decode()
				}
				return make_response(jsonify(response_object)), 200
		else:
			response_object = {
				'status': 'Fail',
				'message': 'Credentials incorrect',
			}
			return make_response(jsonify(response_object)), 404
	except Exception as e:
		print(e)
		response_object = {
			'status': 'Fail',
			'message': 'Try again.'
		}
		return make_response(jsonify(response_object)), 500

@page.route('/api/v1/auth/status')
def get_status_user():
	auth_header = request.headers.get('Authorization')
	if auth_header:
		auth_token = auth_header.split(" ")[1]
	else:
		auth_token = ''
	if auth_token:
		resp = User.decode_auth_token(auth_token)
		if not isinstance(resp, str):
			user = User.query.filter_by(id=resp).first()
			response_object = {
				'status': 'success',
				'data': {
					'user_id': user.id,
					'email': user.email,
					'username': user.username,
					'admin': user.admin,
					'created_at': user.created_at
				}
			}
			return make_response(jsonify(response_object)), 200
		response_object = {
			'status': 'Fail',
			'message': resp
		}
		return make_response(jsonify(response_object)), 401
	else:
		response_object = {
			'status': 'fail',
			'message': 'Provide a valid auth token.'
		}
		return make_response(jsonify(response_object)), 401

@page.route('/api/v1/posts', methods=['GET'])
def get_posts():
	post_user = Post.get_posts_with_user()
	posts_json = [ post.to_json(user) for post, user in post_user ]
	response_object = {
		'posts': posts_json,
		'status': 'Success',
	}
	return make_response(jsonify(response_object)), 200

@page.route('/api/v1/posts', methods=['POST'])
def create_post():
	if not request.json or not 'title' or not 'description' in request.json:
		abort(404)
	post_data = request.get_json()
	auth_user = auth_token_user()
	post = Post.create_element(post_data.get('title'), post_data.get('description'), auth_user.id)
	if post:
		response_object = {
			'post': post.to_json(auth_user),
			'status': 'success',
			'message': 'Post created'
		}
	return make_response(jsonify(response_object)), 200


@page.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
	post_data = request.get_json()
	post = Post.query.get_or_404(post_id)
	auth_user = auth_token_user()
	if post.user_id != auth_user.id:
		abort(401)
	post = Post.update_element(post_data.get('title'), post_data.get('description'), post.id)
	if post:
		return make_response(jsonify({ 'post': post.to_json(auth_user), 'status': 'Success', 'message': 'Updated Successfully' })), 200
	return abort(400)

@page.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	auth_user = auth_token_user()
	if post.user_id != auth_user.id:
		abort(401)
	if Post.delete_element(post.id):
		return make_response(jsonify({ 'status': 'Success', 'message': 'Deleted Successfully'}))
	return abort(404)

