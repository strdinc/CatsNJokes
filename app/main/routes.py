from . import main
from sqlalchemy.sql import func
from flask import Blueprint, render_template, jsonify, request
from app.models import Joke, Image
from app import db
import random
import datetime

@main.route('/')
def index():
    return render_template('index.html', back_classes=['backButton', 'geologica-light'], forward_classes=['forwardButton', 'geologica-light'])


@main.route('/get_content')
def get_content():
    page = int(request.args.get('page', 0))
    total_items = 15
    jokes_min = 6
    jokes_max = 8

    num_total_jokes = Joke.query.count()
    num_total_images = Image.query.count()

    num_jokes = random.randint(jokes_min, jokes_max)
    num_images = total_items - num_jokes

    jokes = Joke.query.order_by(func.random()).limit(num_jokes).all()
    images = Image.query.order_by(func.random()).limit(num_images).all()

    jokes_data = [{'id': j.id, 'text': j.text} for j in jokes]
    images_data = [{'id': i.id, 'path': i.path} for i in images]

    return jsonify({'jokes': jokes_data, 'images': images_data})


@main.route('/get_categories')
def get_categories():
    categories = db.session.query(Joke.category).distinct().all()
    return jsonify([c[0] for c in categories])


@main.route('/get_category_jokes')
def get_category_jokes():
    category = request.args.get('category')

    total_items = 10
    jokes_max = 7  # не больше 7 анекдотов, чтобы были и коты
    jokes = Joke.query.filter_by(category=category).order_by(func.random()).limit(jokes_max).all()

    jokes_data = [{'id': j.id, 'text': j.text} for j in jokes]

    num_jokes = len(jokes_data)
    num_images = total_items - num_jokes

    images = Image.query.order_by(func.random()).limit(num_images).all()
    images_data = [{'id': i.id, 'path': i.path} for i in images]

    return jsonify({'jokes': jokes_data, 'images': images_data})


@main.route('/get_day_joke')
def get_day_joke():
    today = datetime.date.today()
    seed = int(today.strftime('%Y%m%d'))
    random.seed(seed)
    joke = Joke.query.order_by(func.random()).first()
    return jsonify({'text': joke.text})

@main.route('/health')
def health_check():
    try:
        # Проверка подключения к БД
        db.session.execute('SELECT 1')
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

