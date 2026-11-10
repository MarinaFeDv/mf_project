# ============================================================
# Лабораторная работа №3
# REST API для предсказания стоимости автомобилей
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel, Field

from handler import FastAPIHandler

import time

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi.responses import Response

# ============================================================
# 1. Создание FastAPI-приложения
# ============================================================

app = FastAPI(
    title="Car Price Prediction API",
    description="Сервис предсказания стоимости автомобилей",
    version="1.0.0"
)

# ============================================================
# Метрики Prometheus
# ============================================================

REQUEST_COUNT = Counter(
    "prediction_requests_total",
    "Total number of prediction requests",
    ["status"]
)

PREDICTION_TIME = Histogram(
    "prediction_duration_seconds",
    "Time spent calculating predictions"
)

PREDICTED_PRICE = Gauge(
    "predicted_car_price",
    "Last predicted car price"
)

# ============================================================
# 2. Схема входных данных
# ============================================================

class CarFeatures(BaseModel):

    Year: float = Field(
        ...,
        description="Год выпуска автомобиля"
    )

    Present_Price: float = Field(
        ...,
        description="Первоначальная стоимость автомобиля"
    )

    Driven_kms: float = Field(
        ...,
        description="Пробег автомобиля"
    )

    Fuel_Type: str = Field(
        ...,
        description="Тип топлива"
    )

    Selling_type: str = Field(
        ...,
        description="Тип продавца"
    )

    Transmission: str = Field(
        ...,
        description="Тип коробки передач"
    )

    Car_Age: float = Field(
        ...,
        description="Возраст автомобиля"
    )


# ============================================================
# 3. Загрузка ML-модели
# ============================================================

handler = FastAPIHandler()


# ============================================================
# 4. Проверка работы сервиса
# ============================================================

@app.get("/")
def home():
    return {"Hello": "World"}


# ============================================================
# 5. Предсказание стоимости автомобиля
# ============================================================

@app.post("/api/prediction")
def predict_car_price(item_id: int, car: CarFeatures):

    # Засекаем время начала предсказания
    start_time = time.perf_counter()

    try:
        # Получаем характеристики автомобиля
        features = car.model_dump()

        # Получаем предсказание модели
        prediction = handler.predict(features)

        # Учитываем успешный запрос
        REQUEST_COUNT.labels(status="success").inc()

        # Сохраняем последнюю предсказанную цену
        PREDICTED_PRICE.set(float(prediction))

        return {
            "item_id": item_id,
            "predict": prediction
        }

    except Exception:
        # Учитываем ошибку предсказания
        REQUEST_COUNT.labels(status="error").inc()
        raise

    finally:
        # Измеряем продолжительность выполнения
        duration = time.perf_counter() - start_time
        PREDICTION_TIME.observe(duration)

# ============================================================
# 6. Метрики для Prometheus
# ============================================================

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain; version=0.0.4; charset=utf-8"
    )