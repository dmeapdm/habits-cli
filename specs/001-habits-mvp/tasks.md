# Tareas — Spec 001

Ordenadas por dependencia. Cada tarea dura menos de 30 minutos, se implementa
por separado y termina con sus tests en verde. No se empieza una tarea sin
haber terminado (y verificado) la anterior.

- [x] T1. Esqueleto del proyecto: paquete `habits/` con `__init__.py`,
      `tests/`, `pyproject.toml` y pytest configurado.
      (RF: —) Hecho cuando: `pytest -q` se ejecuta sin errores.
- [x] T2. `core.py`: modelo `Habit` y `add_habit` con normalización de
      nombres, detección de duplicados y rechazo del nombre vacío.
      (RF: RF-1, RF-2, RF-3) Hecho cuando: tests de crear, duplicado con
      distinta capitalización y nombre vacío en verde.
- [x] T3. `storage.py`: `load`/`save` del JSON; inexistente → estructura
      vacía; JSON corrupto, con estructura inesperada o vacío → error propio
      sin sobrescribir el archivo. Depende de `core.Habit` (T2).
      (RF: RF-13, RF-15) Hecho cuando: los tests de los cuatro escenarios en
      verde.
- [x] T4. `core.py`: `mark_done` idempotente con la fecha inyectada.
      (RF: RF-4, RF-5, RF-6, RF-18) Hecho cuando: tests de marcar, marcar dos
      veces y marcar un inexistente en verde.
- [x] T5. `core.py`: `remove_habit` que elimina el hábito y su historial.
      (RF: RF-11, RF-12) Hecho cuando: tests de eliminar existente y de
      eliminar inexistente en verde.
- [x] T6. `core.py`: `calculate_streak` con todos los casos límite.
      (RF: RF-14, RF-17) Hecho cuando: tests de racha 0, viva por hoy, viva
      por ayer, rota, de un día, larga y con fecha futura ignorada en verde.
- [x] T7. `core.py`: `list_habits` con el orden definido, el caso sin hábitos y
      la fecha del último día completado.
      (RF: RF-7, RF-8, RF-9, RF-10) Hecho cuando: tests de orden, de lista
      vacía y de última fecha en verde.
- [x] T8. `cli.py`: `argparse` con las cuatro órdenes, mensajes en español,
      resultados a stdout, errores a stderr y códigos de salida 0/1/2.
      (RF: RF-1..RF-12, RF-16) Hecho cuando: tests de las cuatro órdenes y
      del error de uso en verde.
- [x] T9. `__main__.py` para `python -m habits` y README breve con los
      comandos y el flujo de uso.
      (RF: —) Hecho cuando: `python -m habits list` responde con el mensaje de
      lista vacía y el README documenta las cuatro órdenes.
- [x] T10. Validación final: recorrido de la spec RF por RF anotando qué test
      cubre cada requisito.
      (RF: todos) Hecho cuando: cada RF tiene un test asociado en verde y la
      demo manual del flujo crear → marcar → listar → eliminar no falla.
