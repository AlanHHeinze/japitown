# De la 0.1.8.5 a la 0.1.9.1

Todo lo que cambió desde la última build publicada como **0.1.8.5** (commit
`1eec3e2`, 2026-08-20) hasta la **0.1.9.1** (2026-09-16). Cubre tres releases:
0.1.9, 0.1.9a y 0.1.9.1.

**Saves:** la 0.1.9 rompió las partidas anteriores (generación 2). La 0.1.9a y
la 0.1.9.1 son compatibles entre sí y con la 0.1.9 — una partida de cualquiera
de las tres sigue andando.

---

## Contenido nuevo

### Líneas de relación de Violet (0.1.9)

- **Deseo 15 "Anime en estreno"** — layeredimage `violet_magica` y su secuencia.
- **Deseo 20 "Pensando en Violet"** — pasa casi entera en el celular: el MC
  entra de noche a su pieza, queda encerrado hasta escribirle, y el chat corre
  por Mensajear con foto y confesión.
- **Deseo 25 "En su habitación"** — la dispara "Ver TV" en el sótano; Violet lo
  planta, la busca por la casa y la escena sigue por un override de su puerta.
  Incluye la secuencia del beso.
- **Deseo 30** — rediseñada en dos etapas: la charla de la noche y después tres
  días ignorándola. Diálogo escrito de punta a punta y la secuencia del short.
- **Amor 15** — rehecha de cero (Violet visita la pieza del MC). El arco viejo
  se mudó entero a `ventajas/juegosnuevos/jn_pocketboy.rpy` y quedó parkeado.
- **Amor 20** — cuarta fase "Hablar del juego" y botón "Algo para jugar".
- **Amor 25 "Solos en casa"** — corte de luz con cambio de fondo instantáneo,
  secuencia de abrazo y beso, y cierre en el living con las cuatro.
- **Amor 30** — rediseñada: arranca sola en el pasillo de arriba por la tarde
  (el chat que era Requisito se eliminó). Usa el layeredimage `violet_q30a`.
- **Deseo 10** — cierre en la pieza del MC y assets nuevos de
  `violet_tanga_qd10`.

### Quest 09 "Violet enferma" (0.1.9)

Rearmada de punta a punta:

- Arranque nuevo: al despertar, el MC lee la respuesta de la tienda en una
  escena (los mensajes entran al historial ya leídos) y sale el cartel de quest
  temporal.
- Las peticiones no se repiten en toda la quest y Violet dice dónde está cada
  cosa.
- **Minijuego de secarle el sudor**: dos manos (mano/toalla) con funciones
  distintas, ocho sudores que aguantan tres toques, ropa que se saca y tres
  zonas con conversación propia.
- **Desenlace 09_b con tres ramas** según cuánto la cuidaste: sin mensaje y no
  disponible, reproche con −5, o invitación a su habitación. El positivo se
  bifurca otra vez si no vas.
- Mónica se queda en el living todo el día y Jasmine no se baña mientras dura
  la quest (el baño es de donde sale la toalla).

### Ventajas y chats

- **"Beso"** (su habitación, de tarde) y **"Beso (Deseo)"** (de noche, con la
  secuencia de deseo 25). Fuera de lugar u horario ella responde con la pista,
  con los dos personajes en escena.
- **Ropa Nueva**: "volver a ver el jean", repetible. Si el MC está en otra
  locación, Violet lo cita a su habitación. Tres sprites nuevos de jean.
- **Mensajear**: dos conversaciones nuevas (intención en dos partes, ducha) y la
  ventaja "Nuevos Chats" del hito de deseo 30.
- **Hitos nuevos**: amor 20 "Jugando juntos", deseo 10 "Me calienta", deseo 20
  "Confesión", deseo 30 "Sinceridad".

### 0.1.9.1

- **Deseo 30 partida en dos quests**: "Sinceridad" (la noche de la charla) y
  "Distancia" (los tres días). Así el juego no exige hacer todo de corrido.
- **09_a**: golpear la puerta de tarde o de noche antes de saber que está
  enferma ahora hace que Violet conteste "Pasa" (antes decía que no estaba, en
  su propia puerta). Mónica pasa la noche en la cocina para no pisarse con
  Jasmine.
- **Quest 0_b**: ya no desaparece nadie. Mónica y Jasmine siguen su rutina pero
  quedan reservadas para la quest, y Violet está en su pieza.
