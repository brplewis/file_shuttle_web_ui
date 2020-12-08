"""Data models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    account_type = db.Column(
        db.String(6),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Launcher(db.Model):
    """Data model for launch_centre instances."""
    __tablename__ = 'launch_centre'
    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )
    name = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    root_folder = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    assigned_apis = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    def __repr__(self):
        return '<launch_centre {}>'.format(self.id)

class Api(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'api'
    id = db.Column(
        db.Integer,
        primary_key=True,
        auto_increment=True
    )
    email = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )
    api_string = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return '<support_ticket {}>'.format(self.id)


