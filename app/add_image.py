import os
import shutil
from app import create_app, db
from app.models import Image

# Папки
source_folder = os.path.join(os.path.dirname(__file__), 'ImagesTo')
destination_folder = os.path.join(os.path.dirname(__file__), 'CatsImages')
os.makedirs(destination_folder, exist_ok=True)

# Создаём Flask-приложение
app = create_app()

with app.app_context():
    added_count = 0

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.jpg.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
            src = os.path.join(source_folder, filename)
            dest = os.path.join(destination_folder, filename)

            # Копируем файл
            shutil.copy2(src, dest)

            # Путь, сохраняемый в БД
            db_path = os.path.join('static/CatsImages', filename)

            # Проверка на дубликаты
            existing = Image.query.filter_by(path=db_path).first()
            if existing:
                print(f"Пропущено (уже в БД): {filename}")
                continue

            # Добавление в БД
            new_image = Image(path=db_path, likes=0, dislikes=0)
            db.session.add(new_image)
            added_count += 1

    db.session.commit()
    print(f"Добавлено {added_count} изображений в БД.")
