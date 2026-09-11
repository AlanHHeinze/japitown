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

**Y toda restricción lleva `duenio="<id>"`** (el mismo en `activar` y en
`desactivar`). Desde la auditoría 2026-09-10 el slot es **con dueño**: otro
contenido no puede **levantarla** — la llamada se ignora y avisa en desarrollo.
Activar encima sí se permite (con aviso), porque hay gates blandos que duran
días y rechazarlo dejaría a la otra quest sin su recorrido; lo que protege una
cadena en curso es A11. Antes, cualquier `desactivar_restriccion()` suelto de otra quest se
llevaba puesta la cadena de `registrar_label_locacion` ajena. Los labels de
test y cheats usan `duenio="*"`.

**Cómo se detecta.** `python tools/validar_bloqueos.py`, chequeo "restricciones
sin quien las levante".

### A6. Un mensaje prioritario con condiciones que pueden no cumplirse nunca

**Por qué.** Un prioritario entregado bloquea dormir y avanzar. Si además solo se
puede responder en cierto horario (`horario_respuesta`) y ese horario solo se
alcanza avanzando el tiempo, es un ciclo cerrado. Hoy ningún grupo usa
`horario_respuesta`, y A1 lo cubre si alguno lo usa — pero no hay que diseñar
contenido que dependa de esa red.

**La regla.** Un prioritario se entrega cuando el jugador **ya puede**
contestarlo, no antes. Las condiciones van en la entrega (`momento_horario`,
`momento_locacion`, `condicion_entrega`), no en la respuesta.

### A7. Bloquear un botón no es bloquear el efecto

**Qué pasó (0.1.9a, un jugador).** La amor 25 bloqueaba `avanzar_tiempo` de
noche para que el día terminara con la cena. Pero ver TV, entrenar y trabajar
llaman a `avanzar_horario()` por su cuenta, sin pasar por ese botón. El jugador
vio TV en fase 3, cayó en **trasnoche**, y recién ahí cocinó: el corte de luz
pasó a las 3 de la mañana. A esa hora la puerta de Violet contesta "debe estar
durmiendo" — y con dormir bloqueado por la quest y el movimiento acotado al
pasillo, no quedaba nada que hacer.

