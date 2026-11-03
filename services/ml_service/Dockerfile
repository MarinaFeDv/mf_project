FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY main.py /app/main.py
COPY handler.py /app/handler.py

EXPOSE 8000

# Сборка из папки services/ml_service:
# sudo docker build -t car-price-api:1 .

# Запуск с подключением модели:
# sudo docker run --rm -p 8001:8000 \
#   -v "$(pwd)/../models:/models:ro" car-price-api:1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]