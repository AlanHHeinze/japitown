# Testing de sistemas por rutas

Complemento de `arquitectura_sistemas.md`. Explica cómo probar cada sistema recorriendo su
**ruta completa** — qué probar primero, qué debe pasar en cada punto, qué se dispara y a
dónde deriva — y cómo correr la versión automatizada para evitar el testeo manual tedioso.

**El harness automatizado vive en** `game/script/core/utils/test_rutas.rpy`.

---

## 1. Cómo correr las rutas automáticas

1. Abrir el juego en modo desarrollador (correr desde el SDK; `config.developer` activo).
2. **Iniciar una partida descartable** con "Comenzar". Nunca correr rutas desde el menú
   principal (los sistemas no están inicializados) ni en una partida que importe.
3. Abrir la consola con **Shift+O** y ejecutar:

```
jp_test_correr("quests")          # una ruta puntual
jp_test_correr_todas()            # todas las NO destructivas
jp_test_correr_todas(True)        # todas, incluidas las que mutan la partida
```

4. El resultado se imprime en la consola y se **acumula** en `test_rutas_resultado.txt`
   (raíz del proyecto). Cada corrida registra fecha, día y horario de la partida.

Cada ruta se **corta en el primer paso que falla** y reporta el paso exacto: eso responde
"el flujo funciona hasta acá, se rompe en este punto".

### Rutas disponibles

| Ruta | Qué recorre | Destructiva |
|------|-------------|:-----------:|
| `tiempo` | avanzar horario → dormir → día nuevo → resets → save_name | Sí |
| `quests` | catálogo → NPCs → rutinas → pistas | No |
| `eventos` | catálogo → condiciones → labels → validar_eventos() | No |
| `mensajes` | grupos → estructura de pasos/opciones → condiciones de entrega | No |
| `acciones` | catálogo → labels genéricos → disponibilidad | No |
| `restriccion` | activar → bloqueo de acción → bloqueo de movimiento → label por locación → liberar | Sí (reversible) |
| `shopping` | elegir item → fondos → orden → dormir hasta entrega → paquete → inventario | Sí |
| `talk` | reasignación diaria de estados → estado activo por NPC | Sí (reasigna el día) |
| `mapa` | puertas/tabla de acceso → viaje rápido vs locaciones reales | No |
| `guardado` | picklabilidad de TODO el estado guardable (anti-PicklingError) | No |
| `registros` | registros declarativos post-optimización: opciones/overrides/bloqueos de puerta, bloqueos del embudo, triggers de motor (labels existen, condiciones ejecutan, ids únicos) | No |

**"Destructiva"** = muta la partida (avanza días, compra, activa restricciones). Correrlas
solo en partidas descartables. Las no destructivas son de solo lectura (o repiten cosas que
el game_loop ya hace en cada vuelta, como `validar_eventos()`).

---

## 2. La ruta de cada sistema, explicada

Para cada sistema: la secuencia en orden, qué se dispara en cada punto y a dónde deriva.
La columna automatizable indica qué cubre el harness y qué queda para prueba jugada.

### 2.1 Quest (el flujo más importante)

Una quest atraviesa SIEMPRE esta secuencia — probar en este orden:

1. **Registro** (`init 5-11`): la quest existe en `sistema_quests.quests` con su `npc_id`.
   → *Automatizado: ruta `quests`, pasos 1-2.*
2. **Inicio**: `quest.puede_iniciar()` pasa a True (requisitos: stat, día, quest previa) y
   algo llama `iniciar()` — normalmente `actualizar_quests()` en el tick del tiempo.
   → Verificar: `etapa_actual` pasa de 0 a INICIALIZACION→ESPERA (2).
3. **Espera → Condiciones (3) → Rutina (4) → Botón listo (5)**: cada avance ocurre en
   `actualizar_quests()`, que corre al avanzar horario y al dormir. Si una quest "no
   avanza", el primer sospechoso es su condición de etapa; el segundo, que nada esté
   llamando al tick (dormir siempre lo llama).
   → *Manual: consola `sistema_quests.obtener_quest("id").etapa_actual` antes/después de dormir.*
