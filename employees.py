"""Операции с коллекцией сотрудников."""

from models import Employee


def get_next_employee_id(employees: list[Employee]) -> int:
    """Вернуть следующий свободный идентификатор сотрудника."""
    return max((employee.employee_id for employee in employees), default=0) + 1


def add_employee(
    employees: list[Employee], full_name: str, department: str
) -> Employee:
    """Создать сотрудника, добавить его в коллекцию и вернуть объект."""
    employee = Employee(get_next_employee_id(employees), full_name, department)
    employees.append(employee)
    return employee


def get_employee_by_id(
    employees: list[Employee], employee_id: int
) -> Employee | None:
    """Вернуть сотрудника по идентификатору или None."""
    for employee in employees:
        if employee.employee_id == employee_id:
            return employee
    return None
