from app import create_app
from app import db, User

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from config import config

config_class = config["development"]
app = create_app(config_class)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)


if __name__ == "__main__":
    manager = Manager(app)

    manager.add_command("Shell", Shell(make_context=make_shell_context))
    manager.add_command("db", MigrateCommand)

    @manager.command
    def test():
        import unittest

        tests = unittest.TestLoader().discover("tests")
        unittest.TextTestRunner().run(tests)

    manager.run()

