# Plan técnico — Spec 002

Amplía el plan de la Spec 001: no cambia la arquitectura (core puro, storage
única capa de E/S, CLI fina), solo añade el objetivo semanal y una subcomanda.

## Estructura de módulos
| Módulo | Responsabilidad | RF que cubre |
|---|---|---|
| `habits/core.py` | Campo `goal` en el modelo, validación del objetivo, cálculo de la semana, `set_goal`, resumen del listado | RF-1..RF-4, RF-5..RF-9, RF-11..RF-13 |
| `habits/storage.py` | Serializar y leer el objetivo; carga transparente de hábitos anteriores | RF-11, RF-14 |
| `habits/cli.py` | `--goal` en `add`, subcomanda `edit`, formato del listado con el progreso semanal | RF-1..RF-10 |
| `tests/` | pytest, al menos un test por RF | Todos |

## Modelo de datos
El archivo JSON añade una clave opcional `goal` por hábito:

```json
{
  "version": 1,
  "habits": [
    {
      "name": "Estudiar Python",
      "created_at": "2026-10-19",
      "completions": ["2026-10-19", "2026-10-20", "2026-10-21"],
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

- `goal` ausente = el hábito no tiene objetivo (RF-6, RF-14).
- `goal` presente = entero entre 1 y 7 (RF-3).
- Fechas en ISO 8601, orden ascendente y sin duplicados (sin cambios).

## Cálculo de la semana (RF-4)
1. `week_start(today)` = el lunes de la semana de `today` (`today - timedelta(days=today.weekday())`).
2. La semana va de `week_start` (lunes) a `week_start + 6 días` (domingo), ambos incluidos.
3. Se cuentan los días completados dentro de ese intervalo **y** no posteriores a hoy
   (mismo criterio que la racha: los días futuros se ignoran).
4. Cada día cuenta una sola vez, aunque se marquara dos veces.

## Objetivo semanal (RF-1, RF-2, RF-3, RF-13)
- `DEFAULT_WEEKLY_GOAL = 5` en el core.
- `Habit.goal: int | None = None`. `None` significa "sin objetivo" y solo lo
  tienen los hábitos anteriores a esta funcionalidad.
- `add_habit(habits, name, today, goal=None)`: sin objetivo indicado → 5 (RF-2);
  con objetivo indicado → se valida.
- `parse_goal(text)`: convierte el texto de la opción en entero y lanza
  `InvalidGoalError` si no es un entero entre 1 y 7 (RF-3).
- `set_goal(habits, name, goal)`: cambia el objetivo del hábito conservando
  nombre, fecha de creación e historial (RF-8, RF-11).
- El objetivo se guarda en el hábito, así que sobrevive al cambio de semana
  (RF-13).

## Decisiones técnicas (con la alternativa descartada)
- **La opción se llama `--goal`** (en inglés), no `--objetivo`: las órdenes
  existentes (`add`, `done`, `list`, `rm`) ya están en inglés y la constitución
  pide identificadores en inglés. Los mensajes al usuario siguen en español.
  - Alternativa descartada: `--objetivo`, que mezcla idiomas en la misma línea.
  - Alternativa descartada: aceptar ambos como alias; duplica la superficie de
    la CLI y los tests sin aportar nada.
- **`goal: int | None` en el dataclass**, en lugar de `goal: int = 5` con un
  flag aparte: hace falta distinguir "sin objetivo" (RF-6) de "objetivo 5", y
  un `None` ya lo expresa sin campos extra.
  - Alternativa descartada: guardar los objetivos en un diccionario aparte
    (`{"objetivos": {...}}`); rompe la relación "un hábito, un registro".
- **`version` del archivo sigue en `1`**: el cambio es retrocompatible porque
  `goal` es una clave opcional y los hábitos sin ella se leen igual.
  - Alternativa descartada: subir la versión a 2 con código de migración;
  rechazaría los archivos existentes sin motivo (saltaría a `DataCorruptedError`).
- **La clave `goal` solo se escribe si el hábito tiene objetivo**: mantiene el
  archivo limpio y legible (constitución nº 5).
  - Alternativa descartada: escribir siempre `"goal": null`.
- **El progreso de la semana se calcula al listar, no se guarda**: el
  contador guardado se desincroniza del historial en cuanto se edita algo.
  - Alternativa descartada: persistir `week_days` en el JSON.
- **La validación del objetivo vive en el core, no en `argparse`**: RF-3 pide
  salida 1 (error de negocio) para "abc", y `type=int` en argparse daría
  salida 2 (error de uso). La CLI pasa el texto tal cual y el core lo juzga.
- **`edit` es una subcomanda nueva** (`habits edit <nombre> --goal <n>`), no una
  opción de `add`: cambiar el objetivo de un hábito que ya existe no se puede
  expresar como "crear".
  - Alternativa descartada: `habits goal <nombre> <n>`; un verbo para una
    operación que en el futuro editará más cosas.
- **El objetivo no toca la racha ni el orden del listado**: la racha mide
  días consecutivos y el objetivo días por semana; son métricas distintas. El
  orden de la Spec 001 (racha descendente, luego nombre) sigue vigente.

## Contrato de la CLI
- Órdenes: `habits add <nombre> [--goal N]`, `habits done <nombre>`,
  `habits list`, `habits rm <nombre>`, `habits edit <nombre> --goal N`.
- Listado, una línea por hábito:
  - con objetivo: `Estudiar Python — racha 3 días — esta semana 2/5 — último: 2026-10-21`
  - sin objetivo: `Estudiar Python — racha 3 días — sin objetivo — último: 2026-10-21`
- Errores de objetivo: `Error: el objetivo debe ser un número entre 1 y 7.` (salida 1).
- `edit` sin `--goal` o sin nombre: error de uso (salida 2).
- Resultados a stdout, errores a stderr (sin cambios).

## Estrategia de tests
- **Core**: `week_start` (lunes de un lunes, de un martes, de un domingo),
  `weekly_completed` (dentro de la semana, de la anterior, de la siguiente,
  futuro ignorado, día repetido), `add_habit` (objetivo por defecto 5,
  explícito, inválido 0/8/abc), `set_goal` (cambia el objetivo, conserva
  historial y racha, hábito inexistente, objetivo inválido), `list_habits`
  (resumen con objetivo y días de la semana, hábito sin objetivo).
- **Storage**: ida y vuelta con `goal`, archivo heredado sin la clave → `None`,
  `goal` inválido en el archivo → `DataCorruptedError`, `goal` booleano → error.
- **CLI**: `add` con y sin `--goal`, `add` con `--goal` inválido (salida 1),
  `edit` correcto, `edit` con objetivo inválido, `edit` de un hábito
  inexistente, `edit` sin `--goal` (salida 2), listado con "esta semana X/Y" y
  con "sin objetivo", orden desconocida que ya menciona `edit`.
