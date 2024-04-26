from flask import Flask
from flask_pymongo import PyMongo
from os import environ
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()


app.config["MONGO_URI"] = environ.get('MONGO_URI')
# setup 
db_client = PyMongo(app)
db = db_client.db

# stripe config
app.config['STRIPE_PUBLIC_KEY'] = environ.get('STRIPE_PUBLIC_KEY')
app.config['STRIPE_SECRET_KEY'] = environ.get('STRIPE_SECRET_KEY')
