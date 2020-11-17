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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
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
        return redirect('/')              
    return render_template('users/signup.html', form=form)