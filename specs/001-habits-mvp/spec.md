# Spec 001 — MVP de habits-cli

## Contexto y objetivo
Los estudiantes de programación abandonan hábitos de estudio por falta de
seguimiento. habits-cli permite registrar hábitos, marcar el día de hoy como
completado, consultar y eliminar hábitos, y ver la racha de días consecutivos
que lleva cada uno, desde la terminal y sin fricción, para reforzar la
constancia.

## Usuarios / actores
Estudiantes y desarrolladores que viven en la terminal. Un solo usuario por
máquina; sin cuentas ni sincronización.

## Historias de usuario
- H1: Como estudiante quiero crear hábitos con un nombre para tener la lista
  de lo que quiero trabajar cada día.
- H2: Como estudiante quiero marcar un hábito como hecho hoy para registrar
  mi constancia.
- H3: Como estudiante quiero ver mis hábitos con su racha actual y su último
  día completado para motivarme a no romper la racha.
- H4: Como estudiante quiero eliminar un hábito que ya no quiero mantener
  para que mi lista refleje solo lo que me importa.

## Requisitos funcionales (criterios de aceptación en EARS)

### Crear hábito (H1)
- RF-1: CUANDO el usuario ejecute la orden de creación con un nombre no vacío
  que no exista, EL SISTEMA creará el hábito y lo confirmará con un mensaje
  (salida 0).
- RF-2: SI el nombre ya existe (comparación ignorando mayúsculas/minúsculas
  y espacios al inicio o final), ENTONCES EL SISTEMA no creará un duplicado,
  informará del conflicto y conservará el nombre del hábito ya existente tal
  como se creó (salida 1).
- RF-3: SI el nombre está vacío o son solo espacios, ENTONCES EL SISTEMA
  rechazará la orden con un mensaje de error (salida 1).
- RF-16: SI el usuario no indique el nombre del hábito o invoque una orden
  desconocida, ENTONCES EL SISTEMA mostrará un error de uso (salida 2).

### Marcar como hecho (H2)
- RF-4: CUANDO el usuario ejecute la orden de marcado y el hábito exista,
  EL SISTEMA registrará la fecha actual como completada y lo confirmará
  (salida 0).
- RF-5: SI el hábito ya está completado hoy, ENTONCES EL SISTEMA lo
  comunicará sin duplicar el registro (operación idempotente, salida 0).
- RF-6: SI el hábito no existe, ENTONCES EL SISTEMA mostrará un error
  sugiriendo consultar el listado (salida 1).

### Listar con rachas (H3)
- RF-7: CUANDO el usuario ejecute el listado, EL SISTEMA mostrará cada
  hábito con su racha actual en días (calculada según RF-14), ordenados por
  racha descendente y, a igualdad, por nombre alfabético sin distinguir
  mayúsculas/minúsculas (salida 0).
- RF-8: MIENTRAS no exista ningún hábito, EL SISTEMA responderá al listado
  con un mensaje invitando a crear el primero (salida 0).
- RF-9: DONDE un hábito tenga al menos un día completado, EL SISTEMA
  mostrará junto a él la fecha de su día completado más reciente en formato
  ISO 8601 (YYYY-MM-DD).
- RF-10: DONDE un hábito no tenga ningún día completado, EL SISTEMA
  mostrará junto a él que todavía no tiene días completados.

### Eliminar hábito (H4)
- RF-11: CUANDO el usuario ejecute la orden de eliminación y el hábito exista,
  EL SISTEMA lo eliminará junto con su historial, sin pedir confirmación, y lo
  confirmará (salida 0).
- RF-12: SI el hábito que se intenta eliminar no existe, ENTONCES EL SISTEMA
  mostrará un error (salida 1).

### Reglas transversales
- RF-13: EL SISTEMA almacenará todos los datos en un único archivo local en
  formato JSON legible por humanos.
- RF-14: EL SISTEMA calculará la racha como el número de días consecutivos
  completados cuyo último día sea hoy o ayer; si el último registro es
  anterior a ayer, la racha es 0.
- RF-15: SI el archivo de datos existe pero no es JSON válido o no tiene la
  estructura esperada (incluido el archivo vacío), ENTONCES EL SISTEMA abortará
  con un mensaje claro y NO sobrescribirá el archivo (salida 1).
- RF-17: EL SISTEMA ignorará los días completados con fecha futura al
  calcular la racha.
- RF-18: EL SISTEMA identificará un hábito por su nombre ignorando
  mayúsculas/minúsculas y espacios exteriores, tanto al buscarlo para marcarlo
  como para eliminarlo.

## Requisitos no funcionales
- Respuesta inmediata (<1 s) en equipos modestos. Sin acceso a red.
- Multiplataforma: macOS, Linux y Windows.
- Mensajes al usuario en español, claros y accionables.
- Los resultados se escriben en la salida estándar; los errores, en la salida
  de error.
- El listado debe poder leerse de un vistazo en una terminal estándar.

## Casos límite cubiertos
- Nombre vacío o formado solo por espacios → RF-3.
- Nombre con espacios exteriores al crearse → se conserva el original ya
  recortado (RF-1, RF-2).
- Nombres que solo difieren en mayúsculas o espacios exteriores → RF-2.
- Argumento ausente u orden desconocida → RF-16.
- Doble marcado el mismo día → RF-5 (idempotencia).
- Marcado de un hábito inexistente → RF-6.
- Racha con un hueco de más de un día → RF-14 (racha 0).
- Marcado ayer pero aún no hoy → RF-14 (la racha se conserva).
- Hábito recién creado, sin días completados → RF-10 (racha 0, sin fecha).
- Listado sin hábitos → RF-8.
- Eliminación de un hábito inexistente → RF-12.
- Archivo de datos inexistente → estructura vacía inicial (parte de RF-13).
- Archivo vacío o con estructura inesperada → RF-15.
- Día completado con fecha futura → RF-17.
- Búsqueda con distinta capitalización o espacios al marcar o eliminar →
  RF-18.

## Fuera de alcance (MVP)
- Editar o renombrar hábitos.
- Marcar días pasados (solo se puede marcar hoy).
- Estadísticas, gráficos e histórico mensual.
- Colores, emojis y formatos de salida avanzados.
- Recordatorios y notificaciones.
- Cuentas, sincronización y trabajo multiusuario.
- Interfaz TUI.
- Objetivos semanales o pesos por hábito.

## Criterios de finalización
- Todos los RF cubiertos por al menos un test automático y la suite completa en
  verde.
- Demo manual del flujo crear → marcar → listar → eliminar sin errores.

## Dudas abiertas
- Ninguna. (La ubicación del archivo de datos quedó resuelta en el plan
  técnico.)
