# Propuestas de mejora — a partir de la 0.1.9.1

Relevamiento hecho el 2026-09-14, con la 0.1.9.1(Test) a dos días de salir, sobre el
estado real del código (lint, validadores, `planificador.md`, lo que quedó pendiente
de la tanda del controlador). Son sugerencias: nada de esto está implementado.

Cada propuesta lleva: qué es, por qué calza con el proyecto, con qué se arma (lo
que ya existe), cuánto altera, cuánto testeo pide y qué riesgo trae. Están
ordenadas dentro de cada bloque por lo que conviene hacer antes.

Al tomar una: marcarla acá con la fecha y la versión en la que entró, o tacharla
con el motivo si se descarta.

---

## A. Técnicas y de cierre

### A1. Cerrar los assets faltantes que el lint y el validador ya ven

- **Qué**: el lint reporta en cada corrida `audio/sfx/door_knock_3.ogg` (7 sitios:
  puertas de Violet, 04_b, 08_a, 09_a) y `violet_quest01_limpiando_alacena.png`
  (evento03); la memoria del proyecto lista ~22 refs a imágenes inexistentes
  (interacciones de quest 4, `camisa.png`, `caja_cerrada`); el idle de Mónica en la
  cocina se llama `..._skinbae.jpg` (typo). En un build de release no crashea, pero
  el golpe de puerta suena mudo y las imágenes salen como cuadro vacío.
- **Por qué calza**: lo ve un tester en la primera media hora y no lleva diseño.
- **Alcance**: assets + nombres de archivo; cero lógica.
- **Testeo**: bajo — lint a cero de "not loadable", golpear una puerta, evento03.
- **Riesgo**: mínimo. Cuidado con el rename del `skinbae` (rutina base y 09_a
  apuntan al mismo nombre).

### A2. Un solo comando de verificación pre-release (`tools/validar_todo.py`)

- **Qué**: un script que corra en orden lint, `validar_bloqueos`,
  `validar_traducciones`, `validar_sprites` y el harness headless (un
  `game/zz_headless_test_tmp.rpy` con `init 999 python` que corre las rutas
  `registros`, `planificador` y `guardado` durante el lint y se borra), y falle con
  un resumen de una pantalla. Hoy son cinco comandos y el harness solo corre a mano
  dentro del juego.
- **Por qué calza**: con lanzamientos cada pocos días, olvidarse uno es el tipo de
  bug que llegó a jugadores en la 0.1.9.
- **Alcance**: solo `tools/`.
- **Testeo**: correrlo.
- **Riesgo**: ninguno para el juego.

### A3. Unificar los dos flujos de dormir que quedaron con la pantalla vieja

- **Qué**: `accion_dormir` usa `animacion_dormir_capa` (repinta el fondo debajo del
  negro). Amor 25 y el minijuego de la 09 siguen con `call screen animacion_dormir`:
  al despertar se ve la transición de fondo que ya se sacó del flujo principal.
  Además quedó muerta `obtener_horario_despertar_prioritario` (el recorrido de
  horarios la reemplazó).
- **Alcance**: dos labels de contenido + borrar una función.
- **Testeo**: medio-bajo — dormir en el domingo de amor 25 y al cierre de la 09_b.
- **Riesgo**: bajo; el patrón ya está probado (orden: esconder la pantalla →
  autosave).

### A4. Avisos del controlador en el mundo (notificaciones)

- **Qué**: cuando la capa 2 esconde un botón o una quest pasa a "Interrumpida", el
  jugador no ve nada hasta abrir Pistas. `hud_notificaciones.rpy` ya existe (lo usan
  los hitos): disparar una notificación breve cuando una quest **nace**, pasa a
  **Disponible** o queda **Interrumpida (motivo)** — un aviso por transición,
  comparando `planificador_estado_guia` entre vueltas del game_loop.
- **Por qué calza**: cierra el círculo del controlador: el sistema ya sabe el
  motivo; falta decirlo sin que el jugador vaya a buscarlo.
- **Se arma con**: una función en `planificador.rpy` (estado anterior por quest,
  guardado) + una llamada en `game_loop`. Ningún archivo de contenido.
- **Testeo**: medio — los escenarios `interrumpida_*` y `disponible` cubren cada
  transición.
- **Riesgo**: bajo-medio: evitar el spam (una por transición) y no notificar en
  medio de una escena (solo con el HUD visible).

### A5. Agenda en la app de Pistas ("qué viene")

