from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class SignUpForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    first_name = StringField("First Name:", validators=[InputRequired()])
    last_name = StringField("Last Name:", validators=[InputRequired()])
    email = StringField("Email:", validators=[InputRequired(), Email()])

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = StringField("Password:", validators=[InputRequired()])