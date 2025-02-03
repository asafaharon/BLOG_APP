from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User
from app import db, bcrypt
from app.services.auth_service import send_reset_email
from flask_login import current_user
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with that email.', 'danger')
    return render_template('reset_request.html')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token. Please request a new password reset.', 'danger')
        print(f"Failed to verify token: {token}")  # לוג לבדיקת הטוקן שהתקבל
        return render_template('reset_request.html')

    if request.method == 'POST':
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            access_token = create_access_token(identity=user.id)
            flash('Login successful!', 'success')
            return redirect(url_for('post.home'))
        else:
            flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.register'))  # הפניה לדף הרישום
