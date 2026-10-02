# Amor 35 — esquema mecánico

Cómo se arma la quest del lado del motor, antes de escribir una sola línea de
diálogo. La narrativa está en [`plan_amor_35_50.md`](plan_amor_35_50.md).

**La quest está implementada** (2026-09-22): `amor/violet_amor_35.rpy`, más la
fila en `quests_amor_violet.rpy` y la declaración en `planificacion_violet.rpy`.
Falta la narrativa — el diálogo de la escena es un esqueleto provisorio y está
marcado como tal en el archivo. Las dos capacidades que la quest pedía (reserva
del MC, sección 4, y bloqueo de una locación, sección 8) también están hechas.

**Lo que cambió al implementarla**, contra lo que decía este esquema:

- **El chat NO es prioritario.** Un prioritario sin responder bloquea dormir y
  avanzar, y acá el jugador tiene otro camino para dejarlo obsoleto —bajar al
  sótano—: quedaría un bloqueo vivo cuya salida ya no existe (E10). Lo que
  frena el reloj es la reserva del MC, que era el efecto que se buscaba.
- **El trigger de la escena acepta las fases 0 y 1**, y también la trasnoche.
  El chat es un aviso, no una llave: si el jugador baja sin leerlo, la escena
  corre igual. Sigue habiendo **un solo disparador**, bajar al sótano.
- **La reserva la toma el trigger del aviso**, no `activar_quest`: la reserva
  normal nace al activarse la quest, o sea al bajar, y para entonces ya no
  protege nada. Y **se libera al terminar la escena** — si quedara puesta,
  congelaría el reloj justo cuando la salida de la quest es dormir.
- **La reserva es sólo del MC y va sin `dia`.** Una reserva sobre el MC frena a
  cualquier quest ajena, así que no hace falta reservar también a Violet. Y sin
  `dia`, porque con dos días posibles `planificador_reservar` tomaría el próximo
  viernes aunque hoy sea sábado; el día ya lo garantiza el trigger.
- **Los triggers no usan `quest_lista_para_boton`.** Ese predicado corre la capa
  2 entera, que exige el mundo tal como lo piden las demandas —incluido el MC ya
  en el sótano—, así que el aviso nunca se mandaría; y la escena, que es la
  única salida de la noche reservada, no puede depender de que Violet siga
  disponible. Los conflictos igual se chequean: el motor pasa por
  `planificador_trigger_permitido` antes de evaluar un trigger con `quest_id=`.

---

## 1 · Identidad de la quest

| | |
|---|---|
| **Id** | `violet_amor_07` |
| **Nombre / descripción** | a definir al escribir (se ven en el panel de Pistas) |
| **Línea** | `LINEA_AMOR` · umbral **35** |
| **Encadena de** | `violet_amor_06` (la de 30, "¿Qué me pongo?") |
| **Hito** | **no** — según el plan los dos hitos van en 40 y 50 |
| **Se registra en** | `_VIOLET_AMOR_QUESTS` de `amor/quests_amor_violet.rpy`, fila `(7, 35, nombre, descripcion, "violet_amor_06")` |
| **Archivo propio** | `amor/violet_amor_35.rpy` |

La fábrica `_crear_quest_amor_violet` ya pone el `Requisito("amor", …, valor=35)`,
`dias_espera=0` y los textos genéricos de las dos etapas.

---

## 2 · Cuándo puede pasar

**Viernes o sábado, de noche.** Una juntada nocturna entre semana no cierra, y
acotarlo a dos días le da al controlador algo concreto que esperar.

Índices: lunes 0 … **viernes 4**, **sábado 5**, domingo 6 (los mismos que usa
amor 25 con `dia=6`).

El controlador ya soporta "uno de estos dos días" con **dos Recs**: si hay Recs
con slot y ninguno rige en el momento actual, `_pl_mundo_detalle` devuelve *"No
es el momento"* como **tiempo**, no como lugar — o sea que la guía lo muestra en
verde ("Disponible"), porque solo hay que esperar. Es exactamente lo que
queremos: la quest no está interrumpida, está esperando el fin de semana.

---

## 3 · Fases

Una sola quest con flag, igual que amor 25 (`va25_fase`) y deseo 30
(`vd30_fase`):

```
default va35_fase = 0
```

| Fase | Estado | Cómo sale |
|---|---|---|
| **0** | Lista, esperando viernes o sábado a la noche con todo libre | Llega el mensaje de Violet → **1** |
| **1** | Lo llamaron al sótano | Baja al sótano → corre la escena → **2** |
| **2** | La escena pasó. **Violet sigue en el sótano con las amigas y el sótano está cerrado** | Al dormir → se completa la quest |

