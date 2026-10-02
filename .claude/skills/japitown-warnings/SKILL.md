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

### A12. Una demanda del planificador esconde el disparador: declarar solo lo que TODOS los disparadores cumplen

**Qué pasó.** Al construir el planificador (2026-09-11) casi entra
`Rec("puerta", "violet")` como consumo *de vida* de deseo 25 — el override de
puerta es de su fase 1, no de toda la quest. Declarado así, `quest_lista_para_boton`
escondía todas las opciones de puerta de Violet (01_b, 02_a, 03_a, 05_b…) los
días que deseo 25 esperaba al jugador. Y una demanda `npc:violet en=casa_hviolet`
en una quest con botón "en cualquier lado" + opción de puerta esconde el botón
cada vez que Violet no está en su cuarto.

**La regla.** La capa 2 evalúa las demandas adentro de `quest_lista_para_boton`,
o sea en **todos** los disparadores de la quest. Un `Rec("npc", …, en=…)` va
solo si todos coinciden con ese lugar y hora. Un consumo se declara *de vida*
solo si dura toda la quest; lo que impone una restricción (reloj, locaciones,
celular, acciones, override de puerta de una fase) no se declara — el
planificador lo lee de la restricción activa. Y `duenio=` siempre que la quest
tenga restricción: sin él se mide contra la suya.

**Cómo se detecta.** `validar_bloqueos.py`, chequeo "planificador desalineado"
(sin declaración, rutina sin consumo, consumo con `en` sin rutina) y la ruta
`planificador` del harness. En consola: `planificador_estado()` muestra qué
quest está "bloqueada (capa 2)" y por qué.

---

### A13. Una reserva del planificador no puede cerrarle la puerta a su propia secuencia

**Qué pasó.** (0.1.9.1, reporte de jugador, 2026-09-15.) Sinceridad (deseo 30,
`violet_deseo_06`) reserva a Violet esa noche (`Rec("npc", "violet", horario=2,
reserva=True)`) y entra a su pieza **golpeando la puerta común** (ventaja
`puerta_dejar_pasar_noche` del hito de deseo 20; no tiene opción ni override de
puerta propios). `obtener_bloqueo_golpe` contestaba con el texto de cualquier
reserva vigente, también la de la quest en curso. Resultado: reloj congelado
por la reserva, restricción de la fase 1 cerrando todo lo demás
(`npcs_interactuables=["violet"]`, sin dormir ni avanzar) y en la única puerta
que quedaba, "Le dije a Violet que iba esta noche". Ninguna capa lo vio porque
cada pieza hacía lo suyo: el bloqueo era la suma.

**La regla.** Un efecto que impone una quest en curso (reserva, restricción,
bloqueo) **nunca puede cerrar el camino que esa misma quest necesita**. Para la
reserva: la de slot no bloquea el golpe (la secuencia puede entrar por ahí);
solo la de vida lo hace, y las quests de vida traen su propio override de
puerta (09_a). Al declarar `reserva=True` en una quest cuya secuencia pasa por
una puerta, mirar cómo entra: si es por el flujo común, no puede haber nada
que lo tape en ese slot.

**Cómo se detecta.** Paso "reserva" de la ruta `planificador` del harness
(`obtener_bloqueo_golpe` tiene que dar None con reserva de slot y texto con
reserva de vida). En juego: los escenarios del controlador
(`jp_escenario(...)`) y el panel en vivo, que muestra las reservas vigentes.

---

### A14. Dos quests que se sostienen el bloqueo mutuamente (deadlock)

**Qué pasó.** (Auditoría 2026-09-15, potencial, no reportado.) La 0_b de Mónica
pone su restricción al entrar a BOTON_LISTO (`accion_al_entrar`): bloquea
dormir y avanzar hasta que el MC vaya al living, y ese disparador pasa por
`quest_lista_para_boton` → capa 2. La 09_a de Violet arranca al dormir y
reserva a Mónica **de vida**. Si la 0_b llega a BOTON_LISTO la misma mañana en
que arranca la 09_a (Mónica 0_a completada el día anterior), la reserva escondía
el disparador de la 0_b y la restricción de la 0_b bloqueaba el dormir que la
09_a necesita para avanzar sus tres días. Ninguna de las dos podía terminar.

**La regla.** Un bloqueo que una quest sostiene **hasta que pase X** exige que X
no dependa de otra quest que a su vez espere ese bloqueo. En el motor: (1) la
dueña de la restricción activa salta la capa de conflicto
(`_pl_duenia_de_la_restriccion`): su salida no la esconde nadie; (2) toda quest
con `Disp("dormir")` declara `Rec("accion", accion="dormir")`, así una
restricción ajena que bloquea dormir la hace esperar en vez de arrancar encima.
Al agregar una restricción desde `accion_al_entrar`, preguntarse qué otra quest
puede nacer o activarse mientras dura, y qué le pasa a su salida.

