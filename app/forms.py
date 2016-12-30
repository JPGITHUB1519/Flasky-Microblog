from flask import flash
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, validators
from wtforms.validators import *
from app.models import User
import logging

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

class EditForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	about_me = TextAreaField("about_me", validators=[Length(min=0,max=140)])

	# constructor to receive the actual user nickname
	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

	def validate(self):
		""" overriding this form validate method to check if the user is writing a existing nickname"""
		validated = True
		# hacer validacion interna del formulario
		if not Form.validate(self):
			validated = False
			flash("Error de Formulario")
		# Custom Validations
		# if the users enters the same nickname that him
		if self.nickname.data == self.original_nickname:
			return True
		# look for the nickname in db and if exits throw the error
		user = User.query.filter_by(nickname=self.nickname.data).first()
		if user != None:
			self.nickname.errors.append('This nickname is already in use. Please choose another one.')
			validated = False
		flash(validated)
		return validated

class PostForm(Form):
	post = StringField('post', validators=[DataRequired()])




