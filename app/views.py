from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
#importing the app variable of the app/__init__.py
from app import app, db, lm, oid
# importing the wtfform loginform
from .forms import LoginForm
from .models import User

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
@oid.loginhandler
def login():
	# if the user is logged go to the index
	if g.user is not None and g.user.is_authenticated:
		# flask generating url, is better than harcoding
		return redirect(url_for('index'))
	form = LoginForm()
	# if all validations is well it returns true and make the actions
	if form.validate_on_submit():
		# session -> object will be available during that request and any future requests made by the same client
		# Flask keeps a different session container for each client of our application.
		session['remember_me'] = form.remember_me.data
		# trigger authentication
		return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
		return redirect('/index')
	return render_template("login.html",
							title="Sign In",
							# sending wtf form
							form=form,
							providers=app.config["OPENID_PROVIDERS"])

@oid.after_login
# when users authenticad it comes to here else return to the same form
def after_login(resp):
	# resp information returned from openid
	# if emails is invalid go to index
	if resp.email is None or resp.email == "":
		flash('Invalid Login. Please Try Again')
		return redirect(url_for('login'))
	# look for the user in the database, if exits log it! else save it into database and log it!
	user = User.query.filter_by(email=resp.email).first()
	if user is None :
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	# login it
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))