4. **Rutina de quest**: en etapa 4-5 el NPC se mueve a la locación de la rutina (pisa su
   rutina normal, con vigencia por locación — fix E07).
   → *Automatizado: ruta `quests` paso 3 valida que la locación exista; que el NPC esté ahí es prueba jugada.*
5. **Disparador**: según la quest, uno de estos (y solo uno — regla post-refactor).
   Desde la optimización 2026-07-31 TODOS son registros declarativos que el contenido
   puebla en `init 5` desde sus propios archivos (el motor solo itera):
   - **Botón del menú NPC** (`interactions_<npc>.rpy`) — clickear al NPC SIEMPRE abre menú.
   - **Entrada a locación** (`registrar_label_locacion`) — Mónica 0_b, Violet 04_b.
   - **Opción de puerta** (`registrar_opcion_puerta`, en `puertas_<npc>.rpy`) — cadena de Violet.
   - **Al dormir/despertar** (`registrar_trigger_dormir`, fase "antes"/"despues") — Violet 08_a, 09_a, evento 2.
   - **game_loop** (`registrar_trigger_game_loop`) — Violet 09_a piensa, Jasmine 0_b, MC q0/q0b.
   - **Al avanzar horario** (`registrar_trigger_avanzar`) — MC q0 espera.
   - **Item / chat completado** — Mónica 0_c, Violet 07_c.
   La ruta `registros` valida que todo lo registrado sea consistente.
6. **Desarrollo (etapa 7)**: el label de contenido corre; si restringe el mundo usa
   `activar_restriccion(...)`. El label termina en `jump game_loop` (contenido) — nunca
   `return` frameless.
7. **Cierre**: `completar_quest_actual(npc)` → dispara mensajes (`disparar_por_trigger("quest", ...)`)
   → la siguiente quest de la cadena queda habilitada para su propio `puede_iniciar()`.
   → Verificar: pistas del HUD actualizadas, restricción desactivada, Talk sigue disponible.

**Puntos que históricamente se rompieron** (revisar siempre al probar una quest):
- terminar en `return` sin frame → main menu (regla `jump game_loop`).
- registrar acciones/labels en runtime en vez de `init` → se pierde al cargar save.
- lambdas en config → PicklingError al guardar (ruta `guardado` lo detecta).
- doble disparador (botón + locación) → el botón queda inalcanzable (caso Violet 04_b).

### 2.2 Tiempo

Secuencia: `avanzar_horario()` ×3 → `dormir()`.

- Al **avanzar horario** se dispara en orden: paquete del repartidor (si era mañana) →
  rutinas de NPCs → fallos de quests → `actualizar_quests()` → mensajes en espera.
- Al **dormir** se dispara: reset de horario y día +1 → stock (lunes) → `save_name` →
  resets diarios (entrenamiento/trabajo/interacciones NPC) → rutinas especiales del día →
  rutinas → quests → mensajes omitidos y en espera → entregas (prende `repartidor_presente`)
  → resets de acciones → estados de talk.
- Después de `dormir()` el label `accion_dormir` sigue con: autosave (checkpoint + slot A)
  → triggers de contenido (08_a, 09_a, ev03) → `mensajes_al_despertar`.

→ *Automatizado: ruta `tiempo` (sin la parte de contenido del label). Los triggers de
contenido al dormir son prueba jugada: dormir con la quest correspondiente activa.*

### 2.3 Mensajes

1. Un trigger dispara el grupo (`disparar_por_trigger(tipo, id, npc)`) — desde quests
   (etapa/completada/fallo), eventos o manual.
2. Si el grupo tiene **condición de entrega** u horario, queda **en espera**; se re-evalúa
   al avanzar horario, al dormir y al moverse.
3. Entregado: aparece la notificación y el chat en el celular; si es **prioritario**,
   bloquea dormir/avanzar hasta responderlo (y puede despertar al MC).
