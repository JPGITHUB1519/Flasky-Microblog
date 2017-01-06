import os
basedir = os.path.abspath(os.path.dirname(__file__))
# database configuration
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
	{"name" : "Google", "url" : "https://www.google.com/accounts/o8/id"},
	{"name" : "Yahoo", "url" : "https://me.yahoo.com"},
	{"name" : "AOL", "url" : "http://openid.aol.com/<username>"},
	{"name" : "Flickr", "url" : "http://www.flickr.com/<username>"},
	{"name" : "MyOpenId", "url" : "https://www.myopenid.com"}
]

# mail server settings
# MAIL_SERVER = 'localhost'
# MAIL_PORT = 25
# MAIL_USERNAME = None
# MAIL_PASSWORD = None

# # administrator list
# ADMINS = ['juanpedro1519@gmail.com']

# How much post to show in the main page
POSTS_PER_PAGE = 3

# full text searcher config
WHOOSH_BASE = os.path.join(basedir, "search.db")

# max whoosh searcher result
MAX_SEARCH_RESULTS = 50

# Email config

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = 'juanpedro1519@gmail.com'
MAIL_PASSWORD = 'jp23051519'


# administrator list
ADMINS = ['juanpedro1519@gmail.com']
