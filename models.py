"""Классы предметной области системы учёта посетителей."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class Visitor:
    """Посетитель организации."""

    visitor_id: int
    full_name: str
    document: str

    def matches_name(self, query: str) -> bool:
        """Проверить, входит ли строка поиска в ФИО посетителя."""
        return query.lower() in self.full_name.lower()

    def __str__(self) -> str:
        return f"{self.visitor_id}. {self.full_name} (документ: {self.document})"


@dataclass
class Employee:
    """Сотрудник, который принимает посетителей."""

    employee_id: int
    full_name: str
    department: str
    is_available: bool = True

    def can_receive_visitor(self) -> bool:
        """Вернуть возможность принять посетителя в текущий момент."""
        return self.is_available

    def __str__(self) -> str:
        availability = "может принять" if self.is_available else "недоступен"
        return (
            f"{self.employee_id}. {self.full_name}, {self.department} "
            f"— {availability}"
        )


@dataclass
class AccessPass:
    """Пропуск посетителя с датой окончания действия."""

    pass_id: int
    number: str
    visitor: Visitor
    expires_on: date

    def is_valid_on(self, check_date: date) -> bool:
        """Проверить, действует ли пропуск в указанную дату."""
        return self.expires_on >= check_date

    def __str__(self) -> str:
        return (
            f"Пропуск {self.number} для {self.visitor.full_name}, "
            f"действует до {self.expires_on:%d.%m.%Y}"
        )


@dataclass
class Visit:
    """Заявка на посещение организации."""

    visit_id: int
    visitor: Visitor
    employee: Employee
    access_pass: AccessPass
    visit_date: date
    purpose: str
    status: str = "активно"

    def is_allowed(self) -> bool:
        """Определить, можно ли допустить посетителя."""
        return (
            self.status == "активно"
            and self.access_pass.is_valid_on(self.visit_date)
            and self.employee.can_receive_visitor()
        )

    def cancel(self) -> None:
        """Отменить посещение."""
        self.status = "отменено"

    def __str__(self) -> str:
        permission = "допуск разрешён" if self.is_allowed() else "допуск запрещён"
        return (
            f"{self.visit_id}. {self.visit_date:%d.%m.%Y}: "
            f"{self.visitor.full_name} → {self.employee.full_name}. "
            f"Цель: {self.purpose}. Статус: {self.status}, {permission}."
        )
