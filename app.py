"""
app.py — главное приложение с меню.

Структура взята по образцу проекта учителя:
https://github.com/KJrTT/Library-Functools

Меню:
- теоретические разделы (мини‑«Википедия» по hashlib);
- практические демонстрации.
"""

from __future__ import annotations

from typing import Callable, Dict

from logic import (
    show_theory_intro,
    show_theory_algorithms,
    show_theory_digest_vs_hexdigest,
    show_theory_security_notes,
    demo_hash_string,
    demo_compare_strings,
    demo_hash_file,
    demo_many_hashes,
)
from utils import clear_screen, print_title


def show_menu() -> None:
    """Вывести главное меню приложения."""
    print_title("ДЕМОНСТРАЦИОННЫЙ СТЕНД МОДУЛЯ hashlib")
    print("1. Теория: что такое хеш и модуль hashlib")
    print("2. Теория: алгоритмы md5 / sha1 / sha256 / sha512")
    print("3. Теория: digest vs hexdigest")
    print("4. Теория: безопасность и ограничения")
    print("5. Демо: хеширование одной строки")
    print("6. Демо: сравнение двух строк по хешу")
    print("7. Демо: хеширование файла")
    print("8. Демо: хеширование нескольких строк")
    print("0. Выход")


MENU_ACTIONS: Dict[str, Callable[[], None]] = {
    "1": show_theory_intro,
    "2": show_theory_algorithms,
    "3": show_theory_digest_vs_hexdigest,
    "4": show_theory_security_notes,
    "5": demo_hash_string,
    "6": demo_compare_strings,
    "7": demo_hash_file,
    "8": demo_many_hashes,
}


def main() -> None:
    """Главный цикл приложения."""
    while True:
        clear_screen()
        show_menu()
        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "0":
            clear_screen()
            print("Спасибо за использование демонстрационного стенда hashlib!")
            break

        action = MENU_ACTIONS.get(choice)
        clear_screen()

        if action is None:
            print("Неизвестный пункт меню. Попробуйте ещё раз.")
        else:
            action()

        input("\nНажмите Enter, чтобы вернуться в меню...")


if __name__ == "__main__":
    main()


