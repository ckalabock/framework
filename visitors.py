"""Операции с коллекцией посетителей."""

from models import Visitor


def get_next_visitor_id(visitors: list[Visitor]) -> int:
    """Вернуть следующий свободный идентификатор посетителя."""
    return max((visitor.visitor_id for visitor in visitors), default=0) + 1


def add_visitor(
    visitors: list[Visitor], full_name: str, document: str
) -> Visitor:
    """Создать посетителя, добавить его в коллекцию и вернуть объект."""
    visitor = Visitor(get_next_visitor_id(visitors), full_name, document)
    visitors.append(visitor)
    return visitor


def find_visitors_by_name(visitors: list[Visitor], query: str) -> list[Visitor]:
    """Найти посетителей, чьё ФИО содержит строку поиска."""
    return [visitor for visitor in visitors if visitor.matches_name(query)]


def get_visitor_by_id(visitors: list[Visitor], visitor_id: int) -> Visitor | None:
    """Вернуть посетителя по идентификатору или None."""
    for visitor in visitors:
        if visitor.visitor_id == visitor_id:
            return visitor
    return None


def sort_visitors_by_name(visitors: list[Visitor]) -> list[Visitor]:
    """Вернуть посетителей, отсортированных по ФИО."""
    return sorted(visitors, key=lambda visitor: visitor.full_name.lower())
