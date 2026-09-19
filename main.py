"""Начальный сценарий системы учёта посетителей организации."""

from datetime import datetime


print("Система учёта посетителей организации")
print("Регистрация одного посещения")

# Посетитель
visitor_full_name = input("ФИО посетителя: ").strip()
visitor_document = input("Документ посетителя: ").strip()

# Сотрудник
employee_full_name = input("ФИО принимающего сотрудника: ").strip()
employee_is_available = input(
    "Сотрудник может принять посетителя сейчас? (да/нет): "
).strip().lower()

# Пропуск
pass_number = input("Номер пропуска (буквы и цифры допустимы): ").strip()
pass_expiry_text = input("Дата окончания пропуска (ДД.ММ.ГГГГ): ").strip()

# Посещение
visit_purpose = input("Цель посещения: ").strip()
visitor_name_is_valid = visitor_full_name.replace(" ", "").replace("-", "").isalpha()
employee_name_is_valid = employee_full_name.replace(" ", "").replace("-", "").isalpha()

if not visitor_name_is_valid:
    print("Ошибка: в ФИО посетителя разрешены только буквы, пробелы и дефисы.")
elif not employee_name_is_valid:
    print("Ошибка: в ФИО сотрудника разрешены только буквы, пробелы и дефисы.")
elif employee_is_available != "да" and employee_is_available != "нет":
    print("Ошибка: ответьте «да» или «нет» на вопрос о возможности принять посетителя.")
elif not pass_number:
    print("Ошибка: укажите номер пропуска.")
else:
    try:
        pass_expiry_date = datetime.strptime(pass_expiry_text, "%d.%m.%Y").date()
    except ValueError:
        print("Ошибка: дата пропуска должна быть в формате ДД.ММ.ГГГГ.")
    else:
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
