"""Create Word reports for practical works 5 and 6."""

from docx import Document
from docx.shared import Pt
from pathlib import Path


OUT = Path(__file__).parent / "reports"


def report(filename, title, sections):
    document = Document()
    style = document.styles["Normal"]
    style.font.name = "Arial"
    style.font.size = Pt(11)
    document.add_heading(title, 0)
    document.add_paragraph("ФИО: ______________________________________________")
    document.add_paragraph("Группа: ____________________    Преподаватель: ____________________")
    for heading, text in sections:
        document.add_heading(heading, level=1)
        for paragraph in text.split("\n\n"):
            document.add_paragraph(paragraph)
    document.save(OUT / filename)


report("Отчет_ПР5.docx", "Отчёт по практической работе №5\nDjango, HTTP и основы веб-разработки", [
    ("Цель работы", "Освоить создание Django-проекта и приложения, маршрутизацию URL, view-функции и формирование HTML-страниц."),
    ("Выполненная работа", "Созданы manage.py, пакет visitor_project и приложение webapp. В settings.py зарегистрировано приложение, настроены русская локализация, шаблоны и static-файлы. В корневом urls.py подключены маршруты webapp через include()."),
    ("Предметная область", "Страницы системы отображают посетителей, сотрудников, пропуска и посещения. Списки и карточки доступны по именованным URL, а динамические параметры ограничены конвертером <int:...>. Для неизвестного идентификатора возвращается 404."),
    ("Источник данных", "Веб-часть продолжает использовать JSON-файлы data/*.json и классы ПР3 через storage.py. Django ORM, миграции, формы и SQLite на ПР5 не используются согласно методичке."),
    ("HTML, CSS и Bootstrap", "Добавлены главная страница, списки и детали, единое оформление CSS и Bootstrap CDN. Все view используют render(request, template, context)."),
    ("Проверка", "Выполнены команды: python manage.py check; python manage.py test webapp; python -m pytest -v; python -m flake8 . --exclude=.venv. Все проверки проходят."),
    ("Вывод", "Создан рабочий Django-интерфейс учёта посетителей с HTTP-маршрутизацией и отображением данных предметной области."),
])


def create_pr9_fillable_report():
    """Create the PR9 report with explicit places for screenshots and code."""
    document = Document()
    document.styles["Normal"].font.name = "Arial"
    document.styles["Normal"].font.size = Pt(10)
    document.add_heading("Отчёт по практической работе №9", 0)
    document.add_paragraph("Модели Django и Django ORM")
    document.add_paragraph("Образовательная организация: ______________________________________________")
    document.add_paragraph("Дисциплина: Технологии разработки приложений на базе фреймворков")
    document.add_paragraph("Группа: ____________________    ФИО: ____________________    Вариант: __________")

    def placeholder(title, lines=5):
        paragraph = document.add_paragraph()
        run = paragraph.add_run(title)
        run.bold = True
        table = document.add_table(rows=1, cols=1)
        table.style = "Table Grid"
        cell = table.cell(0, 0)
        cell.text = "\n" * lines + "ВСТАВИТЬ СКРИНШОТ ИЛИ ФРАГМЕНТ КОДА ЗДЕСЬ\n\nПодпись: ______________________________________________"
        document.add_paragraph()

    document.add_heading("1. Цель работы", 1)
    document.add_paragraph("Освоить описание сущностей предметной области моделями Django, настройку связей, миграции и операции с базой данных средствами ORM.")
    document.add_heading("2. Выполненные материалы Яндекс Практикума", 1)
    document.add_paragraph("Раздел 05 «База данных и Django ORM»: «Отношения между таблицами» и «Django ORM. Модели».")
    placeholder("Скриншот Яндекс Практикума: раздел «Отношения между таблицами»", 4)
    placeholder("Скриншот Яндекс Практикума: раздел «Django ORM. Модели»", 4)

    document.add_heading("3. Доработка индивидуального проекта", 1)
    document.add_paragraph("В проекте описаны Visitor (аналог Room), Employee (аналог User), AccessPass и Visit (аналог Booking). Реализованы поля CharField, BooleanField, DateField, ограничения max_length, blank, default и choices. Связи ForeignKey используют on_delete=PROTECT и related_name.")
    placeholder("Фрагмент webapp/models.py: модели Visitor, Employee, AccessPass и Visit", 5)
    placeholder("Фрагмент webapp/models.py: ForeignKey, on_delete и related_name", 5)

    document.add_heading("4. Изменение модели и миграции", 1)
    document.add_paragraph("Для демонстрации параметр Visitor.document изменён: max_length с 50 на 80. После изменения созданы и применены миграции командами makemigrations и migrate.")
    placeholder("Фрагмент кода с изменённым max_length", 3)
    placeholder("Скриншот: python manage.py makemigrations webapp", 4)
    placeholder("Скриншот файла webapp/migrations/0002_alter_visitor_document.py", 5)
    placeholder("Скриншот: python manage.py migrate и python manage.py showmigrations", 4)

    document.add_heading("5. Перенос данных и операции ORM", 1)
    document.add_paragraph("Демонстрационные записи перенесены из data/*.json в SQLite командой python manage.py seed_demo. Views используют Model.objects, count(), all(), get_object_or_404(), select_related() и обратные связи.")
    placeholder("Фрагмент webapp/management/commands/seed_demo.py", 5)
    placeholder("Фрагмент webapp/views.py с ORM-запросами", 5)
    placeholder("Скриншот Django Shell: создание, изменение и удаление объекта", 5)

    document.add_heading("6. Проверка проекта", 1)
    document.add_paragraph("☐ python manage.py check    ☐ python manage.py showmigrations    ☐ pytest -v    ☐ flake8 . --extend-exclude=venv")
    placeholder("Скриншот терминала с результатами проверок", 4)

    document.add_heading("7. Git", 1)
    document.add_paragraph("Коммиты ПР9: PR9: add Django ORM models and migrations; PR9: align defense demo and restore card styles.")
    placeholder("Скриншот git log или GitHub с коммитом PR9", 3)

    document.add_heading("8. Результат и вывод", 1)
    document.add_paragraph("В результате модели сущностей описаны средствами Django, связи и миграции настроены, демонстрационные данные перенесены без потери связей, а страницы проекта работают через Django ORM. JSON сохранён как исходный набор для повторяемого импорта.")
    document.add_paragraph("Подпись студента: ____________________    Дата: ______________")
    document.save(OUT / "Отчет_ПР9.docx")


