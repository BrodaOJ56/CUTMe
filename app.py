from flask import Flask, render_template, request, redirect, session, url_for, flash
from io import BytesIO
import random
import string
import qrcode
import base64

import os
from PIL import Image
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'cut_db.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'dcabc46275bceb98bf55e21c'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        flash('Logged in successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    short_code = request.form.get('custom_short_url')

    if not short_code:
        short_code = generate_short_code()
    else:
        existing_url = URL.query.filter_by(short_code=short_code).first()
        if existing_url:
            flash('Custom short URL already exists.', 'error')
            return redirect(url_for('index'))

    short_url = request.host_url + short_code

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        url = URL(short_code=short_code, long_url=long_url, short_url=short_url, custom_short_url=short_code)
        url.created_by = user
    else:
        url = URL(short_code=short_code, long_url=long_url, short_url=short_url, custom_short_url=short_code)

    db.session.add(url)
    db.session.commit()

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url.long_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_base64 = generate_qr_code_data_url(qr_img)

    return render_template('shortened.html', short_url=url.short_url, qr_img_base64=qr_img_base64, url=url)


def generate_qr_code_data_url(qr_img):
    qr_img_byte_array = BytesIO()
    qr_img.save(qr_img_byte_array, format='PNG')
    qr_img_byte_array.seek(0)
    qr_img_base64 = base64.b64encode(qr_img_byte_array.read()).decode('utf-8')
    return qr_img_base64


def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    if URL.query.filter_by(short_code=short_code).first():
        return generate_short_code()
    return short_code


@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        # Create analytics record
        analytics = Analytics(url_id=url.id, timestamp=datetime.now(), user_agent=request.user_agent.string)
        db.session.add(analytics)
        db.session.commit()

        clicks = url.get_clicks()  # Retrieve the clicks associated with the URL
        return render_template('shortened.html', url=url, clicks=clicks)
    else:
        return render_template('404.html'), 404



if __name__ == '__main__':
    app.run()
