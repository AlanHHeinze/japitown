# Planificador de contenido — diseño y tabla de quests

Estado: **implementado** (2026-09-11) en `core/quests/planificador.rpy`, con las
declaraciones en `characters/<npc>/quests/planificacion_<npc>.rpy`. Las
secciones de diseño siguen siendo la referencia; al final están las notas de
implementación de cada punto (1 activación, 2 partir deseo 30, 3 limpieza, 4 el
planificador) y las diferencias entre lo diseñado y lo construido.

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

**Lo que la reserva de slot NO hace: bloquear el golpe a la puerta.** La reserva
de slot existe mientras corre la secuencia de la quest que la puso, y esa
secuencia puede entrar por la puerta común (Sinceridad entra a la pieza de
Violet golpeando, con la ventaja de deseo 20; no tiene opción de puerta
propia). La primera versión bloqueaba el golpe con el texto de la reserva y
dejó a un jugador sin salida (0.1.9.1, día 51, noche: reloj congelado por la
reserva, restricción cerrando el resto, y en la puerta "Le dije a Violet que
iba esta noche"). Desde el 2026-09-15 `planificador_texto_reserva` solo
contesta con la reserva **de vida** ("Mejor no molestar a X ahora"); el menú
del NPC sigue filtrando por quest en los dos tipos. Lo cubre el paso "reserva"
de la ruta `planificador` del harness.

### Reservar al MC (2026-09-22)

Además de los NPCs se puede reservar **al MC**, con un tipo de `Rec` propio:

```python
Rec("mc", dia=4, horario=2, reserva=True)   # la noche del viernes es de esta quest
```

No es `Rec("npc", "mc")` a propósito: el MC no está en `sistema_npcs`, así que
no tiene locación consultable con `obtener_npc`, ni disponibilidad, ni rutina —
todo el camino de NPC daría falso. Es un tipo aparte y hoy hace una sola cosa:

- **Ninguna otra quest se activa en ese slot.** La capa de conflicto
  (`_pl_conflicto_activacion`) corta apenas ve una reserva ajena sobre `"mc"`,
  sin mirar demandas: el MC está en todas las escenas del juego, así que no
  hace falta que ninguna lo declare. La dueña queda exenta, como siempre.
- **Ningún mensaje prioritario ajeno se entrega.** `_puede_entregarse`
  (messagesystem_core) consulta la reserva antes de entregar un prioritario y
  lo manda a espera si el MC está tomado. Solo los prioritarios: uno normal no
  traba nada, y cuanto más chico el radio del bloqueo, mejor.
- **Congela el reloj**, como cualquier reserva de slot. Es automático: toda
  quest que reserve al MC le frena dormir/avanzar al jugador hasta que su
  escena pase. Es lo que evita que se saltee la noche con el mensaje sin leer.

El contenido lo consulta con **`planificador_mc_reservado_por()`** (quest_id o
None), que es lo que necesita un trigger antes de arrancar algo largo — la capa
2 lo usa sola, pero los triggers no pasan por la parte momentánea.

El texto que ve el jugador no puede ser el de los NPCs ("Le dije a Mc que iba
esta noche" no se lee): la reserva del MC dice **"Tengo algo pendiente
{momento}"**, que funciona igual como mensaje del reloj congelado y como motivo
de "Interrumpida" en las otras quests.

Cubierto por el paso "reserva" de la ruta `planificador`: **con el MC reservado
la dueña sigue pudiendo activarse y las ajenas no** — que es justo la forma de
los soft locks E10 y E11.

**La dueña de la restricción activa no se frena.** Una quest cuya restricción
está puesta (misma `duenio`) ya está en su secuencia aunque nadie la haya
pasado por `activar_quest` (las que la ponen desde `accion_al_entrar`, como la
0_b de Mónica). Para la capa de conflicto cuenta como narrativa: una reserva
ajena o los consumos de otra no la esconden, porque su salida es lo único que
levanta la restricción. Lo momentáneo (lugar, hora) se sigue midiendo. Y al
revés, **las quests que se disparan al dormir declaran
`Rec("accion", accion="dormir")`**: con una restricción ajena que bloquee
dormir, esperan. Las dos reglas cierran el deadlock E11 (0_b de Mónica ↔ 09_a):
la 0_b bloqueaba dormir hasta ir al living y la 09_a, naciendo esa misma mañana,
reservaba a Mónica de vida y escondía ese disparador. Auditoría 2026-09-15.

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
| 01_a Un paquete misterioso | repartidor (mañana) | no | — | — (su bloqueo de dormir es un `registrar_bloqueo_accion` que rige solo con el paquete pendiente; no se declara de vida, ver E11) | — |
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
| deseo 30 Sinceridad (06) | hmc (noche) → hviolet | **sí** — *esa* noche | locacion:casa_hmc · ubicacion:violet@noche=hviolet · puerta:violet | ubicacion:violet@noche=hviolet (rutina) | sí (fase 1) → entrar a hviolet |
| deseo 30 Distancia (07) | dormir 3 noches sin contacto → visita (hmc, noche) | no | locacion:casa_hmc | — | — |

### Violet — línea de amor

| Quest | Dispara por | de_corrido | Demandas | Consumos de vida | Secuencia → salida |
|---|---|---|---|---|---|
| amor 5 ¿Mejor? | puerta "Llamarla" (tarde) | no | puerta:violet · ubicacion:violet@tarde=hviolet | — | — |
| amor 10 Buena relación | locación (pasillo) | no | ubicacion:violet (en casa) | ubicacion (rutina) | — |
| amor 15 La visita | locación | no | ubicacion:violet | — | — |
| amor 20 Jugando juntos | comprar → jugar (hmc, noche) | no | accion:comprar · interaccion:violet:jugar · ubicacion:violet (en casa) | — | — |
| amor 25 Solos en casa | domingo (dormir) → 4 fases | **sí** — *ese* domingo | ubicacion:violet · ubicacion:monica=fuera · ubicacion:jasmine=fuera · accion:cocinar · puerta:violet | ubicacion (las tres, domingo) · interaccion:violet (exclusivo) · puerta:violet (fase 4) | sí (fases 1, 3, 4) → living / cocinar / puerta:violet |
| amor 30 ¿Qué me pongo? | locación (pasillo, tarde) | no | ubicacion:violet@tarde=hviolet | — | — |
| amor 35 Las amigas | locación (sótano, viernes/sábado a la noche), avisada por chat | **sí** — *esa* noche | ubicacion:violet@noche=casa_sotano (vie y sáb) · **mc@noche (reserva)** · locacion:casa_sotano · celular | ubicacion:violet@noche+trasnoche=casa_sotano (rutina) | sí (fase 2, el sótano cerrado) → dormir |
| amor 40 La solicitud | auto (la noche siguiente) y después un botón propio | no | celular · interaccion:violet | — | — (ninguna fase bloquea nada) |
| amor 45 La regla de la casa | locación (frente, mañana) | **sí** — *esa* mañana | ubicacion:violet@mañana=cocina · ubicacion:monica@mañana=fuera · ubicacion:jasmine@mañana=hjasmine · locacion:casa_frente | las tres rutinas | — (escena continua, no devuelve el control) |
| amor 50 El domingo solos | dormir (domingo) → living → su puerta o el baño → acción Bañarse → su habitación | **sí** — *ese* domingo | accion:dormir · ubicacion:violet@domingo=hviolet · monica y jasmine@domingo=fuera · puerta:violet · accion:va50_banarse | las tres rutinas + puerta:violet | sí (fase 3, hviolet cerrada) → la acción Bañarse |

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
- **Una para partir**: deseo 30 (la noche sí, los tres días no). **Hecho
  (2026-09-11)**: `violet_deseo_06` "Sinceridad" es la noche de la charla y
  se completa al salir de la pieza; `violet_deseo_07` "Distancia" nace ahí,
  lleva el contador y se completa con la visita (el hito de deseo 30 apunta a
  la 07). Partidas de 0.1.9a que estaban contando migran solas con
  `_gl_trigger_vd30_migracion`. Es la primera quest que se agrega a una línea
  con el mismo umbral que la anterior — la tabla del catálogo lo admite sin
  tocar el motor.
- **09_a es la más invasiva** (consume a Violet entera tres días, mueve a
  Mónica, cambia su skin, saca a Jasmine del baño): cualquier de corrido que
  necesite a Violet espera detrás de ella. Es correcto — está enferma.
- **Todas las secuencias con salida por puerta ya tienen rutina** (0_b, 04_d4,
  deseo 25, amor 25). El chequeo 2 hoy pasa; el validador lo mantiene.

## Implementación — punto 1: el punto de activación (hecho, 2026-09-11)

Antes de esto el motor no sabía *cuándo* una quest pasaba de "esperando al
jugador" a "narrativa en curso": los disparadores saltaban derecho al label,
`intentar_ejecutar()` era código muerto, `validacion_especial` nunca se
evaluaba y `ETAPA_DESARROLLO` se seteaba a mano en dos quests. La capa 2 no
tenía dónde pararse.

**`activar_quest(quest_id, origen)`** (`questsystem_core.rpy`) es ahora el
único lugar por el que pasa ese instante. Lo llama el **motor**, nunca el
contenido, en los seis despachadores:

| Despachador | Dónde | Cómo sabe la quest |
|---|---|---|
| Menú del NPC | `interaccion_<npc>` → `despachar_opcion_quest(_return)` | la screen devuelve `("opcion_especial", label, quest_id)` |
| Menú de puerta / entrada directa | `door_access_system` (menú, trasnoche, diurno) | `registrar_opcion_puerta(..., quest_id=)` |
| Override de puerta | `door_access_system` | `registrar_override_puerta(..., quest_id=)` (nuevo) |
| Triggers | `_ejecutar_triggers` al aceptar un label | `registrar_trigger_game_loop/dormir/avanzar/salir_celular(..., quest_id=)` (nuevo; 19 declarados) |
| Acciones y listeners | `accion_locacion_ejecutar` | `AccionLocacion(quest_id=)` / `ListenerAccion(quest_id=)` (nuevo; 25 declarados) |
| Items | `usar_item` | `"quest_id"` en `CATALOGO_ITEMS` (notebook, mangas) |
| Chats | `seleccionar_grupo` (el jugador abre el chat) | el mecanismo existe (`disparar_por_trigger(..., quest_id=)` → el grupo lo guarda), pero **ningún chat de etapa lo usa desde el paso A**: el chat es un aviso, el disparador que viene después activa |

En todos, si no viene `quest_id` explícito se deduce del prefijo `quest_<id>`
del label (`resolver_quest_id_opcion`, el mismo criterio que el tag " (⭐
Quest)"). Sin quest → no hace nada.

**Qué hace**: `Quest.activar()` prende `narrativa_activa`, guarda
`activada_dia` / `activada_horario`, y deja el id en `_quest_activada_ultima`
(tag `quest_activada` de Sentry). Idempotente: las quests de varios pasos
(05_c, 09_a, favores, amor 25) se activan la primera vez y el resto no cambia
nada. `completar()` y `resetear()` lo apagan. Helper: `quest_en_narrativa(id)`.

**Qué NO hace, a propósito**:
- No mueve `etapa_actual`: 25 disparadores inline miran `ETAPA_BOTON_LISTO`
  para dibujar sus botones y moverla a `DESARROLLO` los escondía. La etapa dice
  "está lista"; el flag dice "está jugándose".
- No bloquea: no evalúa ninguna condición. (`validacion_especial` se evaluó
  como aviso de desarrollo un rato y en el punto 3 se eliminó del todo.)
  Cuando la capa 2 lea demandas, `activar_quest` es el lugar donde va a
  decidir.
- Las quests del MC (`sistema_quests_mc`) quedan afuera: no son parte de la
  tabla.

**Saves**: nada nuevo en `default` que cambie forma; `narrativa_activa` se lee
siempre con `getattr(q, "narrativa_activa", False)`. Una partida de 0.1.9a
cargada tiene todas sus quests con el flag apagado hasta que el jugador vuelva
a tocar un disparador (que es idempotente, así que no pasa nada raro).

**Se fue**: `intentar_ejecutar()`, `intentar_iniciar_quest_actual()`, el
alias viejo `Quest.activar()` (era `iniciar()`), los dos `etapa_actual =
ETAPA_DESARROLLO` a mano (Mónica 0 y 0_c).

**Harness**: ruta `registros`, pasos "punto de activacion: ids" (todo
`quest_id` declarado existe en el catálogo) y "punto de activacion: activar()"
(marca una vez, no mueve la etapa).

## Implementación — punto 3: limpieza de lo que quedó muerto (hecho, 2026-09-11)

Con el punto de activación en el motor y la etapa "en desarrollo" fuera de
juego, esto ya no tenía lector:

- **`validacion_especial`** — parámetro y atributo de `Quest`,
  `obtener_validacion_faltante()`, el tramo de `_generar_que_hacer_validacion`
  que lo leía y los 30 bloques del catálogo (11 con contenido, el resto
  `[]`). Nunca corrió (la "etapa 6"), estaba desactualizado (05_c) y las 11
  quests que lo tenían ya traen `pista`/`que_hacer` propios en BOTON_LISTO, así
  que tampoco generaba texto. Las condiciones que expresaba ("de noche, en su
  cuarto") siguen vivas en la condición de cada disparador y serán las
  demandas.
- **`ETAPA_VALIDACION` (6) y `ETAPA_DESARROLLO` (7)** — las constantes, la
  rama de pista genérica "Quest en progreso..." (y sus strings/traducciones) y
  la entrada del panel de desarrollo. 8 y 9 se conservan por los saves.
- **Los chequeos inline de etapa** — 25 cadenas `q.activa and not q.completada
  and q.etapa_actual == ETAPA_BOTON_LISTO` en los menús de los tres NPCs, dos
  triggers (Mónica 0_b, Violet 04_b), el despachador de favores y el catálogo
  de acciones pasaron a `quest_lista_para_boton(id)`. Cambio de comportamiento
  buscado: ahora todos respetan `npc_disponible`. Quedan dos a propósito, con
  el motivo al lado: `_vq9b_quest_viva` (09_b deja a Violet no disponible y la
  quest tiene que seguir existiendo) y `_vq9a_accion_activa`, que ahora lo
  reusa.
- **Los dos bypasses**: `_puerta_v_0b` (chequeaba a mano "toda la quest"; la
  0_b nace en BOTON_LISTO, es lo mismo) y `revisar_notebook_monica` (idem).
- **El `if` de la 08_a dentro de `accion_ver_tv`** — un disparador de quest
  metido en el label genérico, que se salteaba el registro y el punto de
  activación. Ahora es un `ListenerAccion("ver_tv", ..., quest_id=08_a)` como
  la pizza o la cena de amor 25. Efecto secundario aceptado: como todo
  listener de quest, tiene prioridad sobre el embudo de bloqueos y el "ya usada
  hoy".
- Las variables `_quest_activa = obtener_quest_activa(npc)` de los tres menús,
  que ya no leía nadie.

**Lo que NO se tocó, porque no está muerto** — se migra recién cuando exista
la capa 2:
- Las condiciones de presencia/horario escritas a mano en cada disparador
  (`esta_en_locacion("casa_hviolet") and horario_actual == 2`, etc.): hoy son
  lo único que gatea; serán demandas.
- `prioridad_rutina` (la 09_a la usa para ganar el desempate) y
  `registrar_menu_exclusivo` (amor 25): son consumos declarados a mano, el
  planificador los va a absorber como `interaccion`/`npc`.

## Implementación — punto 4: el planificador (hecho, 2026-09-11)

**Motor**: `core/quests/planificador.rpy`. **Declaraciones**:
`characters/violet/quests/planificacion_violet.rpy`, `…/monica/quests/planificacion_monica.rpy`,
`…/jasmine/quests/planificacion_jasmine.rpy` — `declarar_planificacion(quest_id,
de_corrido, demandas, consumos, duenio)` en `init 6`, 47 quests, 8 de corrido.
Los campos entran en `_CAMPOS` de persistencia: cambiar una declaración alcanza
a los saves.

Dónde engancha:

| Pieza | Dónde | Qué hace |
|---|---|---|
| Capa 1 | `Quest._procesar_avance_etapas`, CONDICIONES → RUTINA | `planificador_puede_nacer`: consumos vs demandas de las **de corrido** activas; secuencia ajena en curso (restricción con `congelar_reloj`) → nadie nace; FIFO por `esperando_desde` |
| Capa 2 | `quest_lista_para_boton` | `planificador_puede_activarse`: reserva ajena → consumos declarados de otras activas → consumos vivos de la restricción ajena → mundo (NPC disponible/no oculto, `en` del slot actual, celular, skin, ánimo). En narrativa no se mide |
| Autodisparos | `_ejecutar_triggers` | un trigger con `quest_id` no se evalúa si su quest no está viva o la frena un **conflicto** (no la parte momentánea: los contadores tienen que correr) |
| Reserva | `activar_quest` → `planificador_reservar` | dos formas: `reserva=True` toma el próximo slot del `Rec("npc", …)` y además frena `ACCIONES_RELOJ` (`PLANIFICADOR_RESERVA_CONGELA_RELOJ`); `reserva="vida"` toma al NPC hasta completar la quest, con el reloj corriendo (09_a: Violet y Mónica). Con cualquiera de las dos, **el NPC solo ofrece las interacciones de la quest que lo reservó**: su menú deja solo las opciones con ese `quest_id` (sin Hablar, eventos ni ventajas — `planificador_opcion_permitida`), su puerta idem, y con reserva **de vida** golpear contesta "Mejor no molestar a X ahora" (`obtener_bloqueo_golpe`; con reserva de slot el golpe sigue su flujo normal: la secuencia puede necesitarlo para entrar); la capa 2 esconde a **toda quest del NPC** (sin que la declare: una quest de la línea de Violet es una interacción con Violet, aunque su disparador sea una acción o una locación) y a las que lo demanden. Vence al pasar el slot (`actualizar_quests` → `planificador_limpiar_reservas`) o al completar |
| Pistas | `Quest.obtener_mensajes` | esperando en capa 1 → "Terminar «X» primero"; frenada por conflicto en capa 2 → el motivo en el "qué hacer". Los "todavía no" momentáneos no escriben nada: el texto propio de la quest ya dice dónde y cuándo |
| Migración | after_load (`persistencia_sistemas`) | restricción activa con el `duenio` de una quest en BOTON_LISTO → esa quest está en narrativa (saves de 0.1.9a) |
| Validador | `tools/validar_bloqueos.py`, chequeo 7 | quest sin declaración; `rutina_quest` sin consumo `npc`; consumo `npc` con `en` sin rutina |
| Harness | ruta `planificador` | tabla de cobertura (17 casos), declaraciones, capa 1, capa 2 y reserva sobre copias |
| Consola | `planificador_estado()` | qué espera, qué reserva, qué bloquea |

**Diferencias con el diseño, y por qué**:

- **La parte momentánea de la capa 2 fue tolerante hasta el paso A** (ver
  abajo): desde entonces es estricta y las demandas son la única fuente del
  "cuándo y dónde".
- **Los autodisparos se gatean por conflicto, no por el mundo.** El trigger
  que cuenta los días de deseo 07 no puede depender de dónde está Violet.
- **Sin `en` en la capa 2 no se usa `tracker_locacion_npc`** sino la locación
  cruda del NPC: las declaraciones usan `"fuera"` igual que las rutinas.
- **Los consumos de secuencia no se declaran** (override de puerta de deseo 25
  fase 1, restricciones): se leen de la restricción activa. Declararlos como
  vida escondía toda opción de puerta de Violet los días que la quest espera.
- **`duenio` es un campo de la quest.** Sin él el planificador mediría a cada
  quest contra su propia restricción (la pizza contra su "no cocinar"), y sin él
  no hay forma de reconocer, en un save viejo, que la quest ya estaba adentro.
- **Reserva de slot en 4 de las 8 de corrido** (08_a mañana, deseo 10
  madrugada, deseo 25 noche, deseo 30/06 noche) y **reserva de vida en 09_a**
  (Violet y Mónica hasta completar, 2026-09-12: en testeo se vio que Mónica
  seguía ofreciendo Hablar y el masaje mientras cuidaba a Violet). J 0_b no es
  de un NPC. Amor 25 no la lleva: su restricción, sus listeners y su menú exclusivo
  ya gobiernan el domingo, y congelar el reloj todo el día le sacaría los
  pasatiempos. El efecto 3 (reloj) queda **activo** y se apaga con una
  constante si en testeo molesta.
- **Ventajas y eventos no declaran demandas** todavía: las ventajas quedan
  cubiertas por el efecto 2 de la reserva; el gate de eventos en
  `validar_eventos` queda para cuando pasen a ser ventajas.
- `prioridad_rutina` y `registrar_menu_exclusivo` siguen (09_a y amor 25 los
  usan); la capa 1 ya evita que dos rutinas se pisen, así que el desempate no
  debería hacer falta más — se saca cuando se confirme en juego.

**Panel del controlador (en vivo)** — `tools/controlador/panel_controlador.rpy`.
`jp_panel_controlador()` (o el menú de cheats) muestra, por quest activa, en qué
capa está y por qué: capa 1 (espera detrás de X), capa 2 (el conflicto) o el
mundo en dos partes, tiempo y lugar, cada una con OK o su motivo; más las
reservas vigentes y la restricción activa. (El laboratorio de escenarios que
armaba el mundo un paso antes de cada disparador se usó para validar la primera
implementación y se retiró el 2026-09-12 para no sobrecargar la herramienta; el
estado se arma a mano desde el menú de cheats — stats, Completar Quests — y la
consola.)

**Lo que hay que mirar en testeo** (consola, `config.developer`): los prints
`[Planificador] X espera para nacer (detras de Y)`, `reserva …`, `AVISO: la
reserva … vencio sin que la quest arrancara`, y `planificador_estado()`.

## Implementación — paso A: el "cuándo y dónde" es de las demandas (hecho, 2026-09-12)

Hasta acá cada disparador chequeaba a mano hora, lugar del NPC y lugar del MC, y
las demandas decían lo mismo — dos fuentes de verdad. Ahora hay una:

**Semántica estricta de la capa 2** (`_pl_mundo_cumple`):
- `npc`: de los Recs de ese NPC, los que rigen en este `(dia, horario)` tienen
  que cumplirse (`en`, `skin`, `animo`, `libre`); si el NPC tiene Recs con slot
  y ninguno rige ahora → "No es el momento". Un Rec sin slot rige siempre.
  Siempre: disponible y no oculto.
- `locacion`: el MC está ahí ahora (`en`, o cualquiera de `locaciones`), en su
  slot si lo tiene, y la restricción activa lo permite.
- Nuevo: `en="casa"` (adentro, en cualquier lado) y `libre=True` (sin rutina
  especial —ducha, salida— e interactuable): es el "sin nada encima" que
  tenían los triggers de deseo 30, amor 15 y amor 30.

**Lo que salió del código** (13 disparadores): 04_a, 06_a (botón), J 0_a/0_c,
puertas de 02_b/amor 5/06_a/06_b, triggers de 04_b (la lista de locaciones y el
oculto), 04_d5 (el oculto), deseo 5, deseo 20, deseo 25, deseo 30 (fase 0),
amor 10, amor 15, amor 25 (el "es domingo"), amor 30, Mónica 0_b. Los helpers
`_vd30_violet_libre` / `_va30_violet_libre` desaparecieron.

**Lo que se queda en el disparador, a propósito**:
- Lo que ninguna demanda expresa: "Violet en el MISMO lugar que el MC" (04_b,
  04_d5), "a solas con Mónica" (M 0), la rama por lugar de 05_c, el botón de
  04_d6 solo dentro de la pieza (afuera el camino es la puerta).
- Las condiciones de **fases posteriores a la activación** (amor 25, deseo 30
  fase 1, deseo 20 cierre, favores): la quest ya está en narrativa y la capa 2
  no la mide.
- 0_b entera (botón y puerta con la tarde a mano): la misma opción es
  activación y paso posterior, y después de activarse la capa 2 ya no la gatea.

**Los chats de etapa dejan de activar.** Con la activación en el chat, una quest
"chat → botón de noche" (06_a, 06_b, 05_c…) quedaba en narrativa al abrir el
chat y la capa 2 dejaba de gatear el botón. El chat es un aviso; activa el
disparador que viene después. (Las quests que son solo un chat se completan
desde el chat y no necesitan activarse.)

**Deseo 10** cambió su declaración: se dispara al ir a dormir (noche o
trasnoche), así que demanda `npc:violet@noche` y `npc:violet@trasnoche` (esta
última con la reserva); la cocina la pone la escena, no es demanda.

**Harness**: paso "capa 2: cuando y donde" en la ruta `planificador` (06_a a la
tarde / con Violet en el living / bien; 04_a en el living / en la cocina).
Necesita el motor corriendo.

**Dormir recorre los horarios (2026-09-12).** `accion_dormir` avanza de a uno
hasta la trasnoche, sin que se vea, corriendo en cada paso lo mismo que el
game_loop (`_vr_interrupcion`: quests, mensajes en espera, eventos, triggers). Un
mensaje prioritario lo despierta en el horario en que llega; un trigger de
game_loop que devuelve label lo despierta con esa escena. Los triggers de dormir
"antes" corren ya en la trasnoche — por eso deseo 10 dispara durmiendo a
cualquier hora. La pantalla de dormir se muestra (no se llama) y el fondo se
repinta debajo del negro (`animacion_dormir_capa`; pausas con `modal=False`
porque `config.modal_blocks_pause`).

**Paso B (pendiente)**: el disparador entero se declara
(`Disparador("boton"|"puerta"|"locacion"|…)`) y el motor arma el botón, la
opción de puerta o el trigger. Ahí desaparecen las funciones `_gl_trigger_*` y
los bloques de `interactions_<npc>.rpy`.

## Personajes prestados y locación madre (hecho, 2026-09-12)

`en` en un `Rec("npc")` acepta una **locación madre** (`LOCACIONES_MADRE`, hoy
`"casa"`): el NPC está en cualquier sublocación de esa madre. `"fuera"` es su
propia madre y **no es parte de la casa** (`madre_de_locacion`,
`viaje_rapido.rpy`): `en="casa"` la excluye, `en="fuera"` la nombra (amor 25
pide a Mónica y Jasmine `en="fuera"` el domingo). Es lo que pide un
personaje **prestado** —otro NPC que habla o se muestra en la escena de una
quest que no es la suya—: tiene que estar en la casa y no reservado, o su
aparición no tiene sentido. Regla: toda quest lo declara con
`Rec("npc", "<otro>", en="casa")` como mínimo (`en=<locación>` si la escena lo
necesita en un lugar puntual).

Relevamiento de las quests de Violet (dialogo o `show` de otro NPC en sus
labels, sin contar los `label test_`):

| Quest | Aparece | Demanda |
|---|---|---|
| 04_a El cosplay de Violet | Jasmine entra a la cocina | `npc:jasmine en=casa` (nuevo) |
| amor 10 Buena relación | Mónica en el living | `npc:monica@mañana en=casa_living` (ya estaba) |
| amor 25 Solos en casa | Mónica y Jasmine se van | `npc:monica/jasmine dia=6 en=fuera` (ya estaba) |
| 09_a Violet enferma | Mónica cuida, Jasmine aparece | `npc:monica` por horario (ya estaba) · `npc:jasmine en=casa` (nuevo) |

El resto solo nombra a otros NPCs para esconderlos (`npcs_ocultos`), mandarles
un chat (01_a) o moverlos por la secuencia (08_a los saca de la casa): no son
apariciones. `validar_bloqueos.py` chequeo 8 ("personajes prestados sin
demanda") lo mantiene.

## La guía la escribe el controlador (hecho, 2026-09-14)

Cada quest declara además su **disparador** (`Disp(tipo, texto, nota)`), y con
eso más las demandas el motor escribe el "qué hacer" completo de BOTON_LISTO
(`planificador_que_hacer`): *Usar la opción «Llamarla» en la puerta de Violet
mientras esté adentro por la tarde* · *Ir al Living con Violet por la mañana con
Mónica* · *Ir a dormir el Domingo con Mónica afuera con Jasmine afuera*. Reglas
de composición: el lugar del NPC propio no se repite si es el destino del MC;
las quests de dormir no dicen horario (el que declaran es el del despertar o
la reserva); varios Recs con lugares/horarios distintos → se omite ese dato; la
`nota` va al final entre paréntesis. En narrativa vuelve el texto propio (las
fases); deseo 07 y amor 20 no declaran `Disp` y conservan su texto dinámico.

Debajo de la pista, la app muestra el **estado** (`planificador_estado_guia`):
verde *Se puede hacer ahora* cuando `quest_lista_para_boton` da True; rojo con el
motivo cuando la frena algo **externo** — reserva ajena, consumos de otra quest,
restricción ajena, NPC no disponible / oculto / fuera de la casa / no donde la
rutina lo pone / ocupado, celular bloqueado (`_pl_mundo_detalle` devuelve ahora
`(tiempo, lugar, externo)`); nada cuando solo falta que el jugador vaya al lugar
o espere el horario, que ya lo dice el "qué hacer". La app de Pistas perdió el
toggle Pistas/Qué hacer: cada bloque tiene un `+` que despliega el "qué hacer"
(estado por pista en `pistas_expandidas`, guardado).

