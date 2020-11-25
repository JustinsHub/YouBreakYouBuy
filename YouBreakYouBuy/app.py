import os

from flask import Flask, render_template, redirect, session, flash, jsonify, url_for, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Product, Purchase
from forms import SignUpForm, LoginForm, ProductForm, PurchaseForm
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

#####***** For User session *****#####

@app.before_request
def add_user_to_g():
    """If we're logged in, add user_id to Flask global.
        Must execute before do_login"""
    
    if CURRENT_USER in session:
        g.user = User.query.get(session[CURRENT_USER])

    else:
        g.user = None

#####***** Home route *****#####

@app.route('/', methods=["GET", "POST"])
def home():
    '''Home with add to cart post method. Saves product in session when added to cart'''
    products = Product.query.all()
    form = ProductForm()
    if "product_id" not in session:
        flash('Your shopping cart is empty.')
        return render_template('cart.html')
    if form.validate_on_submit():
        for product in products:
            session["product"] = product.serialize()
            return redirect(url_for('view_cart'))
    return render_template('home.html', products=products, form=form)


#####***** User sign up/login form *****#####

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
            flash(f'You are now logged in as {user.username}!', 'success')
            return redirect('/profile')
        flash('Invalid Username/Password', 'danger')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    '''Handle the logout for user.'''
    user_logout()
    flash('Successfully logged out.', 'success')
    return redirect('/')

#####***** User Information *****#####

@app.route('/profile')
def user_page():
    '''Users information page. Must login to access.'''
    if g.user:
        user = g.user
        return render_template('users/users-page.html', user=user)
    else:
        flash('Unauthorized. Must login to have access.', 'danger')
        return redirect(url_for('login'))

@app.route('/profile/<int:id>/edit', methods=["GET","POST"])
def edit_user(id):
    '''Edit user profile with authentication/authorization.'''
    user = User.query.get_or_404(id)
    form = SignUpForm(obj=user)
    if g.user:
        if form.validate_on_submit():
            if User.authenticate(form.username.data, form.password.data):
                user.username = form.username.data
                user.first_name = form.first_name.data
                user.last_name = form.last_name.data
                user.email = form.email.data
                db.session.commit()
                return redirect(url_for('user_page')) 
            else:
                form.password.errors = ['Incorrect password.']
    else:
        flash('Unauthorized. Must login to have access.', 'danger')
        return redirect(url_for('login'))
    return render_template('users/edit-user.html', user=user, form=form)


#####***** Shopping Cart *****######

@app.route('/cart')
def view_cart():
    '''Viewing the shopping cart'''
    if "product" in session:
        return render_template('cart/cart.html', product= session["product"])
    return render_template('cart/cart.html')

@app.route('/remove_cart_item')
def remove_item():
    '''Deleted current product saved in session'''
    if "product" in session:
        del session["product"]
        return redirect(url_for('view_cart'))

######***** Checkout *****######

@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    '''Check out the product to be able to purchase'''
    form = PurchaseForm()
    return render_template('cart/checkout.html', form=form) #database purchases commit / get and post ids?

@app.route('/refund')
def refund_policy():
    '''Refund template page'''
    return render_template('cart/refund.html')