**Cómo se detecta.** Paso "reserva" de la ruta `planificador` del harness (0_b
de Mónica con su restricción puesta no queda frenada por la reserva de vida; la
09_a con esa restricción ajena sí espera).

---

### A15. Cerrar una locación es un bloqueo: la abre una flag, y esa flag la apaga alguien

**Qué pasa.** (Capacidad nueva del 2026-09-22, preventivo: todavía no la usó
ninguna quest.) El contenido puede cerrar **una** locación con
`registrar_bloqueo_locacion(locacion_id, condicion, mensaje)` (lo consulta
`accion_bloqueada_movimiento` antes de la restricción). Es la herramienta
correcta para "el mundo abierto menos el sótano, porque Violet sigue con las
amigas" — mucho mejor que una restricción con las otras 17 locaciones en la
whitelist. Pero **no tiene un `desactivar_` que avise**: la salida es que la
condición deje de ser verdadera, y si nadie apaga esa flag la locación queda
cerrada para el resto de la partida. Es la versión por locación de A5.

**La regla.** La condición de un bloqueo de locación se apaga **sí o sí** por un
camino que el jugador va a recorrer igual: al completar la quest, al dormir, al
cambiar el horario. Nunca por entrar a la locación bloqueada (eso es un soft
lock puro), y nunca por una acción opcional. Y como cualquier bloqueo, el
mensaje tiene que decir por qué no se puede, no solo que no se puede.

**Cómo se detecta.** `tools/validar_bloqueos.py`, chequeo 9: lista las
condiciones de `registrar_bloqueo_locacion` cuyas flags no se apagan en ningún
lado. En el harness, el paso "bloqueo de locación registrado" de la ruta
`restriccion` verifica que cierre solo la suya y que se suelte al apagar la
condición.

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

### B5. Borrar una función de módulo que quedó guardada impide ABRIR el save

**Qué pasó.** (Sentry S12, jugador real, 0.1.9.1, 2026-09-15.) Un save guarda los
callables por **referencia**: el pickle anota `store` + el nombre, no el código.
`condicion_aparicion_evento01_violet` (el evento del casco VR) se borró en
0.1.8.6, y al abrir un save que lo tenía, `getattr(store, nombre)` falló:
`AttributeError` adentro de `renpy.load` → pantalla de error, sin poder cargar.

**La regla.** Al **borrar o renombrar** una función de módulo que pueda haber
quedado en un objeto guardado (condición de Event/Skin/EstadoTalk/GrupoMensajes,
texto callable de ConfigEtapa, `ConfigFallo.condicion`), su nombre viejo va a
`JP_NOMBRES_MUERTOS` (`core/utils/compat_nombres_muertos.rpy`), que lo declara
como stub inerte. El control de generaciones **no** cubre esto: corre en
`after_load`, o sea después del unpickle.

**Cómo se detecta.** Comparar los `def` de la última versión publicada contra los
de hoy (`git ls-tree -r --name-only <rev> game/script/` menos los actuales) y
stubbear lo que desapareció. En juego: cargar un save de la versión publicada.

---

### B6. Borrar un `.rpy` deja una bomba en las instalaciones viejas

**Qué pasó.** (Sentry S14, escritorio, 2026-09-17.) Un jugador descomprimió la
0.1.9.1 encima de su carpeta de 0.1.8.x. `tl/english/script/ui/hud/hud_relaciones.rpy`,
borrado en agosto, seguía en su disco; Ren'Py lo cargó, tradujo "Desbloqueos"
dos veces y el juego no arrancó. Cualquier `.rpy` viejo suelto puede hacer
esto, o peor: registrar labels, screens o quests que ya no existen.

**La regla.** **Al borrar un `.rpy` del proyecto, su ruta (sin extensión) va a
`JP_ARCHIVOS_VERSIONES_VIEJAS`** en `core/utils/limpieza_instalacion.rpy`. Esa
lista es lo que el juego borra del disco al arrancar (`init -999`, escritorio,
nunca en developer) antes de reiniciarse limpio. Renombrar un archivo es
borrar uno: la ruta vieja también va.

**Cómo se detecta.** `git log --diff-filter=D --name-only --format="" --
"game/**/*.rpy" | sort -u` contra la lista: todo lo que salga ahí y no exista
hoy tiene que estar listado.

---

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

### D5. Texto con tags de Ren'Py no pasa por `.format()`

