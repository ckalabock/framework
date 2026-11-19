"""Создание простого Word-отчёта по ПР11."""

from pathlib import Path

from docx import Document
from docx.shared import Pt


document = Document()
document.styles["Normal"].font.name = "Arial"
document.styles["Normal"].font.size = Pt(12)
document.add_heading("Отчёт по практической работе №11", 0)
document.add_paragraph("Тема: Формы Django")
document.add_paragraph("ФИО: _____________________________________  Группа: __________")
document.add_heading("Цель работы", 1)
document.add_paragraph("Освоить создание и обработку Form и ModelForm, GET/POST-запросы, валидацию, сохранение объектов и защиту CSRF.")
document.add_heading("Выполненная работа", 1)
for item in (
    "Создана VisitFilterForm для GET-фильтрации посещений.",
    "Создана VisitForm для создания и редактирования посещений.",
    "Настроены labels, widgets и стили полей.",
    "Реализованы проверки даты, пропуска, сотрудника и конфликтующих посещений.",
    "Добавлены вывод ошибок, CSRF-защита и отмена посещения сменой статуса.",
    "Добавлены автоматические тесты форм и пользовательских сценариев.",
):
    document.add_paragraph(item, style="List Bullet")
document.add_heading("Яндекс Практикум", 1)
document.add_paragraph("Вставить скриншоты выполненного спринта «Формы в Django», урок «Работа с формами».")
for title in ("Основные скриншоты", "Дополнительные скриншоты"):
    document.add_paragraph(title).runs[0].bold = True
    table = document.add_table(rows=1, cols=1)
    table.style = "Table Grid"
    table.cell(0, 0).text = "\n\n\n\nВСТАВИТЬ СКРИНШОТЫ ЗДЕСЬ\n\n\n\n"
document.add_heading("Вывод", 1)
document.add_paragraph("Проект дополнен формами Django для фильтрации и безопасного изменения посещений с серверной валидацией.")
document.save(Path(__file__).parent / "reports" / "Отчет_ПР11.docx")
