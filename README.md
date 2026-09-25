# Multi-container Flask + PostgreSQL + pgAdmin

Демонстрация оркестрации через Docker Compose.

## Запуск

1. Скопируйте `.env.example` в `.env` и заполните значения:
   ```bash
   cp .env.example .env
   ```

2. Запустите все сервисы:
   ```bash
   docker compose up -d --build
   ```

3. Откройте:
   - Flask-приложение: http://localhost:5000
   - pgAdmin: http://localhost:8080

## Сервисы

- **web** — Flask-приложение (порт 5000)
- **db** — PostgreSQL 15 (порт 5432, только внутри сети Docker)
- **pgadmin** — веб-интерфейс для БД (порт 8080)