# 1. Базовый образ
FROM python:3.11-slim

# 2. Рабочая директория
WORKDIR /app

# 3. Копируем файлы приложения
COPY . .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Открываем порт (информативно)
EXPOSE 5000

# 6. Команда запуска
CMD ["python", "app.py"]