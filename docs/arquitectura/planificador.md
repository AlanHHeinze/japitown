# Planificador de contenido — diseño y tabla de quests

Estado: **diseño acordado, sin implementar** (2026-09-11). Este documento es la
fuente para la implementación y para la revisión de la tabla.

## Por qué

Con tres líneas de quest por personaje siempre hay más de una activa. Hoy cada
quest se activa sola (`_procesar_avance_etapas`) y se dispara sola (botón,
puerta, locación, mensaje). Nadie mira si dos quests se pisan: si una manda a
Violet afuera "esta noche" y otra la necesita en su cuarto "esta noche", gana un
número (`prioridad_rutina`) y la narrativa de la otra se rompe — o peor, el
jugador queda encerrado por una restricción cuya salida ya no existe.

El planificador decide **qué entra y cuándo**, cruzando dos listas por quest:
lo que **demanda** para funcionar y lo que **consume** mientras corre. No lee
la cadena de labels: solo cruza datos declarados, y `validar_bloqueos.py`
vigila que lo declarado coincida con el código.

## La vida de una quest — dos capas

```
nace ──────────── espera ──────────── activa ──────────── narrativa ──────── termina
 │                                       │
 │ CAPA 1: ¿rompo algo de lo activo?     │ CAPA 2: ¿se cumplen mis necesidades AHORA?
 │ No → nazco. Sí → espero (FIFO).       │ Sí → narrativa. No → el interruptor no responde.
```

Una quest nace al completarse su predecesora, espera hasta que el jugador toca
su interruptor (botón, puerta, locación, mensaje), corre su narrativa y muere
al completarse. El planificador decide en dos momentos:

**Capa 1 — nacer** (`_procesar_avance_etapas`, transición 3→4). La pregunta es
sobre las demás, no sobre ella:

- ¿Hay quests activas? No → nace.
- Sí → ¿mis **consumos de vida** cubren una **demanda** de alguna activa que
  sea `de_corrido`? No → nace. Sí → espera hasta que ya no (FIFO por
  `esperando_desde`; pista *"Terminar «X» primero"*).
- Con una **secuencia en curso** no nace nada: una rutina nueva en medio de la
  noche de otra la rompe. Duran horas.

Al nacer aplica su rutina: desde ese momento el mundo está como declaró, y
las que quieran nacer después se miden contra eso.

