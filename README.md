# Система учёта посетителей

Учебный проект на Python и Django для учёта посетителей, сотрудников, пропусков и посещений.

## Практические работы №5–6

Веб-часть выполнена по методичкам ПР5 и ПР6:

- данные берутся из JSON-файлов `data/` и объектной модели `models.py` (ПР3);
- Django ORM, SQLite-база, Django Forms, авторизация и веб-формы создания записей **на этих работах не используются**;
- ПР5: Django-проект и приложение, настройки, маршрутизация, view-функции, списки и карточки, динамические URL и 404;
- ПР6: `base.html`, наследование, include-навигация, контекст, циклы и условия, фильтры, namespace URL, CSS, SVG и JavaScript.

## Запуск

```powershell
python -m pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Страницы

- `/` — главная и количество записей;
- `/visitors/`, `/visitors/1/` — посетители и карточка посетителя;
- `/employees/`, `/employees/1/` — сотрудники и карточка сотрудника;
- `/passes/` — пропуска;
- `/visits/`, `/visits/1/` — посещения и их карточки.

Идентификатор в URL должен быть числом: `/visitors/abc/` не совпадает с маршрутом, а `/visitors/999999/` возвращает 404, если записи нет.

## Структура веб-части

```text
visitor_project/settings.py  # DEBUG, INSTALLED_APPS, шаблоны и static
visitor_project/urls.py      # корневой URLconf, include("webapp.urls")
webapp/urls.py               # app_name, имена и динамические маршруты
webapp/views.py              # загрузка JSON, context, render, Http404
templates/base.html          # базовый шаблон
templates/includes/          # подключаемая навигация
templates/webapp/            # дочерние шаблоны списков и карточек
static/webapp/               # CSS, JavaScript и SVG
```

## Проверка

```powershell
python manage.py check
python manage.py test webapp
python -m pytest -v
python -m flake8 .
```

Консольная версия запускается командой `python main.py`. Для ПР5–6 источником данных является `data/*.json`; `db.sqlite3` от прежней версии не используется.

Подробные отчёты и сценарии демонстрации находятся в папке `docs/`.
