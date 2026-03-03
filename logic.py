"""
logic.py — логика демонстраций для проекта по модулю hashlib.

Аналогично примеру с functools (см. README в репозитории учителя),
здесь находятся функции, которые:
- красиво объясняют теорию;
- вызывают функции из core.py;
- показывают результаты пользователю.
"""

from __future__ import annotations

from typing import Iterable

from core import (
    hash_text,
    hash_file,
    compare_texts,
    hash_many_texts,
    get_file_hash_info,
)
from utils import print_title, describe_algorithm, timed


def show_theory_intro() -> None:
    """Теория: что такое хеш и модуль hashlib."""
    print_title("ТЕОРИЯ: Введение в hashlib")
    print(
        "hashlib — стандартный модуль Python для работы с криптографическими хеш‑функциями.\n"
        "Хеш‑функция превращает любые данные в «отпечаток» фиксированной длины.\n\n"
        "Свойства хеша:\n"
        "  • один и тот же ввод → всегда один и тот же хеш;\n"
        "  • по хешу нельзя однозначно восстановить исходные данные;\n"
        "  • малое изменение данных сильно меняет хеш.\n"
    )


def show_theory_algorithms() -> None:
    """Теория: основные алгоритмы (md5, sha1, sha256, sha512)."""
    print_title("ТЕОРИЯ: Алгоритмы хеширования")
    for name in ("md5", "sha1", "sha256", "sha512"):
        print(f"{name.upper()} — {describe_algorithm(name)}")
    print(
        "\nВ модуле hashlib есть и другие алгоритмы. Список доступных:\n"
        "  >>> import hashlib\n"
        "  >>> hashlib.algorithms_available\n"
    )


def show_theory_digest_vs_hexdigest() -> None:
    """Теория: разница между digest и hexdigest."""
    print_title("ТЕОРИЯ: digest vs hexdigest")
    print(
        "У объекта хеш‑функции есть два важных метода:\n"
        "  • digest()    — возвращает байты (сырое двоичное представление);\n"
        "  • hexdigest() — возвращает строку из шеснадцатеричных символов.\n\n"
        "В реальных программах почти всегда выводят именно hexdigest, "
        "потому что это удобно читать и копировать.\n"
    )


def show_theory_security_notes() -> None:
    """Теория: важные замечания по безопасности."""
    print_title("ТЕОРИЯ: Безопасность и ограничения")
    print(
        "Важно понимать, что простые хеш‑функции (MD5, SHA1, SHA256 и др.)\n"
        "НЕ предназначены для безопасного хранения паролей в чистом виде.\n\n"
        "Для паролей используют специальные алгоритмы (bcrypt, scrypt, Argon2 и т.п.),\n"
        "часто вместе с солью (salt) и большим количеством итераций.\n\n"
        "hashlib же отлично подходит для:\n"
        "  • проверки целостности файлов;\n"
        "  • быстрых идентификаторов данных;\n"
        "  • контрольных сумм.\n"
    )


def _choose_algo() -> str:
    """Запросить у пользователя алгоритм и вернуть его название."""
    print("Доступные алгоритмы: md5, sha1, sha256, sha512")
    algo = input("Введите название алгоритма (по умолчанию sha256): ").strip().lower()
    if not algo:
        algo = "sha256"
    return algo


def demo_hash_string() -> None:
    """Демонстрация: хеширование одной строки."""
    print_title("ДЕМО: Хеширование строки")
    text = input("Введите строку: ")
    algo = _choose_algo()
    hexdigest = hash_text(text, algo)

    print("\nРезультат:")
    print(f"Алгоритм : {algo}")
    print(f"Строка   : {text!r}")
    print(f"Хеш (hex): {hexdigest}")


def demo_compare_strings() -> None:
    """Демонстрация: сравнение двух строк по их хешам."""
    print_title("ДЕМО: Сравнение строк по хешу")
    t1 = input("Первая строка : ")
    t2 = input("Вторая строка: ")
    algo = _choose_algo()

    equal = compare_texts(t1, t2, algo)
    h1 = hash_text(t1, algo)
    h2 = hash_text(t2, algo)

    print("\nХеш 1:", h1)
    print("Хеш 2:", h2)
    print("\nРезультат сравнения:")
    if equal:
        print("Хеши совпадают → строки, скорее всего, одинаковые.")
    else:
        print("Хеши различаются → строки разные (или крайне редкая коллизия).")


@timed
def _timed_hash_file(path: str, algo: str) -> None:
    """Вспомогательная функция: посчитать хеш файла и вывести его (с таймером)."""
    info = get_file_hash_info(path, algo)  # type: ignore[arg-type]
    print(f"Файл     : {info.path}")
    print(f"Размер   : {info.size_bytes} байт")
    print(f"Алгоритм : {info.algo}")
    print(f"Хеш      : {info.hexdigest}")


def demo_hash_file() -> None:
    """Демонстрация: хеширование файла."""
    print_title("ДЕМО: Хеширование файла")
    path = input("Введите путь к файлу: ").strip()
    algo = _choose_algo()
    try:
        _timed_hash_file(path, algo)
    except FileNotFoundError:
        print("Ошибка: файл не найден.")
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def demo_many_hashes() -> None:
    """Демонстрация: хеширование списка строк."""
    print_title("ДЕМО: Хеширование нескольких строк")
    print("Введите несколько строк. Пустая строка — завершение ввода.")
    lines: list[str] = []
    while True:
        line = input("> ")
        if not line:
            break
        lines.append(line)

    if not lines:
        print("Строки не были введены.")
        return

    algo = _choose_algo()
    hashes = hash_many_texts(lines, algo)

    print("\nРезультат:")
    _print_hash_table(lines, hashes)


def _print_hash_table(texts: Iterable[str], hashes: Iterable[str]) -> None:
    """Распечатать строки и их хеши в виде простой таблицы."""
    print(f"{'№':<3} {'Строка':<20} Хеш")
    print("-" * 70)
    for i, (t, h) in enumerate(zip(texts, hashes), start=1):
        short_text = (t[:17] + "...") if len(t) > 20 else t
        print(f"{i:<3} {short_text:<20} {h}")



