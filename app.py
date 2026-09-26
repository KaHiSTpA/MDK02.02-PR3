import os
import time
from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# --- Читаем ВСЕ настройки из переменных окружения ---
APP_ENV     = os.environ.get('APP_ENV', 'development')
SECRET_KEY  = os.environ.get('SECRET_KEY', 'default-insecure-key')
DEBUG       = os.environ.get('DEBUG', 'False').lower() == 'true'
DATABASE_URL = os.environ.get('DATABASE_URL')

# --- Если DATABASE_URL не задан, собираем вручную ---
if not DATABASE_URL:
    DB_HOST = os.environ.get('DB_HOST', 'db')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_USER = os.environ.get('POSTGRES_USER', 'admin')
    DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'secret')
    DB_NAME = os.environ.get('POSTGRES_DB', 'mydb')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app.config['SECRET_KEY'] = SECRET_KEY
print(f"=== APP_ENV={APP_ENV}, DEBUG={DEBUG}, DB={DATABASE_URL} ===")

Base = declarative_base()

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    message = Column(String(200))

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@app.route('/')
def hello():
    for attempt in range(10):
        try:
            Base.metadata.create_all(engine)
            session = Session()
            session.add(Visit(message=f"Hello from {APP_ENV}!"))
            session.commit()
            count = session.query(Visit).count()
            session.close()
            return f"[{APP_ENV}] Hello, Docker! Записей в базе: {count}"
        except Exception as e:
            print(f"БД пока недоступна (попытка {attempt+1}/10): {e}")
            time.sleep(2)
    return "Не удалось подключиться к базе данных", 500


if __name__ == '__main__':
    # Используем переменные окружения вместо хардкода
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)