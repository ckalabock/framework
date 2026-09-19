"""Начальный сценарий системы учёта посетителей организации."""

from datetime import datetime


print("Система учёта посетителей организации")
print("Регистрация одного посещения")

# Посетитель
visitor_full_name = input("ФИО посетителя: ").strip()
visitor_document = input("Документ посетителя: ").strip()

# Сотрудник
employee_full_name = input("ФИО принимающего сотрудника: ").strip()
employee_is_available = input("Сотрудник доступен (да/нет): ").strip().lower()

# Пропуск
pass_number = int(input("Номер пропуска: "))
pass_expiry_text = input("Дата окончания пропуска (ДД.ММ.ГГГГ): ").strip()
pass_expiry_date = datetime.strptime(pass_expiry_text, "%d.%m.%Y").date()

# Посещение
visit_purpose = input("Цель посещения: ").strip()
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
    print("Решение: допуск запрещён. Принимающий сотрудник недоступен.")
