from app.models import Comment
from app import db

def add_comment(content, user, post):
    comment = Comment(content=content, author=user, post=post)
    db.session.add(comment)
    db.session.commit()
    return comment

def delete_comment(comment):
    db.session.delete(comment)
    db.session.commit()