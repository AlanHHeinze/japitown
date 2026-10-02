---
name: japitown-content
description: Guia unica para desarrollar y entender el juego Ren'Py Japitown. Usar siempre que se trabaje con quests, eventos, interacciones, puertas, skins, rutinas, talk, acciones de locacion, items, mensajes/chat, triggers de motor o cualquier sistema del juego.
---

# Japitown — Guía única de desarrollo

Juego Ren'Py (visual novel). **Todo el contenido nuevo va en español** (código,
comentarios, variables, diálogos, pistas). Este es EL único documento de trabajo;
reemplaza a los antiguos `creacion.md`, `funcionamiento.md`, `creacion_screens.md`
y `expresiones_referencia.md` (fusionados acá el 2026-07-31, tras la tanda de
optimización registrada en `docs/arquitectura/optimizacion.md`).

---

## 1. Reglas de oro (leer siempre)

1. **El motor NUNCA conoce contenido por nombre.** Todo lo que el contenido quiera
   enganchar en el motor (opciones de puerta, triggers de dormir/game_loop, bloqueos,
   acciones, mensajes) se hace **registrándolo en `init 5` desde el archivo del
   contenido** (ver §4). Si un sistema escucha un registro/id, está PROHIBIDO
   hardcodear después un caso especial en el motor — se agrega al registro.
2. **Stats:** los tres NPCs (violet, monica, jasmine) usan `amor` (stat1) y `deseo`
   (stat2). No existen complicidad, sumisión, adulación, provocación, madurez ni
   debilidad. `Requisito` solo acepta amor/deseo/stat/item/dinero/memoria/locacion/
   horario/dia/mensaje/npc_presente.
3. **Anti-PicklingError:** cualquier callable que quede en un objeto alcanzable desde
   una var `default` debe ser **función de módulo** (indent 4 en `init python`),
   nunca lambda cruda ni `def` anidada. Aplica a `Quest`/`ConfigEtapa`/`ConfigFallo`
   (o usar `_qc("clave_unica", lambda: ...)`), `EstadoTalk.condicion`,
   `AccionLocacion.condicion`, `Skin.condicion_desbloqueo`, `condicion_uso` de items.
   Las condiciones de los REGISTROS (§4) también van como funciones de módulo por
   consistencia. Verificación barata: ruta de test `guardado` (§9).
4. **Final de un label — `return` vs `jump game_loop`** (el error más caro del
   proyecto). Preguntá: *después de este label, ¿el caller tiene algo más que hacer?*
   - **No** → **contenido** (cierre de quest/evento/escena, devuelve al juego libre):
     `window hide` + `$ mostrar_hud()` + **`jump game_loop`**.
   - **Sí** → **subrutina** (executor de acciones, `pensar_mensaje`, label de entrada
     de locación, label de pensamiento): **`return`**.
   Detalle, casuística e historial en §3.
5. **Inicio de label narrativo:** `$ ocultar_hud()` + `window show`.
6. **Texto mostrado desde una variable → `renpy.translate_string()`.** `_()` NO
   traduce (solo marca para el extractor). En `piensa "[var]"` Ren'Py busca la
   traducción del literal `"[var]"`, nunca del contenido — traducir ANTES de asignar.
   Strings compuestos: traducir las partes antes de concatenar. Diálogo literal en el
   .rpy no necesita nada (lo cubre la traducción por id); `text _var` en un screen
   tampoco.
7. **Dos líneas seguidas del mismo personaje = cambio de boca en el medio.**
   Si no, el sprite se queda con la boca congelada mientras el jugador avanza
   el texto y la escena parece trabada. Se alterna entre sus dos bocas de
   hablar: **Violet** `b_hablando` ↔ `b_hablandochica`, **el MC** `b_hablando`
   ↔ `b_abiertachica`. Con tres líneas o más se sigue alternando. (Zowie y
   Leah tienen UNA sola boca de hablar: hasta que exista la segunda, sus
   parlamentos largos van cortados por una línea de otro personaje.)
8. **Modo posicionamiento:** TODO botón/imagebutton interactivo lleva
   `if modo_posicionamiento: action NullAction()` / `else: action ...`.
9. **IDs únicos** en todo el proyecto. Convención: `{npc}_{tipo}_{numero}` /
   `{locacion}_{elemento}_{variante}`.
10. **Assets nuevos:** fondos/CG sin alpha → JPG (calidad 90); con alpha → WebP.
   Nombres de archivo SIEMPRE ASCII (`mañana→manana`, `baño→banio`). Los nombres de
   atributo de layered image conservan la ñ (son identificadores, no archivos).
11. **Sprites de personaje van a la capa `personajes`** (tinte por horario,
    `core/utils/tinte_horario.rpy`): `show <tag>` con un tag de prefijo de
    personaje (`violet_`, `monica_`, `jasmine_`, `mc_`, …) va solo; un
    `show expression` lleva `onlayer personajes`. Los idles del HUD NO se
    tiñen (decisión: ya vienen pintados con la luz). `scene` limpia las dos capas.
12. **Cada disparador es ÚNICO:** una quest tiene UN solo disparador previsto (botón,
    puerta, locación, dormir, game_loop, item o chat). Nunca dos (un botón +
    trigger de locación deja el botón inalcanzable — caso real Violet 04_b).

---

## 2. Arquitectura y game loop

```
game/script/
├── core/                 # Motor del juego — NO lleva contenido hardcodeado
│   ├── quests/           # questsystem_core, restriccion_quest_system (embudo de
│   │                     #   bloqueos), questsystem_memories, quest_strings
│   ├── events/           # eventsystem_core, triggers_contenido (registros de
│   │                     #   triggers de dormir/game_loop/avanzar), generics
│   ├── npcs/             # npcsystem_core, npcsystem_interactions (handler de
│   │                     #   movimiento/acciones), npcsystem_interactions_basic
│   ├── talk/             # talksystem_core, _labels, _screens
│   ├── actions/          # actionsystem_core, actions_catalog, actionsystem_screen
│   ├── locations/        # locationsystem_core, locations_house, door_access_system
│   │                     #   (registros de puerta), door_relation_system,
│   │                     #   movesystem_validation, viaje_rapido
│   ├── relationships/    # relationship_unlocks
│   ├── shopping/         # shopping_system, items_shopping, usar_*
│   ├── skins/            # skinsystem_core
│   ├── time/             # timesystem_core (dormir/avanzar/autosave,
│   │                     #   REPARTIDOR_AL_IRSE), despertar_system
│   ├── messages/         # messagesystem_core
│   ├── thoughts/         # pensamiento_system
│   └── utils/            # sentry, persistencia, test_rutas, builtins, transforms
├── characters/<npc>/     # definition, chat/, interaction/ (menú + puertas_<npc>),
│                         #   quests/, events/, screens/, visual/, talk/
├── ui/                   # hud/, menus/, base/
├── tools/                # position/, celular/
└── story/                # intro
```

### El game loop (`intro_main.rpy`)

```renpy
label game_loop:
    python:                                  # drenaje anti-leak (ver §3)
        while renpy.call_stack_depth() > 0:
            renpy.pop_call()
    window hide
    $ save_name = jp_nombre_guardado()       # etiqueta "Día N" de los slots
    $ mostrar_hud()
    $ actualizar_quests()                    # avance de etapas tras CADA acción
    $ sistema_mensajes.verificar_mensajes_en_espera()
    $ validar_eventos()
    $ _gl_trigger_label = ejecutar_triggers_game_loop()   # registros (§4)
    if _gl_trigger_label:
        jump expression _gl_trigger_label
    ...
    pause
    jump game_loop
```

El HUD (`navegacion_locaciones_con_hud`) **nunca se destruye**: se controla con
`ocultar_hud()` / `mostrar_hud()`. El HUD lanza labels con `Call(...)`:
hotspot MOVE → `accion_hotspot_move` · ACTION → `accion_hotspot_action` ·
sprite NPC → `interaccion_<npc>` · acción de locación → `accion_locacion_ejecutar`.

---

## 3. Cómo termina un label — `return` vs `jump game_loop`

Equivocarse produce dos bugs opuestos y graves: `return` de más → **cierra el juego
al menú principal**; `jump` sin drenaje → **frames acumulados → crash en sesiones
largas**. El drenaje del `game_loop` (arriba) elimina el leak estructuralmente: el
game_loop es el loop raíz, nada "retorna a través" de él, así que todo frame vivo ahí
es basura. **Con el drenaje, `jump game_loop` es SIEMPRE un final válido para un
label terminal**, venga con frame o sin frame.