- **Qué**: una sección al final de cada pestaña con las quests que todavía no
  están listas y lo que les falta, calculado de lo declarado: días de espera,
  el requisito de día ("el domingo", amor 25), el stat que falta ("amor 15/20"),
  las reservas vigentes ("esta noche es de Violet"). Hoy esa info existe pero
  repartida entre la pista de CONDICIONES y el panel dev.
- **Por qué calza**: el juego tiene mucho "esperar N días" y "subir un stat"; el
  jugador que ve "te faltan 5" y "Amor 25: el domingo" planifica la semana en vez
  de probar puertas. Es la lógica del calendario de Persona sobre lo que el motor ya
  sabe.
- **Alcance**: `hud_pistas.rpy` + un helper de lectura en `planificador.rpy`.
- **Testeo**: bajo-medio.
- **Riesgo**: bajo; lectura pura (regla de screens sin efectos secundarios).

### A6. Predicción de imágenes en el viaje rápido y el cambio de horario

- **Qué**: los fondos son JPG 1920×1080 (34 MB) y el viaje rápido muestra 2-4 en un
  segundo; cada uno se decodifica la primera vez. `renpy.start_predict` de los
  fondos de la ruta al iniciar el viaje (la ruta ya se calcula antes de caminar) y
  del fondo del próximo horario; los fundidos de 0.15 s dejan de tartamudear, sobre
  todo en web.
- **Alcance**: `viaje_rapido.rpy` (2 líneas) y `avanzar_horario` (1 línea).
- **Testeo**: bajo — viajar de punta a punta en las cuatro horas; probar en web.
- **Riesgo**: mínimo.

### A7. Paso B: el disparador entero se declara

- **Qué**: lo acordado en `planificador.md`: `Disp` ya dice tipo y texto; falta que
  el motor **arme** el botón del menú, la opción de puerta o el trigger de locación
  desde la declaración. Desaparecen ~20 `_gl_trigger_*`, los bloques de
  `interactions_<npc>.rpy` y la mitad de `puertas_violet.rpy`; una quest nueva se
  escribe entera en `planificacion_<npc>.rpy` + su label.
- **Por qué calza**: es la conclusión natural del controlador; hoy hay tres fuentes
  (declaración, disparador a mano, texto del botón) que el validador mantiene
  alineadas a fuerza de chequeos.
- **Alcance**: alto — motor de menús/puertas/triggers y 45 quests.
- **Testeo**: alto — cada disparador, uno por uno.
- **Riesgo**: medio-alto: es el tipo de cambio que produce botones que no aparecen.
  Va con la generación de saves siguiente, no con un parche.

### A8. Ventajas con demandas propias (y ánimo con peso narrativo)

- **Qué**: las ventajas (beso, jugar, ropa nueva, mensajear, provocación) hoy solo se
  esconden por reserva; el diseño preveía que declaren demandas
  (`interaccion:violet:beso`, `npc:violet en=su pieza, libre`). Y `Rec(animo=...)`
  está implementado pero ninguna quest lo usa (ver también B3).
- **Alcance**: medio — declaraciones + 5 ventajas + algunos estados de talk.
- **Testeo**: medio.
- **Riesgo**: medio: un ánimo mal declarado esconde una ventaja durante días (misma
  clase que la advertencia A12 del skill).

### A9. Eventos → ventajas

- **Qué**: el sistema de eventos viejo (masaje de Mónica, evento de Jasmine, evento03
  de Violet) convive con hitos/ventajas y es el único contenido que el controlador
  no gobierna. El doc ya lo declara a extinguir.
- **Por qué calza**: el evento03 fue origen de un bug real (cadena pisada por la
  04_b); con el controlador cubriéndolo, ese choque deja de existir.
- **Alcance**: medio-alto — 3 eventos, sus screens y `eventsystem_core`.
- **Testeo**: medio-alto.
- **Riesgo**: medio: saves con eventos a medias necesitan migración (patrón:
  `_gl_trigger_vd30_migracion`).

### A10. Snapshot del controlador en Sentry

- **Qué**: al crash, adjuntar `planificador_estado()` (qué espera, qué reserva, qué
  bloquea) como contexto, junto al tag `quest_activada` que ya va. Los tres
  reportes de la 0.1.9a se diagnosticaron reconstruyendo el estado desde capturas.
- **Alcance**: `sistema_sentry.rpy`, ~10 líneas.
- **Testeo**: bajo (`jp_forzar_error_prueba` desde consola).
- **Riesgo**: mínimo.

