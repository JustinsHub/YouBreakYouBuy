from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    '''User information for the app.'''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(21), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False)

    @classmethod
    def signup(cls, username, password, first_name, last_name, email):
        '''Sign up method for User. Hashes password'''

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf-8')
        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)

    @classmethod
    def authenticate(cls, username, password):
        '''Looks for username and password to compare it to the User table information. 
        If it's a match, User is authenticated, else it won't continue unless it's matched correctly.'''

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Product(db.Model):
    '''The product represented on the app.'''
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    product_name = db.Column(db.Text, unique=True)
    product_img = db.Column(db.String)
    price = db.Column(db.Float)
    inventory = db.Column(db.Integer)

    def serialize(self):
        return {"id": self.id,
                "product_name": self.product_name,
                "product_img": self.product_img,
                "price": self.price,
                "inventory": self.inventory
                }           

class Purchase(db.Model):
    '''Users purchases'''
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_and_time = db.Column(db.DateTime, default=datetime.utcnow())
    inventory_count = db.Column(db.Integer)

    inventory = db.relationship('Product', backref='purchases')

def connect_db(app):
    '''Connects database with the app'''
    db.app = app
    db.init_app(app)
    