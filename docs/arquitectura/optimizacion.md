# Registro de optimización — desacople de sistemas

Fecha: 2026-07-31. Base: `arquitectura_sistemas.md` (relevamiento de conexiones).
Commit de seguridad previo: `4c818ad`.

Cada entrada registra: qué se cambió, dónde, por qué, el riesgo colateral evaluado y
cómo verificarlo. La ruta de test `registros` (`jp_test_correr("registros")`) valida
la integridad de toda la arquitectura nueva.

**Principio rector de toda la tanda:** el motor NUNCA conoce contenido por nombre.
El contenido se registra en `init 5` desde SUS archivos, con condiciones que son
funciones de módulo (regla anti-pickle), y el motor solo itera registros.

---

## O1 (=C3) — Registro "al irse el repartidor"

**Antes:** `avanzar_horario()` llamaba `manejar_quest1_violet_no_recibido()` por nombre
(protegido con hasattr) — el motor de tiempo conocía la quest 1 de Violet.
**Ahora:** lista `REPARTIDOR_AL_IRSE` en `timesystem_core.rpy`; el motor la itera.
La quest se suscribe en `violet_quest_01_a.rpy` (`init 5`).
**Riesgo:** casi nulo (un solo suscriptor, misma llamada).
**Verificar:** quest 1 de Violet — ignorar al repartidor a la mañana → el paquete
aparece en la cama y llega el mensaje de Mónica.

## O2 (=C2) — Eliminado el congelamiento de horario por Jasmine 0_b

**Antes:** `avanzar_horario()` retornaba sin hacer nada si la quest
`jasmine_questprincipal_0_b` estaba activa (el motor conocía la quest).
**Ahora:** el if se eliminó por PESO MUERTO comprobado: la 0_b pasa de no-iniciada a
BOTON_LISTO en un solo tick del game_loop (`dias_espera=0`, sin requisitos,
`_procesar_avance_etapas` avanza todas las etapas en un `while True`), y su escena
activa una restricción que ya bloquea `avanzar_tiempo`, `dormir` y `cheats`. La
ventana sin protección es inexistente en la práctica.
**Riesgo:** bajo. Cambio de comportamiento visible: durante el chat de Carl, tocar el
botón de tiempo ahora muestra el mensaje de la restricción (antes no hacía nada, sin
feedback). Es mejor UX.
**Verificar:** jugar jasmine 0_a → 0_b: al iniciar 0_b debe saltar el tutorial de
mensajes de inmediato; durante el chat, el botón de tiempo muestra "Me llego un
mensaje debo responderlo"; al responder a Carl, la quest completa y el tiempo avanza
normal.

## O3 (=C7) — Lista de habitaciones desde HABITACION_NPC

**Antes:** `accion_hotspot_move` tenía la lista `["casa_hmonica", "casa_hviolet",
"casa_hjasmine"]` duplicada del dict `HABITACION_NPC`.
**Ahora:** `if _hotspot_temp.destino in HABITACION_NPC:` — única fuente. Agregar un
NPC con habitación = agregarlo a `HABITACION_NPC` y nada más.
**Riesgo:** nulo (mismo contenido).

## O4 (=C8) — Door access declarativo

**Antes:** `obtener_opciones_puerta()` tenía un if por quest de Violet (14 bloques);
el label además hardcodeaba el override de la 09_a y el caso "Violet duerme el
sábado". Cada quest nueva de Violet tocaba el motor de puertas.
**Ahora:** tres registros en `door_access_system.rpy`:
- `registrar_opcion_puerta(npc, texto, label, condicion, ocultar_golpear, tipo)` —
  botones del menú (el orden de registro es el orden del menú).
- `registrar_override_puerta(npc, condicion, label)` — reemplaza TODO el flujo de
  puerta (caso 09_a enferma).
- `registrar_bloqueo_golpe(npc, condicion, mensaje)` — bloquea el golpe con un
  pensamiento (caso sábado dormida).

