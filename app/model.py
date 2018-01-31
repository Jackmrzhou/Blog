from app import db
from datetime import datetime

class User(db.Model):

	id  = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	passwd = db.Column(db.String(20), unique = False, nullable = False)

	def __repr__(self):
		return "<user {}>".format(self.username)

class Post(db.Model):
	id  = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	content = db.Column(db.Text, nullable = False)
	date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

	category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable = False)
	category = db.relationship("Category", backref = db.backref("posts", lazy = True))

	def __repr__(self):
		return "<Post {}>".format(self.title)

class Category(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), nullable = False)

	def __repr__(self):
		return "<Category {}>".format(self.name)