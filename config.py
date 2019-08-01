import os

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host/db_name'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host/db_name'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	TEST = True
	DEBUG = True

config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig,
	'test': TestingConfig
}