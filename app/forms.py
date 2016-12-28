from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, validators
from wtforms.validators import *
from app.models import User

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
		if not Form.validate(self):
			return False

		# if the users enters the same nickname that him
		if self.nickname.data == self.original_nickname:
			return True
		# look for the nickname in db and if exits throw the error
		user = User.query.filter_by(nickname=self.nickname.data).first()
		if user != None:
			self.nickname.errors.append("This Nickname is already in use. Please Choose Another")
			return False
		return True





