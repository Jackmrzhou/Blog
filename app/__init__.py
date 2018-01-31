import sys
import os

sys.path.append(os.path.dirname(__file__))

from flask import Flask
from flask_migrate import Migrate 
from config import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import model,views