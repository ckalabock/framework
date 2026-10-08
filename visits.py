"""Операции с посещениями."""

from datetime import date

from models import AccessPass, Employee, Visit, Visitor


def get_next_visit_id(visits: list[Visit]) -> int:
    """Вернуть следующий свободный идентификатор посещения."""
    return max((visit.visit_id for visit in visits), default=0) + 1


def has_active_visit(
    visits: list[Visit], visitor_id: int, visit_date: date
) -> bool:
    """Проверить, есть ли у посетителя активное посещение на дату."""
    for visit in visits:
        if (
            visit.visitor.visitor_id == visitor_id
            and visit.visit_date == visit_date
            and visit.status == "активно"
        ):
            return True
    return False


def create_visit(
    visits: list[Visit],
    visitor: Visitor,
    employee: Employee,
    access_pass: AccessPass,
    visit_date: date,
    purpose: str,
) -> Visit:
    """Создать посещение, если на эту дату ещё нет активной записи."""
    if has_active_visit(visits, visitor.visitor_id, visit_date):
        raise ValueError("У посетителя уже есть активное посещение на эту дату.")

    visit = Visit(
        get_next_visit_id(visits),
        visitor,
        employee,
        access_pass,
        visit_date,
        purpose,
    )
    visits.append(visit)
    return visit


def get_visit_by_id(visits: list[Visit], visit_id: int) -> Visit | None:
    """Вернуть посещение по идентификатору или None."""
    for visit in visits:
        if visit.visit_id == visit_id:
            return visit
    return None


def cancel_visit(visits: list[Visit], visit_id: int) -> bool:
    """Отменить посещение. Вернуть True, если запись найдена."""
    visit = get_visit_by_id(visits, visit_id)
    if visit is None:
        return False
    visit.cancel()
    return True


def get_visits_for_date(visits: list[Visit], visit_date: date) -> list[Visit]:
    """Вернуть все посещения на выбранную дату."""
    return [visit for visit in visits if visit.visit_date == visit_date]
