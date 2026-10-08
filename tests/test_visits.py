"""Тесты операций с посещениями."""

from datetime import date

import pytest

from models import AccessPass, Employee, Visitor
from visits import cancel_visit, create_visit, has_active_visit


def test_second_active_visit_for_same_date_is_rejected() -> None:
    """Нельзя создать две активные записи одного посетителя на одну дату."""
    visitor = Visitor(1, "Иванов Иван", "4510 123456")
    employee = Employee(1, "Петров Пётр", "Кадры")
    access_pass = AccessPass(1, "A-101", visitor, date(2027, 1, 1))
    visits = []
    create_visit(visits, visitor, employee, access_pass, date(2026, 10, 8), "Встреча")

    with pytest.raises(ValueError):
        create_visit(
            visits, visitor, employee, access_pass, date(2026, 10, 8), "Повтор"
        )


def test_cancelled_visit_does_not_block_new_visit() -> None:
    """После отмены на ту же дату можно создать новую запись."""
    visitor = Visitor(1, "Иванов Иван", "4510 123456")
    employee = Employee(1, "Петров Пётр", "Кадры")
    access_pass = AccessPass(1, "A-101", visitor, date(2027, 1, 1))
    visits = []
    first_visit = create_visit(
        visits, visitor, employee, access_pass, date(2026, 10, 8), "Встреча"
    )

    assert cancel_visit(visits, first_visit.visit_id)
    assert not has_active_visit(visits, visitor.visitor_id, date(2026, 10, 8))

    second_visit = create_visit(
        visits, visitor, employee, access_pass, date(2026, 10, 8), "Повтор"
    )

    assert second_visit.visit_id == 2
