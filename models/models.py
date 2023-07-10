from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from flask_login import UserMixin
from . import db



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)  
    password = db.Column(db.Text, nullable=False)
    created_urls = db.relationship('URL', backref='created_by', foreign_keys='URL.user_id')

    def __init__(self, username, password):
        self.username = username
        self.password = password




class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(6), unique=True, nullable=False)
    long_url = db.Column(db.String)
    short_url = db.Column(db.String)
    custom_short_url = db.Column(db.String)  # Add custom_short_url attribute
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    clicks = db.relationship('Analytics', backref='url', lazy='dynamic')

    def get_clicks(self):
        return self.clicks.all()

    def __init__(self, short_code, long_url, short_url, custom_short_url):
        self.short_code = short_code
        self.long_url = long_url
        self.short_url = short_url
        self.custom_short_url = custom_short_url  # Initialize custom_short_url attribute


class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = Column(Integer, primary_key=True)
    url_id = Column(String, ForeignKey('urls.id'))
    timestamp = Column(DateTime)
    user_agent = Column(String)
