# Validación — Spec 002

Recorrido de la spec requisito por requisito. Para cada RF se indica el test
que lo cubre y el resultado de la ejecución.

**Suite completa:** `pytest -q` → **155 passed** (67 tests de la Spec 001, que
siguen en verde, más 88 nuevos de esta spec).

## Requisitos funcionales

| RF | Qué exige | Test que lo cubre | Resultado |
|---|---|---|---|
| RF-1 | Crear con un objetivo válido y confirmarlo (salida 0) | `test_cli.py::test_add_with_goal_uses_it`<br>`test_core.py::test_add_habit_accepts_an_explicit_goal`<br>`test_core.py::test_add_habit_accepts_a_goal_given_as_text` | ✓ |
| RF-2 | Crear sin objetivo: se usa 5 (salida 0) | `test_cli.py::test_add_without_goal_uses_the_default_goal`<br>`test_core.py::test_add_habit_uses_the_default_goal_when_no_goal_is_given`<br>`test_core.py::test_add_habit_uses_the_default_goal_when_the_goal_is_none`<br>`test_core.py::test_default_weekly_goal_is_five` | ✓ |
| RF-3 | Objetivo no entero o fuera de 1-7: error (salida 1) | `test_cli.py::test_add_with_an_invalid_goal_is_a_business_error`<br>`test_core.py::test_parse_goal_accepts_a_valid_number`<br>`test_core.py::test_parse_goal_rejects_non_integer_text`<br>`test_core.py::test_parse_goal_rejects_values_out_of_range`<br>`test_core.py::test_add_habit_rejects_a_goal_out_of_range`<br>`test_core.py::test_add_habit_rejects_a_non_numeric_goal` | ✓ |
| RF-4 | Contar los días de la semana en curso (lunes a domingo) | `test_core.py::test_week_start_on_monday_is_the_same_day`<br>`test_core.py::test_week_start_on_tuesday_is_the_monday`<br>`test_core.py::test_week_start_on_sunday_is_the_previous_monday`<br>`test_core.py::test_weekly_completed_is_zero_without_completions`<br>`test_core.py::test_weekly_completed_counts_days_inside_the_current_week`<br>`test_core.py::test_weekly_completed_ignores_days_before_the_week`<br>`test_core.py::test_weekly_completed_ignores_days_after_the_week`<br>`test_core.py::test_weekly_completed_ignores_future_days_within_the_week`<br>`test_core.py::test_weekly_completed_ignores_duplicated_days`<br>`test_core.py::test_weekly_completed_counts_the_whole_week_on_sunday`<br>`test_cli.py::test_list_shows_the_weekly_progress`<br>`test_cli.py::test_goal_does_not_depend_on_the_week` | ✓ |
| RF-5 | Con objetivo: mostrar "esta semana X/Y" | `test_cli.py::test_list_shows_the_weekly_progress`<br>`test_core.py::test_list_habits_reports_the_goal`<br>`test_core.py::test_list_habits_reports_the_days_completed_this_week` | ✓ |
| RF-6 | Sin objetivo: mostrar "sin objetivo" | `test_cli.py::test_list_shows_no_goal_for_a_legacy_habit`<br>`test_core.py::test_list_habits_reports_no_goal_for_a_habit_without_one`<br>`test_core.py::test_habit_from_dict_without_goal_key_reads_no_goal`<br>`test_storage.py::test_load_reads_a_legacy_habit_as_having_no_goal` | ✓ |
| RF-7 | Progreso por encima del objetivo: mostrar el número real | `test_cli.py::test_list_shows_the_progress_above_the_goal`<br>`test_core.py::test_list_habits_reports_progress_above_the_goal` | ✓ |
| RF-8 | Editar con objetivo válido y hábito existente (salida 0) | `test_cli.py::test_edit_changes_the_goal`<br>`test_core.py::test_set_goal_changes_the_goal`<br>`test_core.py::test_set_goal_accepts_a_goal_given_as_text`<br>`test_core.py::test_set_goal_finds_habit_ignoring_case_and_spaces` | ✓ |
| RF-9 | Objetivo inválido al editar: error (salida 1) | `test_cli.py::test_edit_with_an_invalid_goal_is_a_business_error`<br>`test_core.py::test_set_goal_rejects_an_invalid_goal` | ✓ |
| RF-10 | Editar un hábito inexistente: error (salida 1) | `test_cli.py::test_edit_of_an_unknown_habit_is_an_error`<br>`test_core.py::test_set_goal_raises_not_found_for_unknown_habit` | ✓ |
| RF-11 | Conservar el historial al cambiar el objetivo | `test_cli.py::test_edit_keeps_the_history_and_recalculates_the_progress`<br>`test_core.py::test_set_goal_keeps_name_creation_date_and_history`<br>`test_core.py::test_set_goal_keeps_the_other_habits`<br>`test_storage.py::test_update_keeps_the_goal_of_a_habit` | ✓ |
| RF-12 | Recalcular el progreso con el objetivo nuevo | `test_cli.py::test_edit_keeps_the_history_and_recalculates_the_progress`<br>`test_core.py::test_list_habits_uses_the_new_goal_after_a_goal_change` | ✓ |
| RF-13 | Conservar el objetivo al cambiar de semana | `test_storage.py::test_save_writes_the_goal_when_the_habit_has_one`<br>`test_storage.py::test_load_reads_back_the_goal_that_was_saved`<br>`test_core.py::test_list_habits_reports_the_goal`<br>`test_cli.py::test_goal_does_not_depend_on_the_week` | ✓ |
| RF-14 | Hábitos anteriores: "sin objetivo" hasta asignarles uno | `test_cli.py::test_list_shows_no_goal_for_a_legacy_habit`<br>`test_core.py::test_habit_from_dict_without_goal_key_reads_no_goal`<br>`test_storage.py::test_load_reads_a_legacy_habit_as_having_no_goal`<br>`test_core.py::test_set_goal_assigns_a_goal_to_a_habit_without_one` | ✓ |

