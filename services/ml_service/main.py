# ============================================================
# Лабораторная работа №3
# REST API для предсказания стоимости автомобилей
# ============================================================

from fastapi import FastAPI
from pydantic import BaseModel, Field

from handler import FastAPIHandler


# ============================================================
# 1. Создание FastAPI-приложения
# ============================================================

app = FastAPI(
    title="Car Price Prediction API",
    description="Сервис предсказания стоимости автомобилей",
    version="1.0.0"
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

    # Получаем характеристики автомобиля
    features = car.model_dump()

    # Получаем предсказание модели
    prediction = handler.predict(features)

    return {
        "item_id": item_id,
        "predict": prediction
    }