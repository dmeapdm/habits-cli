# habits-cli

CLI en Python para registrar hábitos de estudio y ver la racha de días
consecutivos que lleva cada uno. Solo biblioteca estándar; `pytest` es la
única dependencia de desarrollo.

## Requisitos

- Python 3.12 o superior
- `pytest` para ejecutar los tests: `pip install pytest`

## Uso

La aplicación se ejecuta desde el árbol de fuentes, sin instalar nada:

```bash
python -m habits add "Estudiar Python"
python -m habits done "Estudiar Python"
python -m habits list
python -m habits rm "Estudiar Python"
```

| Orden | Qué hace | Salida |
|---|---|---|
| `add <nombre>` | Crea un hábito nuevo | 0 si se crea, 1 si el nombre está vacío o ya existe |
| `done <nombre>` | Marca el hábito como hecho hoy | 0 siempre que el hábito exista, 1 si no existe |
| `list` | Muestra los hábitos con su racha y su último día completado | 0 |
| `rm <nombre>` | Elimina el hábito y su historial | 0 si se elimina, 1 si no existe |

Ejemplo de salida de `habits list`:

```
Estudiar Python — racha 3 días — último: 2026-10-21
Leer — racha 0 días — sin días completados
```

Los errores de negocio (nombre duplicado, hábito inexistente, archivo de
datos corrupto) terminan con código 1 y su mensaje en la salida de error. Los
errores de uso (falta el nombre, orden desconocida) terminan con código 2.

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
      "completions": ["2026-10-20", "2026-10-21"]
    }
  ]
}
```

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
├── core.py       → lógica pura: crear, marcar, eliminar, racha, listar
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
