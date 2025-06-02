from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Joke
import os
from werkzeug.utils import secure_filename
from app import db
from app.models import SuggestedCat, User
from flask import request, redirect, url_for, session, flash, render_template
from . import auth
import uuid

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg.jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

    role = session.get('role')
    categories = db.session.query(db.distinct(Joke.category)).all()
    categories = [c[0] for c in categories]

    if role == 'admin':
        return render_template('admin_profile.html',
                               username=session['user'],
                               categories=categories)
    else:
        return render_template('user_profile.html',
                               username=session['user'],
                               categories=categories)


@auth.route('/suggest_image', methods=['POST'])
def suggest_image():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    file = request.files.get('cat_image')
    if file and allowed_file(file.filename):
        original_filename = file.filename
        extension = original_filename.rsplit('.', 1)[1].lower()

        # Генерация безопасного имени файла
        safe_name = secure_filename(original_filename)
        if not safe_name:
            safe_name = f"{uuid.uuid4().hex}.{extension}"

        save_path = os.path.join(UPLOAD_FOLDER, safe_name)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(save_path)

        user = User.query.filter_by(login=session['user']).first()
        new_image = SuggestedCat(
            image_path=save_path,
            user_id=user.id,
            status='модерация'
        )
        db.session.add(new_image)
        db.session.commit()

        flash('Изображение успешно отправлено на модерацию!', 'success')
    else:
        flash('Файл не выбран или имеет недопустимый формат.', 'error')

    return redirect(url_for('auth.profile'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Проверка на пустые поля
        if not name or not username or not password or not confirm_password:
            error = 'Пожалуйста, заполните все поля.'
        elif password != confirm_password:
            error = 'Пароли не совпадают.'
        elif User.query.filter_by(login=username).first():
            error = 'Пользователь с таким логином уже существует.'
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, login=username, password=hashed_password, role='user')
            from app import db
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

    return render_template('register.html', error=error)
