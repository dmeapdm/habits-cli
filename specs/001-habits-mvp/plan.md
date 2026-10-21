# Plan técnico — Spec 001

## Estructura de módulos
| Módulo | Responsabilidad | RF que cubre |
|---|---|---|
| `habits/storage.py` | Cargar y guardar el archivo JSON; detección de datos corruptos | RF-13, RF-15 |
| `habits/core.py` | Lógica pura: crear, marcar, eliminar, calcular racha, listar. Sin consola ni E/S | RF-1..RF-12, RF-14, RF-17 |
| `habits/cli.py` | `argparse`, mensajes en español, códigos de salida 0/1/2 | RF-1..RF-12, RF-16 |
| `habits/__main__.py` | Permite `python -m habits` | — |
| `tests/` | pytest, al menos un test por RF | Todos |

## Modelo de datos
Archivo JSON con esta forma:

```json
{
  "version": 1,
  "habits": [
    {
      "name": "Estudiar Python",
      "created_at": "2026-10-21",
      "completions": ["2026-10-19", "2026-10-20", "2026-10-21"]
    }
  ]
}
```

- Fechas en ISO 8601 (`YYYY-MM-DD`), orden ascendente y sin duplicados.
- `version` queda para posibles migraciones futuras.
- El archivo es legible y editable a mano (constitución nº 5).

## Ubicación del archivo de datos (resuelve la duda abierta de la spec)
- **Decisión**: `~/.habits-cli/habits.json` (carpeta oculta en el home del
  usuario).
- **Alternativa descartada**: `XDG_CONFIG_HOME` en Linux y `%APPDATA%` en
  Windows. Es más "correcto" en Unix, pero obliga a bifurcar el código por
  sistema operativo para un archivo único.
- **Alternativa descartada**: guardar el JSON en la raíz del proyecto. Mezcla
  datos con el código y rompe en cuanto la herramienta se instale fuera del
  repositorio.
- La ruta se **inyecta** como parámetro en storage y CLI, de modo que los
  tests usen `tmp_path` y el usuario siempre use la ruta por defecto. No se
  añade ninguna opción de línea de comandos para cambiar el archivo: el
  contrato de la CLI es el de la spec (RF-16).

## Algoritmo de racha (RF-14, RF-17)
1. Descartar los días completados con fecha posterior a hoy (RF-17).
2. Si no queda ninguno → racha 0.
3. `last` = fecha más reciente restante. Si `last` es anterior a ayer → racha 0.
4. Contar hacia atrás desde `last` mientras las fechas sean consecutivas.

## Normalización de nombres (RF-2)
- Clave de comparación: `nombre.strip().casefold()`.
- Se guarda y se muestra el nombre original **recortado** de espacios
  exteriores (RF-1, RF-2).

## Decisiones técnicas (con la alternativa descartada)
- **argparse** (stdlib) en lugar de `typer`/`click` → constitución nº 1.
- **La fecha "hoy" se inyecta** en el core (parámetro `today: date`) en lugar
  de llamar a `date.today()` dentro → las rachas se testean sin mockear el
  reloj. La CLI pasa `date.today()`.
- **storage nunca escribe si la carga falló** → es imposible machacar datos
  por error (RF-15).
- **Excepciones propias** en lugar de códigos de retorno mágicos:
  `DataCorruptedError` (storage), `InvalidNameError`, `DuplicateHabitError`,
  `HabitNotFoundError` (core). La CLI las traduce a mensaje en español y
  código de salida.
- **Códigos de salida**: 0 éxito, 1 error de negocio (duplicado, no existe,
  datos corruptos), 2 error de uso (argumento ausente u orden desconocida,
  RF-16).
- **`dataclass Habit`** para el modelo de datos, con `to_dict()`/`from_dict()`
  como único punto de traducción a JSON.

## Contrato de la CLI
- Órdenes: `habits add <nombre>`, `habits done <nombre>`, `habits list`,
  `habits rm <nombre>`.
- Resultados a stdout, errores a stderr.
- Formato del listado, una línea por hábito: nombre, racha en días y último
  día completado (o la indicación de que no tiene días completados, RF-10).
  Ejemplo: `Estudiar Python — racha 3 días — último: 2026-10-21`.
- Sin hábitos: mensaje invitando a crear el primero (RF-8).

## Estrategia de tests
- **Core** (fecha inyectada): racha vacía, viva por hoy, viva por ayer, rota
  (hueco), de un día, larga, y con fechas futuras ignoradas (RF-14, RF-17).
- **Core**: creación, duplicado con distinta capitalización, nombre vacío,
  marcado idempotente, marcado de inexistente, eliminación de existente y de
  inexistente, listado y orden, listado vacío (RF-1..RF-12).
- **Storage** con `tmp_path`: inexistente, válido, JSON corrupto, JSON válido
  con estructura inesperada, archivo vacío, y que no sobrescribe al fallar
  (RF-13, RF-15).
- **CLI**: handlers con ruta inyectada (mensajes, stdout/stderr, códigos de
  salida) y smoke tests del parser para las cuatro órdenes y el error de uso
  (RF-16).
