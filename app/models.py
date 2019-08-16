import datetime
import jwt

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from . import db, app


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_passord = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    admin = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship("Post", lazy="dynamic")

    def verify_password(self, password):
        return check_password_hash(self.encrypted_passord, password)

    def to_json(self):
        return {
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
            "admin": self.admin,
        }

    def encode_auth_token(self, user_id):
        """
            Generates the Auth Token
            :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=10, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            :param auth_token
            :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"))
            return payload["sub"]
        except jwt.ExpiredSignature:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    @property
    def password(self):
        pass

    @password.setter
    def password(self, value):
        self.encrypted_passord = generate_password_hash(value)

    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def create_element(cls, username, password, email):
        """
            Create user with class method
            :return: User object
        """
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def __str__(self):
        return self.username


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def to_json(self, user):
        return {
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "user": {"username": user.username},
        }

    @classmethod
    def get_posts_with_user(cls):
        posts = db.session.query(Post, User).join(User)
        return posts

    @classmethod
    def get_by_id(cls, id):
        post = Post.query.filter_by(id=id).first()
        return post

    @classmethod
    def create_element(cls, title, description, user_id):
        post = Post(title=title, description=description, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def update_element(cls, title, description, post_id):
        post = Post.get_by_id(post_id)
        if post is None or title is None or description is None:
            return False
        post.title = title
        post.description = description
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def delete_element(cls, post_id):
        post = Post.get_by_id(post_id)
        if post is None:
            return False
        db.session.delete(post)
        db.session.commit()
        return True

    def __str__(self):
        return self.username
