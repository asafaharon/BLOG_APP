from app.models import Post
from app import db

def create_post(title, content, user):
    post = Post(title=title, content=content, author=user)
    db.session.add(post)
    db.session.commit()
    return post

def update_post(post, title, content):
    post.title = title
    post.content = content
    db.session.commit()
    return post

def delete_post(post):
    db.session.delete(post)
    db.session.commit()