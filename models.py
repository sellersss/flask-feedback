from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class Users(db.Model):
    """Users schema.

    Includes username (PK), password, email, first name, and last name.
    """

    __tablename__ = 'user'

    username = db.Column(db.VARCHAR(20),
                         primary_key=True,
                         nullable=False,
                         unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.VARCHAR(50), nullable=False, unique=True)
    first_name = db.Column(db.VARCHAR(30), nullable=False)
    last_name = db.Column(db.VARCHAR(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Registers a new user.

        Encrypts the password before being stored in database using bcrypt.
        """

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username,
                   password=hashed_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    def authenticate(cls, username, password):
        """Login authentication.

        Authenticates a username and password by checking if the password hash
        is the same as the one stored.
        """

        user = Users.query.filter_by(username=username).one_or_none()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


def connect_db(app):
    db.app = app
    db.init_app(app)
