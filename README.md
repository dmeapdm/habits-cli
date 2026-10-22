# habits-cli

CLI en Python para registrar hábitos de estudio, ver la racha de días
consecutivos que lleva cada uno y el progreso semanal frente a un objetivo de
días por semana. Solo biblioteca estándar; `pytest` es la única dependencia de
desarrollo.

## Requisitos

- Python 3.12 o superior
- `pytest` para ejecutar los tests: `pip install pytest`

## Uso

La aplicación se ejecuta desde el árbol de fuentes, sin instalar nada:

```bash
python -m habits add "Estudiar Python" --goal 3
python -m habits done "Estudiar Python"
python -m habits list
python -m habits edit "Estudiar Python" --goal 5
python -m habits rm "Estudiar Python"
```

| Orden | Qué hace | Salida |
|---|---|---|
| `add <nombre> [--goal N]` | Crea un hábito; sin `--goal`, objetivo 5 | 0, o 1 si el nombre u objetivo no valen |
| `done <nombre>` | Marca el hábito como hecho hoy | 0 si existe, 1 si no existe |
| `list` | Racha, progreso semanal y último día completado | 0 |
| `edit <nombre> --goal N` | Cambia el objetivo, conserva el historial | 0; 1 si no existe o no vale; 2 si faltan datos |
| `rm <nombre>` | Elimina el hábito y su historial | 0 si se elimina, 1 si no existe |

Ejemplo de salida de `habits list`:

```
Estudiar Python — racha 3 días — esta semana 2/5 — último: 2026-10-21
Leer — racha 0 días — sin objetivo — sin días completados
```

Los hábitos creados antes de que existiera el objetivo semanal se muestran
como «sin objetivo» hasta que se les asigna uno con `habits edit`.

Los errores de negocio (nombre duplicado, objetivo inválido, hábito
inexistente, archivo de datos corrupto) terminan con código 1 y su mensaje en
la salida de error. Los errores de uso (falta el nombre o el objetivo, orden
desconocida) terminan con código 2.

## Dónde se guardan los datos

En un único archivo JSON legible en `~/.habits-cli/habits.json`. Se puede
editar a mano, siempre que conserve esta forma:

```json
{
  "version": 1,
  "habits": [
    {
      "name": "Estudiar Python",
      "created_at": "2026-10-21",
      "completions": ["2026-10-20", "2026-10-21"],
      "goal": 5
    },
    {
      "name": "Leer",
      "created_at": "2026-10-01",
      "completions": ["2026-10-05"]
    }
  ]
}
```

La clave `goal` es opcional: si falta, el hábito se considera «sin objetivo».
Si está, debe ser un entero entre 1 y 7.

Si el archivo no es JSON válido, la aplicación aborta con un mensaje claro y
**no lo sobrescribe**: tus datos quedan intactos para que puedas arreglarlos.

## Tests

```bash
pytest -q
```

## Estructura

```
habits/
├── __init__.py
├── __main__.py   → python -m habits
├── cli.py        → parseo de argumentos y mensajes al usuario
├── core.py       → lógica pura: crear, marcar, eliminar, racha, objetivo semanal, listar
└── storage.py    → lectura y escritura del archivo JSON
tests/            → tests con pytest
```

## Cómo se construyó

El proyecto se desarrolló con Spec-Driven Development. Los artefactos del
proceso están en el repositorio:

| Artefacto | Contenido |
|---|---|
| `docs/constitution.md` | Principios innegociables del proyecto |
| `AGENTS.md` | Contexto y reglas que sigue el agente |
| `specs/001-habits-mvp/spec.md` | Requisitos funcionales en notación EARS |
| `specs/001-habits-mvp/plan.md` | Plan técnico y decisiones justificadas |
| `specs/001-habits-mvp/tasks.md` | Tareas de implementación y su estado |
| `specs/001-habits-mvp/validation.md` | Recorrido RF por RF con el test que cubre cada requisito |
| `specs/002-objetivo-semanal/spec.md` | Objetivo semanal por hábito, en notación EARS |
| `specs/002-objetivo-semanal/plan.md` | Plan técnico y decisiones justificadas de la Spec 002 |
| `specs/002-objetivo-semanal/tasks.md` | Tareas de implementación de la Spec 002 y su estado |
| `specs/002-objetivo-semanal/validation.md` | Recorrido RF por RF de la Spec 002 |
