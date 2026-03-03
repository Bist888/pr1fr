"""
core.py — ядро демонстрационного проекта по модулю hashlib.

Здесь находятся чистые функции, которые:
- считают хеши строк и файлов;
- показывают разные алгоритмы (md5, sha1, sha256, sha512);
- сравнивают хеши.

Структура и идея взяты из задания по functools:
https://github.com/KJrTT/Library-Functools
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Iterable
import hashlib
import os

HashAlgo = Literal["md5", "sha1", "sha256", "sha512"]


def get_hasher(algo: HashAlgo) -> "hashlib._Hash":
    """
    Создать объект хеш‑функции по имени алгоритма.

    :param algo: Название алгоритма ("md5", "sha1", "sha256", "sha512").
    :return: Объект hashlib.*.
    :raises ValueError: если алгоритм не поддерживается.
    """
    algo = algo.lower()
    mapping = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    try:
        return mapping[algo]()
    except KeyError as exc:
        raise ValueError(f"Неизвестный алгоритм: {algo}") from exc


def hash_text(text: str, algo: HashAlgo = "sha256") -> str:
    """
    Посчитать хеш для строки с помощью выбранного алгоритма.

    :param text: Исходная строка.
    :param algo: Алгоритм хеширования.
    :return: Хеш в виде шестнадцатеричной строки (hexdigest).
    """
    h = get_hasher(algo)
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def hash_file(path: str, algo: HashAlgo = "sha256", chunk_size: int = 8192) -> str:
    """
    Посчитать хеш для файла по пути.

    Файл читается по частям, чтобы можно было обрабатывать большие файлы.

    :param path: Путь к файлу.
    :param algo: Алгоритм хеширования.
    :param chunk_size: Размер блока чтения в байтах.
    :return: Хеш в виде шестнадцатеричной строки (hexdigest).
    :raises FileNotFoundError: если файл не существует.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Файл не найден: {path}")

    h = get_hasher(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def compare_texts(text1: str, text2: str, algo: HashAlgo = "sha256") -> bool:
    """
    Сравнить две строки по их хешам.

    :param text1: Первая строка.
    :param text2: Вторая строка.
    :param algo: Алгоритм хеширования.
    :return: True, если хеши совпадают.
    """
    return hash_text(text1, algo) == hash_text(text2, algo)


def hash_many_texts(texts: Iterable[str], algo: HashAlgo = "sha256") -> list[str]:
    """
    Посчитать хеши для набора строк.

    :param texts: Набор строк.
    :param algo: Алгоритм хеширования.
    :return: Список хешей в том же порядке.
    """
    return [hash_text(t, algo) for t in texts]


@dataclass(frozen=True)
class FileHashInfo:
    """
    Информация о хеше файла.

    :param path: Путь к файлу.
    :param algo: Использованный алгоритм.
    :param hexdigest: Хеш в шестнадцатеричном представлении.
    :param size_bytes: Размер файла в байтах.
    """

    path: str
    algo: HashAlgo
    hexdigest: str
    size_bytes: int


def get_file_hash_info(path: str, algo: HashAlgo = "sha256") -> FileHashInfo:
    """
    Получить расширенную информацию о хеше файла.

    :param path: Путь к файлу.
    :param algo: Алгоритм хеширования.
    :return: Объект FileHashInfo.
    """
    hexdigest = hash_file(path, algo)
    size = os.path.getsize(path)
    return FileHashInfo(path=path, algo=algo, hexdigest=hexdigest, size_bytes=size)



