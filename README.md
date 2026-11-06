# Система учёта посетителей организации

Учебный сквозной проект на Python: консольная часть ПР1–ПР3 и веб-интерфейс Django для ПР5–ПР6.

## Что реализовано в ПР5–ПР6 и ПР9

- Django-проект `visitor_project` и приложение `webapp`;
- страницы `/`, `/visitors/`, `/employees/`, `/passes/`, `/visits/` и карточки с числовыми идентификаторами;
- JSON остаётся источником данных: используются классы из `models.py` и загрузчики `storage.py`;
- шаблоны Django с `extends`, `block`, `include`, контекстом, циклами, `empty`, условиями и фильтрами;
- именованные URL с namespace `webapp`, конвертеры `<int:...>` и собственная страница 404;
- Bootstrap, CSS, JavaScript и SVG-логотип/иллюстрация через `{% load static %}`.
- ПР9: модели Django `Visitor`, `Employee`, `AccessPass`, `Visit`, связи `ForeignKey`, миграции и ORM-запросы;
- рабочая SQLite-база `db.sqlite3` и команда `python manage.py seed_demo` для переноса демонстрационных JSON-записей;
- ORM views с `select_related()`, `get_object_or_404()` и обратными связями.

В ПР5–ПР6 источником данных был JSON. Начиная с ПР9 веб-views работают через Django ORM и SQLite. Консольная часть ПР1–ПР3 по-прежнему использует JSON.

## Установка и запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Проверки

```powershell
python manage.py test webapp
python -m pytest -v
python -m flake8 .
```

Для наполнения базы демонстрационными записями:

```powershell
python manage.py migrate
python manage.py seed_demo
```

Консольная версия запускается командой `python main.py`.

## Документы

- [Описание ПР5](docs/ПР5_описание.md)
- [Описание ПР6](docs/ПР6_описание.md)
- [Описание ПР9](docs/ПР9_описание.md)
- [Ответы на первые 10 показателей ПР5 и ПР6](docs/Ответы_первые_10_показателей_ПР5_ПР6.md)
- [Ответы на первые 7 показателей таблицы 7.3 ПР9](docs/Ответы_ПР9_таблица_7_3_первые_7.md)
- Word-отчёты находятся в `reports/`.

Для защиты откройте файлы, указанные в сценарии ответов, и последовательно покажите страницы в браузере.
