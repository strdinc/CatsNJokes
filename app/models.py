from . import db

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # захешированный пароль
    role = db.Column(db.String(20), default='user')  # 'админ' или 'пользователь'

    def __repr__(self):
        return f'<User {self.login}>'

class SuggestedJoke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='модерация')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='suggested_jokes')

    def __repr__(self):
        return f'<SuggestedJoke {self.id} от пользователя {self.user_id}>'

class SuggestedCat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='модерация')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='suggested_images')

    def __repr__(self):
        return f'<SuggestedImage {self.id} от пользователя {self.user_id}>'
