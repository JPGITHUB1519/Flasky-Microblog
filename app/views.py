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

#errors handlers
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	# rollback because session is going to arrive in an invalid state, so we have to roll it back in case a working session is needed for the rendering 
	# of the template for the 500 error.
	db.session.rollback()
	return render_template("500.html"), 500

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
		# make the user follow to himself to see his own post
		db.session.add(user.follow(user))
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
	# passing in the constructor the actual user nickname
	form = EditForm(g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
   	 	g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash("Your changes has been saved")
		return redirect(url_for('edit'))
	elif request.method != "POST":
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)

@app.route("/follow/<nickname>")
@login_required
def follow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user is None :
		flash('User %s not found' % nickname)
		return redirect(url_for('index'))
	if user == g.user :
		flash("You can't Follow yourself!")
		return redirect(url_for('user', nickname=nickname))
	u = g.user.follow(user)
	if u is None :
		flash("Cannot follow " + nickname + ".")
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash("You are now following " + nickname + "!")
	return redirect(url_for('user', nickname=nickname))

@app.route("/unfollow/<nickname>")
@login_required
def unfollow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user is None :
		flash('User %s not found' % nickname)
		return redirect(url_for('index'))
	if user == g.user :
		flash("You can't Follow yourself!")
		return redirect(url_for('user', nickname=nickname))
	u = g.user.unfollow(user)
	if u is None :
		flash("Cannot unfollow " + nickname + ".")
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash("You have stopped following " + nickname + "!")
	return redirect(url_for('user', nickname=nickname))