**Orden sugerido**: A1, A2, A3 son cierre (una tarde). A4 y A5 son lo que más se
nota jugando y usan lo construido. A6 si hay tiempo. A7, A8, A9 son la siguiente
etapa y conviene arrancarlas con la 0.1.9.1 ya afuera. A10 en cualquier momento.

---

## B. Jugabilidad con el contenido actual

Sin escenas nuevas ni assets más allá de un icono. Lo que ya existe y se puede
conectar: acciones diarias (trabajar 2/día +20, entrenar 1/día +1 stat), 4 stats
del MC que hoy gatean 4 decisiones, una tienda con items sin uso (Vino, Pesas,
Jabón, Aceite, Silicona), talk diario con 11 estados de Violet, skins por día,
galería de fotos de chat, menú de Pensamientos con 2 entradas, notificaciones,
y el controlador con `Rec(animo=)` sin usar.

### B1. Que los stats del MC sirvan todos los días

- **Hoy**: fuerza / carisma / destreza / inteligencia se entrenan y gatean cuatro
  decisiones puntuales (carisma ≥ 3 en la 05_c, fuerza ≥ 3 en la 06_b, destreza en
  la 08_a, inteligencia = memoria del talk). El jugador entrena sin saber para qué.
- **Qué**: engancharlos a lo diario: *carisma* sube el `+1` del talk a `+2` cuando
  acierta (a partir de 5, el umbral que ya existe para "reconsiderar"); *fuerza*
  permite 2 entrenamientos por día o desbloquea "Pesas" (item existente, hoy no
  usable); *inteligencia* muestra en Pistas el "qué hacer" completo del controlador
  y sin ella solo la pista; *destreza* suma 5 a "Trabajar" cada 3 puntos.
- **Se arma con**: `talksystem_core` (efectos), `hud_stats` (entrenar/trabajar),
  `hud_pistas` (un `if`), `items_shopping` (Pesas usable).
- **Alcance**: bajo-medio, motor/UI; ninguna quest.
- **Testeo**: medio — el balance más que la mecánica.
- **Riesgo**: medio: cambia la velocidad de subida de stats de NPC; revisar los
  umbrales de las líneas (5-30) contra las ganancias nuevas.

### B2. Regalos con los items que ya están en la tienda

- **Hoy**: Vino, Pesas, Loción, Jabón, Aceite, Silicona están en el catálogo con
  precio y descripción; varios ni siquiera son `usable`. La plata de "Trabajar" solo
  compra items de quest.
- **Qué**: opción "Regalar" en el menú de cada NPC que consuma un item del inventario
  y dé stat según una tabla NPC×item (Vino → Mónica +2 amor, Aceite/Loción → Jasmine
  +2 deseo, Golosinas → Violet +1…), una vez por día por NPC, con una línea genérica
  del NPC.
- **Se arma con**: las opciones del menú (`_opciones_extra_<npc>`), `inventario`,
  `modificar_stat`, y `Rec("interaccion", npc, accion="regalo")` para que el
  controlador lo esconda como a una ventaja cuando el NPC está reservado.
- **Alcance**: bajo — un archivo nuevo (`core/gifts/`) + una entrada por NPC.
- **Testeo**: bajo-medio (tabla, tope diario, 3-4 traducciones).
- **Riesgo**: bajo; balance (tope diario y precios).

### B3. Talk con consecuencias entre días: el ánimo que el controlador ya entiende

- **Hoy**: el talk asigna un estado al azar; acertar da +1, errar −1 o nada; al día
  siguiente se olvida. `Rec(animo=...)` existe y nadie lo usa.
- **Qué**: (a) *Racha*: acertar tres días seguidos activa "de buen humor" (los
  estados especiales con `dias_duracion` ya existen) que duplica el resultado al
  día siguiente; errar dos seguidos activa "enojada" (ya existe). (b) Dos o tres
  quests demandan ánimo: la 06_a pide que no esté enojada; el beso de deseo pide
  "hot". El talk pasa de minijuego suelto a preparar las quests.
- **Se arma con**: `EstadoTalk` especiales + `activar_estado_especial_npc`,
  `Rec(animo=)` en tres declaraciones.
- **Alcance**: bajo en código; medio en diseño.
- **Testeo**: medio — que "enojada" no deje una quest Interrumpida más de un día.
- **Riesgo**: medio: es el tipo de bloqueo que el skill de warnings pide vigilar; la
  salida (esperar / acertar el talk) tiene que estar en la guía.

