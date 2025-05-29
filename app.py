from app import create_app

# Создаём экземпляр Flask-приложения
app = create_app()

# Запуск
if __name__ == '__main__':
    app.run(debug=True)
