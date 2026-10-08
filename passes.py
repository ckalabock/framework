"""Операции с пропусками."""

from datetime import date

from models import AccessPass, Visitor


def get_next_pass_id(access_passes: list[AccessPass]) -> int:
    """Вернуть следующий свободный идентификатор пропуска."""
    return max((access_pass.pass_id for access_pass in access_passes), default=0) + 1


def add_access_pass(
    access_passes: list[AccessPass],
    number: str,
    visitor: Visitor,
    expires_on: date,
) -> AccessPass:
    """Создать пропуск для посетителя и добавить его в коллекцию."""
    access_pass = AccessPass(
        get_next_pass_id(access_passes), number, visitor, expires_on
    )
    access_passes.append(access_pass)
    return access_pass


def get_pass_for_visitor(
    access_passes: list[AccessPass], visitor_id: int
) -> AccessPass | None:
    """Вернуть первый пропуск, выданный указанному посетителю."""
    for access_pass in access_passes:
        if access_pass.visitor.visitor_id == visitor_id:
            return access_pass
    return None
