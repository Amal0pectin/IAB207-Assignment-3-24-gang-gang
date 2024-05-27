from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, unique=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')

    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    location = db.Column(db.String(80))
    genre = db.Column(db.String(10))
    price = db.Column(db.Float)
    numberoftickets = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Open")
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')
    #fk
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    Event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"

class Order(db.Model):
    _tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    ticketsbooked = db.Column(db.Integer)
    
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    Event_id = db.Column(db.Integer, db.ForeignKey('events.id'))