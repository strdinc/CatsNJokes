<img alt="alembic" src="https://img.shields.io/badge/alembic-1.16.1-blue"/>
<img alt="blinker" src="https://img.shields.io/badge/blinker-1.9.0-green"/>
<img alt="click" src="https://img.shields.io/badge/click-8.2.1-yellow"/>
<img alt="colorama" src="https://img.shields.io/badge/colorama-0.4.6-red"/>
<img alt="Flask" src="https://img.shields.io/badge/Flask-3.1.1-orange"/>
![Flask-Migrate](https://img.shields.io/badge/Flask--Migrate-4.1.0-lightgrey)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-3.1.1-blueviolet)
![greenlet](https://img.shields.io/badge/greenlet-3.2.2-brightgreen)
![gunicorn](https://img.shields.io/badge/gunicorn-23.0.0-purple)
![itsdangerous](https://img.shields.io/badge/itsdangerous-2.2.0-lightblue)
![Jinja2](https://img.shields.io/badge/Jinja2-3.1.6-red)
![Mako](https://img.shields.io/badge/Mako-1.3.10-yellowgreen)
![MarkupSafe](https://img.shields.io/badge/MarkupSafe-3.0.2-lightgrey)
![numpy](https://img.shields.io/badge/numpy-2.2.6-blue)
![packaging](https://img.shields.io/badge/packaging-25.0-orange)
![pandas](https://img.shields.io/badge/pandas-2.2.3-lightblue)
![python-dateutil](https://img.shields.io/badge/python--dateutil-2.9.0.post0-brightgreen)
![pytz](https://img.shields.io/badge/pytz-2025.2-green)
![six](https://img.shields.io/badge/six-1.17.0-yellow)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-blueviolet)
![tomli](https://img.shields.io/badge/tomli-2.2.1-red)
![typing_extensions](https://img.shields.io/badge/typing__extensions-4.13.2-purple)
![tzdata](https://img.shields.io/badge/tzdata-2025.2-orange)
![Werkzeug](https://img.shields.io/badge/Werkzeug-3.1.3-lightblue)


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