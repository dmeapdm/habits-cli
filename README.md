# habits-cli

CLI en Python para registrar hábitos de estudio, ver la racha de días
consecutivos que lleva cada uno y el progreso semanal frente a un objetivo de
días por semana. Solo biblioteca estándar; `pytest` es la única dependencia de
desarrollo.

> Reproducción personal del curso [Hello SDD](https://github.com/mouredev/hello-sdd)
> de [Brais Moure](https://moure.dev/), usada como portfolio de Spec-Driven
> Development. Ver [Reproducción del curso Hello SDD](#reproducción-del-curso-hello-sdd-portfolio).

## Requisitos

- Python 3.12 o superior
- `pytest` para ejecutar los tests: `pip install pytest`

## Uso

La aplicación se ejecuta desde el árbol de fuentes, sin instalar nada. En
sistemas donde `python` ya apunta a Python 3, puedes usar `python` en lugar de
`python3`:

```bash
python3 -m habits add "Estudiar Python" --goal 3
python3 -m habits done "Estudiar Python"
python3 -m habits list
python3 -m habits edit "Estudiar Python" --goal 5
python3 -m habits rm "Estudiar Python"
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
├── __main__.py   → python3 -m habits
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

## Reproducción del curso Hello SDD (portfolio)

Este proyecto es una **reproducción personal del curso [Hello SDD:
Spec-Driven Development desde cero](https://github.com/mouredev/hello-sdd) de
[Brais Moure](https://moure.dev/)**, construida de principio a fin con el flujo
que enseña el curso:

> Constitución → Spec → Clarificación → Plan → Tareas → Implementación
> (una tarea cada vez, tests primero) → Validación → Cambio.

- **Spec 001** reproduce el proyecto `habits-cli` del curso: RF-1 a RF-11 en
  EARS, plan, tareas T1–T8 y validación RF por RF.
- **Spec 002** es una extensión propia para practicar la fase de **cambio**:
  primero se actualiza la spec (objetivo semanal por hábito, RF-1 a RF-14),
  después el plan y las tareas, y solo entonces el código.

Qué demuestra el repositorio:

- Requisitos en **EARS** con casos límite y errores explícitos, sin adjetivos no
  medibles.
- Separación estricta entre **spec (qué y por qué)**, **plan (cómo)** y
  **tareas**.
- Implementación **incremental**: un commit por tarea y la suite en verde en cada
  uno (67 → 155 tests).
- **Trazabilidad RF → test** en los `validation.md`, con demo manual y códigos
  de salida.
- Arquitectura en tres capas (core sin I/O, storage JSON, CLI) y solo
  biblioteca estándar.

El historial de commits refleja el avance tarea a tarea; `git log --oneline` es
la mejor forma de ver el proceso.
