<img alt="Flask" src="https://img.shields.io/badge/Flask-3.1.1-orange"/>
<img alt="gunicorn" src="https://img.shields.io/badge/gunicorn-23.0.0-purple"/>
<img alt="Jinja2" src="https://img.shields.io/badge/Jinja2-3.1.6-red"/>
<img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-2.0.41-blueviolet"/>
<img alt="Werkzeug" src="https://img.shields.io/badge/Werkzeug-3.1.3-lightblue"/>


# CatsNJokes

***CatsNJokes*** — это веб-приложение на Flask, представляющее собой сайт с анекдотами и котами


## Структура проекта

- `app/`: основной код приложения
  - `/main`: главная страница
  - `/auth`: защищенная часть приложения
  - `/api`: API
  - `/static`: статические файлы: изображения, js, css
  - `/templates`: шаблоны страниц

    
- `main.py`: точка входа приложения.
- `requirements.txt`: список зависимостей Python.


- `certs/`: SSL-сертификаты для безопасного соединения (HTTPS)


- `docker-compose.yml`: конфигурация для запуска приложения с Docker.
- `Dockerfile`: инструкции для создания Docker-образа.
- `nginx.conf`: конфигурация для Nginx.

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/strdinc/CatsNJokes
   cd CatsNJokes
   pip install -r requirements.txt
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
3. Запустите приложение:
   ```bash
   python main.py
   
Приложение будет доступно по адресу http://localhost:5000

## Docker

### Запустите контейнер
   ```bash
   docker-compose up --build
   ```
или для версиё 3.4+

```bash
docker compose up --build
```