Todo el contenido de Violet vive en `characters/violet/interaction/puertas_violet.rpy`
(14 opciones + 1 override + 1 bloqueo, condiciones = funciones de módulo). Se agregó
el helper genérico `quest_lista_para_boton(id)` en `questsystem_core.rpy` — el
predicado estándar de disparadores manuales.
**Riesgo:** medio-bajo. Se preservó 1:1: orden de opciones, `ocultar_golpear` por
opción, la condición especial de la 0_b (sin exigir BOTON_LISTO), las condiciones
compuestas (inventario+stat de 02_a, chat de 05_a) y el tag "(Evento)" del evento 03.
`obtener_trigger_habitacion_directo` (entrada directa con relación alta) no se tocó:
consume `obtener_opciones_puerta`, que devuelve el mismo formato.
**Traducción:** "Violet debe estar dormida." pasó de bloque de diálogo a string
(`translate_string` en `obtener_bloqueo_golpe`); el `old/new` está en
`tl/english/script/core/locations/door_access_system.rpy` y el bloque huérfano se
eliminó. Los textos de opciones no cambiaron (traducciones intactas).
**Verificar:** cadena de puertas de Violet completa (0_b → 07_b), evento 03 sábado,
09_a enferma, golpear sábado a la mañana. Ruta `registros` valida labels y condiciones.

## O5 (=C5/C6) — Triggers de contenido registrables (dormir / game_loop / avanzar)

**Antes:** `accion_dormir` hardcodeaba 5 bloques de contenido (evento 2 de Violet,
hook final de la quest 0 del MC, 08_a al despertar, gestión diaria de 09_a, mensaje
del evento 03); `game_loop` hardcodeaba 4 (09_a piensa, jasmine 0_b, exploración del
MC, tutorial del celular); `accion_avanzar_tiempo` hardcodeaba 1 (espera de la quest 0).
**Ahora:** archivo nuevo `core/events/triggers_contenido.rpy` con 4 registros:
`TRIGGERS_GAME_LOOP`, `TRIGGERS_DORMIR_ANTES`, `TRIGGERS_DORMIR_DESPUES`,
`TRIGGERS_AVANZAR`. Cada función de trigger chequea su condición y devuelve un label
(el motor hace `jump expression`) o None (efectos python y sigue). El primero que
devuelve label gana — misma semántica que los jumps encadenados que reemplaza.
Las 10 funciones se movieron a sus archivos de contenido:

| Trigger | Registro | Prioridad | Archivo |
|---|---|---|---|
| violet_09a_piensa | game_loop | 40 | violet_quest_09_a.rpy |
| jasmine_0b | game_loop | 30 | jasmine_quest_0_b.rpy |
| mc_q0_exploracion | game_loop | 20 | mc_quest_0_a.rpy |
| mc_q0b | game_loop | 10 | mc_quest_0_b.rpy |
| violet_evento2 | dormir antes | 0 | evento2_violet.rpy |
| mc_q0_final | dormir después | 40 | mc_quest_0_a.rpy |
| violet_08a_despertar | dormir después | 30 | violet_quest_08_a.rpy |
| violet_09a_diaria | dormir después | 20 | violet_quest_09_a.rpy |
| violet_ev03_mensaje | dormir después | 10 | evento03_violet.rpy |
| mc_q0_espera | avanzar | 0 | mc_quest_0_a.rpy |

Las prioridades replican EXACTAMENTE el orden de los ifs originales (determinístico,
no depende del orden alfabético de archivos).
**Instrumentación S11 preservada:** `ejecutar_triggers_game_loop()` setea
`_gl_ultimo_trigger` con el id del trigger (mismos ids que antes) y lo limpia si
ninguno disparó — el tag `gl_trigger` de Sentry sigue funcionando igual.
**Riesgo:** medio (game_loop es la pieza más sensible). Mitigación: semántica de
"primer label gana" idéntica, ids idénticos, prioridades = orden original, lint
limpio, ruta `registros` valida estructura.
**Verificar:** intro completa del MC (exploración → espera → mudanza → sueño final),
jasmine 0_b, violet 08_a/09_a/09_b, evento 2 y mensaje del evento 03.

## O6 (=C11) — Embudo único de bloqueos

