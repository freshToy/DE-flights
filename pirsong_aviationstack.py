import requests
import pandas as pd
from datetime import datetime
import csv

AVIATIONSTACK_KEY = "e5b74db8bfa1133b55b3d5f812bf6a1b"
BASE_URL = "http://api.aviationstack.com/v1/flights"




def get_flight_data():
    params = {
        "access_key": AVIATIONSTACK_KEY,
        "flight_status": "active",  # Только рейсы в воздухе
        "bbox": "27.5,41.0,41.5,44.5", #не работает, т.к. bbox поддерживается исключительно в платном тарифном плане
        "limit": 100,
        #"flight_date": "2025-04-14"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")
    data = response.json()
    black_sea_flights = []
    # Фильтрация по координатам
    for flight in data["data"]:
        live = flight.get("live", {})
        if live != None:
            longitude = live.get("longitude", 0)
            latitude = live.get("latitude", 0)

            #Проверка условий на акваторию Черного моря
            if all([
                longitude is not None,
                latitude is not None,
                27.5 <= longitude <= 41.0,
                41.5 <= latitude <= 44.5
            ]):
                black_sea_flights.append(flight)

    return black_sea_flights



import csv
from datetime import datetime


def load_csv(flights):
    # Определяем названия столбцов
    fields = [
        "timestamp",
        "model",
        "ICAO",
        "airline",
        "departure_airport",
        "arrival_airport",
        "latitude",
        "longitude",
        "registration"
    ]

    with open("AviationStack.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)

        # Если файл пустой, записываем заголовки
        if f.tell() == 0:
            writer.writeheader()

        for flight in flights:
            try:
                # Формируем строку с данными
                live = flight.get("live", {})
                aircraft = flight.get("aircraft", {})
                departure = flight.get("departure", {})
                arrival = flight.get("arrival", {})

                row = {
                    "timestamp": datetime.fromisoformat(live.get("updated")).strftime('%Y-%m-%d %H:%M:%S')
                    if live.get("updated") else "N/A",
                    "model": aircraft.get("iata", "N/A"),
                    "ICAO": aircraft.get("icao"),
                    "airline": flight.get("airline", {}).get("name", "N/A"),
                    "departure_airport": departure.get("airport", "N/A"),
                    "arrival_airport": arrival.get("airport", "N/A"),
                    "latitude": live.get("latitude", 0.0),
                    "longitude": live.get("longitude", 0.0),
                    "registration": aircraft.get("registration", "N/A")
                }

                # Записываем данные в соответствующие столбцы
                writer.writerow(row)

            except Exception as e:
                print(f"Ошибка обработки рейса: {str(e)}")
                continue



def generate_report():
    try:
        # заголовков
        df = pd.read_csv(
            "AviationStack.csv",
            names=[
                "timestamp",
                "model",
                "ICAO",
                "airline",
                "departure_airport",
                "arrival_airport",
                "latitude",
                "longitude",
                "registration"
            ],
            header=0
        )

        # Преобразование времени
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            errors="coerce",
            format="%Y-%m-%d %H:%M:%S"
        )

        # # Удаление некорректных строк
        # df = df.dropna(subset=["timestamp"])

        # Группировка данных
        def create_report(freq):
            return (
                df.groupby([
                    pd.Grouper(key="timestamp", freq=freq),
                    "model",
                    "airline"
                ])
                .size()
                .reset_index(name="count")
                .sort_values(["timestamp", "count"], ascending=[True, False])
            )

        # Создание отчетов
        hourly = create_report("H")
        daily = create_report("D")

        # Сохранение
        hourly.to_csv("hourly_report.csv", index=False)
        daily.to_csv("daily_report.csv", index=False)

        print("Отчеты успешно сгенерированы!")

    except Exception as e:
        print(f"Ошибка генерации отчета: {str(e)}")




if __name__ == "__main__":
    data_flights = get_flight_data()
    load_csv(data_flights)
    generate_report()
