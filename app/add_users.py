from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Добавим пользователя, если нужно
    if not User.query.filter_by(login='admin').first():
        admin = User(
            name='Администратор',
            login='admin',
            password=generate_password_hash('adminpass'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Админ добавлен')
    else:
        print('Админ уже существует')
