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
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'cut_db.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'dcabc46275bceb98bf55e21c'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def index():
    user = current_user
    urls = user.created_urls
    return render_template('index.html', user=user, urls=urls)



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
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))



@app.route('/shorten', methods=['POST'])
@login_required
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

    url = URL(short_code=short_code, long_url=long_url, short_url=short_url, custom_short_url=short_code)
    url.user_id = current_user.id  # Set the user_id attribute to the current user's id

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

        return redirect(url.long_url)
    else:
        return render_template('404.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    urls = URL.query.filter_by(user_id=user.id).order_by(URL.created_at.desc()).all()

    link_data = []
    qr_img_base64 = None

    for url in urls:
        clicks = url.get_clicks()
        click_count = len(clicks)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url.long_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img_base64 = generate_qr_code_data_url(qr_img)

        link_data.append({
            'url': url,
            'click_count': click_count
        })

    return render_template('dashboard.html', user=user, link_data=link_data, qr_img_base64=qr_img_base64)


@app.route('/dashboard/all')
@login_required
def dashboard_all():
    user = current_user
    urls = URL.query.filter_by(user_id=user.id).order_by(URL.created_at.desc()).all()

    link_data = []
    qr_img_base64 = None

    for url in urls:
        clicks = url.get_clicks()
        click_count = len(clicks)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url.long_url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img_base64 = generate_qr_code_data_url(qr_img)

        link_data.append({
            'url': url,
            'click_count': click_count
        })

    return render_template('dashboard_all.html', user=user, link_data=link_data, qr_img_base64=qr_img_base64)

from flask import send_file, make_response

# ...

@app.route('/dashboard/download/<int:url_id>')
@login_required
def download_qr_code(url_id):
    url = URL.query.get_or_404(url_id)

    if url.user_id != current_user.id:
        flash('You are not authorized to download this QR code.', 'error')
        return redirect(url_for('dashboard'))

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url.long_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_img_io = BytesIO()
    qr_img.save(qr_img_io, format='PNG')
    qr_img_io.seek(0)

    response = make_response(send_file(qr_img_io, mimetype='image/png'))
    response.headers.set('Content-Disposition', 'attachment', filename='qr_code.png')
    return response


@app.route('/dashboard/delete/<int:url_id>', methods=['POST'])
@login_required
def delete_url(url_id):
    url = URL.query.get_or_404(url_id)

    if url.user_id != current_user.id:
        flash('You are not authorized to delete this URL.', 'error')
        return redirect(url_for('dashboard_all'))

    db.session.delete(url)
    db.session.commit()

    flash('URL deleted successfully.', 'success')
    return redirect(url_for('dashboard_all'))


@app.route('/dashboard/edit/<int:url_id>', methods=['GET', 'POST'])
@login_required
def edit_url(url_id):
    url = URL.query.get_or_404(url_id)

    if url.user_id != current_user.id:
        flash('You are not authorized to edit this URL.', 'error')
        return redirect(url_for('dashboard_all'))

    if request.method == 'POST':
        long_url = request.form['long_url']
        url.long_url = long_url
        db.session.commit()
        flash('URL updated successfully.', 'success')
        return redirect(url_for('dashboard_all'))

    return render_template('edit_url.html', url=url)

  

if __name__ == '__main__':
    app.run()
