from flask import Flask, render_template
from db import Session, Post
from sqlalchemy import select
from werkzeug.exceptions import abort
from datetime import datetime

app = Flask(__name__)


with Session.begin() as session:
    post1 = Post(title="Test", created=datetime.now(), content="MOCK DATA MOCK DATA MOCK DATA")
    session.add(post1)


@app.get("/")
def index():
    with Session.begin() as session:
        posts = session.scalars(select(Post)).all()  
    return render_template("index.html", posts=posts)


@app.get("/<int:post_id>")
def post(post_id):
    with Session.begin() as session:
        post = session.scalars(select(Post).where(Post.id == post_id)).all()
        
    if post is None:
        post = abort(404)
        
    return render_template("post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True, port=8000)