import os

from flask import Flask, render_template, redirect, flash, session, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_required
from models import db, connect_db, User, Product, Purchase
from forms import SignUpForm, LoginForm
from functions import user_login, user_logout, CURRENT_USER
from secrets import backup_default

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///YouBreakYouBuy'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', backup_default)
toolbar = DebugToolbarExtension(app)

connect_db(app)

##### Login/Authorization helper #####
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

##### For User session #####

@app.before_request
def add_user_to_g():
    """If we're logged in, add user_id to Flask global.
        Must execute before do_login"""
    
    if CURRENT_USER in session:
        g.user = User.query.get(session[CURRENT_USER])

    else:
        g.user = None

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
        user_login(user)
        return redirect('/')              
    return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    '''Handle the login for user.'''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, 
                                password=form.password.data)
        if user:                       
            user_login(user)
            return redirect('/')
        flash('Invalid Username/Password', 'danger')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    '''Handle the logout for user.'''
    user_logout()
    flash('Successfully logged out.', 'success')
    return redirect('/')

##### User Information #####
@app.route('/users')
@login_required
def user_page():
    '''Users information page'''
    user = g.user
    return render_template('users/users-page.html', user=user)