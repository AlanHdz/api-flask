from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


from .views import page
from .models import User

def create_app(config):
    
	app.config.from_object(config)

	app.app_context().push()

	app.register_blueprint(page)

	with app.app_context():
		db.init_app(app)


	return app