# Amor 40 — esquema mecánico

Cómo se arma la quest del lado del motor, antes de escribir diálogo. La
narrativa está en [`plan_amor_35_50.md`](plan_amor_35_50.md) (sección "Amor 40 —
La solicitud") y el banco de variantes en [`ideas_amor_40.md`](ideas_amor_40.md).

**La parte mecánica está implementada** (2026-09-22): `amor/violet_amor_40.rpy`,
más la fila en `quests_amor_violet.rpy`, la declaración en
`planificacion_violet.rpy`, el botón en `interactions_violet.rpy`, el hito en
`hitos_violet.rpy` y el texto de XGram en `hud_celular.rpy`. **Falta el
contenido**: el diálogo de las dos escenas y del chat. La lista completa de lo
que queda está en la cabecera del archivo de la quest, bajo "LO QUE FALTA".

No pidió capacidades nuevas del motor: triggers de game_loop, botón propio en el
menú, grupo de mensajes, `registrar_conversacion_mensajear(forzada=True)`,
trigger de salida del celular y el sistema de hitos ya existían.

**Las decisiones abiertas se tomaron por la recomendación de cada sección**, y
son reversibles: el chat lo abre el MC (Mensajear forzada), la charla cara a
cara pasa donde ella esté, la solicitud se acepta sola (con el flag guardado),
XGram queda narrada pero con el texto del botón cambiado, y el celo sale del
detalle cronometrado de la 35. La única que queda de verdad pendiente es si
"qué la hace admitir el celo" pasa a ser una elección del jugador (§10.5).

Lo que sí toca por primera vez desde hace tiempo es el **hito**: la 40 convierte
el marcador "Próximamente" en un hito real, y eso arrastra el tope del stat y
las ventajas.

---

## 1 · Identidad

| | |
|---|---|
| **Id** | `violet_amor_08` |
| **Nombre / descripción** | a definir al escribir (se ven en Pistas) |
| **Línea** | `LINEA_AMOR` · umbral **40** |
| **Encadena de** | `violet_amor_07` (la de 35, "Las amigas") |
| **Hito** | **sí** — `violet_hito_amor_04`, hoy "Próximamente" |
| **Se registra en** | fila `(8, 40, nombre, descripcion, "violet_amor_07")` de `_VIOLET_AMOR_QUESTS` |
| **Archivo propio** | `amor/violet_amor_40.rpy` |

---

## 2 · Una sola quest con fases, no dos encadenadas

El plan dejaba abierto si la solicitud y la charla eran dos quests (patrón
04_b → 04_c). **La respuesta es una sola quest con un flag de fase**, como la 25
y la 35, por tres razones concretas:

1. **La línea es una quest por umbral.** La fábrica `_crear_quest_amor_violet`
   arma el `Requisito("amor", valor=umbral)` a partir de la fila, y el hito
   referencia **una** `quest_id`. Dos quests para el mismo umbral 40 obligarían
   a inventar una excepción en las dos cosas.
2. **El tope del stat se mueve con el hito.** Con dos quests hay que decidir
   cuál lo otorga, y la otra queda como una quest fantasma en el panel.
3. **04_b → 04_c son dos momentos con días en el medio y disparadores
   distintos**; acá la solicitud y la charla son la misma escena partida por la
   decisión del jugador de ir a buscarla.

```
default va40_fase = 0
```

| Fase | Estado | Cómo sale |
|---|---|---|
| **0** | Llegó a 40 de amor; esperando la noche | Trigger de game_loop → la escena de la solicitud → **1** |
| **1** | Zowie agregada. Queda hablar con Violet | Botón propio en su menú → la charla cara a cara → **2** |
| **2** | Ella se fue a mitad de la charla | El chat (ver §5) → **3** |
| **3** | Chat terminado | Trigger de salida del celular → cierre, hito y quest completa |

**Ninguna fase bloquea nada.** El jugador puede tardar los días que quiera entre
la 1 y la 2, y entre la 2 y la 3. Es lo contrario de la 35 —que se jugaba en una
noche y por eso reservaba al MC— y hace que la quest no tenga ninguna forma de
trabarse: las tres salidas (un botón, un chat, cerrar el celular) están siempre
disponibles.

---

## 3 · Fase 0 → 1 · La solicitud

**Trigger de game_loop**, con `quest_id="violet_amor_08"`, que chequea:

- `_va40_lista()` — viva y en `ETAPA_BOTON_LISTO` (el predicado propio de la 35:
  no `quest_lista_para_boton`, que corre la capa 2 entera)
- `va40_fase == 0`
- **es de noche** (`horario_actual == 2`) y **no es la misma noche** en que la
  quest llegó al umbral → un contador con `dias_totales`, como hace la 09_b
- el celular no está bloqueado (`celular_esta_bloqueado()`)

Devuelve el label de la escena. Como el trigger lleva `quest_id=`, el motor pasa
por `activar_quest` antes de saltar: **ese es el punto de activación de la
quest**, y desde ahí queda `narrativa_activa`.

**La escena** (corta, sin devolver el control en el medio): fondo de la locación
actual (`scene expression locacion_actual.background`, como la 30 y la 35), el
MC en `center`, saca el celular, ve la solicitud de Zowie, la acepta, piensa una
línea y vuelve. `va40_fase = 1`, `jump game_loop`.

> **⚠️ El "esté donde esté" es real:** la escena tiene que funcionar con
> cualquier fondo y sin ningún NPC en escena. Nada de mostrar a Violet ni de
> asumir que está en su cuarto.

### La solicitud en XGram — dos costos

| | Qué es | Costo |
|---|---|---|
| **A. Narrada (recomendada)** | La solicitud se ve en el diálogo/pensamiento del MC. La app sigue como está. | Cero. Ninguna UI nueva. |
| **B. Con pantalla** | XGram deja de narrar "Contenido en desarrollo" y muestra una screen con la solicitud y un botón Aceptar. | Una screen nueva, su estado y su traducción. |

Recomiendo **A**, con un agregado de una línea: que el botón XGram, una vez
aceptada la solicitud, narre otro texto en vez del de "en desarrollo" (hoy es un
`Call("narrar_mensaje", ...)` fijo en `hud_celular.rpy`; pasarlo a una función
que elija el texto según el flag). Si no, el jugador acepta una solicitud y
abre la app para ver a Zowie y se encuentra con el cartel de siempre.

**El flag de la aceptación se guarda igual** (`va40_solicitud = "aceptada"`)
aunque hoy no sea una elección: si más adelante se quiere la rama de rechazarla,
el dato ya está en los saves viejos.

---

## 4 · Fase 1 → 2 · La charla cara a cara

**Botón propio en el menú de Violet**, en `interactions_violet.rpy`, con el
patrón de los que ya hay:

```python
$ _opciones_extra_v.append({"texto": "Preguntarle por Zowie",
                            "label": "violet_amor_40_charla",
                            "condicion": True,
                            "quest_id": "violet_amor_08"})
```

Dentro del `if` que ya chequea la quest, más `va40_fase == 1`.

> **⚠️ `violet_amor_08` va en `_VA_SIN_BOTON`.** Si no, aparece ADEMÁS el botón
> genérico "Charlar un rato" y hay dos disparadores para lo mismo — uno de los
> dos queda inalcanzable (caso real: la 04_b).

**Dónde se puede usar.** Recomiendo **donde ella esté**, sin pedir locación: el
botón del menú ya implica estar con ella, la escena usa el fondo actual y la
quest no depende de que Violet pase por un lugar a una hora. Si se decide que
sea en su habitación, entra como demanda (`Rec("npc", "violet",
en="casa_hviolet")` + `Rec("puerta", "violet")`) y la guía lo dice sola — pero
suma una condición que puede no cumplirse.

**La escena** termina con ella yéndose: `hide violet_parada with dissolve`,
`va40_fase = 2`, y el MC solo. El horario **no** avanza.

**Qué la hace admitir el celo** — del banco de ideas, las tres que le calzan:
que se contradiga sola, que tenga **el detalle cronometrado**, o que él confiese
primero. Va la segunda, que es la que engancha con la 35.

**Y es UN SOLO reproche, no tres versiones** (2026-09-28): la 35 quedó sin
elección y sin flag, así que no hay nada que consultar. Lo que el reproche cita
está escrito en la escena del sótano y el jugador lo vio pasar — Zowie
invitándolo delante de ella, Leah sumándose, y él agradeciéndoles. Citar algo
concreto de ahí es lo que hace que el reclamo no suene injusto.

---

## 5 · Fase 2 → 3 · El chat

La decisión abierta del plan —quién escribe primero— es la que más cambia la
mecánica. Las dos se pueden hacer hoy:

| | Quién abre | Cómo se implementa | Qué significa |
|---|---|---|---|
| **A** | **Ella**, al rato | `GrupoMensajes` + `disparar_por_trigger` desde un trigger de game_loop (o de avanzar horario) en fase 2 | Se fue pero volvió. Más de ella. El jugador no tiene que hacer nada. |
| **B (recomendada)** | **El MC** | `registrar_conversacion_mensajear("amor40", "violet_amor40_chat", condicion=..., prioridad=100, forzada=True)` | El jugador **elige** seguirla. Es el gesto que la quest está midiendo. |

**B** usa el mismo sistema que la quest de deseo 20, incluido `forzada=True`,
que prende el botón "Hablar" sin la ventaja Mensajear, sin gastar el uso diario
y sin pedir que Violet esté en otra locación. Eso importa: **la condición es la
única puerta**, así que va estrecha (`quest viva and va40_fase == 2`).

⚠️ Dos reglas que este sistema ya aprendió por las malas:

- **Los grupos de Mensajear no llevan condiciones de entrega**
  (`momento_horario`, `momento_locacion`, `condicion_entrega`): un grupo con
  condiciones se va a "espera" y `seleccionar_grupo()` no lo encuentra. Las
  condiciones van en el registro de la conversación.
- **Nada de bloquear el resto del juego mientras dura.** El plan dejaba abierto
  hacerlo prioritario para "encerrar" al jugador en el celular; no hace falta y
  es la clase de bloqueo que se vuelve un soft lock (A1). Si el jugador no le
  escribe hoy, le escribe mañana.

**Las elecciones del chat** no son amor contra deseo: son **aceptar su tiempo**
contra **empujar**. Empujar no es un muro — ella se cierra un poco, la quest
avanza igual, y queda la marca:

```python
default va40_acuerdo = None    # "acepto" | "empujo"
```

Es el flag que 45 y 50 van a leer, igual que la 40 lee el de la 35.

---

## 6 · Fase 3 · El cierre, el hito y el tope

`accion_al_completar` del grupo pone `va40_fase = 3`. El cierre no puede correr
ahí adentro (el jugador sigue en el celular), así que va por
**`registrar_trigger_salir_celular`**: al cerrar el celular entra el label de
cierre, que hace el pensamiento final y:

```python
$ completar_quest_actual("violet", quest_id="violet_amor_08")
```

Lo que hay que tocar **además**, y es lo único de esta quest que sale del
archivo de la quest:

1. **`hitos_violet.rpy`** — `violet_hito_amor_04` deja de ser el marcador
   "Próximamente": se le pone `quest_id="violet_amor_08"`, nombre, descripción y
   ventajas, y se le saca `proximamente=True`.
2. **Un marcador nuevo en 50**, con `proximamente=True`, para que la línea siga
   mostrando que hay más (es la convención del archivo).
3. **`registrar_tope_provisorio("violet", "amor", 45)`** en
   `quests_amor_violet.rpy` — hoy está en 40.

### Las ventajas

Las cinco candidatas del plan, con lo que cuesta cada una **de verdad**:

| Ventaja | Qué toca | Costo |
|---|---|---|
| **Puerta abierta** (entrar sin golpear) | `puerta_ingreso_diurno` / `puerta_ingreso_noche` ya existen en el catálogo y son **consultables**: se listan y andan | Ninguno |
| **Su ritmo** (el talk cambia) | Un `EstadoTalk` nuevo o una `OpcionEspecialTalk` | Medio |
| **Hablar en serio** (opción en su menú) | Contenido nuevo: labels de conversación | Alto |
| **Salidas** (proponerle ir a un lado) | Locación nueva | Muy alto |
| **XGram con contenido** | La app | Alto |

**Recomendación:** que el hito otorgue **una ventaja que funcione de verdad** —
la puerta es la obvia, y es el símbolo físico del acuerdo— y que las otras se
**presenten en la escena** sin registrarse. Regla del panel de Desbloqueos: una
ventaja registrada sin ninguna escena le promete al jugador algo que no existe
(hoy pasa con "Nuevos Chats"). Si se registra igual, que el texto lo diga.

---

## 7 · Declaración en el controlador

```python
declarar_planificacion("violet_amor_08",
    disparador=Disp("auto", nota="la noche siguiente, por el celular"),
    demandas=[Rec("celular"),
              Rec("interaccion", "violet")])
```

- **`de_corrido` NO.** La quest dura varios días a propósito y no se apropia de
  ningún momento: marcarla de corrido frenaría al resto del juego sin motivo.
- **Sin reservas** y **sin `duenio`**: no hay restricción ni noche tomada.
- **Sin consumos**: no reubica a nadie ni ocupa un slot.
- **`Rec("celular")`** porque las dos puntas pasan por el teléfono; si otro
  contenido lo tiene bloqueado, la quest espera en vez de pisarlo.
- **La noche no se declara** como Rec: `_pl_mundo_detalle` solo lee el slot de
  los Rec de tipo `npc` y `locacion`, así que un horario suelto no aportaría
  nada. El chequeo vive en la función del trigger y el `nota` del `Disp` es lo
  que se lo cuenta al jugador.

---

## 8 · Textos de las etapas

`ETAPA_CONDICIONES` usa los genéricos de la fábrica ("Subir amor ❤️ (x/40)").
`ETAPA_BOTON_LISTO` necesita textos propios **que miren la fase**, como la 35,
porque el pedido cambia tres veces:

| Fase | Pista | Qué hacer |
|---|---|---|
| 0 | algo que no spoilee la solicitud | "Esperar" |
| 1 | la solicitud de Zowie quedó dando vueltas | "Hablar con Violet" |
| 2 | ella se fue sin terminar | "Escribirle a Violet" (o "Esperar su mensaje", según §5) |
| 3 | — | (dura un instante) |

Van como dos funciones de módulo en el archivo de la quest —`_pista_va40_listo`
y `_quehacer_va40_listo`— referenciadas desde `_VIOLET_AMOR_TEXTOS[8]`. Se
guardan dentro del `ConfigEtapa`, así que funciones de módulo, nunca lambdas.

---

## 9 · Archivos a tocar

| Archivo | Qué |
|---|---|
| `amor/violet_amor_40.rpy` | **nuevo**: flags, condiciones, triggers, botón, grupo de chat, escenas y cierre — **hecho** (diálogo pendiente) |
| `amor/quests_amor_violet.rpy` | fila `(8, 40, …)`, textos de etapa y tope provisorio a 45 — **hecho** |
| `quests/planificacion_violet.rpy` | la declaración de arriba — **hecho** |
| `interaction/interactions_violet.rpy` | el botón propio + `violet_amor_08` en `_VA_SIN_BOTON` — **hecho** |
| `hitos_violet.rpy` | `violet_hito_amor_04` pasa a hito real + marcador nuevo en 50 — **hecho** |
| `ui/hud/hud_celular.rpy` | el texto del botón XGram sale de `xgra_texto_app()` — **hecho** |
| `tl/english/…` | pistas, botón y las líneas del chat ya escritas — **hecho**; el diálogo, al escribirlo |

**Una demanda que el validador pidió y no estaba en el esquema:**
`Rec("npc", "violet")`. Toda quest demanda a su propio NPC — es lo que hace que
una reserva sobre Violet la frene aunque su disparador no pase por ella.
`tools/validar_bloqueos.py` (chequeo 7) lo exige.

---

## 10 · Lo que hay que decidir antes de escribir

1. **Quién escribe primero en el chat** — recomendado **B**, el MC (Mensajear
   forzada). Cambia qué sistema se usa y qué significa la escena.
2. **Dónde se habla cara a cara** — recomendado donde ella esté, sin demanda de
   locación.
3. **Aceptar la solicitud: automático** (recomendado, con el flag guardado) o
   elección con dos ramas.
4. **XGram**: narrada + cambio de texto del botón (recomendado) o pantalla propia.
5. **Qué la hace admitir el celo**: el detalle cronometrado (engancha con la 35),
   que se contradiga sola, o que él confiese primero. Puede ser elección.
6. **Qué ventajas otorga el hito** y cuántas se presentan sin desarrollar.
7. **Si la última palabra es de ella o de él** (narrativo, no mecánico).

---

## 11 · Riesgos a mirar

- **Dos disparadores.** La quest tiene un trigger automático Y un botón. No se
  pisan porque viven en fases distintas (0 y 1) y el botón lleva su condición de
  fase, pero es exactamente el error de la 04_b: al implementar, verificar que
  el botón genérico esté apagado (`_VA_SIN_BOTON`) y que el trigger no pueda
  volver a saltar en fase ≥1.
- **El salto de contenido.** Al existir el hito de 40 el tope sube, y un jugador
  que venía con el amor topeado en 40 va a ver la 35 y la 40 dispararse casi una
  atrás de la otra. Ya estaba anotado para la 35; con la 40 se agrava.
- **Nada que leer de la 35**: no hay flag, así que el reproche se escribe una
  sola vez. Si la 35 recupera su elección, el reproche se parte ahí y no antes.
- **El chat de Mensajear con `forzada=True`**: la condición es la única puerta.
  Si queda ancha, el botón "Hablar" aparece cuando no corresponde.
