from app import db
from hashlib import md5


""" 
Since this is an auxiliary table that has no data other than the foreign keys,
we use the lower level APIs in flask-sqlalchemy to create the table without an associated model
"""
followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

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

	followed = db.relationship('User',
								secondary=followers,
								primaryjoin=(followers.c.follower_id == id),
								secondaryjoin=(followers.c.followed_id == id),
								backref=db.backref('followers', lazy='dynamic'),
								lazy='dynamic')

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
		user = User.query.filter_by(nickname=nickname).first()
		if user is None:
			return user.nickname
		version = 2
		while True :
			new_nickname = user.nickname + str(version)
			if user.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname

	# follow stuffs. its return an object and this object has to be commited
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		# return query object not the result
		return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())



class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	# foreign key
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

	def __repr__(self):
		return "<Post %r>" % (self.body)
