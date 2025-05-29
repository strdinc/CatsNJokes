import pandas as pd
from app import create_app, db  # замените your_project на имя корневой папки (где __init__.py)
from app.models import Joke     # путь до модели Joke

# Создание приложения и контекста
app = create_app()

# Чтение CSV-файла
df = pd.read_csv("filtered_jokes.csv")

# Очистка текста от лишних кавычек и пробелов
df["text"] = df["text"].apply(lambda x: str(x).replace('"', '').strip())

# Добавление анекдотов в базу данных
with app.app_context():
    for _, row in df.iterrows():
        joke = Joke(
            text=row["text"],
            category=row["theme"],
            likes=0,
            dislikes=0
        )
        db.session.add(joke)
    db.session.commit()

print("Анекдоты успешно загружены в базу данных.")
