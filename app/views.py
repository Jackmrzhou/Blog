from app import app
from app.model import *
from flask import render_template,redirect, flash, request, send_from_directory
from app import forms
from flask_login import current_user, login_user, logout_user, login_required
from markdown import markdown
from util import convert_to_html
import os

@app.route('/')
def Home():
	return render_template("Home.html")

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static/pics'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/login', methods=["GET", "POST"])
def login():

	if current_user.is_authenticated:
		return redirect("/manage")

	form = forms.SigninForm()

	if form.is_submitted():
		if form.validate():
			user = User.query.filter_by(username = form.username.data).first()
			if user:
				if form.password.data == user.passwd:
					login_user(user)	
					return redirect('/manage')
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
				content = form.content.data, 
				category = Category.query.filter_by(name = form.category.data).first(),
				content_type = "Markdown" if form.is_md.data else "PlainText")
			db.session.add(p)
			db.session.commit()
			return redirect("/")

	return render_template("write.html", form = form, type = "Post")

@app.route("/edit/<id>", methods = ["GET", "POST"])
@login_required
def edit(id):
	form = forms.PostForm()
	opt = [(c.name, c.name) for c in Category.query.all()]
	form.category.choices = opt
	if form.is_submitted():
		if form.validate():
			p = Post.query.filter_by(id = int(id)).first()
			p.title = form.title.data
			p.content = form.content.data
			p.category = Category.query.filter_by(name = form.category.data).first()
			p.content_type = "Markdown" if form.is_md.data else "PlainText"

			db.session.commit()
			#update the post
			return redirect("/p/"+str(id))
	return render_template("write.html", form = form, type = "Update")

@app.route("/logout")
def logout():
	logout_user()
	return redirect("/")

@app.route("/p/<post_id>")
def post(post_id):
	return render_template("post.html")

@app.route("/Category")
def category():
	return render_template("Category.html", Category = Category.query.all())

@app.route("/AboutMe")
def aboutme():
	return render_template("AboutMe.html")

@app.route("/manage", methods=["POST", "GET"])
@login_required
def manage():
	form = forms.ManageForm()
	if form.validate_on_submit():
		f = request.form.to_dict()
		for k in f:
			if  f[k] == 'Delete':
				try:
					p = Post.query.filter_by(id=int(k.split('-')[1])).first()
					db.session.delete(p)
					db.session.commit()
				except:
					pass#QAQ
	return render_template("manage.html", form = form, posts = Post.query.all())