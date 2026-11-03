# ============================================================
# Лабораторная работа №3
# Загрузка Production-модели из MLflow
# ============================================================

from pathlib import Path

import mlflow


# ============================================================
# 1. Настройки проекта
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

TRACKING_URI = (
    f"sqlite:///{PROJECT_DIR / 'mlflow' / 'mlruns.db'}"
)

MODEL_NAME = "car_price_prediction_model_rebuilt"

MODEL_URI = f"models:/{MODEL_NAME}@Production"

MODEL_PATH = PROJECT_DIR / "services" / "models" / "car_price_model"


# ============================================================
# 2. Подключение к MLflow
# ============================================================

mlflow.set_tracking_uri(TRACKING_URI)

print("Подключение к MLflow:")
print(TRACKING_URI)

print("\nЗагрузка модели:")
print(MODEL_URI)


# ============================================================
# 3. Сохранение модели
# ============================================================

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

mlflow.artifacts.download_artifacts(
    artifact_uri=MODEL_URI,
    dst_path=str(MODEL_PATH.parent)
)

print("\nМодель успешно загружена!")
print("Папка сохранения:", MODEL_PATH.parent)