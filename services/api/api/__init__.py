from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
CORS(app)


from api import routes
