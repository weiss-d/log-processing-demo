# log-processing-demo
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## СТРУКТУРА ПРОЕКТА
```shell
.
├── src
│   └── log_processing_demo
│       ├── database.py  # взаимодействие с БД SQLite
│       ├── __init__.py
│       ├── log_receiver.py  # загрузка и обработка логов
│       ├── __main__.py  # CLI-скрипт
│       └── sort.py  # реализация mergesort
└── tests
    ├── conftest.py
    ├── __init__.py
    ├── test_database.db
    ├── test_database.py
    ├── test_log_receiver.py
    └── test_sort.py
```
## УСТАНОВКА
```shell
$ pip install git+https://github.com/weiss-d/log-processing-demo.git
```

## ЗАПУСК

```
$ python -m log_processing_demo --help
usage: __main__.py [-h] {fetch,show} ...

optional arguments:
  -h, --help    show this help message and exit

commands:
  {fetch,show}
    fetch       Retrieve LOG messages via API for desired date.
    show        Print stored LOG data for selected date and time interval in NDJSON format.
```

### Загрузка логов на заданную дату через API - `fetch`:
```
$ python -m log_processing_demo fetch --help
usage: __main__.py fetch [-h] base_url date_path [db_file]

positional arguments:
  base_url    Base LOG API URL.
  date_path   LOG date in format YYYYMMDD
  db_file     Database file. Default is 'database.db'.

optional arguments:
  -h, --help  show this help message and exit

```
По умолчанию данные сохраняются в файл `database.db` в директории, из-под которой был запущен скрипт. В ту же директорию пишется лог самого скрипта в файл `log_processing_demo.log`.


Пример:
```shell
$ python -m log_processing_demo fetch http://www.dsdev.tech/logs 20210123
```

### Отображение логов на заданную дату и временной интервал в формате NDJSON - `show`:
```
$ python -m log_processing_demo show --help
usage: __main__.py show [-h] [-i INTERVAL] date [db_file]

positional arguments:
  date      Date of LOG messages. Format: YYYY-MM-DD
  db_file   Database file. Default is 'database.db'.

optional arguments:
  -h, --help    show this help message and exit
  -i INTERVAL, --interval INTERVAL
                Time interval. Format: HH:MM:SS-HH:MM:SS
```
Если не указан файл БД, то по умолчанию данные считываются из файла `database.db` в директории, из-под которой был запущен скрипт.


Пример:
```shell
$ python -m log_processing_demo show 2021-01-23 -i 00:00:00-11:00:00
```

## ЗАПУСК ТЕСТОВ
#### Если установлен Poetry
```shell
$ git clone https://github.com/weiss-d/log-processing-demo.git
$ cd log-processing-demo
$ make test
```

#### Без Poetry
```shell
$ git clone https://github.com/weiss-d/log-processing-demo.git
$ cd log-processing-demo
$ python -m venv log_processing_demo_venv
$ source log_processing_demo_venv/bin/activate
$ pip install .  # тесты применяются к уже установленному модулю
$ pip install pytest pytest-mock
$ pytest
```
