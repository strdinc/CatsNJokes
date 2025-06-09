from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Joke, SuggestedJoke, Image
import os
from werkzeug.utils import secure_filename
from app import db
from app.models import SuggestedCat, User
from flask import request, redirect, url_for, session, flash, render_template
from . import auth
import uuid
from flask import jsonify
import shutil
import re

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

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

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        save_path = os.path.join(UPLOAD_FOLDER, safe_name)
        file.save(save_path)

        relative_path = os.path.join('uploads', safe_name).replace('\\', '/')

        user = User.query.filter_by(login=session['user']).first()
        new_image = SuggestedCat(
            image_path=relative_path,
            user_id=user.id,
            status='модерация'
        )
        db.session.add(new_image)
        db.session.commit()

        flash('Изображение успешно отправлено на модерацию!', 'success')
    else:
        flash('Файл не выбран или имеет недопустимый формат.', 'error')

    return redirect(url_for('auth.profile'))


@auth.route('/suggest_joke', methods=['POST'])
def suggest_joke():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    joke_text = request.form.get('text')
    joke_category = request.form.get('category')

    if not joke_text or not joke_category:
        flash('Необходимо заполнить текст анекдота и выбрать категорию.', 'error')
        return redirect(url_for('auth.profile'))

    user = User.query.filter_by(login=session['user']).first()
    if not user:
        flash('Пользователь не найден.', 'error')
        return redirect(url_for('auth.login'))

    new_joke = SuggestedJoke(
        text=joke_text,
        category=joke_category,
        status='модерация',
        user_id=user.id
    )
    db.session.add(new_joke)
    db.session.commit()

    flash('Анекдот отправлен на модерацию!', 'success')
    return redirect(url_for('auth.profile'))

@auth.route('/get_suggested_jokes')
def get_suggested_jokes():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.filter_by(login=session['user']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    jokes = (
        SuggestedJoke.query
        .filter_by(user_id=user.id)
        .order_by(SuggestedJoke.id.desc())
        .all()
    )

    jokes_data = [
        {
            'status': j.status,
            'text': j.text
        }
        for j in jokes
    ]

    return jsonify({'jokes': jokes_data})


@auth.route('/get_suggested_cats')
def get_suggested_cats():
    if 'user' not in session:
        return jsonify({'cats': []})

    page = request.args.get('page', 1, type=int)
    per_page = 4
    user = User.query.filter_by(login=session['user']).first()

    cats_paginated = SuggestedCat.query.filter_by(user_id=user.id) \
        .order_by(SuggestedCat.id.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    cats_data = [
        {
            'status': cat.status,
            'image_path': cat.image_path.replace('static/', '').replace('\\', '/')
        }
        for cat in cats_paginated.items
    ]

    return jsonify({'cats': cats_data})

# Получить все анекдоты на модерации
@auth.route('/admin/get_suggested_jokes')
def get_admin_suggested_jokes():
    jokes = SuggestedJoke.query.filter_by(status='модерация').all()
    data = [{
        'id': joke.id,
        'text': joke.text,
        'category': joke.category,
        'user_id': joke.user_id
    } for joke in jokes]
    return jsonify(data)


# Отклонить анекдот
@auth.route('/admin/deny_joke/<int:joke_id>', methods=['POST'])
def deny_joke(joke_id):
    joke = SuggestedJoke.query.get_or_404(joke_id)
    joke.status = 'отклонён'
    db.session.commit()
    return jsonify({'success': True})


# Принять анекдот и перенести в основную таблицу
@auth.route('/admin/approve_joke/<int:joke_id>', methods=['POST'])
def approve_joke(joke_id):
    joke = SuggestedJoke.query.get_or_404(joke_id)
    new_joke = Joke(text=joke.text, category=joke.category)
    db.session.add(new_joke)
    joke.status = 'принят'
    db.session.commit()
    return jsonify({'success': True})

@auth.route('/admin/get_suggested_cats')
def admin_get_suggested_cats():
    cats = SuggestedCat.query.filter_by(status='модерация').all()
    result = []
    for cat in cats:
        result.append({
            'id': cat.id,
            'image_path': cat.image_path,
            'user_id': cat.user_id
        })
    return jsonify(result)

@auth.route('/moderate_cat', methods=['POST'])
def moderate_cat():
    data = request.json
    cat_id = data['id']
    action = data['action']  # "принять" или "отклонить"

    cat = SuggestedCat.query.get_or_404(cat_id)

    if action == 'принять':
        cat.status = 'принят'

        source_path = os.path.join('app', 'static', cat.image_path)
        file_name = os.path.basename(cat.image_path)
        destination_dir = os.path.join('app', 'static', 'CatsImages')
        destination_path = os.path.join(destination_dir, file_name)

        os.makedirs(destination_dir, exist_ok=True)
        shutil.copyfile(source_path, destination_path)

        new_image = Image(path=file_name)
        db.session.add(new_image)

    elif action == 'отклонить':
        cat.status = 'отклонён'

    db.session.commit()
    return jsonify({'success': True})

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
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

    user_agent = request.headers.get('User-Agent')
    if is_mobile(user_agent):
        return render_template('register_mobile.html')
    else:
        return render_template('register.html')

def is_mobile(user_agent):
    mobile_keywords = ['Mobile', 'Android', 'iPhone', 'iPad', 'Windows Phone']
    if user_agent:
           return any(keyword in user_agent for keyword in mobile_keywords)
    return False