**La quest NO se completa al terminar la escena.** Se completa a la mañana
siguiente, con un trigger de dormir. El motivo es mecánico: `completar_quest()`
**restaura la rutina del NPC**, así que si se completara al salir de la escena,
Violet volvería a su habitación de inmediato y no podría "seguir con las
amigas". Manteniéndola viva en fase 2, su `rutina_quest` la sostiene en el
sótano la noche y la trasnoche.

---

## 4 · Reserva del MC — implementada

**Lo que se quiere:** que la quest, antes de mandar el mensaje, valide que **el
MC no está tomado por otra cosa esa noche**, y que al activarse **lo reserve**,
para que ninguna otra quest ni mensaje prioritario se meta en el medio.

Hoy la reserva existe **solo para NPCs**: `planificador_reservar` filtra
`d.tipo != "npc"`, y las entradas son `{quest_id, npc, dia_total, horario,
texto}`.

### Alcance propuesto

**Un tipo de `Rec` nuevo: `Rec("mc", dia=…, horario=…, reserva=True)`.** No se
reutiliza `Rec("npc", "mc")` porque el MC no está en `sistema_npcs`: no tiene
locación propia consultable por `obtener_npc`, ni disponibilidad, ni rutina, y
todo el camino de NPC (`_pl_npc_en`, `npc_disponible`, `npc_esta_oculto`)
reventaría o daría falso.

Los cuatro puntos a tocar:

1. **`rec_cubre`** — `mc` cubre `mc`.
2. **`planificador_reservar`** — aceptar `d.tipo == "mc"` y guardar la reserva
   con `npc="mc"`. La estructura del dict no cambia.
3. **`_pl_conflicto_activacion`** — una reserva ajena sobre `"mc"` **bloquea
   cualquier quest**, no solo a las que lo declaren. Es el punto: el MC está en
   todas las escenas del juego, así que si su noche es de una quest, es de esa
   quest. (La propia dueña ya queda exenta: el bucle saltea
   `res["quest_id"] == quest.id`.)
4. **Mensajes prioritarios** — `_puede_entregarse` consulta la reserva del MC
   antes de entregar un prioritario ajeno; si está tomado, el mensaje va a
   espera y se reintenta. Sin esto, "que no nos trabe un evento prioritario" no
   se cumple.

### Efectos secundarios a tener en cuenta

- **Congela el reloj.** `planificador_bloqueo_reloj()` devuelve el texto de
  cualquier reserva de slot vigente, así que reservar al MC frena dormir,
  avanzar, ver TV, etc. En esta quest es lo que queremos (que no se saltee la
  noche con el mensaje sin leer). Pero es una consecuencia automática: **toda
  quest que reserve al MC va a congelarle el reloj al jugador** hasta que la
  escena pase.
- **⚠️ La lección de E10 y E11.** Una reserva no puede cerrar el camino que la
  propia quest necesita, y dos bloqueos no se pueden sostener entre sí. Acá la
  salida es bajar al sótano, que ninguna reserva toca. Al implementarlo hay que
  sumar un paso a la ruta `planificador` del harness: **con el MC reservado, la
  quest dueña sigue pudiendo activarse y las demás no**.
- **Alcance deliberadamente acotado**: la reserva del MC frena **quests y
  prioritarios**. No toca el talk, ni las ventajas, ni el menú de los NPCs. Si
  se quisiera eso también, es otra decisión.

### Cómo se consulta desde el contenido

`planificador_mc_reservado_por()` devuelve el `quest_id` de la quest que lo
tiene tomado, o `None`. Es lo que mira el trigger antes de mandar el mensaje —
la capa 2 del controlador ya lo usa sola, pero los triggers no pasan por la
parte momentánea.

---

## 5 · El disparo: Violet lo llama

**Mensaje de Violet** ("bajá al sótano, no anda el proyector"), de un paso y una
sola respuesta. **No es prioritario**: ver la cabecera. El reloj lo congela la
reserva del MC, que el mismo trigger toma al mandar el mensaje.

El aviso se manda **una sola vez** (`disparar_por_trigger` no reentrega un grupo
ya disparado). Si la noche se pierde, la quest vuelve a esperar el próximo
viernes pero el mensaje no vuelve: por eso la **pista del panel** dice dónde y
cuándo, y es la red de seguridad de la quest.

El trigger que lo entrega (game_loop, con `quest_id=`) chequea:

- quest lista (`quest_lista_para_boton`) y `va35_fase == 0`
- **día viernes o sábado** y **horario noche**
- Violet disponible y no oculta
- **el MC no reservado** por otra quest esa noche

⚠️ Los chequeos de día y horario van **también dentro de la función del
trigger**, no solo en las demandas: `planificador_trigger_permitido` gatea por
conflictos, pero a propósito **no mira la parte momentánea** (hay triggers de
contador que tienen que correr fuera de su momento).

