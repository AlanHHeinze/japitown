---
name: japitown-warnings
description: Lo que NO hay que hacer en Japitown. Errores de diseño que ya trabaron partidas de jugadores o rompieron el juego, con el porque y la regla que los evita. Leer ANTES de tocar bloqueos, mensajes/chat, disponibilidad de NPCs, restricciones, screens, traducciones o cualquier estado que se guarde en el save.
---

# Japitown — Advertencias: lo que no hay que hacer

Cada entrada es un bug **real** que llegó a jugadores o a testeo. No es teoría:
es la lista de las formas en que este proyecto ya se rompió. Antes de repetir un
patrón de acá, leer el porqué.

La guía de cómo SÍ se hacen las cosas es `japitown-content`. Esta es su
contraparte: cuando una regla de allá parece un capricho, acá está el jugador
al que le pasó.

Formato de cada entrada: **qué pasó → por qué → la regla → cómo se detecta**.

---

## A. Bloqueos que el jugador no puede resolver

### A1. Un bloqueo solo lo puede sostener algo que el jugador pueda resolver

**Qué pasó (0.1.9, dos jugadores).** La conversación genérica de Mensajear es
repetible. Al terminar se devolvía a "pendiente" a mano (`estado` y `_disparado`)
pero sin reiniciar `paso_actual`, que había quedado en `len(pasos)`. La segunda
vez que salía, el grupo entraba como activo **ya terminado**: sin opciones para
contestar. Y como Mensajear tiene un `registrar_bloqueo_global` mientras hay una
conversación abierta, **todas las acciones del juego quedaron bloqueadas** con
"Debo responderle primero a Violet" — y el chat mostraba "Violet responderá más
tarde" para siempre. Guardado en el save: recargar no lo arreglaba.

**Por qué.** El bloqueo miraba *que hubiera* una conversación abierta, no *que
se pudiera cerrar*. Dos verdades desincronizadas: "hay grupo activo" y "se puede
responder".

**La regla.** Todo bloqueo —prioritario, global, de acción, restricción— tiene
que estar condicionado a que **exista la salida**. Si la salida es contestar un
mensaje, el bloqueo pregunta `chat.puede_responder()`. Si es escribirle, pregunta
`mensajear_puede_hablar()`. Si no se puede resolver ahora, **no bloquea**: el
jugador sigue jugando y el bloqueo vuelve solo cuando se pueda.

Ya lo cumplen `obtener_bloqueo_mensaje_prioritario`, `_mv_hay_conversacion_abierta`
y `_vd20_esperando_mensaje`. Un bloqueo nuevo tiene que nacer así.

**Cómo se detecta.** Ruta `mensajes` del harness, paso "un mensaje no contestable
no bloquea". Y en desarrollo, `obtener_bloqueo_mensaje_prioritario` avisa por
consola cuando un prioritario no se puede contestar.

### A2. `registrar_bloqueo_global` bloquea TODO — solo con salida garantizada

**Por qué.** Corta dormir, avanzar, moverse, hablar, todo. Y suele ir con
`registrar_congelamiento_triggers`, que además apaga los inicios de quest. Si la
condición queda en True sin salida, no hay nada en el juego que la pueda apagar.

**La regla.** La condición de un bloqueo global tiene que ser de la forma
*"falta hacer X **y** X se puede hacer ahora"*. Nunca solo *"falta hacer X"*.
Ver A1.

### A3. Nunca reiniciar el estado de un grupo de mensajes a mano

**Qué pasó.** Ver A1: se bajaron `estado` y `_disparado` uno por uno y se olvidó
`paso_actual`.

**La regla.** Para volver a jugar un grupo, `grupo.resetear()`. Es el único que
sabe cuáles son TODOS los campos. Además `_entregar_grupo` llama a
`reiniciar_progreso()` en cada entrega, así que aunque alguien se olvide, el
grupo arranca de cero. Si aparece un `._disparado =` o `.paso_actual =` fuera de
`messagesystem_core.rpy`, está mal.

**Cómo se detecta.** Ruta `mensajes`, paso "grupos arrancan de cero al
reentregarse".

### A4. Lo que se entrega tiene que poder responderse (la etapa previa)

**Qué pasó.** `disparar_por_trigger` tenía un atajo: grupo sin condiciones de
entrega → entrega inmediata, salteando `_intentar_entrega`. O sea que un grupo
sin condiciones se entregaba aunque el NPC estuviera fuera de juego — y después
`puede_responder()` decía que no. Con un prioritario, eso es dormir y avanzar
bloqueados sin salida.

