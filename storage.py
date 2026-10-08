"""Загрузка и сохранение данных проекта в JSON-файлах."""

import json
from datetime import datetime
from pathlib import Path

from models import AccessPass, Employee, Visit, Visitor


DATA_DIR = Path(__file__).parent / "data"


def load_json(filename: str) -> list[dict]:
    """Загрузить список словарей из JSON; при ошибке вернуть пустой список."""
    file_path = DATA_DIR / filename
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []
    return data


def save_json(filename: str, data: list[dict]) -> None:
    """Сохранить список словарей в JSON с кодировкой UTF-8."""
    DATA_DIR.mkdir(exist_ok=True)
    with (DATA_DIR / filename).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_visitors() -> list[Visitor]:
    """Загрузить посетителей из JSON в объекты Visitor."""
    return [
        Visitor(item["id"], item["full_name"], item["document"])
        for item in load_json("visitors.json")
    ]


def save_visitors(visitors: list[Visitor]) -> None:
    """Сохранить объекты Visitor в JSON."""
    save_json(
        "visitors.json",
        [
            {
                "id": visitor.visitor_id,
                "full_name": visitor.full_name,
                "document": visitor.document,
            }
            for visitor in visitors
        ],
    )


def load_employees() -> list[Employee]:
    """Загрузить сотрудников из JSON в объекты Employee."""
    return [
        Employee(
            item["id"],
            item["full_name"],
            item["department"],
            item.get("is_available", True),
        )
        for item in load_json("employees.json")
    ]


def save_employees(employees: list[Employee]) -> None:
    """Сохранить объекты Employee в JSON."""
    save_json(
        "employees.json",
        [
            {
                "id": employee.employee_id,
                "full_name": employee.full_name,
                "department": employee.department,
                "is_available": employee.is_available,
            }
            for employee in employees
        ],
    )


def load_access_passes(visitors: list[Visitor]) -> list[AccessPass]:
    """Загрузить пропуска из JSON и связать их с посетителями."""
    visitors_by_id = {visitor.visitor_id: visitor for visitor in visitors}
    access_passes = []
    for item in load_json("passes.json"):
        visitor = visitors_by_id.get(item["visitor_id"])
        if visitor is not None:
            access_passes.append(
                AccessPass(
                    item["id"],
                    item["number"],
                    visitor,
                    datetime.strptime(item["expires_on"], "%Y-%m-%d").date(),
                )
            )
    return access_passes


def save_access_passes(access_passes: list[AccessPass]) -> None:
    """Сохранить объекты AccessPass в JSON."""
    save_json(
        "passes.json",
        [
            {
                "id": access_pass.pass_id,
                "number": access_pass.number,
                "visitor_id": access_pass.visitor.visitor_id,
                "expires_on": access_pass.expires_on.isoformat(),
            }
            for access_pass in access_passes
        ],
    )


def load_visits(
    visitors: list[Visitor],
    employees: list[Employee],
    access_passes: list[AccessPass],
) -> list[Visit]:
    """Загрузить посещения из JSON и восстановить связи между объектами."""
    visitors_by_id = {visitor.visitor_id: visitor for visitor in visitors}
    employees_by_id = {employee.employee_id: employee for employee in employees}
    passes_by_id = {
        access_pass.pass_id: access_pass for access_pass in access_passes
    }
    visits = []
    for item in load_json("visits.json"):
        visitor = visitors_by_id.get(item["visitor_id"])
        employee = employees_by_id.get(item["employee_id"])
        access_pass = passes_by_id.get(item["pass_id"])
        if visitor is not None and employee is not None and access_pass is not None:
            visits.append(
                Visit(
                    item["id"],
                    visitor,
                    employee,
                    access_pass,
                    datetime.strptime(item["visit_date"], "%Y-%m-%d").date(),
                    item["purpose"],
                    item.get("status", "активно"),
                )
            )
    return visits


def save_visits(visits: list[Visit]) -> None:
    """Сохранить объекты Visit в JSON."""
    save_json(
        "visits.json",
        [
            {
                "id": visit.visit_id,
                "visitor_id": visit.visitor.visitor_id,
                "employee_id": visit.employee.employee_id,
                "pass_id": visit.access_pass.pass_id,
                "visit_date": visit.visit_date.isoformat(),
                "purpose": visit.purpose,
                "status": visit.status,
            }
            for visit in visits
        ],
    )
