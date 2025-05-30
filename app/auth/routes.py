from . import auth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, session
from app.models import User



@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.login
            session['role'] = user.role
            return redirect(url_for('auth.profile'))
        else:
            error = 'Неверный логин или пароль'

    return render_template('login.html', error=error)

@auth.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('profile.html', username=session['user'], role=session.get('role'))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