**Capa 2 — activar** (el interruptor → `quest_lista_para_boton`). Antes de dar
paso a la narrativa, el motor lee las **demandas** de la quest y las verifica
contra el mundo de ese momento: NPC donde hace falta, disponible, puerta
alcanzable, locación accesible, celular abierto, acción visible. Se cumplen →
arranca, y de ahí la protegen los dueños de restricción hasta completarse. No
se cumplen → el interruptor **se esconde** y la quest sigue esperando. **El
mismo sistema que decide esconderlo escribe en la pista y en el "qué hacer"
qué es lo que interrumpe** ("Terminar «X» primero", "Le dije a Violet que iba
esta noche", "Violet no está en su cuarto"). Nada se rompe porque nada empezó.

**Dentro de la narrativa** — si la quest activa una restricción que encierra,
`activar_restriccion(..., salida=Rec(...))`: el motor verifica que la salida
exista ahora; los dueños impiden que un trigger ajeno salte o que alguien la
levante; el watchdog queda de último recurso.

### El rol de `de_corrido`

No decide si la quest nace: decide si **las demás la respetan**. Una de corrido
nacida ("vení esta noche") impide que nazca cualquier quest cuyos consumos le
pisen esa noche. Una tolerante no protege nada: si otra nace y se lleva a
Violet, su interruptor espera — que es lo que su narrativa admite.

### Las condiciones de los disparadores se vuelven declarativas

Hoy cada botón escribe a mano "Violet en su cuarto y por la tarde". Con la
capa 2 eso **es** la lista de demandas: `Rec("ubicacion", "violet", horario=1,
en="casa_hviolet")`. Las evalúa el motor desde `quest_lista_para_boton`, el
predicado único — por eso los 25 disparadores que hoy chequean la etapa inline
migran a él. Una quest nueva no escribe condiciones: declara qué necesita.

## El vocabulario — nueve recursos

Demandas y consumos usan el mismo vocabulario. Consumo = "tomo R"; demanda =
"necesito R libre".

| Recurso | Forma | Ejemplos reales |
|---|---|---|
| `npc` | `npc:violet @ (dia?, horario?) {en, skin, animo, disponible}` — el **estado** del NPC en un slot, atributo por atributo | `rutina_quest` (en), 09_a (skin de Mónica, disponible=False vía 09_b), estados de talk (animo) |
| `interaccion` | `interaccion:violet` o `interaccion:violet:jugar` | amor 25 (menú exclusivo), 09_a (menú propio), la enojada |
| `puerta` | `puerta:violet` | deseo 25, 09_a, amor 25 fase 4 (override) |
| `locaciones` / `locacion` | consumo: lista permitida · demanda: una locación | toda whitelist · cocinar pide la cocina |
| `reloj` | `reloj` | toda restricción con `congelar_reloj` |
| `accion` | `accion:cocinar`, `accion:ver_tv`, `accion:dormir`… | 08_a intercepta ver_tv; 0_b y 04_d4 cocinar; 01_a bloquea dormir |
| `celular` / `mensajes` | `celular`, `mensajes` | `celular_bloqueado`, deseo 20, Mensajear |

`Rec(tipo, npc=None, dia=None, horario=None, en=None, skin=None, animo=None,
disponible=None, accion=None, reserva=False)`. Sin `dia` = todos; sin
`horario` = todo el día; un atributo en `None` = no lo pido / no lo toco.

### Reglas de cobertura (consumo cubre demanda cuando…)

| Tipo | Cubre si |
|---|---|
| `npc` | mismo NPC, slots superpuestos, **y algún atributo que los dos especifican con valores distintos**. Lo que un lado no especifica no cuenta: "en su cuarto" y "en su cuarto en pijama" son compatibles; "en pijama" y "en ropa casual" chocan |
| `interaccion` | mismo NPC y (consumo total, o misma acción) |
| `puerta` | mismo NPC |
| `locaciones`/`locacion` | la locación demandada no está en la lista |
| `reloj` | siempre; cubre también `accion:dormir/avanzar/ver_tv/…` |
| `accion` | misma acción |
| `celular`/`mensajes` | siempre |

### Dos alcances de consumo

- **De vida** (declarados en el catálogo): valen desde que la quest entra hasta
  que se completa. Son las rutinas (`ubicacion`), las exclusividades de menú y
  puerta que duran toda la quest, `npc`, `skin`, `animo`.
- **De secuencia** (vivos, no declarados): los impone la restricción mientras
  está activa — `reloj`, `locaciones`, `celular`, `accion:*`, `npcs_ocultos` →
  `interaccion`. El planificador los lee de `restricciones activas` en el
  momento; no hace falta declararlos dos veces. Así una quest que bloquea
  dormir *durante su noche* no bloquea a nadie los tres días previos.

## Autodisparos

Las quests que se disparan solas (una locación, un horario, despertar un día)
son triggers de motor. Para que la capa 2 las alcance sin depender de que cada
función chequee bien: **el trigger se registra con `quest_id=`, y el motor no lo
evalúa si `quest_lista_para_boton(quest_id)` da False**. Un trigger sin
`quest_id` (de motor, de ventajas) sigue como hoy.

## La reserva

Garantizar que Violet *va a estar* esta noche no garantiza que la noche sea *de
esta quest*. Si A ("vení esta noche") y B ofrecen las dos algo con Violet a la
noche y el jugador hace B, B avanza el horario y la noche de A pasó — narrativa
rota sin que ninguna capa lo viera, porque B no pisó ninguna rutina.

Cuando una quest `de_corrido` se **activa** y su narrativa fija un momento, el
planificador **reserva** `(npc, dia, horario)` para ella. Sale de la declaración
(`Rec("npc", "violet", horario=2, en="casa_hviolet", reserva=True)`): al
activarse se reserva el próximo slot que coincida (hoy si no pasó, si no
mañana). Mientras la reserva esté en pie:

1. Ninguna otra quest puede activarse sobre ese NPC en ese slot — la capa 2 la
   esconde, y la pista dice *"Le dije a Violet que iba esta noche"*.
2. Las ventajas con ese NPC (besar, jugar, ropa nueva, mensajear) no aparecen
   en ese slot.
3. **El reloj no pasa de largo por el slot**: durante la noche reservada no se
   duerme, no se ve TV, no se entrena — la salida es la quest. (Es lo que la
   pizza y el corte de luz hacen a mano; la reserva lo hace sola.)

Se guarda en el save. Vence cuando el slot pasa o la quest se completa. Si
vence sin cumplirse, avisa en consola: es la narrativa rota que queremos ver
en testeo, no en producción.

## Los huecos entre capas

| Situación | Quién la cubre |
|---|---|
| Entre nacer y activar pasan días, el mundo cambia | De corrido: nadie nace con consumos que le pisen una demanda; su rutina ya rige. Tolerante: no le importa; la capa 2 decide al activar. |
| Una secuencia arrancó y otra quest quiere nacer | "Con una secuencia en curso no nace nada". |
| Una de corrido admitida que el jugador no dispara por días | Decisión de juego (FIFO). Aviso en consola. |
| Una tolerante cuya secuencia necesita al NPC y el NPC se fue | La capa 2 no la activa sin el NPC. Activada, la protegen los dueños. |
| Al activar, algo cambió desde que nació | Justamente por eso la capa 2 relee las demandas en ese momento y no confía en la capa 1. |

### Lo demás que pasa por el planificador

- **Ventajas y eventos**: mismo cruce. Los eventos van a desaparecer en favor
  de ventajas; mientras existan, se gatean en `validar_eventos` al pasar a
  ACTIVO. Las ventajas (besos, jugar, ropa nueva, mensajear) declaran sus
  demandas `interaccion:violet:X`: el botón no aparece si hay un consumo activo
  que lo cubra.
- **Bypasses a corregir** (miran `activa` sin etapa): `puertas_violet.rpy:24`
  (0_b "Intentar hablar") y `monica_quest_0_c.rpy:15` (la notebook).

## Decisiones tomadas

- Slots de `ubicacion` por `(dia_semana, horario)`, igual que las rutinas.
- `de_corrido` es **por quest**. Una quest que tolera esperar hasta un día y
  después no tolera interrupciones se **parte en dos** (modelo: 04_d2…d6).
- Cola FIFO. Si el jugador demora, es del juego: ninguna quest bloquea más de
  dos o tres días por diseño.

---

## La tabla — propuesta para revisar

`de_corrido` es lectura narrativa: **corregir donde no coincida con lo que dice
el personaje**. Las demandas son de admisión; los consumos, de vida. La columna
"secuencia" dice si la quest encierra al jugador en algún tramo y cuál es la
salida (lo que verifica el chequeo 2).

### Violet — línea principal

| Quest | Dispara por | de_corrido | Demandas | Consumos de vida | Secuencia → salida |
|---|---|---|---|---|---|
| 0_a Violet me ignora | botón Saludar | no | interaccion:violet:talk | — | — |
| 0_b ¿Qué le pasa a Violet? | puerta (tarde) / botón | no | puerta:violet · ubicacion:violet@tarde=hviolet | ubicacion (rutina) | sí → accion:cocinar; luego puerta:violet |
| 01_a Un paquete misterioso | repartidor (mañana) | no | — | accion:dormir (mientras la entrega está pendiente) | — |
| 01_b Los mangas de Violet | puerta "Dar paquete" | no | puerta:violet | — | — |
| 02_a ¿Mangas prestados? | puerta "Pedir mangas" | no | puerta:violet | — | — |
| 02_b Buscar los mangas | puerta (noche) | **no** — "pasá a la noche" | puerta:violet · ubicacion:violet@noche=hviolet | — | — |
| 02_c Leer los mangas | usar item | no | accion:usar_item | — | — |
| 03_a Devolver los mangas | puerta / botón | no | puerta:violet | — | sí (en su cuarto) → acciones propias |
| 04_a El cosplay de Violet | botón | no | interaccion:violet | — | — |
| 04_b Violet y el Cosplay | locación (donde esté) | no | ubicacion:violet (en casa) | ubicacion (rutina) | — (gate: solo NPCs interactuables) |
| 04_c Cosplay II | mensaje (trasnoche) | no | celular · ubicacion:violet@trasnoche=hviolet | — | — |
| 04_d Cosplay III | mensaje (trasnoche) | no | celular · hito deseo 10 | — | — |
| 04_d2 Algo por ella | botón | no | interaccion:violet | — | — |
| 04_d3 Las golosinas | botón + item | no | interaccion:violet · accion:comprar | — | — |
| 04_d4 La pizza | botón → cocinar (noche) → puerta | no | interaccion:violet · accion:cocinar · puerta:violet | ubicacion:violet@noche=hviolet (rutina) | sí (tras cocinar) → puerta:violet |
| 04_d5 La limpieza | Violet te busca (pasillo, tarde) | no | ubicacion:violet@tarde=pasilloarriba | ubicacion (rutina) | — |
| 04_d6 Todo lo que me pidió | botón / puerta | no | interaccion:violet ∨ puerta:violet | — | — |
| 04_e Cosplay IV | mensaje | no | celular | — | — |
| 05_a Un nuevo cosplay | chat tienda → botón/puerta | no | celular · accion:comprar (dinero) | — | — |
| 05_b El paquete llegó | repartidor → puerta | no | puerta:violet | — | — |
| 05_c El malentendido | mensaje (noche) → botón/puerta | no | celular · interaccion:violet ∨ puerta:violet | — | — |
| 06_a Las entradas | chat → botón (noche, en su cuarto) | no | celular · interaccion:violet · ubicacion:violet@noche=hviolet | — | — |
| 06_b La prueba del cosplay | mensaje (mañana) → puerta (noche) | no | celular · puerta:violet · ubicacion:violet@noche=hviolet | ubicacion (rutina) | — |
| 07_a El cierre del cosplay | puerta | no | puerta:violet | — | — |
| 07_b El cambio del cosplay | chat tienda → botón | no | celular · interaccion:violet | — | — |
| 07_c Cosplay de reemplazo | mensaje (mañana) | no | celular | — | — |
| 08_a La tormenta | dormir → secuencia al despertar | **sí** — es *esa* mañana | ubicacion:violet (en casa) · accion:ver_tv · locacion:living/hviolet/banioarriba · puerta:violet | — | sí (toda la mañana) → ver_tv → hviolet → baño |
| 09_a Violet enferma | locación → 3 días | **sí** — está enferma *ahora* | npc:violet · ubicacion:violet · puerta:violet · ubicacion:monica · ubicacion:jasmine | ubicacion:violet (todo el día, 3 días) · puerta:violet (override) · interaccion:violet (menú propio) · ubicacion:monica@living · skin:monica · npc:violet (09_b) | — (no acota el mapa; sí el NPC) |

### Mónica y Jasmine

| Quest | Dispara por | de_corrido | Demandas | Consumos de vida | Secuencia → salida |
|---|---|---|---|---|---|
| M 0 Agradecimiento | botón | no | interaccion:monica | — | — |
| M 0_b Mónica enojada | dormir → gate → living | no | locacion:casa_living | accion:dormir · accion:avanzar (gate) | — |
| M 0_c Servicio Técnico | acción notebook | no | accion:usar_item | — | — |
| J 0_a Reencuentro | botón | no | interaccion:jasmine | — | — |
| J 0_b Mensaje de Carl | locación → chat | **sí** — tutorial encerrado | celular | — | sí → mensaje (Carl) |
| J 0_c El regalo | botón (gym, tarde) | no | interaccion:jasmine · ubicacion:jasmine@tarde=gym | — | — |

### Violet — línea de deseo

| Quest | Dispara por | de_corrido | Demandas | Consumos de vida | Secuencia → salida |
|---|---|---|---|---|---|
| deseo 5 Atracción | locación (pasillo, tarde) | no | ubicacion:violet (en casa) | — | — |
| deseo 10 Encuentro nocturno | dormir → sed → cocina | **sí** — *esa* madrugada | locacion:casa_cocina · ubicacion:violet@… (la escena la pone) | — | sí → accion "Tomar agua" |
| deseo 15 Anime en estreno | ver TV (sótano) | no | accion:ver_tv · locacion:casa_sotano | — | — |
| deseo 20 Pensando en Violet | hmc (noche) → celular | **sí** — encerrado en el celular | celular · mensajes | — | sí → mensaje (Mensajear forzada) |
| deseo 25 En su habitación | ver TV (sótano, noche) → puerta | **sí** — *esa* noche | accion:ver_tv · locacion:casa_sotano · puerta:violet | ubicacion:violet@noche=hviolet (rutina) · puerta:violet (override fase 1) | sí → puerta:violet |
| deseo 30 Sinceridad | hmc (noche) → hviolet; luego 3 días ignorándola | **sí** la noche · **no** los 3 días → **partir en dos** | locacion:casa_hmc · ubicacion:violet@noche=hviolet · puerta:violet | ubicacion:violet@noche=hviolet (rutina) | sí (fase 1) → entrar a hviolet |

### Violet — línea de amor

| Quest | Dispara por | de_corrido | Demandas | Consumos de vida | Secuencia → salida |
|---|---|---|---|---|---|
| amor 5 ¿Mejor? | puerta "Llamarla" (tarde) | no | puerta:violet · ubicacion:violet@tarde=hviolet | — | — |
| amor 10 Buena relación | locación (pasillo) | no | ubicacion:violet (en casa) | ubicacion (rutina) | — |
| amor 15 La visita | locación | no | ubicacion:violet | — | — |
| amor 20 Jugando juntos | comprar → jugar (hmc, noche) | no | accion:comprar · interaccion:violet:jugar · ubicacion:violet (en casa) | — | — |
| amor 25 Solos en casa | domingo (dormir) → 4 fases | **sí** — *ese* domingo | ubicacion:violet · ubicacion:monica=fuera · ubicacion:jasmine=fuera · accion:cocinar · puerta:violet | ubicacion (las tres, domingo) · interaccion:violet (exclusivo) · puerta:violet (fase 4) | sí (fases 1, 3, 4) → living / cocinar / puerta:violet |
| amor 30 ¿Qué me pongo? | locación (pasillo, tarde) | no | ubicacion:violet@tarde=hviolet | — | — |

### Ventajas (sin quest — solo demandas)

| Ventaja | Demanda |
|---|---|
| Beso (amor) / Beso (deseo) | interaccion:violet:beso · ubicacion:violet@tarde/noche=hviolet |
| Jugar / Ver anime | interaccion:violet:jugar / :anime · ubicacion:violet (en casa) |
| Ropa nueva (cita) | interaccion:violet:ropa · puerta:violet |
| Mensajear | celular · mensajes · interaccion:violet:chat |
| Provocación (mirar) | puerta:violet (baño) |

## Lo que sale de la tabla

- **7 quests de corrido** de 46. El resto corre en paralelo como hoy.
- **Una para partir**: deseo 30 (la noche sí, los tres días no).
- **09_a es la más invasiva** (consume a Violet entera tres días, mueve a
  Mónica, cambia su skin, saca a Jasmine del baño): cualquier de corrido que
  necesite a Violet espera detrás de ella. Es correcto — está enferma.
- **Todas las secuencias con salida por puerta ya tienen rutina** (0_b, 04_d4,
  deseo 25, amor 25). El chequeo 2 hoy pasa; el validador lo mantiene.
