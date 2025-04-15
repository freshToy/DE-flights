# DE-flights
data parsing with AviationStack  
Задача:  
 Написать сервис/скрипт, который загружает данные с FlightRadar24. Для
мониторинга возьми акваторию Чёрного моря. Загруженные данные по рейсам
должны обязательно содержать позывной, код ICAO, модель самолёта,
принадлежность к авиакомпании, а также маршрутные данные, позволяющие
рассчитать маршрут полёта. Остальные данные загружай на своё усмотрение.  
Данные сохранить в:  
 файлы csv;  
 Написать сервис/скрипт, который наполняет спроектированные таблицы/файлы.  
 Создать витрину данных/отчётность, которая подсчитывает количество рейсов по
моделям самолётов и авиакомпаниям в заданной акватории за час/день.  
 Реализовать запуска проекта:  
 Сформировать venv и файл requirements.txt

### CSV-файл
Структура файла `flights.csv`:
- **Столбцы**:
  - `timestamp` (datetime): Время записи данных.
  - `model` (str): Модель самолета.
  - `icao_code` (str): Код ICAO самолета.
  - `airline` (str): Авиакомпания.
  - `departure_airport` (str): Аэропорт вылета.
  - `arrival_airport` (str): Аэропорт назначения.
  - `latitude` (float): Широта.
  - `longitude` (float): Долгота.
  - `registration` (str): Регистрационный номер самолета.

  - ### CSV-отчеты
Файлы `daily_report.csv` и `hourly_report.csv` содержат агрегированные данные:
- `timestamp` (datetime): Дата/час.
- `model` (str): Модель самолета.
- `airline` (str): Авиакомпания.
- `count` (int): Количество рейсов.
