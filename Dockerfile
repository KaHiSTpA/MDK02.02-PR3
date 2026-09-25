# ============================================
# ЭТАП 1: BUILD — устанавливаем зависимости
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Устанавливаем компиляторы, нужные для сборки psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements — так кэш Docker не сломается при правке app.py
COPY requirements.txt .

# Ставим зависимости в отдельную папку /install
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Этап тестов ----------
FROM builder AS tester
COPY app.py .
# Простейшая проверка: приложение импортируется без ошибок
RUN python -c "import app; print('OK: app imports successfully')"

# ============================================
# ЭТАП 2: RUNTIME — минимальный финальный образ
# ============================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Копируем ТОЛЬКО готовые библиотеки из builder'а
COPY --from=builder /install /usr/local

# Копируем сам код приложения
COPY app.py .

# Создаём непривилегированного пользователя (безопасность)
RUN useradd -m appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]