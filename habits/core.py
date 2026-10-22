"""Lógica pura del dominio de hábitos.

No imprime, no lee de la consola y no accede al sistema de archivos.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import Iterable


class HabitError(Exception):
    """Error base del dominio de hábitos."""


class InvalidNameError(HabitError):
    """El nombre del hábito no es válido."""


class DuplicateHabitError(HabitError):
    """Ya existe un hábito con ese nombre."""


class HabitNotFoundError(HabitError):
    """No existe el hábito solicitado."""


class InvalidGoalError(HabitError):
    """El objetivo semanal no es válido."""


DEFAULT_WEEKLY_GOAL = 5
MIN_WEEKLY_GOAL = 1
MAX_WEEKLY_GOAL = 7
INVALID_GOAL_MESSAGE = "el objetivo debe ser un número entre 1 y 7."


@dataclass
class Habit:
    """Un hábito de estudio con su historial de días completados.

    `goal` es el número de días por semana que se fija como objetivo. `None`
    significa "sin objetivo" y solo ocurre en los hábitos creados antes de
    que existiera esta funcionalidad.
    """

    name: str
    created_at: date
    completions: list[date] = field(default_factory=list)
    goal: int | None = None

    def to_dict(self) -> dict[str, object]:
        """Serializa el hábito a su representación en el archivo de datos.

        La clave `goal` solo se escribe si el hábito tiene objetivo.
        """
        data: dict[str, object] = {
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "completions": [day.isoformat() for day in self.completions],
        }
        if self.goal is not None:
            data["goal"] = self.goal
        return data

    @classmethod
    def from_dict(cls, data: object) -> "Habit":
        """Construye un hábito desde su representación en el archivo de datos.

        Lanza `ValueError` si la representación no es válida.
        """
        if not isinstance(data, dict):
            raise ValueError("cada hábito debe ser un objeto JSON")

        name = data.get("name")
        created_at = data.get("created_at")
        completions = data.get("completions", [])

        if not isinstance(name, str) or not name.strip():
            raise ValueError("el nombre del hábito debe ser un texto no vacío")
        if not isinstance(created_at, str):
            raise ValueError("created_at debe ser una fecha en formato ISO")
        if not isinstance(completions, list):
            raise ValueError("completions debe ser una lista de fechas ISO")
        if not all(isinstance(day, str) for day in completions):
            raise ValueError("completions debe ser una lista de fechas ISO")

        try:
            created = date.fromisoformat(created_at)
            days = [date.fromisoformat(day) for day in completions]
        except ValueError as error:
            raise ValueError("las fechas deben estar en formato ISO 8601") from error

        goal = data.get("goal")
        if "goal" in data:
            if isinstance(goal, bool) or not isinstance(goal, int):
                raise ValueError("goal debe ser un número entero entre 1 y 7")
            if not MIN_WEEKLY_GOAL <= goal <= MAX_WEEKLY_GOAL:
                raise ValueError("goal debe ser un número entero entre 1 y 7")

        return cls(name=name, created_at=created, completions=days, goal=goal)


def normalize_name(name: str) -> str:
    """Recorta los espacios exteriores del nombre."""
    return name.strip()


def name_key(name: str) -> str:
    """Clave de comparación de nombres: sin espacios exteriores ni mayúsculas."""
    return name.strip().casefold()


def parse_goal(text: str) -> int:
    """Convierte el texto de la opción de objetivo en un número válido.

    Lanza `InvalidGoalError` si el texto no es un número entero entre 1 y 7.
    """
    cleaned = text.strip() if isinstance(text, str) else ""
    if not cleaned.isascii() or not cleaned.isdigit():
        raise InvalidGoalError(INVALID_GOAL_MESSAGE)

    return validate_goal(int(cleaned))


def validate_goal(goal: int) -> int:
    """Comprueba que el objetivo sea un número entero entre 1 y 7.

    Devuelve el propio objetivo si es válido y lanza `InvalidGoalError` si no
    lo es.
    """
    if isinstance(goal, bool) or not isinstance(goal, int):
        raise InvalidGoalError(INVALID_GOAL_MESSAGE)
    if not MIN_WEEKLY_GOAL <= goal <= MAX_WEEKLY_GOAL:
        raise InvalidGoalError(INVALID_GOAL_MESSAGE)

    return goal


def find_habit(habits: Iterable[Habit], name: str) -> Habit | None:
    """Devuelve el hábito cuyo nombre coincide con `name`, o None si no existe."""
    key = name_key(name)
    for habit in habits:
        if name_key(habit.name) == key:
            return habit
    return None


def add_habit(
    habits: Iterable[Habit],
    name: str,
    today: date,
    goal: int | str | None = None,
) -> list[Habit]:
    """Devuelve los hábitos con uno nuevo llamado `name` creado hoy.

    `goal` es el objetivo semanal: si no se indica, se usa
    `DEFAULT_WEEKLY_GOAL`; si se indica, se valida. Lanza `InvalidNameError`
    si el nombre está vacío, `DuplicateHabitError` si ya existe un hábito con
    ese nombre e `InvalidGoalError` si el objetivo no es válido.
    """
    clean_name = normalize_name(name)
    if not clean_name:
        raise InvalidNameError("el nombre del hábito no puede estar vacío")

    result = list(habits)
    if find_habit(result, clean_name) is not None:
        raise DuplicateHabitError(f"ya existe un hábito llamado «{clean_name}»")

    if goal is None:
        weekly_goal = DEFAULT_WEEKLY_GOAL
    elif isinstance(goal, str):
        weekly_goal = parse_goal(goal)
    else:
        weekly_goal = validate_goal(goal)

    result.append(Habit(name=clean_name, created_at=today, goal=weekly_goal))
    return result


def mark_done(habits: Iterable[Habit], name: str, today: date) -> list[Habit]:
    """Devuelve los hábitos con el indicado marcado como hecho hoy.

    La operación es idempotente: si el hábito ya estaba completado hoy no se
    añade ningún registro nuevo. Lanza `HabitNotFoundError` si el hábito no
    existe.
    """
    key = name_key(name)
    result = list(habits)

    for index, habit in enumerate(result):
        if name_key(habit.name) != key:
            continue
        if today in habit.completions:
            return result
        result[index] = replace(habit, completions=sorted([*habit.completions, today]))
        return result

    raise HabitNotFoundError(f"no existe el hábito «{name.strip()}»")


def remove_habit(habits: Iterable[Habit], name: str) -> list[Habit]:
    """Devuelve los hábitos sin el indicado.

    Lanza `HabitNotFoundError` si el hábito no existe.
    """
    key = name_key(name)
    current = list(habits)
    result = [habit for habit in current if name_key(habit.name) != key]

    if len(result) == len(current):
        raise HabitNotFoundError(f"no existe el hábito «{name.strip()}»")

    return result


@dataclass(frozen=True)
class HabitSummary:
    """Vista de un hábito preparada para el listado."""

    name: str
    streak: int
    last_completion: date | None


def calculate_streak(completions: Iterable[date], today: date) -> int:
    """Devuelve la racha de días consecutivos completados.

    La racha está viva si el último día completado es hoy o ayer; si es
    anterior a ayer, vale 0. Los días con fecha futura se ignoran.
    """
    days = sorted({day for day in completions if day <= today})
    if not days:
        return 0

    last = days[-1]
    if last < today - timedelta(days=1):
        return 0

    streak = 1
    while streak < len(days) and days[-streak - 1] == days[-streak] - timedelta(days=1):
        streak += 1

    return streak


def last_completion(completions: Iterable[date], today: date) -> date | None:
    """Devuelve el día completado más reciente, o None si no hay ninguno.

    Los días con fecha futura se ignoran, igual que en el cálculo de la racha.
    """
    days = [day for day in completions if day <= today]
    if not days:
        return None
    return max(days)


def week_start(today: date) -> date:
    """Devuelve el lunes de la semana a la que pertenece `today`."""
    return today - timedelta(days=today.weekday())


def weekly_completed(completions: Iterable[date], today: date) -> int:
    """Devuelve los días completados en la semana en curso.

    Cuenta los días entre el lunes y el domingo de la semana de `today`, ambos
    incluidos, ignorando las fechas futuras y los días repetidos. Como `today`
    siempre cae dentro de esa semana, basta con no contar más allá de hoy.
    """
    start = week_start(today)
    return len({day for day in completions if start <= day <= today})


def list_habits(habits: Iterable[Habit], today: date) -> list[HabitSummary]:
    """Devuelve el resumen de cada hábito, ordenado por racha y nombre.

    El orden es racha descendente y, a igualdad de racha, nombre alfabético
    sin distinguir mayúsculas/minúsculas.
    """
    summaries = [
        HabitSummary(
            name=habit.name,
            streak=calculate_streak(habit.completions, today),
            last_completion=last_completion(habit.completions, today),
        )
        for habit in habits
    ]
    return sorted(summaries, key=lambda summary: (-summary.streak, summary.name.casefold()))
