
from flask import render_template, flash, redirect
#importing the app variable of the app/__init__.py
from app import app
# importing the wtfform loginform
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname' : "Jean"}
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
def login():
	form = LoginForm()
	# if all validations is well it returns true and make the actions
	if form.validate_on_submit():
		flash("Login Requested for OpenID = %s, remember me = %s" %
			(form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template("login.html",
							title="Sign In",
							# sending wtf form
							form=form,
							providers=app.config["OPENID_PROVIDERS"])