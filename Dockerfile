FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY bot/ ./bot/

# Запуск
WORKDIR /app/bot
CMD ["python", "main.py"]