Al completarse el chat → `va35_fase = 1`.

---

## 6 · La escena

**Entrada**: trigger de game_loop con `locacion_actual == "casa_sotano"` y
`va35_fase == 1` → `violet_amor_35_sotano`.

**Puesta en escena**:

| | |
|---|---|
| Fondo | `bg_casa_noche_sotano.jpg` (existe) |
| Posiciones | `grupo3_izq` / `grupo3_centro` / `grupo3_der` para las tres chicas, `mc_izquierda` para el MC — el mismo transform de cuatro personajes de la intro y del final de amor 25 |
| Profundidad | la da el orden de los `show`: el último queda al frente |
| Sprites | `violet_parada`, `zowie_parada`, `leah_parada`, `mc_parado_base`, con `b_hablando` / `b_none` alrededor de cada línea |

**Estructura de la escena** (tres tramos):

1. Los cuatro en escena: no anda el proyector, el MC dice que lo revisa.
2. **El MC sale de escena** (`hide mc_parado_base`) y **sigue hablando desde
   afuera**: las líneas de `mc` se muestran igual, con su nombre en el textbox,
   pero sin sprite. Es gratis de producir y da la sensación de que está atrás
   del mueble. Las tres chicas siguen en pantalla y hablan entre ellas.
3. El MC **vuelve a entrar** y la charla sigue un poco más.

**Salida**: el MC se va, `mover_a_locacion("casa_living")`, `mostrar_hud()`,
`jump game_loop`. Queda libre.

⚠️ **Zowie tiene cuatro poses y Leah cinco**: a Zowie le falta `c_rbase_idea`.
Si la escena la necesita, hay que pedir el asset antes de escribir.

---

## 7 · La elección del jugador — SE FUE (2026-09-28)

El esquema preveía un punto de decisión —**cómo responde a la insinuación de
Zowie** (seguir / esquivar / cortar)— guardado en `va35_respuesta_zowie`, que la
quest de 40 leería para medir el tamaño del reproche.

**La escena final no lleva elección**, y el flag **se sacó entero** en vez de
dejarlo fijo en un valor. El motivo es de mantenimiento, no de diseño: un flag
que nadie elige es deuda invisible — cuando la elección se rediseñe, lo más
probable es construir encima sin acordarse de que estaba ahí.