create_pr9_fillable_report()

report("Отчет_ПР6.docx", "Отчёт по практической работе №6\nШаблоны Django", [
    ("Цель работы", "Освоить шаблоны Django: наследование, блоки, include, контекст, циклы, условия, фильтры и static-ресурсы."),
    ("Базовый и дочерние шаблоны", "templates/base.html содержит общую HTML-структуру, навигацию и подключения CSS/JavaScript. Дочерние страницы используют extends и переопределяют блоки title и content."),
    ("Переиспользуемые фрагменты", "Навигация вынесена в templates/includes/navigation.html. Карточка посетителя и статус посещения подключаются через include, поэтому разметка не дублируется."),
    ("Работа с данными", "View передают контекст в render. В шаблонах используются обращение к атрибутам объектов, for/empty, if, фильтры length, default, date и capfirst. Именованные URL namespace webapp формируют ссылки через тег url."),
    ("Static и ошибки", "Подключены Bootstrap, собственный CSS, JavaScript и SVG-иллюстрация через load static/static. Добавлен шаблон 404.html. Некорректные и отсутствующие идентификаторы обрабатываются корректно."),
    ("Ограничения текущего этапа", "JSON остаётся источником данных. ORM, база данных и Django Forms не используются: их изучение относится к следующим практикам."),
    ("Проверка", "Выполнены команды: python manage.py check; python manage.py test webapp; python -m pytest -v; python -m flake8 . --exclude=.venv. В браузере проверены главная, списки, детали и 404."),
    ("Вывод", "Система получила единый адаптивный интерфейс на шаблонах Django с наследованием, компонентами и статическими ресурсами."),
])

'''report("Отчет_ПР9.docx", "Отчёт по практической работе №9\nМодели Django и ORM", [
    ("Цель работы", "Освоить описание сущностей предметной области моделями Django, связи ForeignKey, миграции и CRUD-операции через Django ORM."),
    ("Модели и поля", "В webapp/models.py описаны Visitor, Employee, AccessPass и Visit. Использованы CharField, BooleanField и DateField, ограничения max_length, blank, default, choices и уникальность номера пропуска."),
    ("Связи", "Пропуск связан с посетителем, посещение связано с посетителем, сотрудником и пропуском. Для связей заданы on_delete=PROTECT и related_name. Обратные запросы доступны как visitor.visits, visitor.access_passes и employee.visits."),
    ("Миграции и база", "Создана и применена webapp/migrations/0001_initial.py. Рабочая база — SQLite db.sqlite3. Старый файл предыдущего этапа сохранён как db.sqlite3.pre_pr9.bak."),
    ("Перенос демонстрационных данных", "Команда python manage.py seed_demo читает data/*.json и создаёт связанные записи через ORM. В базу перенесены 3 посетителя, 3 сотрудника, 3 пропуска и 3 посещения."),
    ("ORM в views", "Представления используют Model.objects, count(), all(), get_object_or_404(), select_related() и обратные связи. HTML-шаблоны получают объекты моделей через context."),
    ("Проверка", "Выполнены python manage.py check, python manage.py migrate, python manage.py seed_demo, python manage.py test webapp и python -m pytest -v. Для демонстрации ORM подготовлены команды Django Shell в отдельном файле ответов."),
    ("Вывод", "Веб-приложение переведено на реляционную SQLite-базу и Django ORM с сохранением предметной области и интерфейса предыдущих практик."),
])
'''
