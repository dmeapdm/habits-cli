# Spec 002 — Objetivo semanal por hábito

## Contexto y objetivo
La racha mide días consecutivos, así que un hábito que se pracica tres veces
por semana nunca genera una racha larga aunque se cumpla de sobra. El
objetivo semanal fija un mínimo de días por semana y permite ver, de un
vistazo, cuánto de la semana en curso llevas hecho frente a lo que te
habías planteado.

## Usuarios / actores
Estudiantes y desarrolladores que viven en la terminal. Un solo usuario por
máquina; sin cuentas ni sincronización.

## Historias de usuario
- H1: Como estudiante quiero fijar un objetivo de días por semana al crear un
  hábito para saber si voy por buen camino.
- H2: Como estudiante quiero ver cuántos días llevo esta semana frente a mi
  objetivo para motivarme a cumplirlo.
- H3: Como estudiante quiero corregir el objetivo de un hábito cuando mi ritmo
  cambia para que la herramienta siga siendo útil.

## Relación con la Spec 001
Esta spec **amplía** la Spec 001 y no la sustituye. Los requisitos de la
Spec 001 siguen vigentes salvo los modificados aquí:

- `habits add` acepta un objetivo opcional.
- `habits list` añade el progreso semanal a la línea de cada hábito.
- Aparece una orden nueva: `habits edit <nombre> --goal <n>`.
- Los hábitos creados antes de esta funcionalidad no tienen objetivo.

## Requisitos funcionales (criterios de aceptación en EARS)

### Crear hábito con objetivo (H1)
- RF-1: CUANDO el usuario ejecute la orden de creación indicando un objetivo
  válido, EL SISTEMA creará el hábito con ese objetivo y lo confirmará con un
  mensaje (salida 0).
- RF-2: CUANDO el usuario ejecute la orden de creación sin indicar objetivo,
  EL SISTEMA creará el hábito con un objetivo de 5 días por semana (salida 0).
- RF-3: SI el objetivo indicado no es un número entero entre 1 y 7, ENTONCES
  EL SISTEMA rechazará la orden con un mensaje de error (salida 1).

### Ver el progreso de la semana (H2)
- RF-4: EL SISTEMA contará como días de la semana en curso los días
  completados que caen entre el lunes y el domingo de esa semana, ambos
  incluidos.
- RF-5: DONDE un hábito tenga objetivo, EL SISTEMA mostrará junto a él el
  número de días completados en la semana en curso y su objetivo, con el
  formato "esta semana X/Y".
- RF-6: DONDE un hábito no tenga objetivo, EL SISTEMA mostrará junto a él que
  no tiene objetivo, en lugar del progreso semanal.
- RF-7: DONDE el número de días completados en la semana en curso sea mayor
  que el objetivo, EL SISTEMA mostrará el número real, sin limitarlo al
  objetivo.

### Cambiar el objetivo (H3)
- RF-8: CUANDO el usuario ejecute la orden de edición indicando un objetivo
  válido y el hábito exista, EL SISTEMA actualizará el objetivo del hábito y
  lo confirmará con un mensaje (salida 0).
- RF-9: SI el objetivo indicado no es un número entero entre 1 y 7, ENTONCES
  EL SISTEMA rechazará la orden con un mensaje de error (salida 1).
- RF-10: SI el hábito que se intenta editar no existe, ENTONCES EL SISTEMA
  mostrará un error (salida 1).
- RF-11: EL SISTEMA conservará el historial de días completados del hábito
  cuando se cambie su objetivo.
- RF-12: EL SISTEMA recalculará el progreso semanal mostrado tras un cambio
  de objetivo, usando el nuevo valor.

### Reglas transversales
- RF-13: EL SISTEMA conservará el objetivo de cada hábito al cambiar de
  semana, de modo que el objetivo no dependa del día en que se creó.
- RF-14: EL SISTEMA mostrará los hábitos que ya existían antes de esta
  funcionalidad como "sin objetivo", hasta que se les asigne uno.

## Requisitos no funcionales
- Los requisitos de la Spec 001 siguen en vigor: respuesta inmediata (<1 s),
  sin red, multiplataforma y mensajes en español.
- Resultados a la salida estándar y errores a la salida de error, con los
  mismos códigos de salida: 0 éxito, 1 error de negocio, 2 error de uso.
- La nueva funcionalidad no debe romper ningún flujo existente (crear, marcar,
  listar y eliminar).

## Casos límite cubiertos
- Objetivo no numérico (`--goal abc`) → RF-3.
- Objetivo 0, 8 o negativo → RF-3.
- Objetivo 7 con racha de 3 días → progreso "3/7" (RF-5).
- Más días completados que el objetivo (3 con objetivo 2) → "3/2", sin
  limitar (RF-7).
- Cambio de objetivo a mitad de semana → el progreso se recalcula con el
  nuevo valor (RF-12).
- Cambio de objetivo → no se toca la racha ni el historial (RF-11).
- Hábito creado el domingo → su progreso de la semana siguiente es 0 (RF-4).
- Hábito anterior a esta funcionalidad → "sin objetivo" (RF-6, RF-14).
- Edición de un hábito inexistente → RF-10.
- Objetivo indicado en la creación de un nombre vacío o duplicado → sigue
  mandando la Spec 001 (RF-3 y RF-2 de la Spec 001).

## Fuera de alcance
- Renombrar hábitos: la orden de edición solo cambia el objetivo.
- El valor por defecto de 5 días no se puede cambiar de forma global.
- Objetivos por mes, por temporada o por días concretos (por ejemplo, solo
  lunes y miércoles).
- Pesos, puntuaciones o niveles de dificultad.
- Avisos del tipo "te faltan 2 días para cumplir el objetivo".
- Historial de semanas anteriores.
- Marcar días pasados.
- Objetivos distintos por día de la semana.

## Criterios de finalización
- Todos los RF de esta spec cubiertos por al menos un test automático y la
  suite completa en verde.
- Ninguna regresión: los tests de la Spec 001 siguen en verde.
- Demo manual del flujo crear con objetivo → listar → editar objetivo →
  listar, sin errores.

## Dudas abiertas
Ninguna. Resuelta durante la revisión: el nombre de la opción de línea de
comandos es `--goal` (inglés), por coherencia con las órdenes existentes
(`add`, `done`, `list`, `rm`). Los mensajes al usuario siguen en español.
