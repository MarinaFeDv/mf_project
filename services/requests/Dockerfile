# Базовый образ с Python 3.10
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем список зависимостей
COPY requirements.txt .

# Устанавливаем библиотеку requests
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт генератора запросов
COPY send_requests.py .

# Команда запуска генератора
CMD ["python", "send_requests.py"]

# Сборка образа из корня проекта:
# docker build -t car-price-requests:1 -f services/requests/Dockerfile services/requests

# Запуск всех сервисов через Docker Compose из корня проекта:
# docker compose -f services/compose.yml up -d

# Запуск генератора запросов отдельным контейнером
# docker run --rm --network services_default -e API_URL=http://ml_service:8000/api/prediction car-price-requests:1