**La regla.** Toda entrega pasa por `_puede_entregarse(grupo)`: NPC disponible,
mensajes no bloqueados, primer paso con opciones. Si falla, el grupo va a
**espera** y se reintenta en cada vuelta del game_loop. No se agrega un tercer
camino de entrega que la saltee.

### A5. Una restricción o una indisponibilidad que nadie apaga es un NPC borrado

**Por qué.** `activar_restriccion` es un slot único y `marcar_npc_no_disponible`
no tiene reseteo automático (ni al dormir ni al cargar), a propósito. Quien lo
prende tiene que apagarlo **en todas las ramas**, incluida la de fallo y la de
"el jugador cargó una partida a mitad de la escena".

**La regla.** Al escribir `activar_restriccion(...)` o
`marcar_npc_no_disponible(...)`, escribir en el mismo commit el
`desactivar_restriccion()` / `marcar_npc_disponible()` de cada salida, y
preguntarse: *¿qué pasa si el jugador guarda acá y carga mañana?*

### A6. Un mensaje prioritario con condiciones que pueden no cumplirse nunca

**Por qué.** Un prioritario entregado bloquea dormir y avanzar. Si además solo se
puede responder en cierto horario (`horario_respuesta`) y ese horario solo se
alcanza avanzando el tiempo, es un ciclo cerrado. Hoy ningún grupo usa
`horario_respuesta`, y A1 lo cubre si alguno lo usa — pero no hay que diseñar
contenido que dependa de esa red.

**La regla.** Un prioritario se entrega cuando el jugador **ya puede**
contestarlo, no antes. Las condiciones van en la entrega (`momento_horario`,
`momento_locacion`, `condicion_entrega`), no en la respuesta.

---

## B. Estado que vive en el save

### B1. `default` es save: lo que no deba sobrevivir a una sesión no va ahí

**Qué pasó.** La cola de "escribiendo..." del chat (`_msg_respuestas_pendientes`,
`_msg_escribiendo`, `_msg_timer_id`) es `default`. Si el jugador cierra el
celular a mitad de una respuesta de varias burbujas, el timer que la drena
desaparece (vive dentro de `screen pantalla_chat`) y la cola queda a medias —
guardada. Hoy es solo visual, porque `finalizar()` corre al responder y no al
terminar la animación. Pero es el tipo de estado que **parece** transitorio y no
lo es.

**La regla.** Antes de un `default`, preguntarse: *¿tiene sentido que esto esté
en un save de hace tres días?* Si no, o no se guarda, o se limpia en
`after_load`, o la lógica que lo consume tolera encontrarlo a medias.

### B2. El catálogo que vive en el save no se actualiza solo

**Qué pasó (varias veces en una sesión).** Textos de pista, rutinas de quest,
posiciones de sprite: se corregían en el código y el jugador "lo seguía viendo
igual". Los sistemas con estado (`sistema_quests`, `sistema_mensajes`,
`sistema_talk`, `sistema_skins`, `sistema_events`) son `default` y se guardan
**enteros**, catálogo incluido.

**La regla.** Lo que sea catálogo se refresca en `_ps_refrescar_*`
(`persistencia_sistemas.rpy`) al cargar. Si un campo nuevo es catálogo y no
progreso, agregarlo a `_CAMPOS`. Y al probar un fix de catálogo: **cargar** la
partida, no seguir la sesión abierta.

### B3. `_ps_merge_dict` solo AGREGA lo que falta

**Por qué.** Mergea contenido nuevo hacia saves viejos por id. No pisa lo que ya
existe. Un fix a un objeto que el save ya tiene no llega por acá — llega por
B2.

### B4. Callables en objetos guardados: solo funciones de módulo

Ya está en `japitown-content` (regla 3). Se repite acá porque es el crash más
caro del proyecto: `Can't get local object ...<locals>.<lambda>` al guardar.
Aplica a Quest, ConfigEtapa, EstadoTalk, AccionLocacion, Skin, `condicion_uso` de
items y a **cualquier** callable alcanzable desde un `default`.

---

## C. Screens y UI

### C1. Una screen no puede tener efectos secundarios

**Qué pasó.** Un `$ renpy.hide_screen("say")` dentro de una screen mató el
textbox: el **predictor** ejecuta el cuerpo de una screen aunque no esté en
pantalla.

**La regla.** El cuerpo de una screen solo LEE. Las condiciones de botones
(`registrar_opcion_puerta`, `registrar_bloqueo_accion`, condiciones de Mensajear)
también, porque las evalúa el armado del screen. `_rn_cita_vigente()` está
separada del trigger que la consume exactamente por esto.

### C2. Un timer dentro de una screen muere con la screen

