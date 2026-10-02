# Amor 45 — esquema mecánico

Cómo se arma la quest del lado del motor, antes de escribir diálogo. La
narrativa está en [`plan_amor_35_50.md`](plan_amor_35_50.md) (sección "Amor 45 —
La regla de la casa") y el banco de variantes en
[`ideas_amor_45.md`](ideas_amor_45.md).

**La parte mecánica está implementada** (2026-09-22): `amor/violet_amor_45.rpy`,
más la fila y las rutinas en `quests_amor_violet.rpy`, la declaración en
`planificacion_violet.rpy` y `violet_amor_09` en `_VA_SIN_BOTON`. **Falta el
contenido**: el diálogo de los ocho tramos. La lista completa está en la
cabecera del archivo de la quest, bajo "LO QUE FALTA".

**Es la más simple de las cuatro del lado mecánico y la más cara del lado
narrativo.** Una sola escena continua, sin fases, sin bloqueos y sin sistemas
nuevos: el jugador entra al frente de la casa una mañana y no vuelve a tener el
control hasta que termina, ya de tarde y en la cocina. Todo el trabajo está en
el diálogo de cuatro personajes.

> ## ⚠️ El disparo del plan, tal como está escrito, no puede ocurrir NUNCA
>
> El plan pide **Mónica fuera de la casa** y **Jasmine en su habitación**, por la
> mañana. Las rutinas base dicen otra cosa:
>
> | | Lun–Vie | Sábado | Domingo |
> |---|---|---|---|
> | **Mónica** (mañana) | cocina | living | cocina |
> | **Jasmine** (mañana) | cocina | su habitación | cocina |
> | **Violet** (mañana) | cocina | su habitación | cocina |
>
> Mónica **nunca** está fuera por la mañana, y Jasmine está en su habitación
> sólo el sábado — justo el día en que Mónica está en el living. O sea: cero
> días posibles. Una quest declarada así se queda esperando para siempre, en
> verde, sin que nada la desbloquee.
>
> **La quest tiene que declarar las rutinas que arman esa mañana** (§4). Es la
> misma regla que ya cobró otras veces: *si la escena necesita a alguien en un
> lugar a una hora, la quest lo pone ahí* (regla A9 del skill de advertencias,
> chequeo 6 de `validar_bloqueos.py`).

---

## 1 · Identidad

| | |
|---|---|
| **Id** | `violet_amor_09` |
| **Nombre / descripción** | a definir al escribir (se ven en Pistas) |
| **Línea** | `LINEA_AMOR` · umbral **45** |
| **Encadena de** | `violet_amor_08` (la de 40, "La solicitud") |
| **Hito** | **no** (recomendado) — ver §7 |
| **Se registra en** | fila `(9, 45, nombre, descripcion, "violet_amor_08")` |
| **Archivo propio** | `amor/violet_amor_45.rpy` |
| **Tope provisorio** | pasa de 45 a **50** |

---

## 2 · Sin fases: una escena continua

Las tres quests anteriores tienen flag de fase porque el jugador recupera el
control en el medio. **Acá no.** Del frente a la cocina, el paquete, el pedido,
el comentario de Mónica, la regla, Jasmine y el corte pasan sin devolverle el
control ni una vez.

Consecuencias, todas buenas:

- **No hace falta restricción ni `duenio`.** Nada que bloquear: el jugador no
  puede irse a hacer otra cosa porque nunca tiene el turno.
- **No hace falta `registrar_label_locacion`.** El movimiento frente → cocina lo
  hace el label con `mover_a_locacion`, como en la 30 y la 35.
- **Un solo flag** y es de salida, no de control: la elección del tramo 6b.

```python
default va45_permiso = None    # "acepta" | "empuja"
```

Es lo que la quest de 50 va a leer, igual que la 40 lee la de la 35 y esta puede
leer `va40_acuerdo`.

---

## 3 · El disparo

**Trigger de game_loop** con `quest_id="violet_amor_09"`:

- `_va45_lista()` — viva y en `ETAPA_BOTON_LISTO` (el predicado propio, no
  `quest_lista_para_boton`: ver la 35 y la 40)
- `locacion_actual == "casa_frente"`
- `horario_actual == 0` (mañana)
- **`not repartidor_presente`** — ver el riesgo de §9

Devuelve el label de la escena; el `quest_id=` hace que el motor pase por
`activar_quest` antes de saltar.

`Disp("locacion")`, igual que la 30 y la 35.

---

## 4 · Las rutinas — lo que hace posible la escena

`_VIOLET_AMOR_RUTINAS[9]`, las cuatro franjas de la mañana, los siete días:

```python
_VIOLET_AMOR_RUTINAS[9] = {
    "rutina_quest": {
        (dia, 0): RutinaQuest(locacion="casa_cocina") for dia in range(7)
    },
    "rutinas_adicionales": {
        "monica":  {(dia, 0): RutinaQuest(locacion="fuera") for dia in range(7)},
        "jasmine": {(dia, 0): RutinaQuest(locacion="casa_hjasmine") for dia in range(7)},
    },
}
```

- **Violet en la cocina**: ya es su rutina base seis de siete días; la rutina la
  cubre también el sábado, que es cuando estaría en su pieza y el tramo 2 ("se
  suma a acomodar") no cerraría.
- **Mónica fuera**: `"fuera"` es el valor que el motor entiende como "no está en
  casa" (`tracker_locacion_npc` lo traduce a `None` y desaparece del mapa). Es
  lo que hace verdadera su llegada con el paquete.
- **Jasmine en su habitación**: para que entre a la cocina al final viniendo de
  algún lado, y no estuviera ahí desde el principio.

**Sprites: los dos idles existen**, así que la rutina no necesita declararlos.
Violet en la cocina por la mañana es su rutina visual base, y Jasmine en su
habitación por la mañana ya está registrada para el sábado
(`idle_jasmine_casa_hjasmine_manana_…`, posición `(527, 976)` en
`definition_jasmine.rpy`). Como la rutina de quest no trae sprite propio, el HUD
cae en la rutina visual base — que para Jasmine sólo tiene esa entrada el
**sábado**. O sea: **de lunes a viernes y el domingo, Jasmine en su habitación
por la mañana se dibujaría con el idle de la cocina**. **DECIDIDO: se usa el
idle del sábado los siete días** — dándolo en la `RutinaQuest`:

```python
"jasmine": {(dia, 0): RutinaQuest(
    locacion="casa_hjasmine",
    sprite="images/characters/casa/idle/idle_jasmine_casa_hjasmine_manana_rutinabase_grupobase_skinbase.jpg",
    posicion=(527, 976),
) for dia in range(7)},
```

Es la misma regla que en la 35: **el sprite va siempre que se mueve a un NPC de
donde lo pone su rutina base**, salvo que se pueda demostrar que nadie lo va a
ver. Acá sí se lo puede ver: la habitación de Jasmine es visitable, y la quest
la deja ahí todas las mañanas mientras espera.

### El costo de esas rutinas — DECIDIDO (2026-09-22)

**Van los 7 días** (opción A). Mientras la quest espera el disparo, la cocina se
queda sin Mónica ni Jasmine todas las mañanas: es un cambio visible del mundo
por tiempo indefinido.

**Se acepta a propósito.** La quest se dispara la primera mañana que el jugador
salga al frente, que es algo que hace seguido; y si no lo hace, es su decisión
— la quest está en el panel de Pistas diciéndole dónde y cuándo. La ausencia
además tiene lectura narrativa: Mónica salió temprano y vuelve con el paquete.

Queda descartada la alternativa de acotarla a un solo día de la semana: hacía
esperar hasta seis días por una escena que no depende del día.

---

## 5 · La escena, tramo por tramo

| Tramo | Dónde | Quiénes | Qué pasa mecánicamente |
|---|---|---|---|
| 1 · El paquete | `casa_frente` | MC, Mónica | Fondo de la locación actual; Mónica entra a escena |
| 2 · A la cocina | → `casa_cocina` | MC, Mónica, Violet | `mover_a_locacion("casa_cocina")` + `scene expression` con fade; Violet se suma |
| 3 · El pedido | cocina | los tres | Sin mecánica: es el punto en que se los ve funcionando |
| 4 · El comentario | cocina | los tres | — |
| 5 · Mónica se va | cocina | MC, Violet | `hide monica_parada` |
| 6 · La regla | cocina | MC, Violet | — |
| **6b · El permiso** | cocina | MC, Violet | **`menu:` → `va45_permiso`** |
| 7 · Entra Jasmine | cocina | los tres | `show jasmine_parada` |
| 8 · Cierre | cocina | — | `avanzar_horario()` + `completar_quest_actual` |

**Cuatro personajes en escena**: Mónica y Jasmine son **prestadas** y van
declaradas como demanda (§6) — el chequeo 8 del validador cruza los labels con
la declaración y las reclama si no están.

**El cierre avanza el horario a la tarde**: `$ avanzar_horario()` al final del
label, que es como lo hacen amor 10 y amor 20. No va por
`ConfiguracionRetorno` — la fábrica de la línea arma el suyo
(`avanzar_dia=False`) y no acepta uno propio sin tocarla.

⚠️ **Orden del cierre**: primero `avanzar_horario()` y después
`completar_quest_actual()`, o al revés — hay que decidirlo con una regla: al
completar, el motor **restaura las rutinas**, así que si se completa antes de
avanzar, las tres vuelven a su rutina base de la tarde en ese mismo instante.
Recomendado: **completar primero, avanzar después**, y que la última línea de
Mónica sea compatible con donde la rutina base la deja a la tarde (el living).
Si se quiere que quede en su habitación "haciendo cosas del trabajo", eso es una
rutina más (`(dia, 1)` para Mónica) y deja de ser gratis.

---

## 6 · Declaración en el controlador

```python
declarar_planificacion("violet_amor_09",
    disparador=Disp("locacion"),
    de_corrido=True,
    demandas=[Rec("npc", "violet", horario=0, en="casa_cocina"),
              Rec("npc", "monica", horario=0, en="fuera"),
              Rec("npc", "jasmine", horario=0, en="casa_hjasmine"),
              Rec("locacion", en="casa_frente", horario=0)],
    consumos=[Rec("npc", "violet", horario=0, en="casa_cocina"),
              Rec("npc", "monica", horario=0, en="fuera"),
              Rec("npc", "jasmine", horario=0, en="casa_hjasmine")])
```

- **`de_corrido=True`**: la escena fija un momento y se lo toma entero. No lleva
  `reserva` — no hay nada que proteger entre dos tramos, porque no hay dos
  tramos.
- **Los consumos son las tres rutinas**: es lo que exige el chequeo 7 (una quest
  con `rutina_quest` declara el consumo `npc` correspondiente).
- **Sin `duenio`** y sin bloqueos: no hay restricción.
- Las demandas son las mismas que las rutinas garantizan. Esa redundancia es a
  propósito: la rutina arma el mundo y la demanda es lo que la capa 2 verifica
  antes de dejar activar. Si alguna vez la rutina se saca, la quest no se
  dispara en un mundo incoherente — se queda esperando, que es lo correcto.

---

## 7 · ¿Lleva hito?

El plan tentativo pone los hitos en 40 y 50, pero deja abierto que esta se lo
gane: es donde cambia **cómo se juega**.

**POSTERGADO (2026-09-22): los hitos de la tanda se deciden después**, con la
50 ya escrita. Mientras tanto la 45 no lleva. Las razones para que quede así:

1. **La mecánica que la quest enseña ya existe y ya está activa.** Las dos
   ventajas de beso chequean que no haya nadie en la locación desde antes. La 45
   no *desbloquea* nada: le pone nombre a algo que el jugador ya vivió. Un hito
   promete un desbloqueo.
2. **Cambiar el hito mueve tres cosas**: el marcador "Próximamente" de 50 pasa a
   60, el tope provisorio cambia, y la 50 —que sí cierra la rama— se queda sin
   el suyo o se necesita un hito más. Es el tipo de cambio que conviene hacer
   una vez y con la 50 ya escrita.

Si igual se quiere, el lugar natural es una ventaja tipo **"Sé cuándo"**: que el
panel de Desbloqueos liste la regla, con el texto explicando que las
interacciones íntimas piden estar a solas. Sería la primera ventaja del juego
que documenta una mecánica en vez de habilitarla.

---

## 8 · Un arreglo barato que esta quest justifica

La condición de "no hay nadie más" está **escrita dos veces**:
`_violet_beso_hay_companiia()` en `beso_violet.rpy` y
`_violet_beso_deseo_hay_companiia()` en `beso_deseo_violet.rpy`, idénticas.

**HECHO (2026-09-22).** Se extrajo a un helper único:

```python
npc_a_solas(npc_id)   # ui/hud/hud_tracker.rpy
```

Las dos ventajas de beso ahora preguntan `if not npc_a_solas("violet"):`, y la
45 va a usar el mismo predicado para la regla que Violet enuncia. Está en
`hud_tracker.rpy` y no en `core/`, pegado a `tracker_locacion_npc`, porque esa
es la fuente de verdad de "se puede ubicar al NPC" —la que no cuenta a los que
una restricción escondió— y no tenía sentido separarlas. Cuando la regla cambie
(y la 50 puede cambiarla), cambia en un solo lugar.

---

## 9 · Riesgos a mirar

- **El repartidor** (resuelto). El frente por la mañana es exactamente donde y
  cuándo entrega el repartidor (`repartidor_presente`, timesystem). Dos escenas
  de paquete encimadas en la misma locación es confuso y puede encabalgar dos
  contenidos. **El trigger cede**: si hay repartidor, no dispara y espera a la
  mañana siguiente.
- **El eco de Jasmine.** Ofrecerse a cocinar con el MC justo después de la quest
  de los celos puede leerse como otra chica acercándose. Es un gag buenísimo si
  es a propósito (Violet lo registra sin decir nada) o ruido si no lo es. Hay
  que decidirlo **antes** de escribir el tramo 7, no después.
- **La cocina vacía mientras la quest espera** (§4).
- **Jasmine dibujada con el idle equivocado** si la `RutinaQuest` no trae
  sprite (§4). Es un error silencioso: no rompe nada, se ve mal.
- **`va40_acuerdo` puede ser `None`** en partidas que vengan de antes de la 40.
  Si la 45 lo lee, necesita camino para eso.
- **Cuatro personajes en pantalla**: el transform `grupo3_*` está pensado para
  tres NPCs más el MC (se usó en la 35). Acá nunca hay cuatro NPCs a la vez
  —Mónica se va antes de que entre Jasmine—, así que alcanza; pero conviene
  verificarlo al montar el tramo 7.

---

## 10 · Lo que hay que decidir antes de escribir

**Cerradas el 2026-09-22:** las rutinas las declara la quest (§4), el idle de
Jasmine es el del sábado los siete días (§4), el trigger cede ante el repartidor
(§9), el helper único ya está hecho (§8) y el hito se decide después (§7).

**Las que quedan se resuelven al escribir la narrativa** (decidido el
2026-09-22): ninguna de las tres cambia la mecánica, así que la quest se puede
armar sin ellas y el diálogo las cierra cuando se escriba.

1. **Qué plato pide.** La pizza ya se usó en la 0_b y en la 04_d4.
2. **Si la elección del 6b es la única**, o si además hay una menor cuando ella
   le pide que cocine (aceptar de una / chicanearla antes).
3. **Si Violet acota el alcance de la regla** cuando el jugador pregunta ("¿y si
   estamos solos en la cocina?"). Es la forma más barata de enseñar la mecánica.
4. **Si va un `tutorial "..."` después de la escena** — el Character ya existe
   (`config_globals.rpy`) y lo usa la poción de conquista.
5. **Qué pasa con Jasmine después**: corte inmediato (más limpio) o se queda.
6. **Dónde queda Mónica a la tarde** (§5).
7. **Hito sí o no** (§7).

---

## 11 · Archivos a tocar

| Archivo | Qué |
|---|---|
| `amor/violet_amor_45.rpy` | **nuevo**: flag, predicado, trigger, la escena entera y el cierre — **hecho** (diálogo pendiente) |
| `amor/quests_amor_violet.rpy` | fila `(9, 45, …)`, `_VIOLET_AMOR_RUTINAS[9]`, textos de etapa y tope a 50 — **hecho** |
| `quests/planificacion_violet.rpy` | la declaración de §6 — **hecho** |
| `interaction/interactions_violet.rpy` | `violet_amor_09` en `_VA_SIN_BOTON` (no tiene botón) — **hecho** |
| `ventajas/beso_violet.rpy` + `beso_deseo_violet.rpy` | (§8) el helper único — **hecho** |
| `tl/english/…` | pistas — **hecho**; el diálogo, al escribirlo |
