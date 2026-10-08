"""Точка запуска консольной системы учёта посетителей."""

from employees import add_employee, get_employee_by_id
from passes import add_access_pass, get_pass_for_visitor
from storage import (
    load_access_passes,
    load_employees,
    load_visitors,
    load_visits,
    save_access_passes,
    save_employees,
    save_visitors,
    save_visits,
)
from utils import (
    input_date,
    input_full_name,
    input_int,
    input_nonempty,
    input_yes_no,
    print_items,
)
from visitors import (
    add_visitor,
    find_visitors_by_name,
    get_visitor_by_id,
    sort_visitors_by_name,
)
from visits import cancel_visit, create_visit, get_visits_for_date


def print_menu() -> None:
    """Вывести главное меню приложения."""
    print("\n=== Система учёта посетителей ===")
    print("1. Показать посетителей")
    print("2. Добавить посетителя и пропуск")
    print("3. Найти посетителя по ФИО")
    print("4. Показать сотрудников")
    print("5. Добавить сотрудника")
    print("6. Изменить доступность сотрудника")
    print("7. Зарегистрировать посещение")
    print("8. Показать посещения на дату")
    print("9. Отменить посещение")
    print("0. Выход")


def register_visitor(visitors: list, access_passes: list) -> None:
    """Добавить посетителя и его пропуск, затем сохранить данные."""
    full_name = input_full_name("ФИО посетителя: ")
    document = input_nonempty("Номер документа: ")
    visitor = add_visitor(visitors, full_name, document)
    number = input_nonempty("Номер пропуска: ")
    expires_on = input_date("Пропуск действует до (ДД.ММ.ГГГГ): ")
    add_access_pass(access_passes, number, visitor, expires_on)
    save_visitors(visitors)
    save_access_passes(access_passes)
    print(f"Посетитель добавлен: {visitor}")


def register_employee(employees: list) -> None:
    """Добавить сотрудника и сохранить список сотрудников."""
    full_name = input_full_name("ФИО сотрудника: ")
    department = input_nonempty("Отдел: ")
    employee = add_employee(employees, full_name, department)
    save_employees(employees)
    print(f"Сотрудник добавлен: {employee}")


def change_employee_availability(employees: list) -> None:
    """Изменить возможность сотрудника принимать посетителей."""
    print_items(employees, "Сотрудники отсутствуют.")
    employee = get_employee_by_id(
        employees, input_int("Идентификатор сотрудника: ")
    )
    if employee is None:
        print("Сотрудник не найден.")
        return
    employee.is_available = input_yes_no("Может принять посетителя? (да/нет): ")
    save_employees(employees)
    print("Доступность сотрудника обновлена.")


def register_visit(
    visitors: list, employees: list, access_passes: list, visits: list
) -> None:
    """Создать новое посещение после проверки связанных сущностей."""
    print_items(visitors, "Сначала добавьте посетителя.")
    if not visitors:
        return
    visitor = get_visitor_by_id(visitors, input_int("Идентификатор посетителя: "))
    if visitor is None:
        print("Посетитель не найден.")
        return

    access_pass = get_pass_for_visitor(access_passes, visitor.visitor_id)
    if access_pass is None:
        print("У посетителя нет пропуска.")
        return

    print_items(employees, "Сначала добавьте сотрудника.")
    if not employees:
        return
    employee = get_employee_by_id(
        employees, input_int("Идентификатор принимающего сотрудника: ")
    )
    if employee is None:
        print("Сотрудник не найден.")
        return

    visit_date = input_date("Дата посещения (ДД.ММ.ГГГГ): ")
    purpose = input_nonempty("Цель посещения: ")
    try:
        visit = create_visit(
            visits, visitor, employee, access_pass, visit_date, purpose
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_visits(visits)
    print(visit)


def show_visits_for_date(visits: list) -> None:
    """Вывести посещения на дату, указанную пользователем."""
    selected_date = input_date("Дата посещения (ДД.ММ.ГГГГ): ")
    print_items(
        get_visits_for_date(visits, selected_date),
        "На выбранную дату посещений нет.",
    )


def main() -> None:
    """Загрузить данные и обрабатывать команды главного меню."""
    visitors = load_visitors()
    employees = load_employees()
    access_passes = load_access_passes(visitors)
    visits = load_visits(visitors, employees, access_passes)

    while True:
        print_menu()
        command = input("Выберите действие: ").strip()
        if command == "1":
            print_items(
                sort_visitors_by_name(visitors), "Посетители отсутствуют."
            )
        elif command == "2":
            register_visitor(visitors, access_passes)
        elif command == "3":
            query = input_nonempty("Введите часть ФИО: ")
            print_items(
                find_visitors_by_name(visitors, query), "Совпадения не найдены."
            )
        elif command == "4":
            print_items(employees, "Сотрудники отсутствуют.")
        elif command == "5":
            register_employee(employees)
        elif command == "6":
            change_employee_availability(employees)
        elif command == "7":
            register_visit(visitors, employees, access_passes, visits)
        elif command == "8":
            show_visits_for_date(visits)
        elif command == "9":
            visit_id = input_int("Идентификатор посещения: ")
            if cancel_visit(visits, visit_id):
                save_visits(visits)
                print("Посещение отменено.")
            else:
                print("Посещение не найдено.")
        elif command == "0":
            print("Работа программы завершена.")
            break
        else:
            print("Ошибка: выберите пункт из меню.")


if __name__ == "__main__":
    main()
