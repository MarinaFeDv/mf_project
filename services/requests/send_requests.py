# ============================================================
# Лабораторная работа №4
# Скрипт автоматической отправки запросов к ML-сервису
# ============================================================

import os
import random
import time

import requests


# ============================================================
# 1. Адрес сервиса предсказаний
# ============================================================

# При запуске в Ubuntu используется localhost:8000.
# При запуске через Docker Compose адрес будет задаваться
# переменной окружения API_URL.

API_URL = os.getenv(
    "API_URL",
    "http://localhost:8000/api/prediction"
)


# ============================================================
# 2. Генерация характеристик автомобиля
# ============================================================

def generate_car():

    year = random.randint(2010, 2020)

    car = {
        "Year": float(year),
        "Present_Price": round(random.uniform(3, 25), 2),
        "Driven_kms": float(random.randint(1000, 150000)),
        "Fuel_Type": random.choice(["Petrol", "Diesel", "CNG"]),
        "Selling_type": random.choice(["Dealer", "Individual"]),
        "Transmission": random.choice(["Manual", "Automatic"]),
        "Car_Age": float(2026 - year)
    }

    return car


# ============================================================
# 3. Отправка запроса к сервису
# ============================================================

def send_request(item_id):

    car = generate_car()

    try:
        response = requests.post(
            API_URL,
            params={"item_id": item_id},
            json=car,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        print(f"Автомобиль №{item_id}")
        print(f"Характеристики: {car}")
        print(f"Предсказанная стоимость: {result['predict']}")
        print("-" * 60, flush=True)

    except requests.exceptions.RequestException as error:
        print(
            f"Ошибка при отправке запроса №{item_id}: {error}",
            flush=True
        )


# ============================================================
# 4. Бесконечная отправка запросов
# ============================================================

def main():

    print("Запуск генератора запросов...")
    print(f"Адрес ML-сервиса: {API_URL}", flush=True)

    item_id = 1

    while True:

        send_request(item_id)

        item_id += 1

        # Случайная пауза от 0 до 5 секунд
        delay = random.uniform(0, 5)

        print(
            f"Следующий запрос через {delay:.2f} сек.",
            flush=True
        )

        time.sleep(delay)


# ============================================================
# 5. Точка входа в программу
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print("\nГенератор запросов остановлен.")