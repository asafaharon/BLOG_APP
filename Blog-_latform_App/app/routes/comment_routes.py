from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.models import Comment, Post
from app import db

bp = Blueprint('comment', __name__, url_prefix='/comments')

@bp.route('/add/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    if not content:
        flash('Comment cannot be empty.', 'danger')
        return redirect(url_for('post.post_detail', post_id=post_id))
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    db.session.commit()
    flash('Comment added successfully!', 'success')
    return redirect(url_for('post.post_detail', post_id=post_id))

@bp.route('/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        flash('You do not have permission to delete this comment.', 'danger')
        return redirect(url_for('post.post_detail', post_id=comment.post_id))
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!', 'success')
    return redirect(url_for('post.post_detail', post_id=comment.post_id))