| Tipo | Cuándo | Final |
|---|---|---|
| **Contenido** | Cierra escena/quest/evento y devuelve al juego libre | `jump game_loop` |
| **Subrutina** | El caller sigue ejecutando lógica después | `return` |

**Ojo:** ser invocado por `call expression` NO implica `return` — muchos cierres de
quest entran así y van con `jump game_loop`.

`jump game_loop`: cierres de quest, transiciones de fase, escenas de evento, labels
disparados por triggers de game_loop/dormir.
`return`: `label_generico` de acciones, `pensar_mensaje`, labels de
`registrar_label_locacion` (el flujo de movimiento continúa), labels de pensamiento
(el flujo de dormir continúa), opciones de puerta con post-lógica.

*Historial:* 2026-07-12 se quitó el drenaje y ~22 terminales pasaron a `return` →
2026-07-27 un `return` frameless en la quest 8 de Violet cerraba el juego; se
restauró el drenaje y los terminales volvieron a `jump game_loop`. Moraleja: el leak
se arregla en el loop raíz, no obligando a cada label a acertar.

---

## 4. Los registros declarativos — LA operativa

Todo enganche contenido→motor pasa por un registro. **Registrar en `init 5`** (las
funciones-condición se definen antes, en `init python` del mismo archivo, como
funciones de módulo). El motor itera los registros; jamás se edita un archivo de
`core/` para agregar contenido.

| Qué enganchás | Registro | Se registra en | Motor que lo consume |
|---|---|---|---|
| Botón del menú del NPC | lista `_opciones_extra_<npc>` (inline) | `characters/<npc>/interaction/interactions_<npc>.rpy` | `menu_interaccion_npc_completo` |
| Opción del menú de puerta | `registrar_opcion_puerta(npc, texto, label, condicion, ocultar_golpear, tipo, quest_id)` | `characters/<npc>/interaction/puertas_<npc>.rpy` | `interaccion_puerta_npc` |
| Reemplazo TOTAL del flujo de puerta | `registrar_override_puerta(npc, condicion, label, quest_id)` | idem | idem |
| Bloqueo del golpe de puerta | `registrar_bloqueo_golpe(npc, condicion, mensaje)` | idem | idem |
| Trigger en cada vuelta del loop | `registrar_trigger_game_loop(id, funcion, prioridad, duenio, quest_id)` | archivo de la quest/evento | `game_loop` |
| Trigger al dormir | `registrar_trigger_dormir(id, "antes"/"despues", funcion, prioridad, quest_id)` | idem | `accion_dormir` |
| Trigger al avanzar horario | `registrar_trigger_avanzar(id, funcion, prioridad, quest_id)` | idem | `accion_avanzar_tiempo` |
| Bloqueo de una acción | `registrar_bloqueo_accion(accion_id, condicion, mensaje)` | idem | embudo `accion_bloqueada` |
| Cierre de UNA locación, con su propio mensaje | `registrar_bloqueo_locacion(locacion_id, condicion, mensaje)` | idem | `accion_bloqueada_movimiento` |
| Excepción al bloqueo de trasnoche | `registrar_excepcion_trasnoche(funcion)` — `fn(npc_id) → bool` | archivo de la quest/evento | `npc_durmiendo` → `npc_interactuable` |
| Label al entrar a una locación, **solo dentro de una secuencia ya en curso** (⚠ nunca como disparador de quest — ver abajo) | `restriccion_quest_activa.registrar_label_locacion(loc, label)` | label de la quest (runtime, vive en la restricción) | `accion_hotspot_move` |
| Aviso "repartidor se fue sin atender" | `REPARTIDOR_AL_IRSE.append(funcion)` | archivo de la quest | `avanzar_horario` |
| Acción de locación / interceptor | `sistema_acciones.registrar_accion(AccionLocacion(..., quest_id))` / `registrar_listener(ListenerAccion(..., quest_id))` | **`core/actions/actions_catalog.rpy`, SIEMPRE — ver abajo** | `accion_locacion_ejecutar` |
| Quest / Evento / Skin / Chat / Pensamiento | `registrar_quest` / `registrar_event` / `registrar_skin` / `registrar_grupo` / `registrar_pensamiento` | archivos del NPC | sus sistemas |
| Demandas / consumos de una quest (planificador) | `declarar_planificacion(quest_id, de_corrido, demandas, consumos, duenio)` — ver abajo | `characters/<npc>/quests/planificacion_<npc>.rpy` (`init 6`) | `planificador_puede_nacer` / `planificador_puede_activarse` |

> ### ⚠️ El disparador de una quest NUNCA va en `registrar_label_locacion`
>
> Para "cuando el jugador llegue a tal locación, arrancá la quest" va
> **`registrar_trigger_game_loop`** con una función que chequea locación + etapa.
> Nunca `registrar_label_locacion`.
>
> **Por qué:** ese registro vive dentro de `restriccion_quest_activa`, que es **un
> slot global único**. `activar_restriccion` lo reemplaza entero y
> `desactivar_restriccion` lo borra — y hay decenas de llamadas a las dos en el
> proyecto. Si además se registra desde `accion_al_entrar`, que corre **una sola
> vez** al cambiar de etapa, el primer contenido que corra después se lleva el
> disparo puesto y **la quest queda muerta para siempre** en el panel de pistas.
>
> Bug real reportado por jugadores (2026-08-20): la 0_b de Mónica no arrancaba al
> día siguiente de la 0_a. La 04_b de Violet tenía el mismo defecto y era peor,
> porque su restricción no bloqueaba nada y no daba ningún síntoma. Las dos se
> pasaron a `registrar_trigger_game_loop`.
>
> `registrar_label_locacion` **sí** sirve dentro de una secuencia en curso, donde
> el mismo contenido pone y saca la restricción y la ventana es corta (los pasos
> del tutorial de `mc_quest_0_a`, las escenas de `evento03_violet`). La regla es:
> si entre el registro y el disparo el jugador puede irse a hacer otra cosa, no
> sirve.

> ### ⚠️ TODAS las acciones de locación viven en `actions_catalog.rpy`
>
> Sin excepción, incluidas las de un sistema propio (espiar), las de una
> herramienta de dev y las de contenido parkeado. **Ningún archivo de contenido
> registra acciones**, aunque eso lo deje menos autocontenido.
>
> **Por qué:** una acción se busca por "¿qué botón aparece en esta locación?",
> no por "¿de qué quest era?". Repartidas por el proyecto había que abrir
> decenas de archivos para responder eso, y era fácil registrar dos veces el
> mismo botón en la misma locación sin notarlo.
>
> **Qué va en cada lado:** la `AccionLocacion` en el catálogo; su función de
> condición en el archivo del contenido. El catálogo corre en `init 5` y las
> condiciones en `init python` (prioridad 0), así que siempre existen antes.
>
> **Y NUNCA desde un label** (`$ sistema_acciones.registrar_accion(...)` /
> `registrar_listener(...)`). `sistema_acciones` es un `define`: no se guarda,
> así que un registro hecho en runtime desaparece al cargar la partida y deja la
> quest sin disparador. La quest solo prende y apaga un flag `default`; la
> condición registrada lo lee. Casos reales: vq3a y vq8a.

### Semántica de los triggers de motor (`triggers_contenido.rpy`)

Cada función de trigger chequea su propia condición y devuelve **un label** (el motor
hace `jump expression` — el primero que devuelve gana y corta) o **None** (hizo sus
efectos python, o no aplica, y el flujo sigue). Prioridad mayor = se evalúa primero;
determinística (no depende del orden de archivos). `ejecutar_triggers_game_loop()`
deja el id en `_gl_ultimo_trigger` (tag `gl_trigger` de Sentry, diagnóstico S11).

Fases de dormir: `"antes"` corre antes de `dormir()` (eventos nocturnos — la escena
maneja el avance del día); `"despues"` corre tras el autosave (escenas al despertar,
gestión diaria). Si un trigger "despues" devuelve label, se saltean los siguientes Y
`mensajes_al_despertar` (semántica heredada de los jumps que reemplazó).

### El embudo de bloqueos (`accion_bloqueada` en `restriccion_quest_system.rpy`)

`accion_bloqueada(accion_id)` es LA única puerta para "¿puedo hacer esto?". Consulta
en orden: (1) restricción de quest activa, (2) bloqueos declarados por events,
(3) mensaje prioritario sin responder (solo dormir/avanzar_tiempo), (4) bloqueos
registrados por contenido. Devuelve el mensaje YA TRADUCIDO o None. Los labels hacen
un solo `if` — nunca replicar chequeos de bloqueo en labels. Los `old/new` de los
mensajes del embudo viven en `tl/english/bloqueos_strings.rpy`.

