from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	# relation with posts
	# to get user.posts member that gets us the list of posts from the user
	# backref to get post.author
	posts = db.relationship("Post", backref="author", lazy="dynamic")

	# flask login needs this methos for handling authentication
	@property
	# # neccesary to flask-login
	#returns True if the user has provided valid credentials
	def is_authenticated(self):
		return True

	@property
	# neccesary to flask-login
	# returns True if the user's account is active
	def is_active(self):
		return True

	@property
	# neccesary to flask-login
	# returns True if the current user is an anonymous user
	def is_anonymous(self):
		return False
	# neccesary to flask-login
	# returns the unique ID for that object
	def get_id(self):
		try :
			return unicode(self.id) # python2
		except NameError:	
			return str(self.id) # python 3

	# for prints objects for debugging
	def __repr__(self):
		return "<User %r>" % (self.nickname)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	# foreign key
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

	def __repr__(self):
		return "<Post %r>" % (self.body)