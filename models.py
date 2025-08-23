from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    stall_id = db.Column(db.Integer, db.ForeignKey('stall.id'), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    notes = db.relationship('Note', backref='user', lazy=True)

class Stall(db.Model, UserMixin):
    __tablename__ = "stall"

    id = db.Column(db.Integer, primary_key=True)
    stallname = db.Column(db.String(150), unique=True, nullable=False)
    stallowner = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    openhour = db.Column(db.Time, nullable=True)
    closehour = db.Column(db.Time, nullable=True)

    notes = db.relationship('Note', backref='stall', lazy=True)