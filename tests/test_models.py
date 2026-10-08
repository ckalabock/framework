"""Тесты классов предметной области."""

from datetime import date

from models import AccessPass, Employee, Visitor, Visit


def test_access_pass_is_valid_on_expiry_date() -> None:
    """Пропуск действует включительно по дату окончания."""
    visitor = Visitor(1, "Иванов Иван", "4510 123456")
    access_pass = AccessPass(1, "A-101", visitor, date(2027, 1, 1))

    assert access_pass.is_valid_on(date(2027, 1, 1))


def test_visit_is_allowed_for_valid_pass_and_available_employee() -> None:
    """Посещение разрешено при действующем пропуске и сотруднике на месте."""
    visitor = Visitor(1, "Иванов Иван", "4510 123456")
    employee = Employee(1, "Петров Пётр", "Кадры", True)
    access_pass = AccessPass(1, "A-101", visitor, date(2027, 1, 1))
    visit = Visit(1, visitor, employee, access_pass, date(2026, 10, 8), "Встреча")

    assert visit.is_allowed()


def test_cancelled_visit_is_not_allowed() -> None:
    """Отменённое посещение не может быть допущено."""
    visitor = Visitor(1, "Иванов Иван", "4510 123456")
    employee = Employee(1, "Петров Пётр", "Кадры")
    access_pass = AccessPass(1, "A-101", visitor, date(2027, 1, 1))
    visit = Visit(1, visitor, employee, access_pass, date(2026, 10, 8), "Встреча")

    visit.cancel()

    assert not visit.is_allowed()
