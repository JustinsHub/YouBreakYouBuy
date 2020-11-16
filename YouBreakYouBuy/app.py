import os

from flask import Flask, render_template, redirect, flash, session, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
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