**Qué pasó.** (Sentry S15, 2026-09-19.) El aviso de "Partida incompatible" se
armaba con `renpy.translate_string("{size=+8}Partida incompatible{/size}…
({version})").format(version=config.version)`. `str.format` lee `{size=+8}`
como un campo → `KeyError: 'size=+8'`. El mensaje **nunca se pudo mostrar desde
que existe**, en ningún idioma: el jugador veía la pantalla de error en vez del
aviso.

**La regla.** Un texto que lleva tags de Ren'Py (`{size=…}`, `{color=…}`,
`{b}`, `{/i}`) **no se pasa por `.format()` ni por `%`**. Para interpolar, va
`.replace("{placeholder}", valor)`, que no le pide nada al texto. Escapar las
llaves (`{{size=+8}}`) funciona pero obliga a que el `old` de la traducción
lleve el escape, y se rompe al primer retoque.

**Cómo se detecta.** `tools/validar_traducciones.py`, chequeo "format() sobre
tags de Ren'Py": parsea cada `translate_string(...).format(...)` **en los dos
idiomas** — una traducción puede traer un tag que el original no tenía, y ahí
el crash sale solo en inglés.

---

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

### E4. `Animation()` / `anim.TransitionAnimation` no se usan: animaciones por frames en ATL

**Qué pasó.** (Sentry S13, web, 2026-09-17.) Las capas de agua de la ducha de la
08_a estaban hechas con `Animation(...)`, la API legacy de Ren'Py, que por
debajo arma un `TransitionAnimation`. Su `render()` recorre los frames y, si el
tiempo que le llega no cae en ninguno (un reloj NaN/inf del navegador), **se cae
del bucle y devuelve None**: "`TransitionAnimation.render() must return a
Render`", pantalla de error en medio de la escena.

**La regla.** Toda animación por frames se escribe en **ATL** (`image x:
"f1" pause 0.05 "f2" ... repeat`, con `alpha`/`xoffset` como propiedades y `with
Dissolve(...)` si hace falta fundido entre frames). ATL siempre dibuja el frame
actual, pase lo que pase con el reloj. `Animation()` y `TransitionAnimation`
quedan prohibidos.

**Cómo se detecta.** `grep -rn "Animation(" game/script` tiene que dar cero
fuera de comentarios.

---

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

### F4. Un bucle largo de script dispara el watchdog de Ren'Py: va en Python

**Qué pasó.** (Sentry S11, variante precarga: 0.1.8f y otra vez 0.1.9.1, un
jugador nuevo en su primera carga.) El bucle de precarga del splash era un
`while` de Ren'Py con `pause 0.01` adentro, ~15.000 statements. El watchdog
(`check_infinite_loop`) revienta cada 1000 statements si pasaron >50 s desde el
último frame. Con la pestaña congelada por el navegador, la `pause` en curso
volvía con el plazo vencido y los tres statements hasta la siguiente `pause`
corrían sin refresco: si el contador cruzaba el 1000 ahí, pantalla roja.
`renpy.not_infinite_loop(30)` por lote no lo cubría: cada `pause` vuelve a fijar
el plazo en 50 s (asignación, no máximo).

**La regla.** Un bucle de cientos de vueltas **no se escribe en statements de
Ren'Py**: va en un solo bloque `python:` con `renpy.pause(...)` adentro. Un
bloque Python es UN statement para el watchdog, dé las vueltas que dé.
`not_infinite_loop` queda para bucles cortos que no pueden moverse a Python.

**Cómo se detecta.** En Sentry, el fingerprint de "Possible infinite loop" lleva
ahora el archivo del juego: un issue nuevo con ese mensaje dice dónde está el
bucle. En código: un `while` de Ren'Py con `pause` adentro es sospechoso por
definición.

---

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
python tools/validar_bloqueos.py       # reloj, runtime, puerta, triggers, dueño, rutina, planificador, prestados
```

Más el harness in-game (`jp_test_correr("mensajes")`, `"registros"`, `"planificador"`,
`"guardado"`) para lo que solo se puede probar con el motor corriendo, y el panel
del controlador en vivo (`jp_panel_controlador()`,
`tools/controlador/panel_controlador.rpy`) para VER por qué una quest está
bloqueada, reservada o esperando.

## Cómo se agrega una entrada

Cuando un bug llegue a un jugador o a testeo y la causa sea de diseño —no un
typo—, va acá con las cuatro partes: qué pasó, por qué, la regla, cómo se
detecta. Si se puede escribir un paso del harness (`test_rutas.rpy`) o un
chequeo en `tools/`, se escribe en el mismo commit: una regla sin detector se
vuelve a romper.
