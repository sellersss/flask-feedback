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

    username = db.Column(db.String(20),
                         primary_key=True,
                         nullable=False,
                         unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False, unique=True)
    last_name = db.Column(db.String(30), nullable=False, unique=True)
