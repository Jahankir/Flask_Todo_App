from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "some secret key"
app.config["MONGO_URI"] = 'mongodb://localhost:27017/test.todo'
mongo = PyMongo(app)

from todo import routes