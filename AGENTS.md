# AGENTS.md — habits-cli

## Proyecto
CLI en Python para registrar hábitos de estudio y ver la racha de días
consecutivos que lleva cada uno. Arquitectura en tres capas: `habits/core.py`
(lógica pura, sin consola), `habits/storage.py` (persistencia en JSON) y
`habits/cli.py` (parseo de argumentos y mensajes al usuario). Solo biblioteca
estándar; pytest es la única dependencia de desarrollo.

## Comandos
- Ejecutar: `python -m habits add <nombre>`, `python -m habits done <nombre>`, `python -m habits list`
- Tests: `pytest -q`
- Lint/formato: no hay linter configurado (constitución nº 1). Estilo PEP 8, líneas de 88 caracteres como máximo.

## Estilo y convenciones
- Python 3.12+, type hints en las funciones públicas y dataclasses para el modelo de datos.
- Código, identificadores y nombres de test en inglés; comentarios, mensajes al usuario y documentación en español.
- Fechas en ISO 8601 (`YYYY-MM-DD`).
- Un RF cubierto por al menos un test; nombres descriptivos en inglés (`test_add_habit_rejects_duplicate`).

## Reglas
- Lee `docs/constitution.md` y la spec activa (`specs/001-habits-mvp/spec.md`) antes de tocar código.
- No añadas dependencias que incumplan la constitución.
- No implementes comportamientos que no estén en la spec: si falta una decisión, detente y pregunta.
- Una tarea cada vez. No toques archivos fuera del alcance de la tarea asignada.

## Al terminar cualquier tarea
- Ejecuta `pytest -q` y muestra el resultado.
- Marca la tarea como hecha en `specs/001-habits-mvp/tasks.md` solo si sus tests pasan.
- No avances a la siguiente tarea sin que el usuario lo pida.