### Helper estándar

`quest_lista_para_boton(quest_id)` → True si la quest está activa, sin completar, en
`ETAPA_BOTON_LISTO`, su NPC disponible **y la capa 2 del planificador la deja**
(sin reserva ajena sobre su NPC, sin consumos de otra quest que le pisen una
demanda, y el mundo como sus demandas piden: hora, lugar del NPC, lugar del MC).
Es EL predicado de todo disparador; no repetir la cadena a mano ni chequear hora
o lugar al lado — eso son demandas (ver "El planificador").

### El punto de activación — todo disparador de quest declara `quest_id`

`activar_quest(quest_id, origen)` (`questsystem_core.rpy`) es el instante en que el
motor registra que una quest pasó de "esperando al jugador" a "narrativa en curso"
(`narrativa_activa`, `activada_dia`, tag `quest_activada` de Sentry). **Lo llama el
motor, nunca el contenido**, en todos los despachadores: menú del NPC, menú de puerta
y entrada directa, override de puerta, triggers, acciones/listeners, items y chats.
Lo único que el contenido hace es **decir de qué quest es cada disparador**:

- Botón del menú del NPC: `"quest_id": "<id>"` en el dict de `_opciones_extra_<npc>`.
- Opción/override de puerta, trigger, `AccionLocacion`, `ListenerAccion`: el kwarg
  `quest_id=`. Item: la clave `"quest_id"` en `CATALOGO_ITEMS`.
- Chat de etapa (`ConfigEtapa(trigger_mensaje=...)` en `BOTON_LISTO`): nada — el
  motor le pasa el id al grupo y activa cuando el jugador lo abre.

Si el label se llama `quest_<id>` se deduce solo (mismo criterio que el tag
" (⭐ Quest)"). Un trigger que solo hace efectos python, o que salta a una escena de
ventaja/evento, no lo declara. Es idempotente: los pasos siguientes de una quest de
varios pasos pueden declararlo también (sirve para el diagnóstico) sin efecto.

Sobre esto se para el planificador: sin `quest_id` la quest nunca se "activa" y
la capa 2 no la ve. El harness (ruta `registros`, "punto de activacion: ids")
verifica que todo id declarado exista.

### El planificador — toda quest nueva declara qué necesita y qué toma

`core/quests/planificador.rpy` (diseño completo en
`docs/arquitectura/planificador.md`). Cada quest lleva, en
`characters/<npc>/quests/planificacion_<npc>.rpy` (`init 6`):

```python
declarar_planificacion("violet_deseo_06",
    de_corrido=True, duenio="violet_deseo_30",
    demandas=[Rec("locacion", en="casa_hmc"), Rec("puerta", "violet"),
              Rec("npc", "violet", horario=2, en="casa_hviolet", reserva=True)],
    consumos=[Rec("npc", "violet", horario=2, en="casa_hviolet")])
```

- **Toda quest demanda a su propio NPC**: `Rec("npc", "<npc>")` siempre va
  (una reserva sobre el NPC tiene que frenarla aunque su disparador sea una
  acción o una locación). El validador lo exige.
- **`demandas`** = lo que necesita LIBRE para jugarse. **`consumos`** = lo que
  TOMA del mundo toda su vida (sus rutinas como `Rec("npc", …, en=…)`, un menú o
  una puerta que se queda). Lo que impone una restricción mientras está activa
  (reloj, locaciones, celular, acciones) NO se declara: se lee de la restricción.
- **`de_corrido`** es narrativo: "esta noche", "ese domingo", "está enferma
  ahora". Decide si las demás la respetan al nacer (capa 1). Una quest que
  tolera esperar días y después no tolera interrupciones se **parte en dos**
  (deseo 30 → 06 + 07).
- **`duenio`** = el id de `activar_restriccion(duenio=...)` de la quest, si
  tiene una.
- **`disparador=Disp(tipo, texto, nota)`**: cómo se dispara (`boton`, `puerta`,
  `locacion`, `encuentro`, `dormir`, `accion`, `item`, `chat`, `repartidor`,
  `auto`). Con él, **el "qué hacer" de BOTON_LISTO lo escribe el controlador**
  (`planificador_que_hacer`): opción, con quién, dónde y cuándo, a partir de las
  demandas — "Usar la opción «Preguntar por el cosplay» con Violet estando en la
  Cocina por la mañana con Jasmine en la casa". El texto propio de la quest
  queda para las fases en narrativa; una quest con texto dinámico propio (deseo
  07, amor 20) no declara `Disp`. La guía muestra además el **estado**
  (`planificador_estado_guia`): verde "Se puede hacer ahora", rojo con el
  motivo cuando algo EXTERNO la frena (reserva, otra quest, NPC fuera de la
  casa / no disponible / oculto / ocupado, celular); nada si solo falta ir al
  lugar o esperar el horario.
- **`Rec("mc", dia=…, horario=…, reserva=True)`** reserva **al jugador**: con
  eso, ninguna otra quest se activa en ese slot y ningún mensaje prioritario
  ajeno se entrega (y el reloj queda congelado, como toda reserva de slot). Es
  para las quests que se ganan una noche entera. Se consulta con
  `planificador_mc_reservado_por()`. No confundir con `Rec("npc", "mc")`: el MC
  no es un NPC del sistema.
- **`reserva=True`** en el `Rec("npc")` de una de corrido cuyo momento es
  concreto: al activarse toma el slot y el reloj no pasa. **`reserva="vida"`**:
  el NPC es de la quest hasta completarla (09_a: Violet y Mónica), el reloj
  corre. Con cualquiera de las dos, el NPC solo ofrece las interacciones de esa
  quest: en su menú y su puerta quedan las opciones con ese `quest_id` y nada
  más (ni Hablar, ni eventos, ni ventajas). **Golpear solo lo bloquea la
  reserva de vida**: con reserva de slot el golpe sigue su flujo normal, porque
  la secuencia que la puso puede entrar por ahí (Sinceridad; soft lock real
  E10).
- **Una quest con `Disp("dormir")` declara `Rec("accion", accion="dormir")`**:
  es su disparador, y así una restricción ajena que bloquee dormir (la 0_b de
  Mónica) la hace esperar en vez de arrancar encima. Y **la dueña de la
  restricción activa nunca queda frenada por la capa de conflicto**
  (`_pl_duenia_de_la_restriccion`): su salida es lo único que levanta la
  restricción, así que una reserva ajena no puede esconderla (deadlock E11).
- **Las demandas son LA fuente del "cuándo y dónde"** (paso A): el disparador
  no chequea hora ni lugar a mano — `quest_lista_para_boton` ya lo hace con
  las demandas, estricto (`Rec("npc", …, horario=, en=, libre=)`,
  `Rec("locacion", en=|locaciones=, horario=)`; `en="casa"` = adentro en
  cualquier lado; `libre=True` = sin ducha/salida e interactuable). En el
  disparador queda solo lo narrativo (flags, fases, chats) y lo que ninguna
  demanda expresa ("Violet en el mismo lugar que el MC", "a solas"). Un `Rec
  npc` con `en` va solo si TODOS los disparadores de la quest coinciden; las
  fases posteriores a la activación no pasan por la capa 2 y mantienen sus
  condiciones en el código.
- **El chat de etapa no activa**: es un aviso; activa el botón/puerta que viene
  después, y hasta entonces la capa 2 gatea.
- **Personajes prestados**: si en la escena habla o se muestra otro NPC, la
  quest lo demanda con `Rec("npc", "<otro>", en="casa")` como mínimo (en la
  casa y no reservado); `en=<locación>` si la escena lo necesita en un lugar
  puntual. `en` acepta una locación madre (`LOCACIONES_MADRE`, hoy "casa") y
  `"fuera"`, que es su propia madre — **no es parte de la casa**
  (`madre_de_locacion` en `viaje_rapido.rpy`).
  El validador (chequeo 8) cruza los labels con la declaración.
- Tipos: `npc` (`en`, `skin`, `animo`, `disponible`), `interaccion` (`accion=`
  opcional), `puerta`, `locacion` (demanda) / `locaciones` (consumo), `reloj`,
  `accion`, `celular`, `mensajes`. Cobertura en `rec_cubre`.

