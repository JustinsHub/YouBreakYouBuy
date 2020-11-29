from flask import session

CURRENT_USER = "user_id"
CURRENT_PRODUCT = "product"

def user_login(user):   
    """Log in user."""

    session[CURRENT_USER] = user.id

def user_logout():
    """Logout user."""

    if CURRENT_USER in session:
        del session[CURRENT_USER]

def remove_cart():
    if CURRENT_PRODUCT in session:
        del session[CURRENT_PRODUCT]