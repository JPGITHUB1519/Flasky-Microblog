from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import *

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default = False)

class SignUpForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
	confirm_password = StringField('confirm_password', validators=[DataRequired()])
