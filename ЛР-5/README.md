## Компьютерный практикум

# Лабораторная работа №5

Структура проекта:
ЛР-5
└── Part1/
    ├── flask/
    │   ├── [config.py](Part1/flask/config.py)           # Файл конфигурации
    │	└── [flask_server.py](Part1/flask/flask_server.py)     # Файл приложения
    ├── http_server/
    │   └── [http_server.py](Part1/http_server/http_server.py)      # Файл веб-сервиса
    Part2/
    ├── db/
    │   ├── [logtable.db](Part2/db/logtable.db)         # База данных sqlite
    │   └── [logger.json](Part2/db/logger.json)         # Файл журнала
    ├── flask/
    │   ├── templates/          # Директория шаблонов
    │   │   ├── [form.html](Part2/flask/templates/form.html)       # Шаблон формы
    │   │   └── [base.html](Part2/flask/templates/base.html)       # Шаблон ответа
    │   ├── [app.py](Part2/flask/app.py)              # Файл настройки приложения
    │   ├── [config.py](Part2/flask/config.py)           # Файл конфигурации
    │	├── [main.py](Part2/flask/main.py)             # Основной файл приложения
    │	├── [models.py](Part2/flask/models.py)           # Файл моделей дополнительного функционала (коннектор к базе данных)
    │	└── [view.py](Part2/flask/view.py)             # Файл вьюшек
    └── http_server/
        ├── [connector.py](Part2/http_server/connector.py)        # Файл коннектора к базе данных
        └── [main.py](Part2/http_server/main.py)             # Основной файл веб-сервиса
