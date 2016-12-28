# this file is used to run the web application
# importing the app variable of the app/__init__.py
from app import app
# debug mode to see errors. do no deploy the app in debug mode
app.run(debug=True)