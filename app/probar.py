from app import app, db
# importing the wtfform loginform
from .forms import *
from .models import User, Post
import flask_whooshalchemy as whooshalchemy

print Post.query.whoosh_search('post').all()