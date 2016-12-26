#importing the app variable of the app/__init__.py
from app import app

@app.route('/')
@app.route('/index')
def index():
	return "Hello World"