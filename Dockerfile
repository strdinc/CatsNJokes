# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Открываем порт 5000
EXPOSE 5000

# Запускаем Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]