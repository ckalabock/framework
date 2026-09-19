"""Консольная программа для регистрации посещения организации."""

from datetime import datetime


def request_full_name(prompt):
    """Запрашивает ФИО, состоящее из букв, пробелов и дефисов."""
    while True:
        full_name = input(prompt).strip()
        name_without_separators = full_name.replace(" ", "").replace("-", "")

        if name_without_separators.isalpha():
            return full_name

        print("Ошибка: ФИО может содержать только буквы, пробелы и дефисы.")
        print("Попробуйте снова.")


def request_document():
    """Запрашивает номер документа, состоящий из цифр."""
    while True:
        document = input("Номер документа посетителя (только цифры): ").strip()
        document_without_spaces = document.replace(" ", "")

        if document_without_spaces.isdigit():
            return document

        print("Ошибка: номер документа должен содержать только цифры и пробелы.")
        print("Попробуйте снова.")


def request_employee_availability():
    """Запрашивает, может ли сотрудник принять посетителя."""
    while True:
        answer = input(
            "Сотрудник может принять посетителя сейчас? (да/нет): "
        ).strip().lower()

        if answer == "да" or answer == "нет":
            return answer

        print("Ошибка: введите только «да» или «нет».")
        print("Попробуйте снова.")


def request_pass_number():
    """Запрашивает номер пропуска из букв, цифр и дефисов."""
    while True:
        pass_number = input(
            "Номер пропуска (буквы, цифры и дефисы допустимы): "
        ).strip()
        pass_without_hyphens = pass_number.replace("-", "")

        if pass_without_hyphens.isalnum():
            return pass_number

        print("Ошибка: номер пропуска может содержать только буквы, цифры и дефисы.")
        print("Попробуйте снова.")


def request_pass_expiry_date():
    """Запрашивает дату окончания действия пропуска."""
    while True:
        date_text = input("Дата окончания пропуска (ДД.ММ.ГГГГ): ").strip()

        try:
            expiry_date = datetime.strptime(date_text, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите существующую дату в формате ДД.ММ.ГГГГ.")
            print("Попробуйте снова.")
        else:
            return expiry_date


def request_visit_purpose():
    """Запрашивает цель посещения."""
    while True:
        purpose = input("Цель посещения: ").strip()

        if purpose:
            return purpose

        print("Ошибка: цель посещения не может быть пустой.")
        print("Попробуйте снова.")


print("Система учёта посетителей организации")
print("Регистрация одного посещения\n")

# Посетитель
visitor_full_name = request_full_name("ФИО посетителя: ")
visitor_document = request_document()

# Сотрудник
employee_full_name = request_full_name("ФИО принимающего сотрудника: ")
employee_is_available = request_employee_availability()

# Пропуск
pass_number = request_pass_number()
pass_expiry_date = request_pass_expiry_date()

# Посещение
visit_purpose = request_visit_purpose()
visit_time = datetime.now()
pass_is_valid = pass_expiry_date >= visit_time.date()
employee_can_receive = employee_is_available == "да"

print("\nКарточка посещения")
print(f"Посетитель: {visitor_full_name}")
print(f"Документ: {visitor_document}")
print(f"Сотрудник: {employee_full_name}")
print(f"Пропуск № {pass_number}, действует до: {pass_expiry_date:%d.%m.%Y}")
print(f"Цель: {visit_purpose}")
print(f"Время регистрации: {visit_time:%d.%m.%Y %H:%M}")

if pass_is_valid and employee_can_receive:
    print("Решение: допуск разрешён. Посещение зарегистрировано.")
elif not pass_is_valid:
    print("Решение: допуск запрещён. Срок действия пропуска истёк.")
else:
    print("Решение: допуск запрещён. Принимающий сотрудник не может принять посетителя.")