**Por qué.** Se bloqueó UNA de las entradas a un cambio de estado que tiene
varias. El comentario del propio archivo lo sabía ("el horario también lo
mueven cocinar, ver TV, entrenar, trabajar y el talk") y aun así solo se
registró el botón.

**La regla.** Antes de bloquear una acción para proteger un estado, listar
**todo** lo que muta ese estado y bloquearlo entero. Para el horario ya está
hecho: **`activar_restriccion(..., congelar_reloj=True)`** bloquea
`ACCIONES_RELOJ` entero (avanzar, dormir, ver TV, cocinar, entrenar, trabajar,
hablar, usar item — un solo set en `restriccion_quest_system.rpy`). Una acción
nueva que llame a `avanzar_horario()` se agrega a ese set y queda cubierta en
todas las restricciones. Si el reloj tiene que quedar libre a propósito (la
salida ES dormir, o ES ver TV), va la línea
`# validar_bloqueos: reloj libre — motivo` encima del `activar_restriccion`.

**Cómo se detecta.** `python tools/validar_bloqueos.py`, chequeo "reloj que se
escapa": mira qué acciones de reloj quedan **alcanzables** desde la whitelist
de la restricción (cocinar solo cuenta con la cocina permitida, hablar solo
con NPCs interactuables, etc.).

### A8. Una opción de puerta puede no llegar a dibujarse nunca

**Qué pasó.** Ver A7: la salida del corte de luz era la opción "Entrar" del
menú de puerta. Pero `interaccion_puerta_npc` chequea **trasnoche antes de
armar el menú**, y a horario 3 con deseo < 50 corta con "debe estar durmiendo".
La opción existía, estaba registrada, tenía su condición en True — y no había
forma de verla.

**La regla.** Una opción de puerta es para *ofrecer* algo. Si es la **única
salida** de una fase, no puede depender del menú: va como
`registrar_override_puerta`, que se evalúa antes que todo el flujo (trasnoche,
nivel de acceso, presencia). `violet_deseo_25`, `09_a` y ahora `amor_25` lo
usan así.

**Cómo se detecta.** `validar_bloqueos.py` lista toda `registrar_opcion_puerta`
con `ocultar_golpear=True` en un archivo sin override, para revisar.

### A9. Si la única salida es una puerta, el NPC tiene que estar detrás

**Qué pasó (0.1.9, un jugador).** En "La pizza" (04_d4) la única forma de
avisarle a Violet es la opción de puerta "Ya está la comida", de noche. Pero de
noche Violet no siempre está en su cuarto: el domingo la rutina base la manda al
living, y cualquier noche puede tocarle la ducha (25%) o salir (20%). Con la
puerta vacía y la restricción de la pizza bloqueando dormir y avanzar, no
quedaba nada que hacer. El diseño lo había decidido a propósito ("tener también
el genérico sería ofrecer dos caminos para lo mismo") — sin mirar dónde iba a
estar ella.

**La regla (obligatoria desde 2026-09-10).** Toda restricción que congela el
reloj y cuya salida necesita a un NPC en un lugar a una hora **lleva en la
misma quest la `rutina_quest` que lo pone ahí**, los siete días, con su sprite
y posición. La rutina de quest le gana a la base (el living del domingo) y a
las especiales (ducha, salida). Sin eso, "esperar a mañana" no existe: el reloj
está congelado. Modelo: deseo 25, deseo 30, amor 25, 04_d4.

**Cómo se detecta.** `validar_bloqueos.py`, chequeo "salidas por puerta de NPC
sin rutina": restricción con `congelar_reloj` + override/opción de puerta en el
archivo + quest sin `rutina_quest` en su catálogo.

### A10. `registrar_listener` / `registrar_accion` NUNCA dentro de un label

**Qué pasó (auditoría 2026-09-10).** La quest 0_b de Violet —la primera de
todas— registraba el listener de "Cocinar" en runtime, dentro de los labels de
elección. `sistema_acciones` es `define`: quien guardaba entre la elección y el
cocinar cargaba **sin listener**. "Cocinar" corría el genérico, la restricción
(sin dormir, sin avanzar, celular bloqueado, NPCs ocultos) no se levantaba
nunca. Ya había pasado con la 3_a y la 8_a, y el header de la 04_d4 lo decía
en voz alta: *"a diferencia de la 0_b, el listener se registra en init"*.

**La regla.** Ya estaba en `japitown-content`: acciones y listeners **siempre en
`actions_catalog.rpy`, en init**, con `condicion=` que lea estado guardado. Y
mejor si la condición se **deriva** de lo que ya se guarda (la quest activa, la
ruta elegida) en vez de un flag nuevo: así una partida que ya venía trabada se
destraba sola al cargar.

**Cómo se detecta.** `validar_bloqueos.py`, chequeo "registros en runtime".

### A11. Un trigger de game_loop no salta adentro de la restricción de otro

**Qué pasó.** El trigger de la 04_b mira la locación cruda de Violet (no si
está oculta) y su label arranca con `desactivar_restriccion()`. La 04_b y
evento03 viven el mismo tramo del juego: con evento03 en medio de su cadena
(NPCs ocultos, recorrido acotado), la 04_b se disparaba igual y se llevaba la
cadena puesta.

**La regla.** `registrar_trigger_game_loop(..., duenio="<id>")` — el mismo id
que la restricción de la quest. **Mientras hay una restricción con dueño
activa, el motor ignora el label de cualquier trigger de otro dueño** (el
trigger corre igual por sus efectos python). Un trigger sin dueño cuenta como
ajeno. Los triggers que tienen que poder saltar adentro de su propia
restricción (las fases de amor 25, deseo 30, mc 0_b...) declaran el suyo.

**Cómo se detecta.** `validar_bloqueos.py`, chequeo "triggers que pisan
restricciones ajenas".

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

**Ojo con las rutinas de quest.** El refresco actualiza `rutina_quest` en el
objeto Quest, y de ahí sale el **sprite** (lo lee directo). Pero la
**locación** sale de `npc.rutinas_quest`, una copia que se hace al entrar a
ETAPA_RUTINA y que el refresco no vuelve a copiar. Una partida guardada en
etapa 4 o 5 no ve una rutina agregada después. No hay re-aplicado genérico al
cargar a propósito (la 04_d5 y la 04_b levantan su rutina a mitad de camino y
volver a aplicarla las rompe): si una quest necesita que su rutina nueva llegue
a partidas ya empezadas, lo hace ella con un trigger de game_loop que la
re-aplica solo cuando falta — ver `_gl_trigger_vq4d4_rutina`.

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

## Los detectores

Tres scripts, uno por familia, todos con la misma idea: cubrir lo que el lint
no ve. Correr los tres antes de commitear contenido.

```
python tools/validar_traducciones.py   # old rotos, new vacíos, %, sin traducir
python tools/validar_sprites.py        # atributos de layeredimage
python tools/validar_bloqueos.py       # reloj, runtime, puerta, triggers, dueño
```

Más el harness in-game (`jp_test_correr("mensajes")`, `"registros"`,
`"guardado"`) para lo que solo se puede probar con el motor corriendo.

## Cómo se agrega una entrada

Cuando un bug llegue a un jugador o a testeo y la causa sea de diseño —no un
typo—, va acá con las cuatro partes: qué pasó, por qué, la regla, cómo se
detecta. Si se puede escribir un paso del harness (`test_rutas.rpy`) o un
chequeo en `tools/`, se escribe en el mismo commit: una regla sin detector se
vuelve a romper.
