"""Capa de línea de comandos: parseo de argumentos y mensajes al usuario.

Es una capa fina: traduce argumentos en llamadas al núcleo ytraduce los
resultados o errores del núcleo en mensajes y códigos de salida.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import NoReturn, Sequence, TextIO

from habits import core, storage

EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_USAGE = 2

COMMANDS = ("add", "done", "list", "rm", "edit")


class SpanishArgumentParser(argparse.ArgumentParser):
    """Parser que informa de los errores de uso en español."""

    def error(self, message: str) -> NoReturn:
        self.exit(
            EXIT_USAGE,
            f"{self.prog}: error de uso. Revisa la ayuda con «{self.prog} --help».\n",
        )


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos de la aplicación."""
    parser = SpanishArgumentParser(
        prog="habits",
        description="Registra hábitos de estudio y consulta su racha de días.",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Crea un hábito nuevo")
    add_parser.add_argument("name", nargs="?", help="Nombre del hábito")
    add_parser.add_argument(
        "--goal",
        help="Objetivo de días por semana (1-7). Por defecto, 5.",
    )

    done_parser = subparsers.add_parser(
        "done", help="Marca un hábito como hecho hoy"
    )
    done_parser.add_argument("name", nargs="?", help="Nombre del hábito")

    subparsers.add_parser("list", help="Muestra los hábitos y su racha")

    rm_parser = subparsers.add_parser("rm", help="Elimina un hábito y su historial")
    rm_parser.add_argument("name", nargs="?", help="Nombre del hábito")

    edit_parser = subparsers.add_parser(
        "edit", help="Cambia el objetivo de un hábito"
    )
    edit_parser.add_argument("name", nargs="?", help="Nombre del hábito")
    edit_parser.add_argument(
        "--goal",
        help="Objetivo de días por semana (1-7).",
    )

    return parser


def main(
    argv: Sequence[str] | None = None,
    path: Path | None = None,
    today: date | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Ejecuta la aplicación y devuelve el código de salida."""
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    data_path = path if path is not None else storage.default_data_path()
    current_day = today if today is not None else date.today()

    parser = build_parser()
    arguments = list(argv) if argv is not None else sys.argv[1:]

    if arguments and not arguments[0].startswith("-") and arguments[0] not in COMMANDS:
        print(
            f"Error: orden desconocida «{arguments[0]}». "
            f"Órdenes disponibles: {', '.join(COMMANDS)}.",
            file=err,
        )
        return EXIT_USAGE

    try:
        args = parser.parse_args(arguments)
    except SystemExit as error:
        return error.code if isinstance(error.code, int) else EXIT_USAGE

    if args.command is None:
        print(
            f"Error: falta la orden. Órdenes disponibles: {', '.join(COMMANDS)}.",
            file=err,
        )
        return EXIT_USAGE

    if args.command == "add":
        if args.name is None:
            print("Error: falta el nombre del hábito. Uso: habits add <nombre>", file=err)
            return EXIT_USAGE
        return _run_add(data_path, args.name, current_day, args.goal, out, err)
    if args.command == "done":
        if args.name is None:
            print(
                "Error: falta el nombre del hábito. Uso: habits done <nombre>",
                file=err,
            )
            return EXIT_USAGE
        return _run_done(data_path, args.name, current_day, out, err)
    if args.command == "list":
        return _run_list(data_path, current_day, out, err)
    if args.command == "edit":
        if args.name is None:
            print(
                "Error: falta el nombre del hábito. "
                "Uso: habits edit <nombre> --goal N",
                file=err,
            )
            return EXIT_USAGE
        if args.goal is None:
            print(
                "Error: falta el objetivo. Uso: habits edit <nombre> --goal N",
                file=err,
            )
            return EXIT_USAGE
        return _run_edit(data_path, args.name, args.goal, out, err)
    if args.name is None:
        print("Error: falta el nombre del hábito. Uso: habits rm <nombre>", file=err)
        return EXIT_USAGE
    return _run_rm(data_path, args.name, out, err)


def _run_add(
    path: Path,
    name: str,
    today: date,
    goal: str | None,
    out: TextIO,
    err: TextIO,
) -> int:
    try:
        habits = storage.update(
            path, lambda current: core.add_habit(current, name, today, goal)
        )
    except (core.HabitError, storage.StorageError) as error:
        print(f"Error: {error}", file=err)
        return EXIT_ERROR

    print(f"Hábito «{habits[-1].name}» creado.", file=out)
    return EXIT_SUCCESS


def _run_done(
    path: Path, name: str, today: date, out: TextIO, err: TextIO
) -> int:
    already_done = False

    def mark(current: list[core.Habit]) -> list[core.Habit]:
        nonlocal already_done
        habit = core.find_habit(current, name)
        already_done = habit is not None and today in habit.completions
        return core.mark_done(current, name, today)

    try:
        storage.update(path, mark)
    except core.HabitNotFoundError as error:
        print(
            f"Error: {error}. Consulta tus hábitos con «habits list».",
            file=err,
        )
        return EXIT_ERROR
    except (core.HabitError, storage.StorageError) as error:
        print(f"Error: {error}", file=err)
        return EXIT_ERROR

    if already_done:
        print(f"«{name.strip()}» ya estaba marcado como hecho hoy.", file=out)
    else:
        print(f"«{name.strip()}» marcado como hecho hoy.", file=out)
    return EXIT_SUCCESS


def _run_edit(
    path: Path, name: str, goal: str, out: TextIO, err: TextIO
) -> int:
    try:
        habits = storage.update(
            path, lambda current: core.set_goal(current, name, goal)
        )
    except core.HabitNotFoundError as error:
        print(f"Error: {error}. Consulta tus hábitos con «habits list».", file=err)
        return EXIT_ERROR
    except (core.HabitError, storage.StorageError) as error:
        print(f"Error: {error}", file=err)
        return EXIT_ERROR

    updated = core.find_habit(habits, name)
    goal_days = updated.goal if updated is not None else goal
    days = "1 día" if goal_days == 1 else f"{goal_days} días"
    print(f"Objetivo de «{name.strip()}» actualizado a {days} por semana.", file=out)
    return EXIT_SUCCESS


def _run_list(path: Path, today: date, out: TextIO, err: TextIO) -> int:
    try:
        habits = storage.load(path)
    except storage.StorageError as error:
        print(f"Error: {error}", file=err)
        return EXIT_ERROR

    summaries = core.list_habits(habits, today)
    if not summaries:
        print(
            "Todavía no tienes hábitos. Crea el primero con «habits add <nombre>».",
            file=out,
        )
        return EXIT_SUCCESS

    for summary in summaries:
        if summary.goal is None:
            weekly = "sin objetivo"
        else:
            weekly = f"esta semana {summary.week_completed}/{summary.goal}"
        if summary.last_completion is None:
            detail = "sin días completados"
        else:
            detail = f"último: {summary.last_completion.isoformat()}"
        days = "1 día" if summary.streak == 1 else f"{summary.streak} días"
        print(f"{summary.name} — racha {days} — {weekly} — {detail}", file=out)

    return EXIT_SUCCESS


def _run_rm(path: Path, name: str, out: TextIO, err: TextIO) -> int:
    try:
        storage.update(path, lambda current: core.remove_habit(current, name))
    except core.HabitNotFoundError as error:
        print(f"Error: {error}", file=err)
        return EXIT_ERROR
    except (core.HabitError, storage.StorageError) as error:
        print(f"Error: {error}", file=err)
        return EXIT_ERROR

    print(f"Hábito «{name.strip()}» eliminado.", file=out)
    return EXIT_SUCCESS