Qué pasa con eso: la capa 1 frena el nacimiento de una quest cuyos consumos le
pisen una demanda a una de corrido activa (pista "Terminar «X» primero"); la
capa 2, adentro de `quest_lista_para_boton`, esconde el disparador si otra
activa consume lo que esta demanda o el mundo no está como pide (y escribe el
motivo en el "qué hacer" cuando es un conflicto). Una quest en narrativa no se
mide. `tools/validar_bloqueos.py` (chequeo 7) avisa de quests sin declaración y
rutinas sin consumo; el harness (ruta `planificador`) prueba cobertura, capas y
reserva; `planificador_estado()` en consola dice qué espera y qué reserva, y
`jp_panel_controlador()` (`tools/controlador/panel_controlador.rpy`, también en el
menú de cheats) lo muestra en vivo por quest: capa 1, capa 2, y el mundo en dos
partes —tiempo y lugar— con OK o el motivo de cada una.

---

## 5. Sistemas del motor (cómo funcionan)

### 5.1 Tiempo — `timesystem_core.rpy`

Horarios 0-3 (Mañana/Tarde/Noche/Trasnoche), días de semana 0-6, `dias_totales`
(contador absoluto para quests), 31 días/estación.

`avanzar_horario()`: paquete del repartidor si era mañana (+ avisa a
`REPARTIDOR_AL_IRSE`) → `horario += 1` → bg con fade → rutinas NPC → fallos de quests
→ `actualizar_quests()` → mensajes en espera.

`dormir()`: horario=0, avanza día/semana/`dias_totales` → stock (lunes) →
`save_name` → resets diarios → rutinas especiales del día → rutinas →
`actualizar_quests()` → mensajes omitidos y en espera → entregas
(`repartidor_presente`) → resets de acciones → estados de talk nuevos.

