# Amor 50 — esquema mecánico

Cómo se arma la quest del lado del motor, antes de escribir diálogo. La
narrativa está en [`plan_amor_35_50.md`](plan_amor_35_50.md) (sección "Amor 50 —
El domingo solos").

**Es la más grande de la tanda por lejos.** Cinco fases, cuatro escenas, una
acción nueva, dos caminos que confluyen, una secuencia con botones y el cierre
de la rama. Y es la única que además pide **arte nuevo**.

**La parte mecánica está implementada** (2026-09-22): `amor/violet_amor_50.rpy`,
la acción Bañarse en `actions_catalog.rpy`, el layeredimage `violet_toalla` en
`sprites_violet.rpy`, más la fila, las rutinas y la declaración. **Falta el
contenido**: el diálogo de las cuatro escenas y, sobre todo, **la escena final,
que no tiene arte** — hoy hay un corte honesto que cierra la quest igual. La
lista completa está en la cabecera del archivo de la quest.

> **Cambio con la narrativa final (2026-09-30): ya no hay fase 2.** El
> despertar deja al MC acotado hasta el living (restricción `violet_amor_50`,
> reloj congelado), y la despedida sigue sola —sin devolver el control— hasta el
> pasillo de arriba y Violet saliendo en toalla. Los dos caminos de la fase 2
> (golpear su puerta o entrar al baño) se eliminaron junto con su override de
> puerta y su trigger. Las fases 3 y 4 no cambiaron. Lo que sigue en este
> documento sobre la fase 2 es historia.

**Al final no tocó el motor.** El esquema pedía un `registrar_override_banio`
para interceptar el menú del baño ocupado; al implementarlo se vio que esa vía
trababa la quest y se resolvió de otra forma (§5).

---

## 1 · Identidad

| | |
|---|---|
| **Id** | `violet_amor_10` |
| **Nombre / descripción** | a definir al escribir |
| **Línea** | `LINEA_AMOR` · umbral **50** |
| **Encadena de** | `violet_amor_09` (la de 45, "La regla de la casa") |
| **Hito** | **sí** — es el cierre de la rama (ver §8) |
| **Se registra en** | fila `(10, 50, nombre, descripcion, "violet_amor_09")` |
| **Archivo propio** | `amor/violet_amor_50.rpy` |
| **Tope provisorio** | se **borra** o pasa a 60 (ver §8) |

---

## 2 · Las fases

```python
default va50_fase = 0
```

| Fase | Estado | Cómo sale |
|---|---|---|
| **0** | Esperando el domingo | Trigger de **dormir** (`"despues"`), domingo → **1** |
| **1** | Despertó solo; ellas todavía están | Trigger de **game_loop**: entrar al living → la despedida → **2** |
| **2** | Se fueron. Violet está en la ducha | Puerta de su habitación **o** puerta del baño → la escena → **3** |
| **3** | "Date una ducha tú también" | La **acción Bañarse** del baño de arriba → **4** |
| **4** | Bañado; ella espera en su habitación | Entrar a `casa_hviolet` → la escena final → **5** |
| **5** | Terminada | — |

Cinco fases y **cada una con un disparador distinto y excluyente**: ninguna
convive con otra, que es la regla que hace que no haya dos formas de avanzar al
mismo tiempo (mismo esquema que la 25, que tiene seis).

---

## 3 · Fase 0 → 1 · El domingo

**Trigger de dormir, fase `"despues"`** — igual que amor 25:

```python
registrar_trigger_dormir("violet_amor_50_domingo", "despues",
                         _va50_trigger_dormir, quest_id="violet_amor_10")
```

Chequea quest lista + `va50_fase == 0` + `dia_semana_actual == 6`, y devuelve el
label del despertar.

⚠️ Un trigger `"despues"` que devuelve label **saltea los siguientes y también
`mensajes_al_despertar`** (semántica heredada de los jumps que reemplazó). Es
aceptable acá —el domingo de esta quest se come el resto— pero hay que saberlo.

**La escena del despertar** es corta y termina devolviendo el control: el MC
recuerda que hoy se queda solo, mira la hora y piensa que quizás todavía no se
fueron. `va50_fase = 1`, `jump game_loop`.

---

## 4 · Fase 1 → 2 · La despedida en el living

**Trigger de game_loop** con `locacion_actual == "casa_living"` y
`va50_fase == 1`.

En la escena están **Mónica y Jasmine** (prestadas): el cargador, la charla del
viaje, la pregunta por Violet ("se sentía mal"), y se van. Cierra con el
pensamiento que empuja a la fase 2 — *Violet ama ir a lo de su tía, se debe
sentir muy mal*.

**Al terminar, las dos salen de la casa de verdad**: es lo que hace cierto el
resto del día. Lo resuelven las rutinas (§7).

> **⚠️ La premisa es la misma que amor 25.** "Solos en casa" también es un
> domingo en que Mónica y Jasmine se van y Violet se queda. **Decidido: es
> callback, no repetición** — el MC lo dice en una línea en el despertar o en el
> living (*"la última vez que quedamos solos se cortó la luz"*). Si no se dice,
> se va a leer como que se repitió el recurso. Es una línea de diálogo, no
> mecánica, pero tiene que estar.

---

## 5 · Fase 2 → 3 · La ducha de Violet — los dos caminos

Los dos llegan al **mismo label**, con un flag que decide si antes va un
pensamiento extra. Un label con un flag, no dos labels.

| Camino | Cómo se engancha |
|---|---|
| **Puerta de su habitación** | `registrar_bloqueo_golpe("violet", _va50_en_la_ducha, "Violet no responde, pero escucho la ducha abierta…")` — el golpe no abre nada, solo informa |
| **Puerta del baño** | El handler de movimiento a `casa_banioarriba`: es el que dispara la escena |

### La puerta del baño — RESUELTO: el motor ya hace casi todo

Lo que el plan proponía era `registrar_label_locacion("casa_banioarriba", …)`,
como hace la 08_a. **No sirve acá**: ese registro vive dentro de
`restriccion_quest_activa`, un slot global único, y la 08_a lo usa *porque tiene
una restricción puesta*. Esta quest no tiene ninguna, y poner una sólo para
colgar el registro es al revés de como se decidió toda la tanda.

Tampoco sirve un trigger de game_loop sobre `casa_banioarriba`: **el jugador
nunca llega a entrar**. El handler de movimiento intercepta antes
(`npcsystem_interactions`): si hay un NPC en el baño, salta a
`interaccion_banio_ocupado` y abre el menú.

> ### ⚠️ DESCARTADO AL IMPLEMENTAR (2026-09-22)
>
> Poner a Violet en el baño para que el motor abriera su menú **traba la
> quest**: la fase siguiente es el MC bañándose *en ese mismo baño*, y con ella
> "adentro" el handler lo intercepta y no lo deja entrar a usar la acción.
> Sacarla a mano tampoco sirve: al cargar un save, `_ps_refrescar_quests`
> reaplica las rutinas de las quests vivas y la devuelve al baño.
>
> **Cómo quedó**: su rutina la tiene en su habitación todo el domingo y **la
> ducha es narrativa — se oye, no se modela**. Los dos caminos de la fase 2
> siguen existiendo: la puerta de su habitación es un `registrar_override_puerta`
> y el baño es un trigger de locación (el baño está vacío, así que el jugador
> entra de verdad). Con eso la quest **no necesita ningún registro nuevo en el
> motor**, y de paso "Espiar" deja de ser una decisión: no hay menú de baño.
>
> Lo de abajo queda como estaba porque explica por qué el camino parecía bueno.

**El flujo del baño ocupado ya existe entero:**

- `obtener_npc_en_banio(banio_id)` sólo mira `npc.locacion_actual == banio_id`,
  así que **alcanza con que la rutina de quest ponga a Violet en
  `casa_banioarriba`** esa mañana. Nada más.
- El menú (`menu_banio_npc`) se dibuja con el fondo del pasillo, que es
  exactamente la puesta en escena del plan: el MC afuera, ella adentro.
- Al golpear, hoy contesta *"Me estoy bañando"* — una línea **hardcodeada por
  npc_id** en `door_access_system.rpy`.

Lo único que falta es poder reemplazar esa línea por la charla de la quest
(*"¿estás bien?" / "era la oportunidad perfecta" / "ya salgo"*). Para eso va el
registro nuevo, gemelo del que ya existe para las puertas:

```python
registrar_override_banio(npc_id, condicion, label)
```

consultado por `interaccion_banio_ocupado` antes de abrir el menú (o antes de la
respuesta al golpe, según se prefiera). Son ~10 líneas, sigue el patrón del
resto del motor y de paso deja el enganche para cualquier quest futura que
quiera pasar algo en la puerta del baño. **Sería el momento de sacar de ahí las
tres líneas hardcodeadas por NPC**, que hoy son el único lugar del door access
donde el motor conoce contenido por nombre.

> **Decisión que trae de regalo:** ese menú incluye **"Espiar"** (el minijuego de
> la ducha). Con Violet bañándose a propósito y esperándolo, dejarlo disponible
> es contenido gratis y muy en tono; sacarlo es más limpio narrativamente. Hay
> que elegir — el override permite las dos.

### La salida

Violet aparece envuelta en una toalla, le dice que se duche él también y se va a
su habitación. `va50_fase = 3`.

---

## 6 · Fase 3 → 4 → 5 · La ducha del MC y la habitación

### La acción Bañarse — hay que crearla

**No existe ninguna acción de bañarse en el juego.** Se registra como cualquier
otra, en `actions_catalog.rpy` **en init**, con el patrón exacto de "cocinar" y
"ver_tv":

```python
sistema_acciones.registrar_accion(AccionLocacion(
    id="va50_banarse", nombre="Bañarse", icono=u"🚿",
    quest_id="violet_amor_10",
    locacion_id="casa_banioarriba", label_generico="violet_amor_50_ducha_mc",
    reseteo=None, condicion=_va50_banarse_visible,
))
```

`condicion` es una función de módulo que lee el flag (`va50_fase == 3`). **Nunca
registrar en runtime**: `sistema_acciones` es `define`, un registro dentro de un
label se pierde al cargar la partida y ya trabó dos quests (vq3a, vq8a).

### Que el jugador no se saltee la ducha

El plan pedía "restricción acotada o mensaje de recordatorio". **Con lo que se
sumó en esta tanda hay algo mejor**: cerrar la habitación de Violet con el
registro de la 35, sin tocar el slot de restricción.

```python
registrar_bloqueo_locacion("casa_hviolet", _va50_falta_ducharse,
                           "Primero una ducha")
```

La condición se apaga sola al pasar a la fase 4, y la salida —bañarse— está
siempre disponible: el baño de arriba está vacío (las dos se fueron) y la acción
es visible. Cumple la regla A15 sin esfuerzo.

### La habitación

Fase 4: **trigger de game_loop** con `locacion_actual == "casa_hviolet"`. Violet
en tanga, la línea del apuro (donde va **la elección del jugador**, §9), "ya
llegó el tiempo", la secuencia de beso y la escena de cama.

### La secuencia con botones

**Patrón E del skill** (modelo: `violet_quest_09_minijuego.rpy`). Los dos puntos
que más cuestan: `zorder` negativo y **sin** `modal True`, y el bucle con
`ui.interact()` devolviendo `Return(...)` en vez de llamar labels desde la
screen.

---

## 7 · Las rutinas y la declaración

Ese domingo: Violet en casa todo el día, las otras dos afuera después de la
despedida. Mismo esquema que amor 25, que ya manda a las dos afuera el domingo.

```python
_VIOLET_AMOR_RUTINAS[10] = {
    "rutina_quest": {
        # ⚠️ La FASE 2 la quiere en `casa_banioarriba` (es lo que hace que el
        # motor abra el menú del baño ocupado, §5) y la FASE 4 en su cuarto. Una
        # rutina es una tabla fija por franja, así que el cambio lo hace la
        # ESCENA moviéndola (`npc.locacion_actual = ...`), como ya hacen otras
        # quests; la rutina la deja donde termina.
        (6, 0): RutinaQuest(locacion="casa_hviolet"),
        (6, 1): RutinaQuest(locacion="casa_hviolet"),
    },
    "rutinas_adicionales": {
        "monica":  {(6, 0): RutinaQuest(locacion="casa_living"),
                    (6, 1): RutinaQuest(locacion="fuera"),
                    (6, 2): RutinaQuest(locacion="fuera")},
        "jasmine": {(6, 0): RutinaQuest(locacion="casa_living"),
                    (6, 1): RutinaQuest(locacion="fuera"),
                    (6, 2): RutinaQuest(locacion="fuera")},
    },
}
```

⚠️ **Las dos arrancan el domingo en el living** (para la despedida) y recién
después quedan `"fuera"`. Como la rutina es una tabla por franja y la despedida
pasa en la mañana, **la mañana las tiene en el living aunque el jugador todavía
no haya ido**: si entra al living, la escena salta; si no entra, están ahí
paradas. Es correcto — todavía no se fueron.

**Sprites**: Mónica en el living por la mañana no es su rutina visual base
(está en la cocina), así que **la `RutinaQuest` tiene que traer el sprite**, como
se hizo con Jasmine en la 45. Hay que verificar qué idles existen para las dos en
el living por la mañana **antes** de escribir; si falta alguno, o se pide el
asset o la despedida pasa en la cocina, que es donde las dos ya tienen idle.

```python
declarar_planificacion("violet_amor_10",
    disparador=Disp("dormir", nota="el domingo"),
    de_corrido=True, duenio=None,
    demandas=[Rec("accion", accion="dormir"),
              Rec("npc", "violet", dia=6, en="casa_hviolet"),
              Rec("npc", "monica", dia=6, horario=0, en="casa_living"),
              Rec("npc", "jasmine", dia=6, horario=0, en="casa_living"),
              Rec("accion", accion="va50_banarse")],
    consumos=[Rec("npc", "violet", dia=6, en="casa_hviolet"),
              Rec("npc", "monica", dia=6, en="fuera"),
              Rec("npc", "jasmine", dia=6, en="fuera"),
              Rec("puerta", "violet")])
```

- **`de_corrido=True`**: la quest se toma el domingo entero, como la 25.
- **Sin reserva y sin `duenio`**: no congela el reloj ni pone restricción. Lo que
  acota al jugador es el bloqueo de una locación, que es mucho más chico.
- **`Rec("puerta", "violet")`** como consumo: la quest usa su puerta (el bloqueo
  de golpe de la fase 2).

---

## 8 · El hito y el tope

Esta es **la quest que cierra la rama**, así que es donde el hito tiene sentido.
Al implementarla:

1. `violet_hito_amor_05` —que hoy es el marcador "Próximamente" que puso la 40—
   pasa a hito real con `quest_id="violet_amor_10"`, nombre, descripción y
   ventajas.
2. **Marcador nuevo en 60** con `proximamente=True`, o ninguno si se decide que
   la línea termina acá.
3. `registrar_tope_provisorio("violet", "amor", …)` pasa a 60 **o se borra** (si
   no hay más contenido, el tope sin quest siguiente deja el stat suelto hasta
   100: hay que decidirlo explícitamente).

Las ventajas siguen pendientes de la decisión general de la tanda. La candidata
obvia de esta quest es algo que use lo que la escena establece; lo que **no**
conviene es registrar ventajas sin escena detrás (regla del panel de
Desbloqueos).

---

## 9 · El arte — lo que ya hay y lo que falta

El plan la marcaba como "la más cara de la tanda en arte". **Revisando los
assets, bastante menos de lo que parecía:**

| Lo que pide la escena | Estado |
|---|---|
| Violet en la ducha | **Existe**: `violet_ducha_quest_1..6.webp` + bocas y ojos propios (quest 08) |
| Violet recién salida, mojada | **Existe**: layeredimage `violet_mojada` |
| Violet en toalla | **El arte existe** (`violet_parada_cuerpo_toalla_base.webp` + 4 bocas de toalla), pero **NO está declarado en ningún layeredimage**. Hay que armarlo — es media hora, no producción |
| Violet en tanga | **Existe**: layeredimage `violet_tanga`, con cuerpos de deseo 10 y deseo 30 |
| Secuencia de beso con quitado de ropa | **Falta**. Producción nueva |
| Escena de cama con animación simulada | **Falta**. Producción nueva, y es la más cara |

O sea: de las seis piezas, **cuatro ya están** (una a medio camino). Las dos que
faltan son las dos últimas, que son justamente las que definen el cierre — así
que siguen siendo lo que hay que dimensionar antes de arrancar.

---

## 10 · Lo que hay que decidir antes de escribir

1. **El callback a amor 25** (§4): decidido que va, falta escribir dónde.
2. **Si "Espiar" sigue disponible** en el menú del baño durante la escena (§5).
   El override permite las dos, y no es lo mismo narrativamente.
3. **Dónde pasa la despedida**: living (pide sprites nuevos) o cocina (las dos
   ya tienen idle ahí). §7.
4. **La elección del jugador**: la respuesta a *"¿estabas apurado para algo?"* es
   el lugar natural; la secuencia final ya trae botones, que es otra forma de
   decisión. Y acá se puede **leer `va45_permiso` y `va40_acuerdo`**: el jugador
   que empujó dos veces merece que ella se lo nombre.
5. **Cuánto dura el día**: si la quest ocupa la mañana entera, a qué horario
   queda el mundo al terminar y dónde queda el MC.
6. **Zowie y XGram**, que quedaron abiertos en la 40. Si no se tocan acá, quedan
   para la tanda siguiente — **que sea una decisión y no un olvido**.
7. **El voseo**: el plan trae *"date una ducha vos también"*. El juego está todo
   en tuteo neutro y hubo una pasada entera sacando el voseo: va *"tú también"*.
8. **Hito y ventajas** (§8).

---

## 11 · Archivos a tocar

| Archivo | Qué |
|---|---|
| `amor/violet_amor_50.rpy` | **nuevo**: flags, predicados, los cuatro triggers, el override de puerta, el bloqueo de locación, las cinco escenas y el cierre — **hecho** |
| `amor/quests_amor_violet.rpy` | fila `(10, 50, …)`, `_VIOLET_AMOR_RUTINAS[10]`, textos por fase y tope a 60 — **hecho** |
| `core/actions/actions_catalog.rpy` | la acción **Bañarse** (§6) — **hecho** |
| ~~`core/locations/door_access_system.rpy`~~ | descartado (§5): la quest no toca el motor |
| `quests/planificacion_violet.rpy` | la declaración de §7 — **hecho** |
| `interaction/interactions_violet.rpy` | `violet_amor_10` en `_VA_SIN_BOTON` — **hecho** |
| `visual/sprites_violet.rpy` | el layeredimage `violet_toalla` (§9) — **hecho** |
| `hitos_violet.rpy` | el hito de 50 y el marcador siguiente (§8) — **pendiente**, con los hitos de la tanda |
| `tl/english/…` | pistas, nombre de la acción y mensaje del bloqueo — **hecho**; el diálogo, al escribirlo |

---

## 12 · Riesgos

- **Cinco fases es mucho estado.** Cada una tiene su disparador y su salida; la
  que más hay que mirar es la 3 → 4, porque es la única donde el jugador podría
  quedarse dando vueltas. El bloqueo de `casa_hviolet` lo empuja, pero **hay que
  verificar en juego que la acción Bañarse sea visible** — si la condición queda
  mal, el jugador se queda encerrado fuera de la habitación sin forma de entrar,
  que es la forma exacta de E10.
- **El trigger de dormir que saltea `mensajes_al_despertar`** (§3): si hay un
  mensaje prioritario pendiente esa mañana, no se entrega. Hay que decidir si
  importa.
- **Dos quests con la misma premisa** (§4).
- **`va45_permiso` y `va40_acuerdo` pueden ser `None`** en partidas viejas.
- **La escena de cama es la única del juego con animación simulada por botones
  fuera del minijuego de la 09**: conviene releer el Patrón E entero antes de
  empezarla, no en el medio.
