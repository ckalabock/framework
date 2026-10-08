"""Вспомогательные функции безопасного ввода данных."""

from datetime import datetime


def input_nonempty(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: поле не может быть пустым. Попробуйте снова.")


def input_full_name(prompt: str) -> str:
    """Запросить ФИО, содержащее буквы, пробелы и дефисы."""
    while True:
        full_name = input_nonempty(prompt)
        plain_name = full_name.replace(" ", "").replace("-", "")
        if plain_name.isalpha():
            return full_name
        print("Ошибка: разрешены только буквы, пробелы и дефисы.")


def input_int(prompt: str) -> int:
    """Безопасно запросить целое число."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число. Попробуйте снова.")


def input_date(prompt: str) -> datetime.date:
    """Безопасно запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        value = input(prompt).strip()
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите существующую дату в формате ДД.ММ.ГГГГ.")


def input_yes_no(prompt: str) -> bool:
    """Запросить ответ «да» или «нет» и вернуть логическое значение."""
    while True:
        answer = input(prompt).strip().lower()
        if answer == "да":
            return True
        if answer == "нет":
            return False
        print("Ошибка: введите «да» или «нет». Попробуйте снова.")


def print_items(items: list[object], empty_message: str) -> None:
    """Вывести объекты коллекции или сообщение при отсутствии данных."""
    if not items:
        print(empty_message)
        return
    for item in items:
        print(item)
