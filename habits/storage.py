"""Persistencia de los hábitos en un único archivo JSON local y legible.

Este módulo es el único que toca el sistema de archivos. Si los datos no se
pueden interpretar, se lanza `DataCorruptedError` y el archivo se queda
intacto: nunca se sobrescribe información que no se ha leído bien.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Iterable

from habits.core import Habit

DATA_VERSION = 1
DATA_DIRNAME = ".habits-cli"
DATA_FILENAME = "habits.json"


class StorageError(Exception):
    """Error base de la capa de persistencia."""


class DataCorruptedError(StorageError):
    """El archivo de datos existe pero no se puede interpretar."""


def default_data_path() -> Path:
    """Ruta por defecto del archivo de datos: `~/.habits-cli/habits.json`."""
    return Path.home() / DATA_DIRNAME / DATA_FILENAME


def load(path: Path) -> list[Habit]:
    """Carga los hábitos del archivo de datos.

    Si el archivo no existe devuelve una lista vacía. Si existe pero está
    corrupto lanza `DataCorruptedError`.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    except OSError as error:
        raise StorageError(f"no se puede leer el archivo de datos: {error}") from error

    if not raw.strip():
        raise DataCorruptedError(
            f"el archivo de datos está vacío: {path}. "
            "Bórralo o corrígelo para empezar de cero."
        )

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        raise DataCorruptedError(
            f"el archivo de datos no contiene JSON válido: {path}. "
            "No se ha modificado; bórralo o corrígelo para empezar de cero."
        ) from error

    return _habits_from_payload(payload, path)


def save(path: Path, habits: Iterable[Habit]) -> None:
    """Guarda los hábitos en el archivo de datos, creando la carpeta si falta."""
    payload = {
        "version": DATA_VERSION,
        "habits": [habit.to_dict() for habit in habits],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as error:
        raise StorageError(f"no se puede escribir el archivo de datos: {error}") from error


def update(
    path: Path, mutate: Callable[[list[Habit]], list[Habit]]
) -> list[Habit]:
    """Carga los hábitos, aplica el cambio y guarda el resultado.

    Si la carga falla no se escribe nada: es imposible machacar datos que no
    se han podido leer.
    """
    habits = load(path)
    updated = mutate(habits)
    save(path, updated)
    return updated


def _habits_from_payload(payload: object, path: Path) -> list[Habit]:
    if not isinstance(payload, dict):
        raise DataCorruptedError(
            f"el archivo de datos no tiene la estructura esperada: {path}. "
            "No se ha modificado; bórralo o corrígelo para empezar de cero."
        )

    version = payload.get("version")
    if version != DATA_VERSION:
        raise DataCorruptedError(
            f"el archivo de datos usa una versión no soportada ({version!r}): "
            f"{path}. No se ha modificado."
        )

    raw_habits = payload.get("habits")
    if not isinstance(raw_habits, list):
        raise DataCorruptedError(
            f"el archivo de datos no tiene la estructura esperada: {path}. "
            "No se ha modificado; bórralo o corrígelo para empezar de cero."
        )

    try:
        return [Habit.from_dict(item) for item in raw_habits]
    except ValueError as error:
        raise DataCorruptedError(
            f"el archivo de datos contiene un hábito con datos inválidos: {path}. "
            f"No se ha modificado. Detalle: {error}"
        ) from error
