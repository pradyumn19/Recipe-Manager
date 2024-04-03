from flask_login import UserMixin
from sqlalchemy.orm import relationship
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Define a constructor to initialize User objects
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # Optional: define __repr__ method for better representation of User objects
    def __repr__(self):
        return f"User('{self.username}')"

    recipes = relationship('Recipe', backref='author', lazy=True)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
