from flask import Flask, render_template, request, url_for, flash, redirect
from db import Session, Post
from sqlalchemy import select
from werkzeug.exceptions import abort
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config["SECRET_KEY"] = f"{getenv('SECRETKEY')}"

@app.get("/")
def index():
    context = dict()
    with Session.begin() as session:
        context["posts"] = session.scalars(select(Post)).all()
        return render_template("index.html", **context)




@app.get("/post/<int:post_id>")
def _id(post_id):
    context = dict()
    with Session.begin() as session:

        context["post"] = session.scalars(select(Post).where(Post.id == post_id)).one()

        if context["post"] is None:
            context["post"] = abort(404)

        return render_template("post.html", **context)


@app.get("/create")
def create_get():
    return render_template('create.html')

@app.post("/create")
def create_post():
    title = request.form.get("title")
    content = request.form.get("content")
    if not title:
        flash("Title is required!!")
    else:
        with Session.begin() as session:
            post1 = Post(title=title, created=datetime.now(), content=content)
            session.add(post1)
        return redirect(url_for('index'))
    return render_template('create.html')


@app.get("/edit/<int:edit_id>")
def edit(edit_id):
    context = dict()
    with Session.begin() as session:
        context["post"] = session.scalars(select(Post).where(Post.id == edit_id)).one()
    
        return render_template('edit.html', **context)

@app.post("/edit/<int:edit_id>")
def edit_post(edit_id):
    title = request.form.get("title")
    content = request.form.get("content")
    with Session.begin() as session:
        post = session.scalars(select(Post).where(Post.id == edit_id)).one()
        post.title = title
        post.content = content
    flash("Post updated successfully")
    return redirect(url_for('index'))

@app.get("/edit/delete/<int:edit_id>")
def delete_post(edit_id):
    with Session.begin() as session:
        post = session.scalars(select(Post).where(Post.id == edit_id)).one()
        if post is None:
            abort(404)
        session.delete(post)
    flash("Post deleted successfully!")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8000)