- **Quest 02_b**: la opción de amor se reescribió ("Sigues siendo la misma de
  siempre") — las dos elecciones se leían casi iguales.

---

## Jugabilidad y presentación

- **Guía "Qué hacer" generada por el controlador** (0.1.9.1): el texto sale de
  lo que la quest declara (disparador + demandas), y muestra el estado en verde
  **Disponible** o en rojo **Interrumpida (motivo)** cuando algo externo la
  frena. Ya no hay textos escritos a mano que se desactualizan.
- **App de Pistas rediseñada** (0.1.9.1): solo pestañas, sin el toggle entre
  Pistas y Qué hacer; un `+` por pista despliega qué hacer y queda prendido o
  apagado de manera individual; sin barra de scroll; títulos de todas las apps
  centrados.
- **Tinte por horario** (0.1.9.1): los sprites de los personajes se tiñen según
  la hora (tarde, noche y trasnoche, en modo multiplicar). Los idles del HUD no
  se tiñen.
- **Dormir recorre los horarios** (0.1.9.1): la acción avanza hora por hora
  hasta la trasnoche sin que se vea, así lo que pasa en el medio puede
  interrumpir el sueño. El fondo se repinta debajo de la pantalla negra: al
  despertar ya no se ve la transición del fondo viejo al nuevo.
- **Viaje rápido con recorrido** (0.1.9a): ya no teletransporta. Calcula la ruta
  y la recorre tramo a tramo; si algo salta en el medio (una quest, un mensaje,
  un evento) el viaje se corta ahí y quedás donde te interrumpieron. En la
  0.1.9.1 se aceleró y cada cambio de fondo lleva un fundido corto.
- **"(Pensamiento)"** después del nombre cuando el MC piensa, a 3/4 del tamaño y
  con el color del nombre; el namebox subió a la mitad del textbox (0.1.9.1).
- **Pensamientos en blanco con itálica real** (0.1.9).
- **Disclaimer de ficción** en español (0.1.9).
- **Menú principal** (0.1.9.1): en pantalla grande el menú sube para despegarse
  de los enlaces, y ahora el nombre del enlace también linkea, no solo el icono.
- **Talk bloqueado** mientras Mónica o Jasmine están en bikini (0.1.9a) —
  temporal, hasta que exista el arte de cuerpo para el talk con ese skin.

---

## Bugs corregidos

### Reportados por jugadores

| Qué pasaba | Versión |
|---|---|
| **Soft lock de Mensajear**: la conversación genérica se reentregaba ya terminada, sin opciones para contestar, y su bloqueo cortaba TODAS las acciones ("Debo responderle primero a Violet") para siempre | 0.1.9a |
| **Amor 25, corte de luz**: se podía ver TV y caer en trasnoche antes de cocinar; a esa hora la puerta de Violet contestaba "debe estar durmiendo" y la opción "Entrar" no se dibujaba nunca | 0.1.9a |
| **04_d4 "La pizza"**: la única salida era la puerta de Violet de noche, y de noche podía estar en el living, en el baño o afuera | 0.1.9a |
| **Sinceridad (deseo 30)**: la reserva de la quest bloqueaba el golpe a la puerta que la propia quest necesitaba para entrar; con el reloj congelado y la restricción puesta, no quedaba ninguna acción posible | 0.1.9.1 (E10) |
| **Saves que no abrían**: un save que todavía tenía el evento del casco de realidad virtual pedía una función borrada en 0.1.8.6 y la carga moría con `AttributeError` | 0.1.9.1 (S12) |
| Un `%` literal en un diálogo crasheaba el juego ("30% de descuento") | 0.1.9(test) |
| 51 bloques de traducción vacíos: el jugador en inglés veía el cuadro de diálogo **en blanco** | 0.1.9(test) |

### Encontrados en auditoría

- **Mónica 0_b y Violet 04_b quedaban muertas para siempre**: su disparador
  vivía en `registrar_label_locacion`, que es un slot global único que cualquier
  otro contenido pisa (0.1.9).
- **Violet 0_b**, la primera quest del juego: el listener de "Cocinar" se
  registraba en runtime; guardar y cargar en el medio lo borraba y la
  restricción no se levantaba nunca (0.1.9a).
- **04_b** disparaba con Violet oculta por otra restricción y se llevaba puesta
  la cadena de evento03 (0.1.9a).
- **Deadlock 0_b de Mónica ↔ 09_a**: la 0_b bloqueaba dormir hasta ir al living
  y la 09_a, naciendo esa misma mañana, reservaba a Mónica y escondía ese
  disparador (0.1.9.1, E11).
- **Deseo 30**: la charla y la visita cerraban la quest cruzada, así que
  "Distancia" no se cerraba nunca y el hito de deseo 30 no se otorgaba
  (0.1.9.1, E12).
- Bloqueos globales que tapaban las apps del celular — el bloqueo que obligaba a
  escribirle a Violet escondía la app de Chat (0.1.9).
- Mensaje de chat duplicado que además trababa la quest; una foto sin texto que
  se perdía (0.1.9).

---

## Motor

### Controlador de quests (0.1.9.1)

El cambio más grande de la versión. Un sistema que sabe qué necesita cada quest
para jugarse y decide, solo, si puede empezar:

- **Las 47 quests declaran** lo que demandan (NPC, puerta, interacción,
  locación, acción, horario, día, ánimo, skin) y lo que consumen del mundo.
- **Capa 1 — nacer**: una quest no nace si pisa lo que otra ya tiene tomado;
  espera su turno en una cola.
- **Capa 2 — activar**: el disparador solo aparece si se cumple todo; si no, la
  guía dice por qué.
- **Punto de activación único** (`activar_quest`): todo camino por el que una
  quest arranca pasa por ahí y queda registrado (también en Sentry).
- **Reserva**: una quest que fija un momento ("vení esta noche") se reserva a
  ese personaje en ese horario, el reloj no pasa de largo, y el NPC solo ofrece
  las interacciones de esa quest. La 09_a reserva a Violet y Mónica los tres
  días de la enfermedad.
- **El "cuándo y dónde" salió de los disparadores**: antes cada uno chequeaba la
  hora y el lugar a mano; ahora lo hace el controlador con lo declarado.
- **Personajes prestados**: una quest que necesita a otro NPC en la casa lo pide
  con la locación madre, sin atarlo a un cuarto puntual.

### Otros sistemas

- **Restricciones con dueño** (0.1.9a): quien la puso es el único que puede
  levantarla, y mientras está activa el motor ignora los triggers ajenos. Es lo
  que protege una cadena en curso.
- **`congelar_reloj=True`** (0.1.9a): un solo interruptor que bloquea todo lo
  que gasta el día, en vez de ocho acciones enumeradas a mano en cada quest.
- **Disponibilidad de NPCs** (0.1.9): un interruptor por personaje que corta
  clickearlo, verlo, sus quests, sus rutinas y sus mensajes, aplicado en los
  siete embudos que ya existían.
- **Contacto diario** (0.1.9): registro de "hoy hice algo con ella", que usa
  deseo 30 para medir lo contrario.
- **Contenido de una ventaja** (0.1.9): el ojo del panel de Desbloqueos abre la
  lista de situaciones que habilita cada ventaja, con su estado y una pista.
- **Rutinas**: cupos por locación y reglas registrables, en vez del reparto de
  baños cableado a Violet y Jasmine (0.1.9).
- **`registrar_trigger_salir_celular`** (0.1.9): cuarto punto de enganche; el
  motor ya no conoce ninguna quest por nombre al salir del celular.
- **Chat**: `mensaje_inicial` y las opciones aceptan listas (varias burbujas);
  una foto sin texto es una burbuja de imagen y pasa por el "escribiendo"
  (0.1.9).
- **Nombres muertos** (0.1.9.1): una lista de funciones borradas que se declaran
  como stub, para que un save viejo nunca falle al abrirse. Lo que cierra S12.
- **Compatibilidad de saves por generación** (0.1.9): `JP_HISTORIAL_SAVES`
  decide, release por release, si las partidas anteriores siguen sirviendo. Los
  slots incompatibles salen deshabilitados en la pantalla de Cargar, con la
  versión con la que se crearon.

---

## Traducción al inglés

- 322 entradas que faltaban, traducidas (0.1.9(test)).
- 40 `old` reenganchados: una tilde nueva en la fuente desengancha la traducción
  en silencio y el jugador en inglés ve la línea en español.
- 51 bloques que Ren'Py había generado con la traducción vacía.
- Los 284 strings de `common.rpy` que salían vacíos en inglés (0.1.9).
- Purga de 23 huérfanos en el tl de deseo 30.
- El intercambio del cosplay por chat, que un tester no entendía: en español es
  un juego de palabras con "llamar la atención" y en inglés se había traducido
  con la misma elipsis, que no se sostiene (0.1.9.1).

---

## Reportes y diagnóstico

- **Los reportes de error y de feedback ahora dicen quién los manda** (el nombre
  del jugador, con `(tester)` si corre en modo dev) **y qué estaba procesando el
  controlador**: la restricción activa, las reservas y cómo veía a cada quest
  viva. En Sentry van como tag `jugador` y extra `controlador` (0.1.9.1).
- Sentry: tag de la última quest activada; agrupamiento reverificado.

---

## Herramientas (no viajan al jugador)

- **Panel del controlador en vivo** y **laboratorio de escenarios**: entrar a
  cualquier combinación (quest interrumpida, reserva, secuencia ajena) sin tener
  que avanzar hasta ahí jugando (0.1.9.1).
- **`tools/validar_bloqueos.py`** (0.1.9a, ampliado en 0.1.9.1): ocho chequeos
  que el lint no ve — reloj que se escapa, registros en runtime, salidas sin
  override, restricciones sin quien las levante, quests desalineadas con lo que
  declaran.
- **`tools/validar_traducciones.py`** (0.1.9(test)): seis chequeos de traducción
  que ni el lint ni nada avisan.
- **`tools/escanear_saves.py`** (0.1.9.1): lee los saves sin ejecutarlos y avisa
  si piden un nombre que el código ya no define, o sea un save que no va a
  abrir.
- **Harness de rutas**: rutas nuevas `planificador` y `mapa`, y tres pasos más en
  `mensajes`.
- **Herramienta de posicionamiento**: modo Zonas y tres listas excluyentes de
  imágenes (0.1.9).
- **Perfiles de tester**: `lucastest` → Lucas y `marcetest` → Marcelo, con
  acceso a las herramientas, como `alanhhdev` (0.1.9.1).
- **Skill `japitown-warnings`** (0.1.9a): los bugs de diseño que llegaron a
  jugadores, cada uno con su regla y su detector. Regla madre: *un bloqueo solo
  lo puede sostener algo que el jugador pueda resolver*.
