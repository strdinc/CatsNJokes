from app import create_app
from app.models import db, Joke

app = create_app()

def input_multiline(prompt="> "):
    print("Введите анекдот. Пустая строка — завершение ввода текста:")
    lines = []
    while True:
        line = input(prompt)
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

with app.app_context():
    while True:
        print("\n=== Новый анекдот ===")

        text = input_multiline()
        if not text.strip():
            print("Пустой анекдот. Пропуск...")
            continue

        category = input("Введите категорию (или 'exit' для выхода): ").strip()
        if category.lower() == 'exit':
            print("Выход...")
            break
        if not category:
            category = "Без категории"

        new_joke = Joke(text=text, category=category)
        db.session.add(new_joke)
        db.session.commit()
        print("Анекдот успешно добавлен!")
