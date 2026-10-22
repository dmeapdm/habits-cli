# Tareas — Spec 002

> **Estado**: T1-T7 completadas (suite en verde: 154 tests). La siguiente es **T8**.
> Actualiza esta línea al terminar cada tarea.

Ordenadas por dependencia. Cada tarea dura menos de 30 minutos, se implementa
por separado y termina con sus tests en verde. No se empieza una tarea sin
haber terminado (y verificado) la anterior.

- [x] T1. `core.py`: campo `goal` en el dataclass `Habit` (con `to_dict` y
      `from_dict`), constante `DEFAULT_WEEKLY_GOAL`, excepción
      `InvalidGoalError` y `parse_goal` que rechaza texto no entero y valores
      fuera de 1-7.
      (RF: RF-3, RF-14) Hecho cuando: tests de serializar y deserializar el
      objetivo, y de rechazar "abc", 0, 8 y -1 en verde.
- [x] T2. `core.py`: `add_habit` acepta el objetivo; sin objetivo indicado usa
      el valor por defecto 5 y con objetivo indicado lo valida.
      (RF: RF-1, RF-2, RF-3) Hecho cuando: tests de crear con objetivo
      explícito, con valor por defecto y con objetivo inválido en verde.
- [x] T3. `core.py`: `week_start` (lunes de la semana) y `weekly_completed`
      (días completados de la semana en curso, ignorando los futuros).
      (RF: RF-4) Hecho cuando: tests de semana de lunes, de martes y de
      domingo, y de conteo dentro, fuera y después de la semana en verde.
- [x] T4. `core.py`: `set_goal` cambia el objetivo del hábito conservando
      nombre, fecha de creación e historial; falla si el hábito no existe.
      (RF: RF-8, RF-10, RF-11) Hecho cuando: tests de cambio de objetivo, de
      conservación del historial y de hábito inexistente en verde.
- [x] T5. `core.py`: `HabitSummary` incluye objetivo y días de la semana;
      `list_habits` los rellena sin cambiar el orden.
      (RF: RF-5, RF-6, RF-7, RF-12) Hecho cuando: tests del resumen con
      objetivo, sin objetivo y con progreso que supera el objetivo en verde.
- [x] T6. `storage.py`: guardar y cargar la clave `goal`; los hábitos
      anteriores sin la clave se leen como "sin objetivo"; un `goal` inválido
      en el archivo es dato corrupto. Depende de T1.
      (RF: RF-11, RF-14) Hecho cuando: tests de ida y vuelta, de archivo
      heredado y de objetivo inválido en el archivo en verde.
- [x] T7. `cli.py`: `--goal` en `add`, subcomanda `edit`, y el listado muestra
      "esta semana X/Y" o "sin objetivo". Depende de T2, T4, T5 y T6.
      (RF: RF-1..RF-10) Hecho cuando: tests de crear con y sin objetivo, de
      editar, de los dos formatos del listado y de los códigos de salida en
      verde.
- [ ] T8. Validación final: recorrido de la spec RF por RF anotando qué test
      cubre cada requisito, más la demo manual.
      (RF: todos) Hecho cuando: cada RF tiene un test asociado en verde y la
      demo manual crear con objetivo → listar → editar objetivo → listar no
      falla.