**El puente a la 40 no se perdió: dejó de ser un flag y pasó a ser la escena.**
Zowie lo invita delante de Violet (*"Cuando quieras ver una película con alguien
me puedes invitar"*), Leah se suma, Violet se pone territorial (*"Ese es un
asunto de él"*) y el MC les agradece. El reproche de la 40 cita **eso**, que el
jugador vio pasar — es material más concreto que un string.

Si la elección vuelve, el lugar natural es la respuesta a *"Bueno, entonces te
puedes quedar"*, y ahí se decide qué flag hace falta.

---

## 8 · Después de la escena: el sótano cerrado

En fase 2, hasta el día siguiente:

- **Violet sigue en el sótano** la noche y la trasnoche → lo sostiene su
  `rutina_quest`, que sigue viva porque la quest no se completó.
- **El sótano queda bloqueado** con un mensaje propio: *"Violet sigue con las
  amigas, mejor no molestarlas"*.

### El bloqueo de locación — hecho (2026-09-22)

Hasta ahora `accion_bloqueada_movimiento` **solo** consultaba la whitelist de la
restricción activa, y esa whitelist tiene **un único mensaje para todos los
destinos**: para cerrar el sótano había que o listar las otras 17 locaciones en
`locaciones_permitidas` (una lista que se desactualiza sola, y que ocupa el slot
global de restricción varias horas por un bloqueo de un solo destino) o dar un
texto genérico. Se eligió la opción A: sumarle al motor el registro que faltaba,
como el que ya existía para las acciones y para el golpe de puerta.

```python
registrar_bloqueo_locacion("casa_sotano", _va35_sotano_cerrado,
                           "Violet sigue con las amigas, mejor no molestarlas")
```

Vive en `core/quests/restriccion_quest_system.rpy`, al lado de
`registrar_bloqueo_accion` / `registrar_bloqueo_global`, y lo consulta
`accion_bloqueada_movimiento` **antes** de mirar la restricción (es más
específico: nombra una locación y trae su propio texto). Vale con restricción
activa o sin ella, y cubre los tres caminos de entrada porque todos pasan por
esa función: hotspot MOVE (`movesystem_validation`), viaje rápido —que corta el
recorrido en el tramo bloqueado— y el handler de puertas/baños
(`npcsystem_interactions`).

Como siempre: el bloqueo solo lo sostiene la condición de la quest, que se apaga
al completarla. Cubierto por el último paso de la ruta de test `restriccion`
("bloqueo de locación registrado"), que verifica que cierra **solo** la suya y
que se suelta apenas la condición da False.

### El cierre

Trigger de **dormir, fase "despues"**: si `va35_fase == 2`, completa la quest y
apaga el bloqueo del sótano. Al completar, el motor restaura sola la rutina de
Violet.

---

## 9 · Declaración en el controlador

En `quests/planificacion_violet.rpy`:

```python
declarar_planificacion("violet_amor_07",
    disparador=Disp("locacion", nota="después de que Violet te escriba"),
    de_corrido=True,
    demandas=[Rec("npc", "violet", dia=4, horario=2, en="casa_sotano", reserva=True),
              Rec("npc", "violet", dia=5, horario=2, en="casa_sotano", reserva=True),
              Rec("mc", dia=4, horario=2, reserva=True),
              Rec("mc", dia=5, horario=2, reserva=True),
              Rec("locacion", en="casa_sotano"),
              Rec("celular")],
    consumos=[Rec("npc", "violet", dia=4, horario=2, en="casa_sotano"),
              Rec("npc", "violet", dia=4, horario=3, en="casa_sotano"),
              Rec("npc", "violet", dia=5, horario=2, en="casa_sotano"),
              Rec("npc", "violet", dia=5, horario=3, en="casa_sotano")])
```

- **`de_corrido=True`**: la narrativa fija un momento, así que ninguna otra
  quest nace ni se activa encima esa noche.
- **`reserva=True`** en Violet y en el MC: toman el slot de esa noche y frenan
  el reloj.
- **Los consumos incluyen la trasnoche**, porque en fase 2 Violet sigue ahí.
- **`Rec("celular")`**: el disparo pasa por el chat.
- **`duenio`**: la quest no necesita restricción; el sótano se cierra con
  `registrar_bloqueo_locacion` (punto 8).

---

## 10 · Archivos a tocar

| Archivo | Qué |
|---|---|
| `core/quests/planificador.rpy` | tipo `Rec("mc")`, reserva del MC, conflicto (punto 4) — **hecho** |
| `core/messages/messagesystem_core.rpy` | `_puede_entregarse` consulta la reserva del MC — **hecho** |
| `core/quests/restriccion_quest_system.rpy` | `registrar_bloqueo_locacion` + el hook en `accion_bloqueada_movimiento` (punto 8) — **hecho** |
| `core/utils/test_rutas.rpy` | pasos nuevos: reserva del MC (ruta `planificador`) y bloqueo de locación (ruta `restriccion`) — **hecho** |
| `amor/quests_amor_violet.rpy` | fila `(7, 35, …)`, rutina del sótano, textos de la etapa y tope provisorio a 40 — **hecho** |
| `amor/violet_amor_35.rpy` | **nuevo**: flags, condiciones, triggers, grupo de chat, escena y cierre — **hecho** (diálogo provisorio) |
| `quests/planificacion_violet.rpy` | la declaración de arriba — **hecho** |
| `interaction/interactions_violet.rpy` | `violet_amor_07` a `_VA_SIN_BOTON` — **hecho** |
| `tl/english/…` | pistas, mensaje del sótano y chat — **hecho**; el diálogo de la escena, al escribirlo |

---

## 11 · Lo que hay que mirar antes de cerrar

- **El tope de stat.** Hoy, completada la quest de 30, no queda ninguna quest de
  la línea sin completar → **el amor no tiene tope y sube hasta 100**. Al sumar
  las cuatro vuelve a haber topes en 35/40/45/50, y **un jugador que ya tiene el
  amor arriba de 35 va a ver las quests nuevas dispararse una tras otra**. No
  está roto; hay que decidir si se acepta.
- **El hito de amor 40 "Próximamente"** (`violet_hito_amor_04`) es hoy un
  marcador sin `quest_id`. Cuando exista la quest de 40 hay que convertirlo en
  hito real o moverlo a 60.
- **Un solo disparador**: el trigger de locación del sótano. El chat solo cambia
  la fase. Si además se le pusiera botón en el menú de Violet, uno de los dos
  quedaría inalcanzable (caso real: la 04_b).
- **`registrar_trigger_game_loop`, nunca `registrar_label_locacion`** para
  disparar la escena: el segundo vive en el slot global de la restricción activa
  y cualquier otro contenido lo pisa (regla F3).
- **Las acciones y listeners, siempre en `actions_catalog.rpy` en init**, nunca
  en runtime, si la escena llega a necesitar alguna.
- **Qué pasa si el jugador nunca baja al sótano.** Con el reloj congelado por la
  reserva no puede dormir ni avanzar, así que la única salida es bajar — que es
  lo correcto. Pero conviene verificarlo en juego: es justo la forma del soft
  lock de E10.
