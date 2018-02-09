from app import app
from app.model import *
from flask import render_template,redirect, flash
from app import forms
from flask_login import current_user, login_user, logout_user, login_required
from markdown import markdown
from uti import convert_to_html

@app.route('/')
def Home():
	posts = Post.query.all()
	return render_template("Home.html", posts = posts)

@app.route('/login', methods=["GET", "POST"])
def login():

	if current_user.is_authenticated:
		return redirect("/")

	form = forms.SigninForm()

	if form.is_submitted():
		if form.validate():
			user = User.query.filter_by(username = form.username.data).first()
			if user:
				if form.password.data == user.passwd:
					login_user(user)	
					return redirect('/write')
				else:
					flash('Password is not correct!')
					return redirect('/login')
			else:
				flash('Username not found!')
				return redirect('/login')
		else:
			flash('Username and Password must between 6 and 20!')
			return redirect('/login')
	return render_template('login.html',
		form = form)

@app.route('/write', methods=["GET", "POST"])
@login_required
def write():
	form = forms.PostForm()
	opt = [(c.name, c.name) for c in Category.query.all()]
	form.category.choices = opt
	if form.is_submitted():
		if form.validate():
			p = Post(title = form.title.data, 
				content = markdown(form.content.data) if form.is_md.data else convert_to_html(form.content.data), 
				category = Category.query.filter_by(name = form.category.data).first())
			db.session.add(p)
			db.session.commit()
			return redirect("/")

	return render_template("write.html", form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect("/")

@app.route("/p/<post_id>")
def post(post_id):
	return render_template("post.html", post = Post.query.filter_by(id = int(post_id)).first())

@app.route("/Category")
def category():
	return render_template("Category.html", Category = Category.query.all())

@app.route("/AboutMe")
def aboutme():
	return render_template("AboutMe.html")