**Antes:** tres mecanismos paralelos: la restricción (vía `accion_bloqueada`), los
bloqueos de events (`hay_bloqueo`, consultado SOLO en avanzar tiempo) y 3 ifs sueltos
(mensaje prioritario duplicado en dormir y avanzar con textos distintos; flag de la
quest 1 de Violet en dormir).
**Ahora:** `accion_bloqueada(accion_id)` en `restriccion_quest_system.rpy` es LA
única puerta y consulta en orden: (1) restricción activa, (2) bloqueos de events,
(3) mensaje prioritario sin responder (solo dormir/avanzar_tiempo), (4) bloqueos
registrados por contenido (`registrar_bloqueo_accion`). Los labels quedaron con un
solo if. La quest 1 de Violet registra su bloqueo de dormir desde su archivo.
**Cambios de comportamiento (evaluados):**
- Los bloqueos de events ahora aplican en TODA acción que consulte el embudo (antes
  solo avanzar tiempo). Es el comportamiento correcto: un event que declara un
  bloqueo espera que se cumpla.
- El texto del bloqueo prioritario se unificó a "Debo responder el mensaje de {npc}
  antes de continuar" (antes dormir decía "antes de dormir"). Un solo old/new.
- El "despertar anticipado" por mensaje prioritario NO se movió: es un flujo
  alternativo, no un bloqueo; sigue en `accion_dormir`.
- Los chequeos de paquete y entrega de hoy siguen en `accion_dormir` en su orden
  original (moverlos al embudo alteraba la precedencia con el flujo del paquete).
**Traducción:** archivo nuevo `tl/english/bloqueos_strings.rpy` (4 strings); los 4
bloques de diálogo huérfanos se eliminaron de los tl de npcsystem_interactions y
timesystem_core.
**Verificar:** con mensaje prioritario pendiente, dormir y avanzar muestran el mismo
mensaje; quest 1 de Violet bloquea dormir; el evento del casco VR (si declara
bloqueos) bloquea donde corresponde.

## O7 (=C13) — Stock mutable fuera de CATALOGO_ITEMS

**Verificado: ya estaba resuelto.** `violet_quest_05_c` muta `stock_tienda` (default,
persiste en el save) y el comentario en el código ya prohíbe mutar `CATALOGO_ITEMS`.
Se confirmó por grep que al catálogo solo se lo LEE en runtime. Sin cambios.
(La nota de memoria que motivó C13 estaba desactualizada.)

## O8 — Herramientas de verificación

- Ruta de test nueva `registros` en `test_rutas.rpy`: valida que todo label
  registrado exista, que las condiciones puras ejecuten sin excepción y que los ids
  de triggers sean únicos. (Las funciones de trigger NO se ejecutan en el test:
  tienen efectos.)
- `testing_sistemas.md` actualizado con la ruta nueva y la tabla de disparadores
  declarativos.

## Decisiones de alcance (qué NO se hizo y por qué)

- **Hooks del tick (§5.3 del relevamiento):** no se implementaron. El propio
  relevamiento los marca como el refactor de menor valor y el orden del tick hoy
  está explícito y testeado por la ruta `tiempo`. Reevaluar si aparece un cuarto
  llamador del grupo "rutinas+quests+mensajes".
- **Puertas de Mónica/Jasmine:** no tienen contenido de puerta propio todavía; los
  registros quedan listos para cuando lo tengan (crear `puertas_monica.rpy` /
  `puertas_jasmine.rpy` con el mismo patrón).

## Estado de las conexiones tras la tanda

| Conexión del relevamiento | Estado |
|---|---|
| C2 (tiempo→jasmine 0_b) | RESUELTA (if eliminado) |
| C3 (tiempo→quest 1 violet) | RESUELTA (registro) |
| C5 (dormir→contenido) | RESUELTA (TRIGGERS_DORMIR) |
| C6 (game_loop→quests) | RESUELTA (TRIGGERS_GAME_LOOP) |
| C7 (lista habitaciones) | RESUELTA (HABITACION_NPC) |
| C8 (puerta→quests violet) | RESUELTA (registros de puerta) |
| C11 (bloqueos fragmentados) | RESUELTA (embudo) |
| C13 (stock en catálogo) | YA ESTABA RESUELTA |
| C1/C4/C12 (tick) | Sin cambios, a propósito (ver arriba) |
| C9/C10/C14–C18 | Eran limpias/aceptables, sin cambios |
