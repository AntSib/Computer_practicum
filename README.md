## Компьютерный практикум

# Лабораторная работа №5

Структура проекта:
    ЛР-5<br>
    └── Part1/<br>
        ├── flask/<br>
        │   ├── config.py           # Файл конфигурации<br>
        │	└── flask_server.py     # Файл приложения<br>
        ├── http_server/<br>
        │   └── [http_server.py](Part1/http_server/http_server.py)      # Файл веб-сервиса<br>
        Part2/<br>
        ├── db/<br>
        │   ├── [logtable.db](Part2/db/logtable.db)         # База данных sqlite<br>
        │   └── [logger.json](Part2/db/logger.json)         # Файл журнала<br>
        ├── flask/<br>
        │   ├── templates/          # Директория шаблонов<br>
        │   │   ├── [form.html](Part2/flask/templates/form.html)       # Шаблон формы<br>
        │   │   └── [base.html](Part2/flask/templates/base.html)       # Шаблон ответа<br>
        │   ├── [app.py](Part2/flask/app.py)              # Файл настройки приложения<br>
        │   ├── [config.py](Part2/flask/config.py)           # Файл конфигурации<br>
        │	├── [main.py](Part2/flask/main.py)             # Основной файл приложения<br>
        │	├── [models.py](Part2/flask/models.py)           # Файл моделей дополнительного функционала (коннектор к базе данных)<br>
        │	└── [view.py](Part2/flask/view.py)             # Файл вьюшек<br>
        └── http_server/<br>
            ├── [connector.py](Part2/http_server/connector.py)        # Файл коннектора к базе данных<br>
            └── [main.py](Part2/http_server/main.py)             # Основной файл веб-сервиса