**Label `accion_dormir`** (todo lo de contenido va por registros, §4):
embudo de bloqueos → paquete bloqueando → entrega de hoy → menú de Pensamientos →
animación → **recorrido de los horarios que faltan hasta la trasnoche**, de a uno
y sin que se vea (`avanzar_horario(silencioso=True)` + `_vr_interrupcion()`, lo
mismo que evalúa el game_loop: quests, mensajes en espera, eventos, triggers) —
un mensaje prioritario lo despierta en el horario en que llega ("Me despertó un
mensaje") y un trigger de game_loop que devuelve label lo despierta con esa
escena (el día no cambia) → `ejecutar_triggers_dormir("antes")` (ya en la
trasnoche) → `dormir()` → `autoguardar_partida()` (checkpoint + autosave; SOLO
se autoguarda al dormir) → `ejecutar_triggers_dormir("despues")` →
`mensajes_al_despertar`. Consecuencia para el contenido: dormir de mañana
**pasa por la tarde y la noche**; un trigger que asuma "el MC está en su pieza
a la tarde" se dispara también mientras duerme — que es lo buscado.

### 5.2 NPCs — `npcsystem_core.rpy`

`NPC(id, nombre, ...)` con `amor`/`deseo` (0-100, clamp) y `progreso` (+1 por quest).
`modificar_stat1/2` sincronizan la variable default `{npc}_{stat}`. Helpers:
`obtener_stat1/2`, `cambiar_stat1/2`, `obtener_relacion_total`,
`interactuar_con_npc`.

**Rutinas** (dónde está el NPC), por prioridad: override de evento → rutina de quest
(`npc.rutinas_quest`) → rutina especial del día (probabilística: fuera/ducha,
cooldown 2 días) → rutina base (`definition_<npc>.rpy`). Sprite/posición visuales:
pasillo (door access) → skin de quest/evento → rutina especial → rutina visual base
(`establecer_rutina_visual_<npc>`).

### 5.3 Quests — `questsystem_core.rpy`

Etapas: `1 INICIALIZACION → 2 ESPERA (dias_espera) → 3 CONDICIONES (requisitos) →
4 RUTINA (aplica rutina_quest) → 5 BOTON_LISTO → 8-9 completar()`. El avance corre en
`actualizar_quests()` (game_loop, avanzar, dormir) y `_procesar_avance_etapas` avanza
TODAS las etapas posibles en un tick (una quest sin espera ni requisitos llega a
BOTON_LISTO al toque). **La quest se queda en BOTON_LISTO mientras se juega**: el
"está jugándose" es el flag `narrativa_activa` que prende `activar_quest` (§4, punto
de activación), no una etapa. Las etapas 6 (VALIDACION) y 7 (DESARROLLO) y el
parámetro `validacion_especial` de `Quest` **ya no existen** (2026-09-11): nunca
corrieron. Las condiciones de disparo ("de noche, en su cuarto") hoy van en la
condición del disparador; van a ser las demandas del planificador.

`completar_quest_actual(npc)`: restaura rutina, aplica `retorno`, progreso +1,
dispara chat (trigger `"quest"`), inicia la siguiente (`quest_anterior == este_id`).

`Requisito(tipo, mensaje, **params)`; `ConfigEtapa(pista, que_hacer,
mensaje_despertar, trigger_mensaje, accion_al_entrar)` — textos str o callable,
traducidos con translate_string; `ConfigFallo(condicion, trigger_mensaje,
cambio_relacion, pista)` — máx 1 vez/día, solo en etapas 4-5.

**Serialización:** las quests SE GUARDAN. Funciones con `def` → referencia directa;
lambdas inline → `_qc("clave_unica", lambda: ...)` (registro reconstruido en cada
arranque, se picklea solo la clave).

Rutinas de quest: `rutina_quest={(dia,horario): RutinaQuest(locacion, sprite,
posicion)}` + `rutinas_adicionales={npc: {...}}` + `prioridad_rutina`. Vigencia
validada por locación real del NPC (fix E07). Al cargar un save, las rutinas de
toda quest viva se **reaplican** (`persistencia_sistemas`): cambiar una rutina en el
catálogo alcanza a las partidas en curso (antes la copia en `npc.rutinas_quest`
quedaba vieja).

### 5.4 Eventos — `eventsystem_core.rpy`

Estados `OCULTO → VISIBLE → ACTIVO → COMPLETADO`; tipos ESPORADICO / PERSISTENTE.
`validar_eventos()` (game_loop) los hace aparecer/activar. `condicion_aparicion` →
VISIBLE; `condicion_activacion` (None = autoactiva) → ACTIVO; `on_aparicion` corre
una vez al aparecer (útil para anclar `dias_totales`). `config_etapas` por estado.
`modificaciones`: `"rutinas"` (override de ubicación), `"fondos"`, `"bloqueos"`
(lista de acciones — las aplica el embudo §4 en TODA acción que consulte).
`completar()` limpia modificaciones y dispara chat (trigger `"event"`).

### 5.5 Talk — `talksystem_core.rpy`

Conversación diaria (1 vez/día) con 5 opciones base (`complacerla, provocarla,
escucharla, hablarle, adularla`). `EstadoTalk` = ánimo del día: `efectos` mapea
opción → `resultado_id` (`+1_amor … -1_deseo, nada` → `RESULTADO_A_STAT`).
Estados: generales (pool aleatorio al dormir), condicionales (con `condicion`),
especiales (`es_especial`, `jerarquia`, `dias_duracion`, activados con
`activar_estado_especial_npc`). `OpcionEspecialTalk` = opción extra condicional
(ítem, estado). Memoria del MC limitada por `mc_inteligencia`; `mc_carisma` ≥2
preview, ≥5 reconsiderar. Al terminar avanza el horario.

### 5.6 Acciones de locación — `actionsystem_core.rpy` + `actions_catalog.rpy`

`AccionLocacion(id, nombre, icono, locacion_id, label_generico, reseteo, condicion,
mensaje_reintento)` — `reseteo`: diario/semanal_lunes/None. `ListenerAccion` permite
a una quest interceptar una acción genérica (prioridad quest > evento > generico).
Flujo `accion_locacion_ejecutar`: listeners → (sin listeners) embudo de bloqueos →
disponibilidad → `label_generico`. **REGLA: registrar SIEMPRE en `actions_catalog.rpy`
en init 5 con `condicion` que lea flags default** — nunca registrar/sacar acciones en
labels (se pierde al cargar un save; bug real vq3a/vq8a).

### 5.7 Puertas / Door access — `door_access_system.rpy` + `door_relation_system.rpy`

`HABITACION_NPC` (habitación→npc, ÚNICA fuente — el handler de movimiento la lee),
`PASILLO_NPC`, `MENSAJES_AUSENTE`. Niveles por stats (`TABLA_ACCESO_HABITACION`):

| NPC | ingreso_noche (deseo) | ingreso_diurno (amor) | dejar_pasar | sale_pasillo |
|---|---|---|---|---|
| Violet | 50 | 50 | 30 | 10 |
| Jasmine / Monica | 50 | 40 | 15 | 0 |

Flujo `interaccion_puerta_npc`: **overrides registrados** (primer match reemplaza
todo el flujo) → trasnoche/diurno directo (con `obtener_trigger_habitacion_directo`,
que reusa las opciones registradas para no perder triggers al entrar directo) →
presencia → menú (`Golpear` + **opciones registradas** + `Volver`) → al golpear:
**bloqueos de golpe registrados** → dispatch por nivel. Todo el contenido vive en
`puertas_<npc>.rpy` (§4); el panel de Relaciones es solo informativo.

### 5.8 Restricción — `restriccion_quest_system.rpy`

`restriccion_quest_activa` (una a la vez): `locaciones_permitidas`,
`acciones_bloqueadas` (+mensajes), `npcs_ocultos`/`npcs_interactuables` (whitelist),
`celular_bloqueado`, `elementos_escena`, `labels_por_locacion`
(`registrar_label_locacion` — el label entra por `call expression` y DEBE terminar en
`return`). `activar_restriccion(duenio="<id>", ...)` /
`desactivar_restriccion(duenio="<id>")` — **el `duenio` es obligatorio** y tiene que
ser el mismo en las dos: otro contenido no puede pisar ni levantar una restricción
ajena. Para frenar el tiempo va `congelar_reloj=True` (bloquea `ACCIONES_RELOJ`
entero), nunca una lista a mano. Los triggers de game_loop de la misma quest llevan
el mismo `duenio=` en `registrar_trigger_game_loop`. **Si la salida de la
restricción necesita a un NPC en un lugar (una puerta, entrar a su cuarto), la quest
declara la `rutina_quest` que lo pone ahí a esa hora los siete días** — regla
obligatoria, sin excepciones. Todo esto lo vigila `tools/validar_bloqueos.py`; el
porqué está en la skill `japitown-warnings`.
El **embudo `accion_bloqueada`** vive acá (§4). Un bloqueo de horario/tiempo se hace
con restricción (`acciones_bloqueadas=["avanzar_tiempo", ...]`), NUNCA con ifs en el
motor de tiempo.

**Acotar el movimiento — cuál de los dos.** La restricción dice a dónde **sí** se
puede ir (`locaciones_permitidas`) con un único `mensaje_movimiento` para todo lo
demás: es lo correcto mientras dura una escena, donde el mundo se achica a unas
pocas locaciones. Para lo contrario —el mundo abierto con **una** puerta cerrada y
un motivo propio— va `registrar_bloqueo_locacion(locacion_id, condicion, mensaje)`
(§4), que `accion_bloqueada_movimiento` consulta **antes** de la restricción y vale
con restricción activa o sin ella. Listar las 17 locaciones restantes para cerrar
una sola es una lista que se desactualiza en cuanto se agrega una locación.

También vive acá el bloqueo de **trasnoche** (`npc_durmiendo`,
`registrar_excepcion_trasnoche`), que es la otra regla general sobre los NPCs y no
depende de ninguna restricción activa — ver §5.14.

### 5.9 Mensajes / Chat — `messagesystem_core.rpy`

`GrupoMensajes(id, npc_id, mensaje_inicial, pasos, trigger_id, tabla_recompensas,
horario_respuesta, momento_locacion/horario, condicion_entrega, prioritario,
accion_al_completar)`. `disparar_por_trigger(tipo, trigger_id, npc)` con tipos:
`"quest"` (al completar), `"quest_etapa"` (ConfigEtapa.trigger_mensaje),
`"quest_fallo"`, `"event"`, `"event_aparicion"`, `"manual"`. Con condiciones de
entrega queda EN ESPERA (re-evaluado en game_loop, avanzar, mover, dormir).
`prioritario=True` bloquea dormir/avanzar vía embudo y puede despertar anticipado.
`grupo_completado(id)` → para `Requisito("mensaje", grupo_id=...)`.

### 5.10 Compras e items — `items_shopping.rpy` + `shopping_system.rpy`

`CATALOGO_ITEMS[id]` = nombre, emoji, precio, dias_entrega, usable, vendible,
consumible, `condicion_uso` (función de módulo), `label_uso`, stock, reposicion.
**El stock en runtime vive en `stock_tienda` (default); NUNCA mutar
`CATALOGO_ITEMS`** (es dato de init, no sobrevive save/load). `inventario` =
`{item_id: cantidad}`. Flujo: comprar → orden con día de entrega → al dormir ese día
`repartidor_presente` → si no se atiende, paquete en habitación.

### 5.11 Skins — `skinsystem_core.rpy`

Grupos: base, entrenamiento, bikini, pijama, ropa_interior, vestidos. `Skin(id
{npc}_{grupo}_{variante}, ...)`; `skins_activos` guardable (un activo por grupo);
`rutinas_skin_grupos` mapea rutina → grupo (con condición). `desbloquear_skin(id)`
desde quests; `cuerpo_activo(npc)` → `"c_rbase"`/`"c_pijama"` (`GRUPO_CUERPO_MAP`).

### 5.12 Pensamientos — `pensamiento_system.rpy`

`registrar_pensamiento(id, npc_id, nombre, label, condicion)`. El menú de la cama
ofrece "Pensar" si hay disponibles. El label es repetible y termina en `return`.

### 5.13 Desbloqueos de relación — `relationship_unlocks.rpy`

`npc.agregar_desbloqueo(stat, umbral, icono, nombre, desc, condicion_extra,
nombre_pendiente)` — SOLO informativo (panel de Relaciones); el acceso real lo decide
`TABLA_ACCESO_HABITACION`.

### 5.14 Interacción con NPC — `interactions_<npc>.rpy` + `menu_interaction.rpy`

Clickear al NPC **SIEMPRE abre el menú** (no hay auto-disparos: se eliminaron el
2026-07-31 porque secuestraban el click y hacían desaparecer "Hablar" — bug E09).
Orden fijo del menú: **quest → evento → Hablar**. El label arma
`_opciones_extra_<npc>` (dicts `{"texto","label","condicion","tipo"?}` — el screen
agrega el tag `" (Quest)"`/`" (Evento)"` y traduce con translate_string) →
`call screen menu_interaccion_npc_completo` → `("opcion_especial", label)` →
`jump expression`.

**El click pasa por `npc_interactuable(npc_id)`** (`restriccion_quest_system.rpy`),
que evalúa en orden: (1) `npc_durmiendo()` → (2) restricción de quest activa. Si da
False, sale `mensaje_npc_bloqueado(npc_id)` como pensamiento — **pasarle siempre el
npc_id**: sin él no distingue "duerme" de un bloqueo de quest y, cuando el bloqueo es
solo por horario, no hay restricción de la que sacar texto y devuelve `""`.

**De TRASNOCHE (horario 3) ningún NPC es clickeable**: duermen y no se los molesta
(`MENSAJE_NPC_DURMIENDO`). Es regla general del juego, no de una quest — la puerta ya
lo hacía por su lado (`door_access_system` corta el trasnoche salvo con la ventaja
`puerta_ingreso_noche`, que deja **entrar** pero no hablar). Se sale del bloqueo por
dos vías, las dos declarativas:

- **ventaja** `npc_interaccion_trasnoche` — para cuando un hito habilite hablarle de
  madrugada (hoy no la otorga ninguno);
- **`registrar_excepcion_trasnoche(fn)`** — `fn(npc_id) → bool`, función de módulo,
  para el contenido que necesita la escena igual (una quest que te hace despertarla).

⚠️ **Contenido nuevo en trasnoche: sin excepción registrada el NPC no se puede
clickear.** Es el error fácil al escribir una escena de madrugada.

### 5.15 Persistencia, autosave y utilidades

- Sistemas con estado: `default sistema_x = _ps_copia_fresca("sistema_x")` +
  instancia poblada en `init 4-11`. El merge de `after_load`
  (`persistencia_sistemas.rpy`) agrega contenido nuevo a saves viejos. Agregar un
  sistema con estado = agregarlo ahí.
- Autosave SOLO al dormir (`autoguardar_partida()` = checkpoint + force_autosave;
  los 3 disparadores automáticos de Ren'Py están apagados; `has_autosave` queda
  True). Nunca meter el autosave dentro de `dormir()`.
- `config.save_dump` NUNCA se activa (crashea en este proyecto).
- Sentry manual (`sistema_sentry.rpy`): tags dispositivo/renderer/navegador/
  `gl_trigger`; dedup por sesión.

---

## 6. Recetas de creación

### 6.1 Quest

Definición en `characters/<npc>/quests/quest_<npc>.rpy`, labels en
`<npc>_quest_XX.rpy`, screens en `screens/`.

```renpy
init python:   # funciones nombradas ANTES del init 5 (picklables)
    def _pista_<npc>_qX():
        return "Mensaje de pista"

init 5 python:
    quest_<npc>_X = Quest(
        id="<npc>_questprincipal_X", npc_id="<npc>",
        nombre="Nombre", descripcion="Descripción desde el MC",
        numero_quest=X, dias_espera=4,
        quest_anterior="<npc>_questprincipal_Y",   # se inicia sola al completar la previa
        requisitos=[Requisito("mensaje", "Esperar el chat", grupo_id="<grupo>")],
        rutina_quest={(5,0): RutinaQuest(locacion="casa_h<npc>", sprite="...", posicion=(800,700))},
        retorno=ConfiguracionRetorno(avanzar_dia=False),
        config_etapas={
            ETAPA_ESPERA: ConfigEtapa(pista=_pista_<npc>_qX, que_hacer="..."),
            ETAPA_CONDICIONES: ConfigEtapa(pista="...", que_hacer="...",
                                           trigger_mensaje=("<grupo_chat>", "<npc>")),
            ETAPA_BOTON_LISTO: ConfigEtapa(
                pista=_qc("<npc>_qX_bl", lambda: "Pista {}".format(store.var)),
                que_hacer="...", mensaje_despertar="..."),
        },
    )
    sistema_quests.registrar_quest(quest_<npc>_X)
```

Label narrativo: `$ ocultar_hud()` + `window show` → escena → al final
`$ desactivar_restriccion()` (si activaste una) + `$ completar_quest_actual("<npc>")`
+ `window hide` + `$ mostrar_hud()` + `jump game_loop`.

**Disparador (elegir UNO, §4):** botón del menú NPC (6.4) · opción de puerta (6.5) ·
trigger de dormir/game_loop/avanzar (6.6) · item (`label_uso`) · chat
(`accion_al_completar`). El disparador declara `quest_id` (§4, punto de activación)
y NO chequea hora ni lugar: eso va en la declaración de abajo.

**Declaración del planificador (obligatoria)** en
`characters/<npc>/quests/planificacion_<npc>.rpy`, `init 6`:

```renpy
declarar_planificacion("<npc>_questprincipal_X",
    de_corrido=False,                       # True si fija un momento ("esta noche")
    duenio="<id de activar_restriccion>",   # si la quest activa una restricción
    disparador=Disp("boton", "Texto del boton"),   # cómo se dispara → "qué hacer" generado
    demandas=[Rec("npc", "<npc>", horario=2, en="casa_h<npc>"),   # siempre a su NPC
              Rec("puerta", "<npc>"),
              Rec("npc", "<otro>", en="casa")],                   # personaje prestado
    consumos=[Rec("npc", "<npc>", horario=2, en="casa_h<npc>")])  # = su rutina_quest
```

`tools/validar_bloqueos.py` (chequeos 7 y 8) y la ruta `planificador` del harness
avisan si falta la declaración, si no demanda a su NPC, si la rutina y el consumo no
coinciden o si otro NPC aparece en la escena sin estar demandado.

### 6.2 Evento

```renpy
init python:
    def condicion_aparicion_evXX():
        q = store.sistema_quests.obtener_quest("<npc>_questprincipal_Y")
        return bool(q and q.completada)

init 5 python:
    event_<npc>_XX = Event(
        id="<npc>_evento_XX", nombre="...", tipo=TIPO_EVENT_ESPORADICO, prioridad=10,
        condicion_aparicion=condicion_aparicion_evXX,
        condicion_activacion=None,          # None = autoactiva al aparecer
        on_aparicion=None, label_efecto=None, npc_id="<npc>", descripcion="...",
        config_etapas={
            ESTADO_EVENT_VISIBLE: ConfigEtapa(pista="...", que_hacer="..."),
            ESTADO_EVENT_ACTIVO:  ConfigEtapa(pista="...", que_hacer="...",
                                              mensaje_despertar="..."),
        },
    )
    sistema_events.registrar_event(event_<npc>_XX)
```

`mensaje_despertar` va SOLO en `config_etapas[ESTADO_EVENT_ACTIVO]` (como parámetro
suelto se dispara cada mañana). Al terminar la narrativa: `$ evento.completar()` +
cierre de contenido normal.

### 6.3 Rutina

En `definition_<npc>.rpy` dentro de `inicializar_<npc>()`:
`<npc>.establecer_rutina(dia, horario, "locacion_id")` +
`establecer_rutina_visual_<npc>([dias], horario, "sprite.png", (x, y))` (ancla
centro-inferior; ajustar con la herramienta P). Rutinas especiales:
`agregar_rutina_especial(RutinaEspecial(id, locacion, probabilidad, horarios, ...))`.

### 6.4 Botón en el menú del NPC

En `interactions_<npc>.rpy`, dentro de `label interaccion_<npc>`:

```renpy
if quest_lista_para_boton("<npc>_questprincipal_X"):      # la hora y el lugar son demandas
    $ _opciones_extra_<npc>.append({
        "texto": "Saludar",              # → old/new en botones_interaccion_strings.rpy
        "label": "mi_label_propio",
        "condicion": True,
        "quest_id": "<npc>_questprincipal_X",   # punto de activación (se deduce si el label es quest_<id>)
        # "tipo": "evento",              # solo si dispara un evento (tag "(Evento)")
    })
```

**Cada botón nuevo lleva su `old/new`** en `tl/english/botones_interaccion_strings.rpy`
(un solo `old` por texto en todo el proyecto — duplicarlo crashea).

### 6.5 Opción / override / bloqueo de puerta

En `characters/<npc>/interaction/puertas_<npc>.rpy` (crear si no existe; ver
`puertas_violet.rpy` como modelo):

```renpy
init python:
    def _puerta_<npc>_qX():
        return quest_lista_para_boton("<npc>_questprincipal_X")   # "de noche" es demanda

init 5 python:
    registrar_opcion_puerta("<npc>", "Texto del boton",
                            "label_destino", _puerta_<npc>_qX,
                            ocultar_golpear=True,          # oculta "Golpear"
                            quest_id="<npc>_questprincipal_X")
    # tipo="evento" para eventos. El ORDEN de registro es el orden del menú.
```

Override total (`registrar_override_puerta(npc, condicion, label, quest_id=)`) para
quests que manejan la puerta entera; bloqueo de golpe (`registrar_bloqueo_golpe`)
para "está dormida/ocupada" — su mensaje necesita `old/new` (patrón en el tl de
door_access_system). Con el NPC reservado por una quest, la puerta solo ofrece las
opciones de esa quest y golpear no responde (lo hace el motor).

### 6.6 Trigger de motor (dormir / game_loop / avanzar)

En el archivo de la quest/evento:

```renpy
init python:
    def _dormir_trigger_mi_quest():
        if quest_lista_para_boton("<npc>_questprincipal_X"):   # hora/lugar: demandas
            return "mi_label_al_despertar"      # el motor hace jump
        return None                              # o efectos python y seguir

init 5 python:
    registrar_trigger_dormir("mi_quest_despertar", "despues",
                             _dormir_trigger_mi_quest, prioridad=0,
                             quest_id="<npc>_questprincipal_X")
```

Igual con `registrar_trigger_game_loop(..., duenio=, quest_id=)` /
`registrar_trigger_avanzar` / `registrar_trigger_salir_celular`. El label destino es
CONTENIDO → termina en `jump game_loop`. `quest_id` es el punto de activación: con
él el motor no evalúa el trigger si la quest no está viva o la frena un conflicto.
`duenio` si la quest tiene restricción. Usar prioridad solo si el orden contra otros
triggers importa (mayor = primero). Lo que queda en la función es lo narrativo (flags,
fases) y lo que ninguna demanda expresa ("Violet en el mismo lugar que el MC").
Dormir recorre los horarios hasta la trasnoche: un trigger de game_loop que pide "el
MC en su pieza a la noche" se dispara también mientras duerme.

### 6.7 Skin

En `visual/skins_<npc>.rpy` dentro de `inicializar_skins_<npc>()`: `Skin(...)` +
`sistema_skins.registrar_skin(...)` + `establecer_grupo_rutina(npc, dias, horario,
grupo, condicion=_funcion_de_modulo)`. Otorgar: `$ desbloquear_skin("<id>")`.
Grupo nuevo con cuerpo propio → actualizar `GRUPO_CUERPO_MAP`.

### 6.8 Estado / opción de Talk

En `talk/<npc>_talk.rpy` dentro de `inicializar_talk_<npc>()`: `EstadoTalk(id,
nombre, intro, efectos={opcion: resultado_id}, mensaje, estados_posteriores)` +
agregar el id a `estados_generales_ids`. Condicional: + `condicion=funcion_modulo`.
Especial: + `es_especial=True, jerarquia, dias_duracion`; activar con
`activar_estado_especial_npc`. `OpcionEspecialTalk(id, texto, condicion, ...)` →
`opciones_especiales_<npc>`. `resultado_id` nuevo → también en `RESULTADO_A_STAT` y
`RESULTADO_TEXTO`.

### 6.9 Acción de locación

En `actions_catalog.rpy` (init 5): `sistema_acciones.registrar_accion(
AccionLocacion(id, nombre, icono, locacion_id, label_generico, reseteo,
condicion=_funcion_que_lee_flag_default))`. La quest solo prende/apaga el flag.
El `label_generico` termina en `return`. Interceptar una acción existente:
`registrar_listener(ListenerAccion(accion_id, label, nombre_menu, prioridad="quest",
condicion=..., unico=True))`.

### 6.10 Item

En `items_shopping.rpy`, entrada en `CATALOGO_ITEMS` (nombre, emoji, precio,
dias_entrega, usable, vendible, consumible, `condicion_uso` función de módulo,
instruccion_uso, label_uso, stock, reposicion). Ítem de quest: precio 0, vendible
False, stock 0. Dar: `$ inventario["id"] = inventario.get("id", 0) + 1`.
Stock en runtime: mutar `stock_tienda`, no el catálogo.

### 6.11 Chat

En `chat/chat_<npc>.rpy` (init 5): `GrupoMensajes(id, npc_id, mensaje_inicial,
trigger_id, pasos=[PasoConversacion(opciones_jugador=[OpcionRespuesta(texto,
respuesta_npc, puntos)])], tabla_recompensas=TablaRecompensas({...}))` +
`sistema_mensajes.registrar_grupo("<npc>", grupo)`. Se dispara por
`trigger_mensaje` de una etapa, al completar la quest (trigger_id == quest_id) o
manualmente. Requisito de quest: `Requisito("mensaje", "...", grupo_id=...)`.

### 6.12 Pensamiento

`init 6 python:` → `sistema_pensamientos.registrar_pensamiento(id, npc_id, nombre,
label, condicion=funcion_modulo)`. Label repetible, termina en `return`.

### 6.13 Desbloqueo de relación

`<npc>.agregar_desbloqueo(stat, umbral, icono, nombre, desc)` en
`inicializar_<npc>()`. Informativo; los umbrales reales van en
`TABLA_ACCESO_HABITACION`.

---

## 7. Screens interactivos en quests

Ejemplos reales: `violet_quest_04.rpy` + `violet_quest04_screens.rpy`. Regla
universal: todo botón verifica `modo_posicionamiento` → `NullAction()`.

**Patrón A — Overlay sobre el HUD:** screen con imagebutton transparente
(`idle Transform(img, alpha=0.0)`, `hover img`) que se auto-oculta con
`timer 0.01 action Hide(...)` si el jugador salió de la locación. Se muestra desde
un label de `registrar_label_locacion` que hace `show screen` + `return`.

**Patrón B — Screen de exploración:** botón fondo 1920x1080 `background None
action NullAction()` que absorbe clicks + imagebuttons por objeto. Interacción
simple (diálogo y volver) → `action Call("label")` (el label hace `return` y el
screen se re-evalúa). Interacción que cambia escena → `action [Hide(...),
Jump("label")]`. Salir → `[Hide, Jump("label_verificar")]`.

**Patrón C — Mini-escena con `ui.interact()`:** ocultar HUD, `scene` propio,
`show screen`, y loop:

```renpy
    $ _en_ropero = True
    while _en_ropero:
        $ _resultado = ui.interact()
        if _resultado == "pijama":
            hide screen vq4_screen_ropero
            window show
            mc "Esto necesitaba."
            window hide
            $ _en_ropero = False
        elif _resultado == "volver":
            $ _en_ropero = False
        else:
            hide screen vq4_screen_ropero
            window show
            mc "..."
            window hide
            show screen vq4_screen_ropero
```

El screen usa `action Return(...)`. El `hide screen` antes de cada diálogo que
se ve arriba **funciona pero parpadea** — para algo con muchos diálogos, ver el
Patrón E.

**Patrón D — Verificación de salida:** label que chequea el objetivo; si falta,
pensamiento + volver a mostrar el screen; si está, continuar.

**Patrón E — Minijuego** (modelo: `violet_quest_09_minijuego.rpy`). Es el
Patrón C llevado a una escena entera con muchas piezas y muchos diálogos. Los
seis puntos que costaron sangre, en orden de aparición:

1. **`zorder` negativo, NO modal.** El textbox de Ren'Py vive en zorder 0.
   Con la screen arriba hay que bajarla en cada diálogo, y en el hueco entre el
   `hide` y el `show` se ve un frame de la capa master (el fondo de la escena
   anterior): eso es el pestañeo. Con `zorder -5` el textbox queda arriba solo y
   la screen no se baja nunca. Y **sin `modal True`**: un modal se come el click
   que hace avanzar el diálogo y el texto no pasa nunca.
2. **Un flag `hablando`** para apagar lo interactivo mientras corre un diálogo.
   Es lo que reemplaza al `hide screen`: `if not vq9_hablando:` envuelve zonas y
   botones, la escena se sigue viendo y nada roba el click.
3. **El orden de los botones es el orden de dibujo.** El último hijo queda
   arriba y se lleva el click. Si la ropa se dibuja sobre los sudores, su botón
   también tiene que ir después — al revés, el botón del sudor tapado se come el
   click de la prenda que lo cubre.
4. **Alpha por pieza ⇒ NO es layeredimage.** Los atributos de un layeredimage
   solo se prenden y se apagan; no tienen opacidad individual. Si una pieza
   tiene que ir desvaneciéndose, la escena se compone en la screen con un `add`
   por pieza leyendo el estado. El layeredimage sí sirve para grupos
   excluyentes sin alpha (la boca).
5. **Los `show` van a la capa master, o sea DEBAJO de la screen.** Un
   `show vq9_boca b_hablando` no se ve. Lo que se dibuja sobre la escena de un
   minijuego se maneja como estado (`vq9_boca_estado`) y lo pinta la screen.
6. **Los botones devuelven, no llaman.** `Call(...)` desde una screen mostrada
   con `show screen` + `pause` corta ese pause, y al terminar el handler el
   flujo sigue en la línea de después — que suele ser `jump game_loop`. Con
   `Return((tipo, dato))` + `ui.interact()` el control vuelve al bucle.

**Cursor propio** (una mano, una herramienta): `config.mouse_displayable`.
Esconde el puntero del sistema y dibuja por encima de todo, textbox incluido.
Dos avisos: **no lo mueve** —lo agrega en (0,0), hay que posicionarlo con un
`Transform(function=...)` que lea `renpy.get_mouse_pos()`— y **no corre** si el
jugador activó la preferencia "cursor del sistema". Zoom, ancla y rotación van
como constantes arriba del archivo: se ajustan mirando la pantalla, no
calculando.

**Posiciones de las piezas.** `sistema_pos` **es un stub sin efecto**
(`posicionamiento_elementos.rpy`): sus métodos no hacen nada y llamarlos no
rompe pero tampoco sirve. El flujo real es la **tecla P** (`MODO_DEV`), que
tiene tres listas excluyentes:

| lista | qué muestra |
|---|---|
| **Fondos** | `images/bg/` + las bases de escena (nombre con `fondo`) |
| **Sprites** | idles de personaje, de movimiento y de quest |
| **Assets** | las piezas sueltas de quests y minijuegos |
| **Zonas** | rectángulos invisibles: se crean, arrastran y redimensionan |

Se arrastra, **Guardar** escribe en `tools/posiciones_idle.txt` (append, nunca pisa) y
de ahí se pega a una tabla en el archivo del contenido:

```python
VQ9_POS = {
    "sudor_pelo": (159, 324),
    ...
}
```

La herramienta exporta con **el mismo anclaje que usa la screen**
(`xanchor 0.0 yanchor 0.0` para todo lo que no sea idle de personaje), así que
el par se copia tal cual. Las piezas de 1920x1080 no llevan entrada: van en 0,0.

**Assets del minijuego:** con alpha → WebP; sin alpha → JPG (§1 regla 9). Las
zonas de interacción son imágenes que en el juego van invisibles
(`Transform(img, alpha=0.0)`): solo aportan su rectángulo clickeable.

---

## 8. Sprites — notación y referencia de expresiones

Layered images. Grupos de atributos: `a_` área · `ca_` cabeza · `b_` boca ·
`o_` ojos · `c_` cuerpo/ropa · `ot_` otros. Cada `show` que cambia un sprite lleva
ENCIMA un comentario semántico con solo los grupos presentes (sin `at`/`with`/
`xzoom`):

```renpy
# (Mc cuerpo base ojos base boca neutral)
show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
# (Violet boca hablando)
show violet_parada b_hablando
violet "Texto"
```

Rutas: idle `images/characters/casa/idle/idle_<npc>_casa_<loc>_<horario>_<rutina>_
<grupo>_<skin>.png` · menú skin `images/characters/casa/menu/...` · quest
`images/quest/<npc>/questX/...` · bg `images/bg/casa/bg_casa_<horario>_<loc>.jpg`.
Transiciones: `fade` (escena), `sprite_fast`/`sprite_normal` (sprite), `dissolve`.

### MC — `mc_parado_base`

**Cuerpo:** base `c_rbase_base` · asustado `_asustado` · avergonzado `_avergonzado` ·
brazos cruzados `_brazoscruzados` · celular `_celular` · confianza `_confianza` ·
enojado `_enojado` · idea `_idea` · pensando `_pensando` · señalando `_señalando` ·
victoria `_victoria` · perfume `_perfume` · mochila 1-4 `_mochila1..4` ·
regalo jasmine `_regalojasmine` · regalo violet `_regaloviolet` (+`abierto`) ·
manga yamete `_mangayamete` (+`pp`) · facepalm `_facepalm` · vr `_vr` ·
cuestionando `_cuestionando` · neutral `c_none`.

**Boca:** abierta `b_abierta` · abierta chica `b_abiertachica` · aburrida
`b_aburrida` · asustada `b_asustada` · disgusto `b_disgusto` · enojada cerrada
`b_enojadacerrada` · feliz abierta/cerrada `b_felizabierta`/`b_felizcerrada` ·
hablando `b_hablando` · molesta `b_molesta` · seria `b_seria` · triste `b_triste` ·
neutral `b_none`.

**Ojos:** base `o_base` · aburridos `o_aburridos` (+`nm`) · felices `o_felices`
(+`nm`, +`cerrados`) · asustados `o_asustados` (+`nm`) · abajo `o_abajonm` · arriba
`o_arribanm` · cerrados `o_cerrados` · disgusto `o_disgustonm` · enojados
`o_enojados` (+`nm`) · molestos `o_molestos` (+`nm`) · serios `o_serios` (+`nm`) ·
sorprendidos `o_sorprendidos` (+`nm`) · tristes `o_tristesnm` · neutral `o_none`.
(`nm` = "sin mirar".)

### MC — `mc_espalda_base`

`# (Mc espalda ...)`: brazos cruzados `brazoscruzados` · golpeando `golpeando`
(+`ruido`) · rascarse 1/2 `rascarse1`/`rascarse2`. Suele ir con `xzoom -1.0`.

### Violet — `violet_parada`

**Boca:** aburrida `b_aburrida` · bostezo grande `b_bostezogrande` · abierta/cerrada
chica `b_abiertachica`/`b_cerradachica` · contenta `b_contenta` · feliz `b_feliz` ·
gritando `b_gritandomucho` · hablando `b_hablando` (+`chica`) · mordiendo
`b_mordiendo` · sexy `b_sexy` · sonrisa cerrada/costado/leve/pequeña
`b_sonrisacerrada`/`b_sonrisacostado`/`b_sonrisaleve`/`b_sonrisapequeña` · triste
`b_triste` · neutral `b_none`.

**Ojos:** base `o_base` · abiertos `o_abiertos` · abajo/arriba `o_abajonm`/
`o_arribanm` · cerrados `o_cerrados` · dormidos `o_dormidos` · enojados `o_enojados`
· felices `o_felices` (+`nm`) · guiñando `o_guiñando` · juzgando `o_juzgandonm` ·
llorando `o_llorandomuchonm` · bostezo `o_bostezograndenm` · sexys `o_sexys` ·
tristes `o_tristes` · pensando `o_pensando` · costado `o_costadobase` · neutral
`o_none`.

**Cuerpo rbase:** base `c_rbase_base` · brazos cruzados `_brazoscruzados` · celular
`_celu` · chek `_chek` · cola `_cola` · dedo labio `_dedolabio` · enojada `_enojada`
· fuck you `_fuckyou` · gestito `_gestito` · idea `_idea` · not ok/ok `_notok`/`_ok`
· paz `_paz` · pensando `_pensando` · señalando `_señalando` · sorprendida
`_sorprendido` · tetas `_tetas` · verguenza `_verguenza` · victoria `_victoria` ·
regalo `_regalo` · neutral `c_none`.

**Cuerpo pijama:** base `c_pijama_base` · agotada `_agotada` · bostezo 1/2
`_bostezo1`/`_bostezo2` · brazos cruzados `_brazoscruzados` · rascando 1/2
`_rascando1`/`_rascando2` · escoba `_escoba`.

**Cabeza:** rbase `ca_base` · pijama `ca_pijama` · neutral `ca_none`.
**Otros:** sonrojo `ot_avergonzada`.

Mapeos rápidos: `b_none/c_none/o_none → neutral` · `ot_avergonzada → sonrojo` ·
`c_rbase_ → cuerpo` · `c_pijama_ → cuerpo pijama`. Usar `cuerpo_activo("<npc>")` al
armar escenas para no asumir la ropa.

---

## 9. Testing

Guía completa en `docs/arquitectura/testing_sistemas.md`. Harness:
`game/script/core/utils/test_rutas.rpy` — en partida descartable, consola (Shift+O):

```
jp_test_correr("registros")   # integridad de TODOS los registros del §4
jp_test_correr("guardado")    # anti-PicklingError sin necesidad de guardar
jp_test_correr_todas()        # todas las no destructivas
```

Tras crear contenido: correr `registros` (labels/condiciones registrados) y
`guardado` (callables picklables). Lint SIEMPRE tras cada edición:
`"C:/Renpy/renpy-8.4.1-sdk/lib/py3-windows-x86_64/python.exe"
"C:/Renpy/renpy-8.4.1-sdk/renpy.py" . lint` — sin
error/exception/traceback/already exists.

---

## 10. Checklists

### Nueva Quest
- [ ] `Quest(...)` + `registrar_quest()` en `quest_<npc>.rpy`; labels en archivo propio
- [ ] Cero lambdas crudas (def de módulo o `_qc`); requisitos solo con tipos válidos
- [ ] UN disparador, registrado según §4 (botón / puerta / trigger / locación / item / chat).
      Si es por locación → `registrar_trigger_game_loop`, nunca `registrar_label_locacion`
- [ ] Textos de botones nuevos con `old/new` en su archivo de strings
- [ ] `ocultar_hud()`+`window show` al iniciar; `mostrar_hud()`+`jump game_loop` al cerrar
- [ ] `desactivar_restriccion()` + `completar_quest_actual()` al finalizar
- [ ] Botones con `modo_posicionamiento → NullAction()`
- [ ] Lint + rutas `registros` y `guardado`

### Nuevo Evento
- [ ] `Event(...)` + `registrar_event()`; condiciones como funciones de módulo
- [ ] `mensaje_despertar` SOLO en `config_etapas[ESTADO_EVENT_ACTIVO]`
- [ ] `evento.completar()` al terminar; bloqueos declarados en `modificaciones`

### Cualquier registro nuevo
- [ ] Funciones-condición en `init python` (módulo), registro en `init 5`
- [ ] El label registrado existe y termina como corresponde (§3)
- [ ] Nada hardcodeado en `core/` — si el motor necesita un caso nuevo, se agrega
      un REGISTRO nuevo al motor, no un if de contenido

---

## Apéndice — Variables globales frecuentes

| Variable | Significado |
|---|---|
| `horario_actual`, `dia_semana_actual`, `dia_actual`, `dias_totales` | tiempo |
| `<npc>_amor`, `<npc>_deseo`, `<npc>_progreso` | stats guardables sincronizados |
| `inventario`, `dinero`, `stock_tienda` | economía del MC |
| `skins_activos` | `{npc: {grupo: skin_id}}` |
| `mc_inteligencia`, `mc_carisma`, `mc_personalidad` | stats del MC |
| `restriccion_quest_activa` | restricción activa o None |
| `repartidor_presente`, `paquete_en_habitacion` | entregas |
| `modo_posicionamiento` | herramienta de posicionamiento activa |
| `_gl_ultimo_trigger` | instrumentación S11 (id del último trigger de game_loop) |
