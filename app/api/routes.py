from . import api
from flask import request, jsonify, abort
from werkzeug.security import check_password_hash
from app.models import db, User, Joke, SuggestedJoke, SuggestedCat, Image

def authenticate(login, password):
    user = User.query.filter_by(login=login).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

@api.route('/jokes/<login>/<password>', methods=['GET'])
def get_all_jokes(login, password):
    if not authenticate(login, password):
        return jsonify({'error': 'Unauthorized'}), 401

    jokes = Joke.query.all()
    result = [{'id': j.id, 'text': j.text, 'category': j.category} for j in jokes]
    return jsonify(result)

@api.route('/jokes/<int:joke_id>/<login>/<password>', methods=['GET'])
def get_joke_by_id(joke_id, login, password):
    if not authenticate(login, password):
        return jsonify({'error': 'Unauthorized'}), 401

    joke = Joke.query.get(joke_id)
    if not joke:
        return jsonify({'error': 'Joke not found'}), 404

    return jsonify({'id': joke.id, 'text': joke.text, 'category': joke.category})

@api.route('/jokes/category/<category>/<login>/<password>', methods=['GET'])
def get_jokes_by_category(category, login, password):
    if not authenticate(login, password):
        return jsonify({'error': 'Unauthorized'}), 401

    jokes = Joke.query.filter_by(category=category).all()
    result = [{'id': j.id, 'text': j.text, 'category': j.category} for j in jokes]
    return jsonify(result)