### B4. Pensamientos con contenido

- **Hoy**: el menú "Pensar" al dormir tiene 2 pensamientos registrados en todo el
  juego.
- **Qué**: generarlos desde el estado, sin escribir escenas: uno por quest
  **Disponible** (el "qué hacer" del controlador en primera persona: "Mañana podría
  ir a la puerta de Violet por la tarde…"), uno por quest **Interrumpida** con el
  motivo, uno por hito cerca del umbral ("Siento que Violet está más cerca de
  confiar en mí" cuando faltan ≤ 3).
- **Se arma con**: `pensamiento_system` + `planificador_estado_guia` +
  `planificador_que_hacer`.
- **Alcance**: bajo — un archivo de pensamientos genéricos.
- **Testeo**: bajo. **Riesgo**: mínimo.

### B5. La galería como colección

- **Hoy**: junta las fotos que llegan por chat, sin más.
- **Qué**: mostrar los huecos: cuántas fotos existen por NPC y cuántas tiene
  ("Violet 3/7"), con el slot vacío en gris. El total se cuenta en init de los
  grupos registrados (`foto_inicial` / `foto_respuesta`). Incentivo de rejugar
  Mensajear sin arte nuevo.
- **Alcance**: bajo — `hud_galeria.rpy`. **Testeo**: bajo.
- **Riesgo**: mínimo; no revelar por nombre fotos de quests futuras (mostrar "?").

### B6. Skins y días con sentido de calendario

- **Hoy**: el día de la semana decide rutinas y skins (bikini de Mónica/Jasmine
  ciertos días, Violet duerme hasta tarde el sábado, domingo en el living), sin
  forma de saberlo salvo memoria.
- **Qué**: en el tracker del HUD agregar la próxima aparición notable ("Mónica ·
  bikini mañana en el patio", "Violet · domingo en el living"), leída de las rutinas
  visuales y las condiciones de skin registradas.
- **Alcance**: bajo — una función de lectura y una línea en `hud_tracker.rpy`.
- **Testeo**: bajo. **Riesgo**: mínimo.

### B7. Mensajear con iniciativa del NPC

- **Hoy**: Mensajear es una ventaja: el jugador escribe cuando quiere; los NPCs solo
  mandan mensajes de quest.
- **Qué**: que el pool genérico (`mv_respuestagenerica`, ya escrito) también lo
  inicie Violet sola con probabilidad baja (10-15 % por día, no más de uno cada 3
  días, nunca con un prioritario pendiente ni con reserva puesta). Cero texto
  nuevo: los mismos grupos con la dirección invertida.
- **Se arma con**: un trigger de dormir "despues" que elige un grupo del pool y lo
  entrega con `disparar_por_trigger`; `puede_responder()` y el embudo de mensajes
  cubren lo demás.
- **Alcance**: bajo — un archivo en `ventajas/mensajear/`.
- **Testeo**: medio — la interacción con prioritarios y con el recorrido de dormir
  (decidir que NO cuentan como prioritarios).
- **Riesgo**: medio-bajo: el sistema de mensajes fue la fuente de los soft locks de
  la 0.1.9a; va con la ruta `mensajes` del harness.

### B8. Usos diarios visibles en cada acción

- **Hoy**: límites sueltos por acción (trabajar 2/día, entrenar 1/día, talk 1/día,
  hablar/cocinar por horario) que el jugador descubre a golpes de "ya lo hiciste".
- **Qué**: mostrar los usos que quedan en los botones ("Trabajar 1/2", "Entrenar ✓")
  y atenuar el agotado — la información existe (`trabajo_hoy`, `entrenamiento_hoy`,
  `_usados_hoy` de acciones; los botones ya tienen `esta_disponible` y
  `mensaje_reintento`).
- **Alcance**: bajo, solo UI (`hud_stats.rpy`, `actionsystem_screen.rpy`).
- **Testeo**: bajo. **Riesgo**: mínimo.

**Orden sugerido por juego que dan por hora de trabajo**: B4 y B8 son una tarde y se
sienten enseguida; B2 y B6 son un día y dan uso a la tienda y a las skins; B1 y B3
son las que más cambian la sensación de progreso pero piden decidir números; B7 es
la que más vida le da a Violet y la que más testeo pide; B5 es cosmética pero
barata.
