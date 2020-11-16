from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(21), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.Text(21), nullable=False)
    last_name = db.Column(db.Text(21), nullable=False)
    email = db.Column(db.String, nullable=False)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    product_name = db.Column(db.Text, unique=True)
    product_img = db.Column(db.String )
    price = db.Column(db.Integer )
    inventory = db.Column(db.Intege )

class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_and_time = db.Column(db.Datetime, default=datetime.utcnow())

def connect_db(app):
    db.app = app
    db.init_app(app)