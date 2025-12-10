FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем reqs
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY app /app/app

EXPOSE 8000

# Запускаем backend + api + telegram bot
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
