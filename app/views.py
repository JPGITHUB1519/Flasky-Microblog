from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
#importing the app variable of the app/__init__.py
from app import app, db, lm
# importing the wtfform loginform
from .forms import *
from .models import User
import utility
from datetime import datetime
# load user from database
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

# this will run before any request
@app.before_request
def before_request():
	g.user = current_user
	# update the time the last user visited the page
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required  # need been logged to access it!
def index():
	# getting the user logged
	user = g.user
	if not g.user.is_authenticated :
		return redirect(url_for('login'))
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
	""" View For Login User"""
	# # if the user is logged go to the index
	if g.user and g.user.is_authenticated:
		# flask generating url, is better than harcoding
		return redirect(url_for('index'))
	form = LoginForm()
	# if all validations is well it returns true and make the actions
	if form.validate_on_submit():
		user = User.query.filter_by(nickname=form.username.data).first()
		if user:
			if utility.valid_password(form.username.data, form.password.data, user.password):
				user.authenticated = True
				db.session.add(user)
				db.session.commit()
				login_user(user, remember=form.remember_me.data)
				return redirect(request.args.get('next') or url_for('index'))
	return render_template("login.html",
	title="Sign In",
	# sending wtf form
	form=form,
	providers=app.config["OPENID_PROVIDERS"])


@app.route("/logout")
@login_required  # need been logged to access it!
def logout():
	""" View for Logout Users """
	user = current_user
	user.authenticated = False
	db.session.add(user)
	db.session.commit()
	logout_user()
	return redirect(url_for('login'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	""" View for Sign Up a user """
	form = SignUpForm()
	if request.method == "POST" and form.validate():
		user = User(nickname=form.username.data, password=utility.make_password_hash(form.username.data, form.password.data))
		user.authenticated = True
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('index'))
	return render_template("signup.html",
							form = form)

# <nickname> = parameter
@app.route('/user/<nickname>')
@login_required
def user(nickname):
	""" View to Show the user Profile"""
	user = User.query.filter_by(nickname=nickname).first()
	if user == None :
		flash("User %s Not Found" % nickname)
		return redirect(url_for('index'))
	posts = [
		{"author": user, "body" : 'Test Post #1'},
		{"author": user, "body" : 'Test Post #2'},
	]
	return render_template('user.html',
							user = user,
							posts = posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm()
	if request.method == "POST" and form.validate_on_submit:
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash("Your changes has been saved")
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)