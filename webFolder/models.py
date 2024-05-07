from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    price = db.Column(db.Integer)
    day = db.Column(db.String(1000))
    time = db.Column(db.String(1000))
    place = db.Column(db.String(1000))
    link = db.Column(db.String(10000))
    name = db.Column(db.String(1000))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    events = db.relationship('Event')
