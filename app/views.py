from app import app
from app.model import *
from flask import render_template
@app.route('/')
def Home():
	posts = Post.query.all()
	return render_template("Home.html", blog_name = "Jack's Blog", posts = posts)