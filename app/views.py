from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
#importing the app variable of the app/__init__.py
from app import app, db, lm
# importing the wtfform loginform
from .forms import *
from .models import User
import utility

# load user from database
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

# this will run before any request
@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
@login_required  # need been logged to access it!
def index():
	# getting the user logged
	user = g.user
	posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
	return render_template("index.html",
							title='Home',
							user=user,
							posts=posts
							)

# this view have get and post methods
@app.route("/login", methods=['GET', 'POST'])
# login view function
# g = place to store and share data during the life of a request.
def login():
	# # if the user is logged go to the index
	# if g.user is not None and g.user.is_authenticated:
	# 	# flask generating url, is better than harcoding
	# 	return redirect(url_for('index'))
	form = LoginForm()
	# if all validations is well it returns true and make the actions
	if form.validate_on_submit():
		user = User.query.filter_by(nickname=form.username.data).first()
		if user:
			if utility.valid_password(form.username.data, form.password.data, user.password):
				login_user(user)
				return redirect(request.args.get('next') or url_for('index'))

	return render_template("login.html",
	title="Sign In",
	# sending wtf form
	form=form,
	providers=app.config["OPENID_PROVIDERS"])

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	if request.method == "POST" and form.validate():
		user = User(nickname=form.username.data, password=utility.make_password_hash(form.username.data, form.password.data))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template("signup.html",
							form = form)