4. Al completar el grupo: puntos → recompensas por tabla → `grupo_completado(id)` queda
   True (las quests lo usan como requisito).

→ *Automatizado: ruta `mensajes` (estructura y condiciones). El flujo de entrega/respuesta
es prueba jugada: la ruta `tiempo` fuerza las re-evaluaciones.*

### 2.4 Eventos

1. `validar_eventos()` corre en CADA vuelta del game_loop: oculto → visible
   (condición de aparición) → activo (condición de activación o auto).
2. Visible/activo: aparece en pistas; sus botones "(Evento)" salen en el menú del NPC.
3. Completado: si es esporádico desaparece; los replay usan labels `_check_replay`.

→ *Automatizado: ruta `eventos` (condiciones ejecutan, labels existen, validar corre).*

### 2.5 Shopping

Compra → orden con día de entrega → al dormir ese día `repartidor_presente` → atenderlo
(o no: al pasar a tarde deja `paquete_en_habitacion`) → interacción entrega items →
`inventario`. Los items con `condicion_uso` se usan desde el inventario.

→ *Automatizado: ruta `shopping` completa (compra hasta inventario, incluyendo el paquete
no atendido). Atender al repartidor en persona es prueba jugada (labels de contenido).*

### 2.6 Restricción de quest

Activar → solo locaciones permitidas, acciones bloqueadas con mensaje, NPCs ocultos,
celular bloqueado, labels por locación → desactivar al cerrar la escena.

→ *Automatizado: ruta `restriccion` entera (activa una de prueba y la revierte).*

### 2.7 Door access

Click en puerta → `accion_hotspot_move` desvía a `interaccion_puerta_npc` → opciones por
quest activa + decisión por stats (`TABLA_ACCESO_HABITACION`: Violet 50/50/30/10, Jasmine y
Mónica 50/40/15/0) → entrar / dejar pasar / sale al pasillo / no abre.

→ *Automatizado: ruta `mapa` (consistencia de tablas). Los umbrales por stat son prueba
jugada rápida: `obtener_npc("violet").modificar_stat("amor", 50)` en consola y golpear.*

### 2.8 Talk / Skins / Pensamientos

Talk: estado diario reasignado al dormir; opciones especiales con condición; el botón
Hablar vive en el menú (siempre presente post-refactor). Skins: condición de desbloqueo +
menú. Pensamientos: registrados por contenido, ofrecidos en la cama antes de dormir.

→ *Automatizado: ruta `talk` (reasignación). El contenido de las conversaciones es jugado.*

### 2.9 Guardado / Persistencia

La ruta `guardado` corre `jp_buscar_no_picklables()` sobre todas las raíces del save: si
algo (lambda, def anidada) rompería el guardado, lo lista SIN necesidad de guardar.
Correrla **después de agregar cualquier callable a un objeto con estado** es la forma
barata de evitar el PicklingError clásico.

Prueba jugada complementaria: guardar, cargar, y verificar que la quest activa siga
avanzando (detecta registros hechos en runtime en vez de `init`).

---

## 3. Cómo agregar una ruta nueva

En `test_rutas.rpy`:

1. Escribir cada paso como función `_jpt_<ruta>_<paso>()` que devuelva
   `_jpt_ok("detalle")` o `_jpt_fallo("qué se rompió")`. Estado compartido entre pasos:
   dict `_JPT_CTX` (se limpia al arrancar cada ruta).
2. Registrar la ruta en `JP_RUTAS_TEST` con nombre, sistemas cubiertos, flag
   `destructiva` y la lista ordenada de pasos.
3. Regla: los pasos van **en el orden real del flujo** (qué probar primero), y cada
   `_jpt_fallo` debe decir qué esperaba y qué encontró — el mensaje es el diagnóstico.

Plantilla mental para diseñar la ruta de una quest nueva: seguir §2.1 punto por punto y
escribir un paso por transición (registrada → puede iniciar → etapa avanza al dormir →
disparador visible → …). Todo lo que sea estado (etapas, flags, inventario, locación del
NPC) es automatizable; solo el diálogo en pantalla queda manual.
