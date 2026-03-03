"""
utils.py — вспомогательные функции и утилиты для проекта по hashlib.

Аналогично примеру с functools, здесь:
- функции для красивого вывода;
- простейший "таймер" для примеров;
- справочная информация по алгоритмам.
"""

from __future__ import annotations

import os
import time
from typing import Callable, Any


def clear_screen() -> None:
    """Очистить экран консоли (Windows / Linux / macOS)."""
    os.system("cls" if os.name == "nt" else "clear")


def separator(char: str = "=", width: int = 50) -> str:
    """Вернуть строку‑разделитель."""
    return char * width


def print_title(title: str) -> None:
    """Печать заголовка с разделителями."""
    print(separator())
    print(title)
    print(separator())


def timed(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Простой декоратор для измерения времени выполнения функции.

    Используется в демонстрациях для сравнения скорости разных алгоритмов
    или подходов (например, хеширование большого файла).
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f"\n⏱ Время выполнения: {duration:.6f} секунд")
        return result

    return wrapper


ALGO_DESCRIPTIONS: dict[str, str] = {
    "md5": "MD5 — устаревший алгоритм, годится только для некритичных задач (контроль целостности).",
    "sha1": "SHA1 — также считается небезопасным для криптографии, но встречается в старых системах.",
    "sha256": "SHA256 — современный алгоритм семейства SHA‑2, широко используется.",
    "sha512": "SHA512 — еще один алгоритм семейства SHA‑2 с более длинным хешем.",
}


def describe_algorithm(name: str) -> str:
    """
    Вернуть краткое текстовое описание алгоритма.

    :param name: Название алгоритма (например, 'sha256').
    :return: Описание или сообщение по умолчанию.
    """
    return ALGO_DESCRIPTIONS.get(
        name.lower(),
        "Информация по этому алгоритму отсутствует в справочнике.",
    )



