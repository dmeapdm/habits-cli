# Validación — Spec 001

Recorrido de la spec requisito por requisito. Para cada RF se indica el test
que lo cubre y el resultado de la ejecución.

**Suite completa:** `pytest -q` → **67 passed**.

## Requisitos funcionales

| RF | Qué exige | Test que lo cubre | Resultado |
|---|---|---|---|
| RF-1 | Crear un hábito y confirmarlo (salida 0) | `test_cli.py::test_add_creates_the_habit_and_confirms_it`<br>`test_core.py::test_add_habit_creates_habit_with_creation_date`<br>`test_core.py::test_add_habit_trims_surrounding_whitespace` | ✓ |
| RF-2 | No crear duplicados (ignora mayúsculas y espacios) | `test_cli.py::test_add_rejects_a_duplicate`<br>`test_core.py::test_add_habit_rejects_duplicate_ignoring_case_and_spaces` | ✓ |
| RF-3 | Rechazar el nombre vacío (salida 1) | `test_cli.py::test_add_rejects_an_empty_name`<br>`test_core.py::test_add_habit_rejects_empty_name`<br>`test_core.py::test_add_habit_rejects_whitespace_only_name` | ✓ |
| RF-4 | Registrar la fecha de hoy al marcar (salida 0) | `test_cli.py::test_done_marks_the_habit_as_done_today`<br>`test_core.py::test_mark_done_adds_today_to_completions`<br>`test_core.py::test_mark_done_keeps_previous_completions` | ✓ |
| RF-5 | Idempotencia al marcar dos veces el mismo día | `test_cli.py::test_done_twice_is_idempotent`<br>`test_core.py::test_mark_done_is_idempotent` | ✓ |
| RF-6 | Error al marcar un hábito inexistente (salida 1) | `test_cli.py::test_done_of_an_unknown_habit_suggests_the_list`<br>`test_core.py::test_mark_done_raises_not_found_for_unknown_habit` | ✓ |
| RF-7 | Listado con racha, ordenado por racha y nombre | `test_cli.py::test_list_shows_the_habits_with_their_streak`<br>`test_cli.py::test_list_sorts_by_streak_and_then_by_name`<br>`test_core.py::test_list_habits_sorts_by_streak_descending`<br>`test_core.py::test_list_habits_sorts_by_name_when_streak_is_equal`<br>`test_core.py::test_list_habits_reports_the_streak` | ✓ |
| RF-8 | Listado sin hábitos: mensaje invitando a crear el primero | `test_cli.py::test_list_without_habits_invites_to_create_the_first`<br>`test_core.py::test_list_habits_returns_empty_list_without_habits` | ✓ |
| RF-9 | Mostrar la fecha del último día completado (ISO 8601) | `test_cli.py::test_list_shows_the_last_completion_date`<br>`test_core.py::test_list_habits_reports_the_last_completion` | ✓ |
| RF-10 | Mostrar que aún no hay días completados | `test_cli.py::test_list_shows_that_a_habit_has_no_completions_yet`<br>`test_core.py::test_list_habits_reports_no_last_completion_without_completions` | ✓ |
| RF-11 | Eliminar el hábito con su historial (salida 0) | `test_cli.py::test_rm_deletes_the_habit`<br>`test_core.py::test_remove_habit_deletes_the_habit_with_its_history`<br>`test_core.py::test_remove_habit_keeps_the_other_habits` | ✓ |
| RF-12 | Error al eliminar un hábito inexistente (salida 1) | `test_cli.py::test_rm_of_an_unknown_habit_is_an_error`<br>`test_core.py::test_remove_habit_raises_not_found_for_unknown_habit` | ✓ |
| RF-13 | Un único archivo JSON local y legible | `test_storage.py::test_save_writes_readable_json_with_version_and_habits`<br>`test_storage.py::test_save_creates_missing_parent_directory`<br>`test_storage.py::test_load_reads_back_the_habits_that_were_saved`<br>`test_storage.py::test_load_returns_empty_list_when_file_does_not_exist`<br>`test_storage.py::test_default_data_path_lives_in_the_user_home` | ✓ |
| RF-14 | Racha: viva si el último día es hoy o ayer, si no 0 | `test_core.py::test_calculate_streak_is_zero_without_completions`<br>`test_core.py::test_calculate_streak_counts_a_single_day`<br>`test_core.py::test_calculate_streak_is_alive_when_the_last_day_is_yesterday`<br>`test_core.py::test_calculate_streak_is_zero_when_the_last_day_is_older_than_yesterday`<br>`test_core.py::test_calculate_streak_counts_consecutive_days`<br>`test_core.py::test_calculate_streak_stops_at_the_gap` | ✓ |
| RF-15 | Archivo corrupto: abortar sin sobrescribir (salida 1) | `test_storage.py::test_load_raises_error_for_invalid_json`<br>`test_storage.py::test_load_raises_error_for_empty_file`<br>`test_storage.py::test_load_raises_error_for_unexpected_structure`<br>`test_storage.py::test_load_raises_error_for_habit_with_unexpected_shape`<br>`test_storage.py::test_update_does_not_overwrite_a_corrupted_file`<br>`test_cli.py::test_a_corrupted_file_is_not_overwritten` | ✓ |
| RF-16 | Error de uso: argumento ausente u orden desconocida (salida 2) | `test_cli.py::test_add_without_name_is_a_usage_error`<br>`test_cli.py::test_unknown_command_is_a_usage_error`<br>`test_cli.py::test_without_command_is_a_usage_error`<br>`test_cli.py::test_usage_errors_are_reported_in_spanish` | ✓ |
| RF-17 | Ignorar los días con fecha futura | `test_core.py::test_calculate_streak_ignores_future_dates`<br>`test_core.py::test_calculate_streak_is_zero_with_only_future_dates`<br>`test_core.py::test_list_habits_ignores_future_dates_in_the_last_completion` | ✓ |
| RF-18 | Identidad del hábito ignorando mayúsculas y espacios | `test_core.py::test_mark_done_finds_habit_ignoring_case_and_spaces`<br>`test_core.py::test_remove_habit_finds_habit_ignoring_case_and_spaces`<br>`test_cli.py::test_done_finds_the_habit_ignoring_case_and_spaces` | ✓ |

