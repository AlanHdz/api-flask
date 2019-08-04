import os

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:lol123@localhost/api_flask'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:lol123@localhost/api_flask_test'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEST = True
	DEBUG = True

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig,
	'test': TestingConfig
}