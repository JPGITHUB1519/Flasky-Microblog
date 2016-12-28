from app import db
from hashlib import md5

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	# relation with posts
	# to get user.posts member that gets us the list of posts from the user
	# backref to get post.author
	posts = db.relationship("Post", backref="author", lazy="dynamic")
	about_me = db.Column(db.String(40))
	last_seen = db.Column(db.DateTime)

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

	def avatar(self, size):
		# d -> placeholder for image, s = pixel of images
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	@staticmethod
	def make_unique_nickname(nickname):
		""" Suggest a new nickname if the passed on the parameter exits """
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True :
			new_nickname = new_nickname + str(version)
			if user.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	# foreign key
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

	def __repr__(self):
		return "<Post %r>" % (self.body)