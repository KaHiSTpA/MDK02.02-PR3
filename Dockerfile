# ============================================
# ЭТАП 1: BUILD
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================
# ЭТАП 2: RUNTIME — минимальный финальный образ
# ============================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Копируем готовые библиотеки из builder'а
COPY --from=builder /install /usr/local

# Создаём непривилегированного пользователя
RUN useradd -m -s /bin/bash appuser

# Копируем код и сразу отдаём права appuser'у
COPY --chown=appuser:appuser app.py .

# Переключаемся на appuser — все команды ниже и CMD выполняются от него
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]