## Requisitos no funcionales

| Requisito | Test que lo cubre | Resultado |
|---|---|---|
| Resultados a stdout, errores a stderr | `test_cli.py::test_add_with_goal_uses_it` (stderr vacío)<br>`test_cli.py::test_add_with_an_invalid_goal_is_a_business_error` (stdout vacío) | ✓ |
| Códigos de salida 0 / 1 / 2 | `test_cli.py::test_add_with_goal_uses_it` (0)<br>`test_cli.py::test_edit_with_an_invalid_goal_is_a_business_error` (1)<br>`test_cli.py::test_edit_without_goal_is_a_usage_error` (2)<br>`test_cli.py::test_edit_without_name_is_a_usage_error` (2) | ✓ |
| Respuesta inmediata (<1 s), sin red | No aplica a test: solo operaciones locales. La suite completa tarda ~0,3 s. | ✓ |
| Mensajes al usuario en español | `test_cli.py::test_usage_errors_are_reported_in_spanish` y comprobaciones de texto en los tests de CLI | ✓ |
| Sin regresión de los flujos existentes | Los 67 tests de la Spec 001 siguen en verde dentro de la suite de 155. | ✓ |
| Validación de `goal` inválido en el archivo | `test_storage.py::test_load_raises_error_for_invalid_goal_in_file`<br>`test_core.py::test_habit_from_dict_rejects_goal_out_of_range`<br>`test_core.py::test_habit_from_dict_rejects_non_integer_goal` | ✓ |

## Demo manual

Flujo crear con objetivo → listar → editar objetivo → listar, ejecutado con
`python -m habits` sobre un `HOME` de prueba (fecha real: 2026-10-22), más los
casos de error:

| Orden | Salida | Código |
|---|---|---|
| `add "Estudiar Python" --goal 3` | Hábito «Estudiar Python» creado. | 0 |
| `list` | Estudiar Python — racha 0 días — esta semana 0/3 — sin días completados | 0 |
| `done "Estudiar Python"` | «Estudiar Python» marcado como hecho hoy. | 0 |
| `list` | Estudiar Python — racha 1 día — esta semana 1/3 — último: 2026-10-22 | 0 |
| `edit "Estudiar Python" --goal 2` | Objetivo de «Estudiar Python» actualizado a 2 días por semana. | 0 |
| `list` | Estudiar Python — racha 1 día — esta semana 1/2 — último: 2026-10-22 | 0 |
| `add "Leer" --goal 0` | Error: el objetivo debe ser un número entre 1 y 7. | 1 |
| `edit "No existe" --goal 3` | Error: no existe el hábito «No existe». Consulta tus hábitos con «habits list». | 1 |
| `edit "Estudiar Python"` | Error: falta el objetivo. Uso: habits edit <nombre> --goal N | 2 |
| `borrar` | Error: orden desconocida «borrar». Órdenes disponibles: add, done, list, rm, edit. | 2 |

El archivo JSON resultante contiene `"goal": 2` en el hábito editado y conserva
su `created_at` y su historial.

## Defectos encontrados durante la validación y corregidos

Ninguno. El único hueco detectado fue de cobertura: no había un test que
cruzara un cambio de semana mostrando que el objetivo se conserva. Se añadió
`test_cli.py::test_goal_does_not_depend_on_the_week` (crea un hábito el domingo
con objetivo 3 y lo lista el lunes siguiente: "esta semana 0/3").

## Limitación conocida

El esqueleto de la ayuda de `argparse` (`usage:`, `options:`) sigue en inglés
porque lo genera el framework; los textos de la aplicación sí están en
español. Es la misma limitación aceptada en la Spec 001.

## Veredicto

**Spec 002 cumplida.** Los 14 requisitos funcionales tienen al menos un test en
verde, los requisitos no funcionales se respetan, los 67 tests de la Spec 001
siguen pasando y la demo manual del flujo principal funciona sin errores.