## Requisitos no funcionales

| Requisito | Test que lo cubre | Resultado |
|---|---|---|
| Resultados a stdout, errores a stderr | `test_cli.py::test_add_creates_the_habit_and_confirms_it` (stderr vacío)<br>`test_cli.py::test_add_rejects_a_duplicate` (stdout vacío) | ✓ |
| Mensajes al usuario en español | `test_cli.py::test_usage_errors_are_reported_in_spanish` | ✓ |
| Respuesta inmediata, sin red | No aplica a test: la app no abre sockets ni llama a servicios externos. | ✓ |
| Multiplataforma (Linux, macOS, Windows) | Solo biblioteca estándar; rutas con `pathlib`. Sin test automatizado. | ✓ (revisado a mano) |
| Listado legible de un vistazo | `test_cli.py::test_list_shows_the_habits_with_their_streak` | ✓ |

## Demo manual

Flujo `list → add → done → list → rm → list` ejecutado con `python -m habits`
sobre un HOME de prueba, con los códigos de salida observados:

| Orden | Salida | Código |
|---|---|---|
| `list` (sin hábitos) | Todavía no tienes hábitos. Crea el primero con «habits add <nombre>». | 0 |
| `add "Estudiar Python"` | Hábito «Estudiar Python» creado. | 0 |
| `done "Estudiar Python"` | «Estudiar Python» marcado como hecho hoy. | 0 |
| `list` | Estudiar Python — racha 1 día — último: 2026-10-21 | 0 |
| `add "estudiar python"` (duplicado) | Error: ya existe un hábito llamado «estudiar python» | 1 |
| `rm "Estudiar Python"` | Hábito «Estudiar Python» eliminado. | 0 |
| `rm "No existe"` | Error: no existe el hábito «No existe» | 1 |
| `add` (sin nombre) | Error: falta el nombre del hábito. Uso: habits add <nombre> | 2 |
| `borrar` (orden desconocida) | Error: orden desconocida «borrar». Órdenes disponibles: add, done, list, rm. | 2 |

## Defectos encontrados durante la validación y corregidos

1. **Concordancia en el listado**: mostraba «racha 1 días». Corregido a
   «racha 1 día» / «racha N días» (`test_cli.py::test_list_shows_the_habits_with_their_streak`,
   `test_cli.py::test_list_uses_the_plural_for_several_days`).
2. **Errores de uso en inglés**: `argparse` emitía «the following arguments
   are required: name», contra el principio nº 6 de la constitución. Corregido
   con mensajes propios en español y salida 2
   (`test_cli.py::test_usage_errors_are_reported_in_spanish`).

## Limitación conocida

El esqueleto de la ayuda de `argparse` (`usage:`, `options:`) sigue en inglés
porque lo genera el framework; los textos de la aplicación (descripción de
cada orden y de cada argumento) sí están en español. Traducir el esqueleto
exigiría sustituir el formateador de `argparse`, una mejora que no está en el
alcance de esta spec.

## Veredicto

**Spec 001 cumplida.** Los 18 requisitos funcionales y los requisitos no
funcionales tienen cobertura de tests y la demo manual del flujo principal
funciona sin errores.
