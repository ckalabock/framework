"""Генерация простого отчёта по ПР9."""

from pathlib import Path

from docx import Document
from docx.shared import Pt


OUT = Path(__file__).parent / "reports" / "Отчет_ПР9.docx"


def main():
    document = Document()
    document.styles["Normal"].font.name = "Arial"
    document.styles["Normal"].font.size = Pt(12)

    document.add_heading("Отчёт по практической работе №9", 0)
    document.add_paragraph("Тема: Модели Django и Django ORM")
    document.add_paragraph("ФИО: ______________________________________________")
    document.add_paragraph("Группа: ____________________    Вариант: __________")

    document.add_heading("Цель работы", 1)
    document.add_paragraph(
        "Освоить создание моделей Django, настройку связей между моделями, "
        "создание миграций и выполнение операций с данными средствами Django ORM."
    )

    document.add_heading("Выполненная работа по проекту", 1)
    items = [
        "В Django-приложении webapp созданы модели Visitor, Employee, AccessPass и Visit.",
        "Для моделей настроены поля CharField, BooleanField и DateField, а также параметры max_length, blank, default и choices.",
        "Между моделями настроены связи ForeignKey. Для связей указаны on_delete=PROTECT и related_name.",
        "Созданы и применены миграции базы данных: 0001_initial.py и 0002_alter_visitor_document.py.",
        "Демонстрационные данные перенесены из JSON-файлов в SQLite командой python manage.py seed_demo.",
        "Представления проекта переведены на Django ORM и используют objects.all(), count(), get_object_or_404() и select_related().",
        "Добавлены тесты ORM, проверяющие страницы, связи между моделями и обработку страницы 404.",
        "Обновлены README, документация ПР9 и инструкция по демонстрации первых пунктов таблицы 7.3.",
    ]
    for item in items:
        document.add_paragraph(item, style="List Bullet")

    document.add_heading("Проверка проекта", 1)
    document.add_paragraph("Выполнены команды:")
    for command in [
        "python manage.py check",
        "python manage.py showmigrations",
        "python manage.py seed_demo",
        "python manage.py test webapp",
        "python -m pytest -v",
        "python -m flake8 .",
    ]:
        document.add_paragraph(command, style="List Bullet")
    document.add_paragraph("Ошибок при проверке проекта не обнаружено.")

    document.add_heading("Яндекс Практикум", 1)
    document.add_paragraph(
        "В этот раздел вставить скриншоты выполненных заданий Яндекс Практикума "
        "по темам «Отношения между таблицами» и «Django ORM. Модели»."
    )
    table = document.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table.cell(0, 0).text = (
        "\n\n\n\n\n"
        "ВСТАВИТЬ СКРИНШОТЫ ЯНДЕКС ПРАКТИКУМА ЗДЕСЬ\n\n"
        "Подпись к скриншоту: ______________________________________________\n\n\n\n\n"
    )
    document.add_paragraph("\n")
    table = document.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table.cell(0, 0).text = (
        "\n\n\n\n\n"
        "МЕСТО ДЛЯ ДОПОЛНИТЕЛЬНЫХ СКРИНШОТОВ\n\n"
        "Подпись к скриншоту: ______________________________________________\n\n\n\n\n"
    )

    document.add_heading("Вывод", 1)
    document.add_paragraph(
        "В ходе работы проект переведён на модели Django и Django ORM. "
        "Созданы связанные модели, миграции применены к SQLite, демонстрационные "
        "данные загружены в базу, а веб-страницы получают данные через ORM."
    )
    document.add_paragraph("Дата: ______________    Подпись: ____________________")
    document.save(OUT)


if __name__ == "__main__":
    main()
