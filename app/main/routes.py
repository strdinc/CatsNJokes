from . import main
from sqlalchemy.sql import func
from flask import Blueprint, render_template, jsonify, request
from app.models import Joke, Image
from app import db
import random

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

    # Случайный выбор из базы данных
    jokes = Joke.query.order_by(func.random()).limit(num_jokes).all()
    images = Image.query.order_by(func.random()).limit(num_images).all()

    # Приводим к словарям
    jokes_data = [
        {'id': j.id, 'text': j.text}
        for j in jokes
    ]
    images_data = [
        {'id': i.id, 'path': i.path}
        for i in images
    ]

    return jsonify({'jokes': jokes_data, 'images': images_data})

@main.route('/vote/<int:joke_id>/<action>', methods=['POST'])
def vote(joke_id, action):
    joke = Joke.query.get_or_404(joke_id)
    if action == 'like':
        joke.likes += 1
    elif action == 'dislike':
        joke.dislikes += 1
    db.session.commit()
    return jsonify({'rating': joke.likes - joke.dislikes})
