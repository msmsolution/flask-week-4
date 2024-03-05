from flask import render_template
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.forms import RegistrationForm
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import redirect, url_for, flash, request
from urllib.parse import urlsplit

# Home page route
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Stephen'}
    posts = [
        {
            'author': { 'username': 'Stephen'},
            'body': 'I am a software engineer!'
        },
        {
            'author': { 'username': 'Victor'},
            'body': 'I am a data scientist!'
        }
    ]
    return render_template('index.html', title='Home Page', posts = posts)
# About page route
@app.route('/about')
def about():
    return render_template('about.html', title='About')

# Contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Logout page route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)