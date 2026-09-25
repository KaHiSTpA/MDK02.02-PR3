import os
import time
from flask import Flask
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# --- 1. Читаем переменные окружения (те, что зададим в compose) ---
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DB', 'postgres')

# --- 2. Формируем строку подключения ---
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- 3. Настраиваем SQLAlchemy ---
Base = declarative_base()

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    message = Column(String(200))

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@app.route('/')
def hello():
    # Пытаемся подключиться к БД, делая до 10 попыток
    # (Postgres может стартовать медленнее, чем Flask)
    for attempt in range(10):
        try:
            Base.metadata.create_all(engine)  # создаём таблицу, если её нет
            session = Session()
            # Добавляем новую запись
            visit = Visit(message="Hello, Docker!")
            session.add(visit)
            session.commit()
            # Считаем, сколько записей всего
            count = session.query(Visit).count()
            session.close()
            return f"Привет из bind mount! Записей: {count}"
        except Exception as e:
            print(f"БД пока недоступна (попытка {attempt+1}/10): {e}")
            time.sleep(2)

    return "Не удалось подключиться к базе данных", 500


if __name__ == '__main__':
    # debug=True включает авто-перезагрузку при изменении кода
    app.run(host='0.0.0.0', port=5000, debug=True)