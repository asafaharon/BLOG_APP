from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Message

bp = Blueprint('messages', __name__, url_prefix='/messages')


@bp.route('/send', methods=['GET', 'POST'])
@login_required
def send_message():
    if request.method == 'POST':
        recipient_id = request.form['recipient_id']
        content = request.form['content']

        recipient = User.query.get_or_404(recipient_id)
        message = Message(sender_id=current_user.id, recipient_id=recipient.id, content=content)
        db.session.add(message)
        db.session.commit()

        flash('Message sent successfully!', 'success')
        return redirect(url_for('messages.inbox'))

    users = User.query.filter(User.id != current_user.id).all()
    return render_template('send_message.html', users=users)


@bp.route('/select_recipient')
@login_required
def select_recipient():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('select_recipient.html', users=users)


@bp.route('/inbox')
@login_required
def inbox():
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('inbox.html', messages=messages)


@bp.route('/sent')
@login_required
def sent_messages():
    messages = current_user.sent_messages
    return render_template('sent_messages.html', messages=messages)
