import os

from flask import Flask, render_template, redirect, flash, session, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Product, Purchase
from forms import SignUpForm, LoginForm
from secrets import backup_default

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///YouBreakYouBuy'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', backup_default)
toolbar = DebugToolbarExtension(app)

connect_db(app)

CURRENT_USER = "user_id"

@app.before_request
def add_user_to_g():
    """If we're logged in, add user_id to Flask global.
        Must execute before do_login"""
    
    if CURRENT_USER in session:
        g.user = User.query.get(session[CURRENT_USER])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURRENT_USER] = user.id

def do_logout():
    """Logout user."""

    if CURRENT_USER in session:
        del session[CURRENT_USER]

##### Home route #####

@app.route('/')
def home():
    return render_template('home.html')


##### User sign up/login form #####

@app.route('/signup', methods=["GET", "POST"])
def signup():
    '''Signup/register the user.'''
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.signup(username=form.username.data,
                            password=form.password.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            email=form.email.data,
                            )
        db.session.add(user)
        db.session.commit()
        do_login(user)
        return redirect('/')              
    return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    '''Handle the login for user.'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, 
                                password=form.password.data)
        do_login(user)
        return redirect('/')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    '''Handle the logout for user.'''
    do_logout()
    return redirect('/')