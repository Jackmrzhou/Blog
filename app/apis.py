from app import app
from app.model import Post, Comment
from flask import jsonify, request
from app import db
@app.route("/api/p/<id>")
def post_api(id):
	p = Post.query.filter_by(id = int(id)).first()
	if p:
		return jsonify({"status":1,
			"id" : p.id,
			"title" : p.title,
			"content" : p.content,
			"date" : p.date,
			"content_type" : p.content_type,
			"category": p.category.name})
	return jsonify({"status":0})

@app.route("/api/batch")
def batch():
	o = request.args.get('o', 1, type = int)
	posts = Post.query.order_by(db.desc(Post.id)).paginate(o, 4, False) #4 posts per batch
	if posts:
		return jsonify(
			{
				"status":1,
				"posts" : [
							{"id": p.id, 
							"title":p.title, 
							"content":p.content, 
							"date": p.date,
							"content_type" : p.content_type}
								for p in posts.items],
				"next" : posts.has_next
			})
	return jsonify({"status":0})

@app.route("/api/c/<id>")
def comments(id):
	cs = Post.query.filter_by(id = int(id)).first().comments
	if cs:
		return jsonify({
				"status" : 1,
				"comments" :[
					{
						"id":c.id,
						"name":c.name,
						"content":c.content,
						"content_type":c.content_type
					} for c in cs 
				]
			})
	return jsonify({"status":0})