**Qué pasó.** Ver B1. El timer de "escribiendo..." vive en `pantalla_chat`;
cerrar la screen corta la máquina de estados a la mitad.

**La regla.** Una máquina de estados que tiene que terminar sí o sí no se
avanza desde un `timer` de screen. O se resuelve de forma síncrona (como hace
`responder()`), o el estado tolera quedar a medias y se retoma al reabrir.

### C3. Durante un `pause` el HUD es clickeable

**Qué pasó.** El recorrido del viaje rápido hace `pause` por tramo; con el HUD
arriba, el jugador podía arrancar un segundo movimiento encima del primero.

**La regla.** Toda secuencia con `pause` que no quiera interrupciones hace
`ocultar_hud()` antes y `mostrar_hud()` en **cada** salida.

---

## D. Traducción

### D1. Editar un texto fuente desengancha su traducción sin avisar

**Qué pasó (0.1.9).** Una pasada ortográfica agregó tildes a todo el juego. 40
entradas `old` quedaron apuntando a la versión sin tilde; el jugador en inglés
veía "Violet no está en su habitación." en español. **Ni el lint ni nada avisa.**
Lo mismo con los bloques de diálogo: el id es un hash del texto, así que una
tilde nueva es un bloque nuevo (huérfano el viejo, vacío el nuevo).

**La regla.** Corregir el español **antes** de traducir, nunca después. Y
después de tocar cualquier texto: `python tools/validar_traducciones.py`. Sus
seis chequeos existen porque cada uno fue un bug.

### D2. Un `%` suelto en un diálogo crashea el juego

**Qué pasó.** "30% de descuento" tira `TypeError: %o format` al mostrarse:
`renpy.exports.say` hace `what % tag_quoting_dict` en toda línea. El lint no lo
ve. Va `%%`.

### D3. Un bloque de traducción vacío deja el cuadro de diálogo EN BLANCO

Peor que verlo en español. Al regenerar desde Ren'Py los bloques nuevos salen
con `""`. `validar_traducciones.py` los lista como "diálogos con traducción
VACIA".

### D4. Un texto que sale de una variable no se traduce solo

`piensa "[var]"` busca la traducción del literal `"[var]"`, nunca del
contenido. Traducir con `renpy.translate_string()` **antes** de asignar, y las
plantillas con `{}` se traducen **antes** del `.format()` (si no, haría falta
una entrada por cada valor del contador).

---

## E. Sprites y transiciones

### E1. Un `with` aplica a TODOS los cambios pendientes desde la última interacción

Un `hide` sin `with` seguido de un `show ... with dissolve` disuelve los dos
juntos. A veces es lo que se quiere (cruzar dos sprites sin hueco); a veces no.
Ponerlo a propósito, no por accidente.

### E2. El lint NO valida atributos de layeredimage

`show violet_parada ot_verguenza` con un atributo que no existe pasa el lint y
revienta en runtime. `python tools/validar_sprites.py` después de tocar sprites.

### E3. Dos poses con la cabeza en otro lugar necesitan dos grupos de boca

`violet_tanga` tiene `boca` (para los cuerpos de la deseo 10) y `boca_qd30`
(para los de la 30). Una `b_hablando` sobre un cuerpo de la 30 cae al costado
de la cara. Mismo caso en `violet_magica` (frente/espalda). No mezclar.

---

## F. Motor de tiempo y triggers

### F1. `renpy.random.choice()` no se registra en el rollback

Solo `random()` queda logueado. Una elección por `choice()` puede cambiar al
deshacer y rehacer. Para sorteos que tienen que ser estables, guardarlos.

### F2. Los triggers de game_loop ahora corren una vez por TRAMO del viaje rápido

Antes corrían una vez por acción. Un trigger escrito asumiendo "una vez por
acción del jugador" ahora puede dispararse a mitad de viaje — que es lo que se
busca, pero hay que saberlo al escribir uno.

### F3. `registrar_label_locacion` no es un disparador de quest

Ya está en `japitown-content` (§4). Se repite porque fue bug de jugadores: el
registro vive en el slot único de restricción y el primer contenido que lo toca
se lleva el disparo. Para "cuando llegue a X arrancá la quest" va
`registrar_trigger_game_loop`.

---

## Cómo se agrega una entrada

Cuando un bug llegue a un jugador o a testeo y la causa sea de diseño —no un
typo—, va acá con las cuatro partes: qué pasó, por qué, la regla, cómo se
detecta. Si se puede escribir un paso del harness (`test_rutas.rpy`) o un
chequeo en `tools/`, se escribe en el mismo commit: una regla sin detector se
vuelve a romper.
