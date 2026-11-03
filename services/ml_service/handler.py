# ============================================================
# Лабораторная работа №3
# Обработчик предсказаний FastAPIHandler
# ============================================================

from pathlib import Path

import mlflow.pyfunc
import numpy as np
import pandas as pd


# ============================================================
# 1. Пути к сохранённой модели
# ============================================================

MODEL_PATH = (
    Path("/models")
    if Path("/models/MLmodel").exists()
    else Path(__file__).resolve().parent.parent / "models"
)


# ============================================================
# 2. Класс обработчика
# ============================================================

class FastAPIHandler:

    def __init__(self):
        # Загружаем модель один раз при создании обработчика
        self.model = mlflow.pyfunc.load_model(
            str(MODEL_PATH)
        )

    def predict(self, features: dict) -> float:

        # Преобразуем входные данные в DataFrame
        data = pd.DataFrame([features])

        # Числовые признаки
        numeric_columns = [
            "Year",
            "Present_Price",
            "Driven_kms",
            "Car_Age"
        ]

        for column in numeric_columns:
            data[column] = data[column].astype(np.float32)

        # Категориальные признаки
        categorical_columns = [
            "Fuel_Type",
            "Selling_type",
            "Transmission"
        ]

        for column in categorical_columns:
            data[column] = data[column].astype(str)

        # Получаем предсказание
        prediction = self.model.predict(data)

        return float(np.asarray(prediction).reshape(-1)[0])