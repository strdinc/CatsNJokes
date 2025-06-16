import requests
import pytest
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

# 🔧 Конфиг
BASE_URL = "http://catsnjokes.ru/api/jokes"
LOGIN = "admin"
PASSWORD = "adminpass"
DB_PATH = "sqlite:///app.db"

# 🎯 Хелпер
def make_url(endpoint):
    return f"{BASE_URL}{endpoint}/{LOGIN}/{PASSWORD}"

# 🧠 SQLAlchemy setup
engine = create_engine(DB_PATH)
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

joke_table = Table("joke", metadata, autoload_with=engine)

def get_all_jokes_from_db():
    return session.query(joke_table).all()

def get_jokes_by_category_from_db(category):
    return session.query(joke_table).filter(joke_table.c.category == category).all()

def get_unique_categories():
    return session.query(joke_table.c.category).distinct().all()

# ✅ По ID
@pytest.mark.parametrize("joke", get_all_jokes_from_db())
def test_joke_by_id_matches_db(joke):
    joke_id = joke.id
    r = requests.get(make_url(f"/{joke_id}"))
    assert r.status_code == 200
    api_data = r.json()
    assert api_data["id"] == joke.id
    assert api_data["text"] == joke.text
    assert api_data["category"] == joke.category

# 📚 По категориям
@pytest.mark.parametrize("cat_tuple", get_unique_categories())
def test_jokes_by_category_match_db(cat_tuple):
    category = cat_tuple[0]
    db_jokes = get_jokes_by_category_from_db(category)
    r = requests.get(make_url(f"/category/{category}"))
    assert r.status_code == 200
    api_jokes = r.json()

    # 🔄 Сортировка для детерминированности
    api_sorted = sorted(api_jokes, key=lambda x: x["id"])
    db_sorted = sorted(db_jokes, key=lambda j: j.id)

    assert len(api_sorted) == len(db_sorted)

    for api_joke, db_joke in zip(api_sorted, db_sorted):
        assert api_joke["id"] == db_joke.id
        assert api_joke["text"] == db_joke.text
        assert api_joke["category"] == db_joke.category
