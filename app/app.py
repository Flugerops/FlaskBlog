from flask import Flask, render_template
from db import Session, Post
from sqlalchemy import select
from werkzeug.exceptions import abort
from datetime import datetime

app = Flask(__name__)


with Session.begin() as session:
    post1 = Post(title="Test id 1", created=datetime.now(), content="MOCK DATA MOCK DATA MOCK DATA")
    session.add(post1)
    post2 = Post(title="Test id 2", created=datetime.now(), content="MOCK DATA MOCK DATA MOCK DATA")
    session.add(post2)

@app.get("/")
def index():
    context = dict()
    with Session.begin() as session:
        context["posts"] = session.scalars(select(Post)).all()
        return render_template("index.html", **context)


@app.get("/<int:post_id>")
def post(post_id):
    context = dict()
    with Session.begin() as session:
        
        context["post"] = session.scalars(select(Post).where(Post.id == post_id)).one()
        
        if context["post"] is None:
            context["post"] = abort(404)
        
        return render_template("post.html", **context)

if __name__ == "__main__":
    app.run(debug=True, port=8000)