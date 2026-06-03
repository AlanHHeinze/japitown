# Versión 0.1.3

---

## 1. Sistema de Talk (nuevo)

### Qué es

El sistema de Talk reemplaza la interacción directa con los NPCs por un mini-juego de conversación. Cuando el jugador habla con un NPC, aparece una escena con sprites y un menú de 5 opciones. Cada NPC tiene un **estado de ánimo** del día que determina qué efecto produce cada opción (positivo, negativo o neutro). El jugador no sabe de entrada cuál opción conviene, y tiene que aprenderlo a lo largo de las partidas.

---

### Archivos del sistema

| Archivo | Contenido |
|---|---|
| `game/script/core/talk/talksystem_core.rpy` | Clases, constantes, y el gestor central `SistemaTalk` |
| `game/script/core/talk/talksystem_labels.rpy` | Label `talk_iniciar` — el flujo completo de la interacción |
| `game/script/characters/violet/talk/violet_talk.rpy` | Estados y configuración de Violet |
| `game/script/characters/monica/talk/monica_talk.rpy` | Estados y configuración de Mónica |
| `game/script/characters/jasmine/talk/jasmine_talk.rpy` | Estados y configuración de Jasmine |

---

### Flujo de una interacción Talk

```
1. Al despertar (despertar_system.rpy)
   └─ sistema_talk.asignar_estado_aleatorio(npc_id)
      └─ Elige un estado general al azar y lo guarda en npc.talk_estado_id

2. Jugador hace click en el NPC → call talk_iniciar

3. Validaciones:
   ├─ accion_bloqueada("hablar") → si está bloqueado, muestra piensa y sale
   ├─ NPC existe y tiene config registrada
   └─ npc.puede_interactuar("hablar") → solo una vez por día

4. Se obtiene el estado activo:
   ├─ Si hay estados especiales activos → el de mayor jerarquía
   └─ Si no → el estado general asignado al despertar

5. Escena de conversación:
   ├─ ocultar_hud()
   ├─ scene con el background de la locación actual
   ├─ show mc_parado_base (izquierda)
   ├─ show sprite del NPC (derecha, según obtener_sprite_menu_npc)
   └─ Narrador muestra estado.intro ("Violet parece estar ansiosa.")

6. Menú de 5 opciones:
   ├─ Complacerla / Provocarla / Escucharla / Hablarle / Adularla
   ├─ Opciones ya usadas muestran el resultado recordado en verde
   ├─ Si mc_carisma ≥ 2: una opción desconocida muestra un preview en amarillo
   └─ Opciones especiales se agregan al final si su condición es True

7. Resultado:
   ├─ Se determina el resultado_id según estado.efectos[opcion_elegida]
   ├─ Si mc_carisma ≥ 5 y resultado negativo y no usó reconsiderar:
   │   └─ piensa "No creo que esto dé buen resultado..." → vuelve al menú
   ├─ Se registra la interacción (bloquea hablar por el resto del día)
   ├─ Se modifica el stat correspondiente
   └─ Se muestra un texto combinado con 4 partes (ver abajo)

8. Post-interacción:
   ├─ Se guarda en la memoria del MC (limitado por mc_inteligencia)
   ├─ Se asigna el estado posterior al NPC (para otros sistemas)
   └─ Se vuelve al HUD
```

---

### Las 5 opciones base

Siempre son las mismas para todos los NPCs:

| ID | Texto en menú |
|---|---|
| `complacerla` | Complacerla |
| `provocarla` | Provocarla |
| `escucharla` | Escucharla |
| `hablarle` | Hablarle |
| `adularla` | Adularla |

---

### Los 5 resultados posibles

Cada estado distribuye exactamente estos 5 resultados entre las 5 opciones (uno por opción, sin repetir):

| resultado_id | Efecto en stats | Texto visible |
|---|---|---|
| `+2_amor` | amor +2 | "+2 amor" |
| `+1_deseo` | deseo +1 | "+1 deseo" |
| `-2_amor` | amor -2 | "-2 amor" |
| `-1_deseo` | deseo -1 | "-1 deseo" |
| `nada` | sin efecto | "sin efecto" |

---

### Texto de resultado (4 partes en un bloque)

El resultado se muestra como un único texto narrado que une 4 partes:

```
Parte 1: config.mensaje_general
         "Tuviste un momento de conversación con Violet."

Parte 2: config.mensajes_opciones[opcion_elegida]
         "Decidiste provocarla."

Parte 3: estado.mensaje
         "Violet estaba ansiosa y nerviosa."

Parte 4: config.resoluciones[resultado_id]
         "Violet quedó muy molesta con la situación."

→ Resultado final: "Tuviste un momento de conversación con Violet. Decidiste provocarla. Violet estaba ansiosa y nerviosa. Violet quedó muy molesta con la situación."
```

---

### Sistema de memoria del MC

El MC recuerda el resultado de combinaciones (NPC, estado, opción) ya usadas. Esas opciones se marcan en verde en el menú con el resultado recordado.

- **Límite**: `mc_inteligencia` entradas por NPC (mín. 1)
- **Almacenamiento**: `store.talk_memoria[npc_id]` — lista de dicts `{estado, opcion, resultado}`
- Con mc_inteligencia 1, solo recuerda la última interacción por NPC

---

### Preview de carisma (mc_carisma ≥ 2)

Si el MC tiene carisma 2 o más, el juego elige al azar una opción que el jugador aún no conoce para ese estado y muestra el resultado en amarillo con un signo de pregunta:

```
Escucharla  (+2 amor?)   ← preview en amarillo, puede ser incorrecto
```

El preview se basa en el resultado real, no es al azar — es información filtrada por el carisma del MC.

---

### Reconsiderar (mc_carisma ≥ 5)

Si el MC tiene carisma 5 o más y elige una opción que daría un resultado negativo (`-2_amor` o `-1_deseo`):

- Se muestra: `piensa "No creo que esto dé buen resultado..."`
- El menú vuelve a aparecer con las mismas opciones
- Solo funciona una vez por interacción (`talk_reconsiderar_usado`)

---

### Estados de ánimo por NPC

Cada NPC tiene 6 estados generales. Uno se asigna al azar al despertar cada día.

#### Violet

| ID | Nombre | Intro |
|---|---|---|
| `violet_defensiva` | Defensiva | "Violet parece estar a la defensiva hoy." |
| `violet_molesta` | Molesta | "Violet parece estar molesta." |
| `violet_dormida` | Dormida | "Violet parece tener sueño." |
| `violet_hambre` | Hambre | "Violet parece tener hambre." |
| `violet_ansiosa` | Ansiosa | "Violet parece estar ansiosa." |
| `violet_sumisa` | Sumisa | "Violet parece estar especialmente dócil hoy." |

#### Mónica

| ID | Nombre | Intro |
|---|---|---|
| `monica_cansada` | Cansada | "Mónica parece estar cansada." |
| `monica_ocupada` | Ocupada | "Mónica parece estar ocupada con algo." |
| `monica_picante` | Picante | "Mónica tiene un brillo picante en los ojos." |
| `monica_alegre` | Alegre | "Mónica parece estar de muy buen humor." |
| `monica_energica` | Enérgica | "Mónica está llena de energía." |
| `monica_abierta` | Abierta | "Mónica parece estar abierta y receptiva." |

#### Jasmine

| ID | Nombre | Intro |
|---|---|---|
| `jasmine_provocativa` | Provocativa | "Jasmine parece estar en humor provocativo." |
| `jasmine_celosa` | Celosa | "Jasmine parece estar celosa." |
| `jasmine_tranquila` | Tranquila | "Jasmine parece estar tranquila y relajada." |
| `jasmine_alegre` | Alegre | "Jasmine parece estar de muy buen humor." |
| `jasmine_energica` | Enérgica | "Jasmine está llena de energía." |
| `jasmine_agotada` | Agotada | "Jasmine parece estar agotada." |

---

### Estados especiales

Además de los generales, el sistema soporta **estados especiales** que se activan desde quests, eventos o ítems. Tienen prioridad sobre el estado general.

- Tienen `es_especial=True`, una `jerarquia` (número) y `dias_duracion`
- Si hay varios especiales activos, el de mayor jerarquía tiene prioridad
- Se decrementan al dormir. Cuando llegan a 0 días, se eliminan
- Se activan con: `activar_estado_especial_npc(npc_id, estado_id, dias_duracion=None)`

---

### Opciones especiales

Además de las 5 opciones base, se pueden agregar opciones extra que aparecen en el menú bajo condiciones específicas (una quest activa, tener un ítem, etc.).

```python
OpcionEspecialTalk(
    id="darle_flores",
    texto="Darle flores",
    condicion=lambda: inventario.get("flores", 0) > 0,
    mensaje_opcion="Le diste flores.",
    resultado_id="+2_amor",
    item_requerido="flores",
    item_consumible=True,
)
```

Los callables (`condicion`, `recompensa_extra`) se excluyen del pickle para no romper los saves.

---

### Cómo agregar un estado nuevo a un NPC

En el archivo `*_talk.rpy` del NPC, dentro de `estados_<npc>`:

```python
EstadoTalk(
    id="violet_nueva",
    nombre="Nombre visible",
    intro="Texto narrado antes del menú.",
    efectos={
        "complacerla": "+2_amor",   # cada opción tiene un resultado distinto
        "provocarla":  "-1_deseo",  # los 5 resultados deben aparecer una vez
        "escucharla":  "+1_deseo",
        "hablarle":    "nada",
        "adularla":    "-2_amor",
    },
    mensaje="Violet estaba [descripción para parte 3 del resultado].",
    estados_posteriores={
        "+2_amor":  "posterior_feliz",
        "+1_deseo": "posterior_hot",
        "-2_amor":  "posterior_molesta",
        "-1_deseo": "posterior_cerrada",
        "nada":     "posterior_indiferente",
    },
),
```

Luego agregar el ID a `estados_generales_ids` si es un estado general.

---

## 2. Bug fix — Diálogos desapareciendo

### Síntoma

Los mensajes de diálogo (`say`, `piensa`) aparecían brevemente y desaparecían. El juego seguía esperando el click del jugador pero el texto no era visible. Afectaba especialmente a los últimos mensajes de cada label de quest.

### Causa

En `hud_notificaciones.rpy`, el screen `notificaciones_stats` estaba registrado como overlay persistente (`config.overlay_screens`) y contenía:

```renpy
timer 0.5 action Function(_limpiar_notificaciones_expiradas) repeat True
```

En Ren'Py, la action `Function(fn)` llama a `renpy.restart_interaction()` automáticamente cuando la función devuelve `None`. Como `_limpiar_notificaciones_expiradas()` no devolvía nada (retorno implícito `None`), esto disparaba `restart_interaction()` cada 500ms. Al estar el screen en los overlays, se ejecutaba durante **todos** los say statements, reiniciando la interacción activa cada medio segundo — el texto aparecía y desaparecía en loop mientras el juego esperaba el click.

`notificar_cambio_stat()` también llamaba a `renpy.restart_interaction()` al agregar una notificación, lo que causaba un flash en el say statement que seguía inmediatamente a un cambio de stat.

### Fix aplicado (`hud_notificaciones.rpy`)

1. **Eliminado el timer** del screen `notificaciones_stats`.

2. **Filtrado inline**: el screen ahora calcula las notificaciones activas en cada render filtrando por timestamp, sin necesitar un timer externo:
   ```renpy
   $ _notifs_actuales = [n for n in _notificaciones_stats if _time_module.time() - n["timestamp"] < _NOTIF_DURACION]
   ```

3. **Limpieza proactiva**: `notificar_cambio_stat()` llama a `_limpiar_notificaciones_expiradas()` antes de agregar la nueva notificación, manteniendo la cola limpia sin intervención periódica.

4. **Eliminado `renpy.restart_interaction()`** de `notificar_cambio_stat()` — la notificación aparece naturalmente al inicio de la siguiente interacción (el overlay se re-evalúa en cada render), sin necesidad de forzarlo.

---

## 3. Pantalla de ingreso de nombre (rediseño)

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/_init/config_globals.rpy` | Screen y label reescritos |
| `game/tl/english/script/_init/config_globals.rpy` | Traducciones al inglés actualizadas |

---

### Visual

La pantalla usa el mismo overlay y frame que el `confirm` screen del juego (`gui/overlay/confirm.png` + `gui/confirm_frame.png`), integrándose con la estética del menú principal.

Contenido del cuadro (de arriba a abajo):

1. **Título** — "Ingresa el nombre del personaje" en azul `#4FC3F7` (/ "Enter the character's name" en inglés)
2. **Subtítulo** — "Nombre por defecto: Mc" en gris (/ "Default name: Mc" en inglés)
3. **Campo de texto** — sobre fondo oscuro semitransparente, centrado
4. **Mensaje de error** — en rojo `#FF5252`, solo visible cuando el nombre es inválido
5. **Botones** — "Confirmar" y "Cancelar" con el estilo del juego (blanco / naranja hover)

---

### Validación de caracteres

El campo de texto usa el parámetro `allow` de Ren'Py para filtrar en tiempo real. Solo se aceptan:

- Letras a-z y A-Z
- Letras con acento y caracteres especiales de lenguas latinas (á, é, ñ, ü, etc.)
- Espacio

Números y símbolos (`.`, `/`, `#`, `@`, etc.) son bloqueados mientras se escribe.

Como segunda capa, el label valida el contenido al confirmar. Si detecta caracteres inválidos (p. ej. texto pegado), muestra el error y reabre el screen con el texto previo conservado.

---

### Comportamiento al confirmar

| Situación | Resultado |
|---|---|
| Campo vacío → Confirmar | `mc_name = "Mc"` |
| Campo vacío → Cancelar | `mc_name = "Mc"` (si no había nombre previo) |
| Nombre válido → Confirmar | `mc_name = nombre_ingresado.strip()` |
| Nombre inválido → Confirmar | Muestra error, reabre el screen con el texto conservado |
| Cancelar con nombre previo | `mc_name` mantiene el valor ya guardado |

---

### Strings bilingües

| Español | Inglés |
|---|---|
| Ingresa el nombre del personaje | Enter the character's name |
| Nombre por defecto: Mc | Default name: Mc |
| Confirmar | Confirm |
| Cancelar | Cancel |
| El nombre no puede contener números ni caracteres especiales | The name cannot contain numbers or special characters |

---

## 4. Textos del motor de Ren'Py traducidos al español

### Contexto

Los mensajes del engine de Ren'Py (diálogos de confirmación, guardados, modo saltar, etc.) se mostraban en inglés al jugar en español. Se creó el archivo de traducciones para el idioma base (None = español).

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/tl/None/spanish_strings.rpy` | Nuevo — traducciones al español del engine |
| `game/tl/english/common.rpy` | Completados strings que tenían `new ""` vacío |

### Strings traducidos al español (selección principal)

| Original (inglés) | Español |
|---|---|
| Are you sure you want to quit? | ¿Estás seguro de que querés salir del juego? |
| Are you sure you want to return to the main menu? | ¿Estás seguro de que querés volver al menú principal? |
| Are you sure you want to delete this save? | ¿Estás seguro de que querés borrar este guardado? |
| Are you sure you want to overwrite your save? | ¿Estás seguro de que querés sobreescribir este guardado? |
| Loading will lose unsaved progress. | Al cargar se perderá el progreso sin guardar. |
| Are you sure you want to begin skipping? | ¿Querés empezar a saltar diálogos? |
| Quick save complete. | Guardado rápido completado. |
| Automatic saves | Guardados automáticos |
| Quick saves | Guardados rápidos |
| Skip Mode | Modo saltar |
| Yes | Sí |
| Monday–Sunday | Lunes–Domingo |
| January–December | Enero–Diciembre |

Las traducciones al español se aplicaron directamente en `game/tl/None/common.rpym` (el archivo generado por Ren'Py para el idioma base). El archivo `spanish_strings.rpy` se reserva solo para strings propios del juego que no están en `common.rpym` (`empty slot`, formato de fecha de slots, Upload/Download Sync).

El idioma inglés (`tl/english/`) no fue modificado en su comportamiento — los strings ya correctos se mantuvieron y los que tenían `new ""` se llenaron explícitamente. Se eliminaron duplicados de `tl/english/script/ui/base/screens.rpy` que ya existían en `tl/english/common.rpy` (causaban crash al arrancar).

---

## 5. Bug fix — Notificación negativa mostraba `--`

### Síntoma

Al obtener un resultado negativo en el sistema de Talk (ej: `-2 amor`), la notificación visual mostraba `--2 Violet` en lugar de `-2 Violet`.

### Causa

En `hud_notificaciones.rpy`, la función `notificar_cambio_stat()` construía el texto así:

```python
signo = "+" if positivo else "-"
texto = "{}{} {}".format(signo, cantidad, npc_nombre)
```

Cuando `cantidad` es `-2`, el resultado era `"-" + "-2" + " Violet"` = `"--2 Violet"`.

### Fix (`hud_notificaciones.rpy`)

Cambiado a `abs(cantidad)` en todas las variantes de construcción del texto:

```python
texto = "{}{} {}".format(signo, abs(cantidad), npc_nombre)
```

---

## 6. Sistema de Talk — formato del texto de resultado

### Cambio

El texto compuesto de 4 partes que se muestra al finalizar una interacción Talk ahora se une como una oración continua en lugar de un conjunto de frases separadas.

**Antes:** `"Tuviste una conversación con Violet. Decidiste provocarla. Violet estaba ansiosa. Violet quedó molesta."`

**Después:** `"Tuviste una conversación con Violet decidiste provocarla violet estaba ansiosa violet quedó molesta"`

### Reglas aplicadas (`talksystem_labels.rpy`)

1. Se elimina el punto final de cada parte con `rstrip(".")`
2. La primera letra de las partes 2, 3 y 4 se convierte a minúscula
3. Las partes se unen con espacio

El resultado simula una narración fluida en lugar de una lista de frases separadas.

---

## 7. Panel de pistas — reorganización por NPC

### Problema

El panel de pistas mostraba las quests y los eventos en dos secciones separadas e independientes. Como los eventos actuales solo se vuelven visibles después de que se completa la quest del NPC, en la práctica nunca se veían ambos al mismo tiempo. Además, cuando un NPC tenía un evento activo, este reemplazaba el mensaje de "sin quest" en lugar de coexistir con él.

### Cambio (`hud_pistas.rpy`)

El panel se reorganizó para iterar **por NPC conocido**, mostrando para cada uno:

1. **Bloque de quest** (fondo azul oscuro, título dorado) — visible si el NPC tiene quest activa
2. **Bloque "sin quest"** (fondo azul oscuro, título gris) — visible si el NPC **no** tiene quest activa, siempre presente aunque haya eventos
3. **Un bloque por evento** (fondo verde oscuro, título verde) — independiente de si hay quest o no

### Comportamiento resultante

| Estado del NPC | Panel muestra |
|---|---|
| Quest activa, sin evento | Bloque quest |
| Quest activa + evento activo | Bloque quest + bloque evento |
| Sin quest, evento activo | Bloque "sin contenido" + bloque evento |
| Sin quest, sin evento | Bloque "sin contenido" |

El mensaje de "sin quest" ya no desaparece cuando hay un evento activo para el mismo NPC.

---

## 8. Eliminación del stat `mc_personalidad`

### Contexto

El stat `mc_personalidad` era un atributo global del MC que se incrementaba por ciertas elecciones de diálogo en quests y por opciones del sistema de conversación diaria. No tenía representación visual en el panel de stats ni efecto activo en el gameplay, y causaba notificaciones de stat (`😎 personalidad`) que no correspondían a ningún stat visible.

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/mc/mc_data.rpy` | Eliminada la variable `default mc_personalidad = 0` |
| `game/script/core/npcs/npcsystem_core.rpy` | Eliminado el método `modificar_personalidad()` y su rama en `modificar_stat()` y en la función de emojis de cheat |
| `game/script/ui/hud/hud_notificaciones.rpy` | Eliminadas las entradas `"personalidad"` de `_NOTIF_ICONOS` y `_NOTIF_COLORES` |
| `game/script/characters/violet/interaction/conversacion_violet.rpy` | `"stat": "personalidad"` → `"stat": "amor"` (todas las entradas) |
| `game/script/characters/monica/interaction/conversacion_monica.rpy` | Ídem |
| `game/script/characters/jasmine/interaction/conversacion_jasmine.rpy` | Ídem |
| `game/tl/english/script/characters/violet/interaction/conversacion_violet.rpy` | Ídem |
| `game/tl/english/script/characters/monica/interaction/conversacion_monica.rpy` | Ídem |
| `game/tl/english/script/characters/jasmine/interaction/conversacion_jasmine.rpy` | Ídem |
| `game/script/characters/monica/quests/monica_quest_0.rpy` | Eliminado `$ mc_personalidad += 1` de la opción "Independencia" |
| `game/script/characters/jasmine/quests/jasmine_quest_0.rpy` | Eliminado `$ mc_personalidad += 1` de la opción "Realidad" |
| `game/script/characters/violet/quests/violet_quest_11.rpy` | Eliminada la condición `if mc_personalidad >= 20:` — la opción C del menú queda siempre disponible |

### Decisiones de diseño

- Las opciones de conversación diaria que antes sumaban `personalidad` ahora suman `amor`, manteniendo el sistema de 3 opciones (amor / deseo / amor) por pregunta.
- La opción C de violet_quest_11 era narrativamente equivalente a las opciones A y B (todas llevan al mismo cierre). Quitarle la condición no cambia el peso narrativo de la quest.

---

## 9. Sistema de Talk — mejoras y correcciones

### 9.1 Traducción faltante en intro_airport

`game/tl/english/script/story/intro/intro_airport.rpy` — completada la traducción del bloque `intro_llegada_casa_9ed93577` correspondiente a la línea de Mónica `"Bueno dejemos que [mc_name] se acomode tranquilo."`.

---

### 9.2 Estado del NPC visible mientras el jugador elige

**Antes:** el narrador mostraba el estado del NPC (`"[_t_estado.intro]"`) y el jugador tenía que hacer click para avanzar al menú de opciones. Al aparecer el menú, el texto desaparecía.

**Después:** el texto se muestra con `interact=False` — aparece en el textbox sin requerir click y permanece visible mientras el menú de opciones está activo.

**Archivo:** `talksystem_labels.rpy`

```renpy
# Antes:
"[_t_estado.intro]"

# Después:
"[_t_estado.intro]" (interact=False)
```

---

### 9.3 Expresión del MC durante la interacción

El sprite del MC durante la escena de Talk pasó de `b_serio` a `b_none`.

**Archivo:** `talksystem_labels.rpy`

---

### 9.4 Mensajes del resultado — pronombre y conjunción

**Archivo:** `violet_talk.rpy`, `monica_talk.rpy`, `jasmine_talk.rpy`

#### Parte 3 (estado.mensaje)

El nombre del NPC al inicio del mensaje fue reemplazado por el pronombre **"ella"** para que fluya mejor como parte de una oración continua.

| Antes | Después |
|---|---|
| `"Violet estaba a la defensiva."` | `"ella estaba a la defensiva."` |
| `"Mónica estaba cansada."` | `"ella estaba cansada."` |
| `"Jasmine estaba celosa."` | `"ella estaba celosa."` |

#### Parte 4 (resoluciones)

El nombre del NPC fue reemplazado por **"Y"** para indicar continuación de la oración. La lógica de composición lo baja a minúscula (`"y quedó..."`) al unir las partes.

| Antes | Después |
|---|---|
| `"Violet quedó muy satisfecha con la interacción."` | `"Y quedó muy satisfecha con la interacción."` |
| `"Mónica se alejó un poco de vos."` | `"Y se alejó un poco de vos."` |

#### rstrip ampliado

El limpiador de puntuación final en el loop de composición ahora también elimina comas:

```python
# Antes:
_p = _p.rstrip(".")

# Después:
_p = _p.rstrip(".,")
```

---

### 9.5 Emojis en los resultados del menú

Los textos en `RESULTADO_TEXTO` ahora incluyen el emoji del stat correspondiente. Aplica a los tres contextos de display: cheat, memoria y preview de carisma.

| resultado_id | Texto anterior | Texto actual |
|---|---|---|
| `+2_amor` | `+2 amor` | `+2 amor ❤️` |
| `+1_deseo` | `+1 deseo` | `+1 deseo 💋` |
| `-2_amor` | `-2 amor` | `-2 amor ❤️` |
| `-1_deseo` | `-1 deseo` | `-1 deseo 💋` |

**Archivo:** `talksystem_core.rpy`

---

### 9.6 Paréntesis en las opciones del menú

Los paréntesis que rodeaban el resultado en las opciones del menú fueron eliminados. Solo se mantienen los paréntesis del label `(Cheat)`.

| Contexto | Antes | Después |
|---|---|---|
| Cheat | `Complacerla (+2 amor ❤️) (Cheat)` | `Complacerla +2 amor ❤️ (Cheat)` |
| Memoria | `Complacerla (+2 amor ❤️)` | `Complacerla +2 amor ❤️` |
| Preview carisma | `Complacerla (+2 amor ❤️?)` | `Complacerla +2 amor ❤️?` |

**Archivo:** `talksystem_labels.rpy`

---

### 9.7 Mensaje general dinámico con horario y locación

**Antes:** la parte 1 del resultado era un texto fijo por NPC (`"Tuviste un momento de conversación con Violet."`).

**Después:** se construye dinámicamente en runtime con el horario actual y la locación donde ocurre la conversación.

**Formato:** `"Aprovechaste la {horario} para hablar con {NPC} en {locación}."`

**Ejemplos:**
- `"Aprovechaste la tarde para hablar con Violet en su habitación."`
- `"Aprovechaste la mañana para hablar con Mónica en la cocina."`
- `"Aprovechaste la noche para hablar con Jasmine en el pasillo de arriba."`

#### Lógica de locaciones (`talksystem_core.rpy`)

Las habitaciones tienen tratamiento especial:

| Locación | NPC con quien se habla | Texto |
|---|---|---|
| `casa_hmc` | cualquiera | `"tu habitación"` |
| `casa_hviolet` | Violet | `"su habitación"` |
| `casa_hviolet` | otro NPC | `"la habitación de Violet"` |
| `casa_hjasmine` | Jasmine | `"su habitación"` |
| `casa_hjasmine` | otro NPC | `"la habitación de Jasmine"` |
| `casa_hmonica` | Mónica | `"su habitación"` |
| `casa_hmonica` | otro NPC | `"la habitación de Mónica"` |

Constantes agregadas en `talksystem_core.rpy`: `_TALK_HORARIO_NOMBRES`, `_TALK_LOCACIONES_NOMBRES`, `_TALK_HABITACIONES_DUENO`.

---

### 9.8 Avance de tiempo al finalizar Talk

Al terminar la interacción de Talk se llama a `avanzar_horario()` antes de devolver el control al HUD. Cada conversación consume 1 período del día.

**Archivo:** `talksystem_labels.rpy`

---

### 9.9 Expresión del NPC según resultado

Al mostrar el texto del resultado, el sprite del NPC cambia de expresión según el resultado obtenido, con una transición `dissolve`.

| Resultado | Expresión |
|---|---|
| `+2_amor` | `b_feliz` + ojos positivos |
| `+1_deseo` | `b_sexy` + ojos seductores |
| `nada` | sin cambio |
| `-1_deseo` / `-2_amor` | `b_aburrida` / `b_enojada` + ojos enojados |

#### Expresiones por NPC

| NPC | `+2_amor` | `+1_deseo` | negativos |
|---|---|---|---|
| Violet | `b_feliz o_felices` | `b_sexy o_sexys` | `b_aburrida o_enojados` |
| Mónica | `b_feliz o_felicesnm` | `b_sexy o_sexysnm` | `b_enojada o_enojadosnm` |
| Jasmine | `b_feliz o_sexysnm` | `b_sexy o_sexysnm` | `b_aburrida o_enojadosnm` |

#### Integración con el sistema de skins

El atributo `c_` (cuerpo) y la imagen layered se determinan consultando `obtener_skin_activo(npc_id)` — el skin realmente activo en ese momento, no solo el grupo. Esto garantiza que si el jugador cambió el skin dentro de un grupo, la expresión use la ropa correcta.

Constantes en `talksystem_core.rpy`:

- `_TALK_EXPRESION_FACIAL`: dict `(npc_id, resultado_id)` → `(b_attr, o_attr)`
- `_TALK_SKIN_CUERPO`: dict `skin_id` → `(imagen_layered, c_neutral, c_caliente)`

| skin_id | Imagen | c_neutral | c_caliente |
|---|---|---|---|
| `violet_base_base` | `violet_parada` | `c_rbase_base` | `c_rbase_dedolabio` |
| `violet_pijama_base` | `violet_parada` | `c_pijama_base` | `c_pijama_base` |
| `monica_base_base` | `monica_parada` | `c_rbase_base` | `c_rbase_dedolabio` |
| `monica_bikini_base` | `monica_parada` | `c_rbase_base` | `c_rbase_dedolabio` |
| `jasmine_base_base` | `jasmine_parada` | `c_rbase_base` | `c_rbase_dedolabio` |
| `jasmine_bikini_base` | `jasmine_parada` | `c_rbase_base` | `c_rbase_dedolabio` |
| `jasmine_entrenamiento_base` | `jasmine_parada` | `c_rbase_base` | `c_rbase_dedolabio` |
| `jasmine_entrenamiento_deportiva` | `jasmine_paradadeportiva` | `c_base` | `c_expectativa` |

Para registrar futuros skins, agregar una entrada en `_TALK_SKIN_CUERPO`.

---

## 10. Estado especial "Feliz" — los 3 NPCs

### Qué es

Se agregó un estado especial de tipo "feliz" para Violet, Mónica y Jasmine. Es el estado de mayor jerarquía del juego (jerarquía 5) y dura 2 días. Reemplaza temporalmente cualquier estado general o especial de menor jerarquía. Todos sus efectos son positivos, funcionando como recompensa visible al completar quests principales.

---

### Activación

Se activa al completar la **Quest 0** de cada NPC mediante la función existente `activar_estado_especial_npc()`. En versiones posteriores podrá activarse también desde eventos u otras quests.

| NPC | ID del estado | Activado al completar |
|---|---|---|
| Violet | `violet_feliz` | `violet_questprincipal_0` |
| Mónica | `monica_feliz` | `monica_questprincipal_0` |
| Jasmine | `jasmine_feliz` | `jasmine_questprincipal_0` |

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/talk/violet_talk.rpy` | Agregado `EstadoTalk` `violet_feliz` |
| `game/script/characters/monica/talk/monica_talk.rpy` | Agregado `EstadoTalk` `monica_feliz` |
| `game/script/characters/jasmine/talk/jasmine_talk.rpy` | Agregado `EstadoTalk` `jasmine_feliz` |
| `game/script/characters/violet/quests/violet_quest_0.rpy` | `activar_estado_especial_npc("violet", "violet_feliz")` al completar |
| `game/script/characters/monica/quests/monica_quest_0.rpy` | `activar_estado_especial_npc("monica", "monica_feliz")` al completar |
| `game/script/characters/jasmine/quests/jasmine_quest_0.rpy` | `activar_estado_especial_npc("jasmine", "jasmine_feliz")` al completar |

---

## 11. Ítems de la tienda — nuevos y modificados

### Cambios

| Ítem | Cambio | Precio | Entrega | Stock |
|---|---|---|---|---|
| `golosinas` | Renombrado desde `chocolate`, nuevo ícono 🍭 | $20 | 1 día | 10 (repone 5) |
| `locion_masajes` | Precio y entrega actualizados | $20 | 1 día | 10 (repone 5) |
| `bebida_energetica` | **Nuevo ítem** 🥤 | $20 | 1 día | 10 (repone 5) |

Los tres ítems tienen `usable=True` con un texto de instrucción de uso que aparece en el inventario. No se usan directamente desde el inventario — su uso está vinculado al sistema de Talk (ver sección 12).

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/shopping/items_shopping.rpy` | Modificados `golosinas` y `locion_masajes`, agregado `bebida_energetica` |

---

## 12. Opciones especiales Talk — basadas en ítems

### Qué son

Tres nuevas `OpcionEspecialTalk` que aparecen en el menú de Talk cuando el jugador tiene el ítem correspondiente **y** el NPC está en el estado de ánimo adecuado. Consumen el ítem y otorgan +2 amor +1 deseo.

| Opción | Aparece con | Condición de NPC | Efecto |
|---|---|---|---|
| "Darle golosinas" | `golosinas` en inventario | Violet en estado `violet_hambre` | +2 amor, +1 deseo |
| "Darle la loción" | `locion_masajes` en inventario | Mónica en estado `monica_cansada` | +2 amor, +1 deseo |
| "Darle la bebida" | `bebida_energetica` en inventario | Jasmine en estado `jasmine_agotada` | +2 amor, +1 deseo |

La parte 4 del texto resultado para estas opciones es: `"Y lo que le diste fue justo lo que necesitaba."`

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/talk/violet_talk.rpy` | `OpcionEspecialTalk` `violet_golosinas` |
| `game/script/characters/monica/talk/monica_talk.rpy` | `OpcionEspecialTalk` `monica_locion` |
| `game/script/characters/jasmine/talk/jasmine_talk.rpy` | `OpcionEspecialTalk` `jasmine_bebida` |
| `game/tl/english/script/core/talk/talksystem_strings.rpy` | Traducciones al inglés de las 3 opciones |

---

## 13. Opciones especiales Talk — basadas en atributos del MC

### Qué son

Tres nuevas `OpcionEspecialTalk` que aparecen cuando el MC tiene el atributo requerido **y** el NPC está en el estado de ánimo específico. No consumen ítems. Otorgan +2 amor +1 deseo.

| Opción | Aparece con | Condición de NPC | Efecto |
|---|---|---|---|
| "Jugar videojuegos" | `mc_inteligencia ≥ 3` | Violet en estado `violet_ansiosa` | +2 amor, +1 deseo |
| "Ayudarla con cosas de la casa" | `mc_destreza ≥ 3` | Mónica en estado `monica_ocupada` | +2 amor, +1 deseo |
| "Entrenar juntos" | `mc_fuerza ≥ 3` | Jasmine en estado `jasmine_energica` | +2 amor, +1 deseo |

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/characters/violet/talk/violet_talk.rpy` | `OpcionEspecialTalk` `violet_videojuegos` |
| `game/script/characters/monica/talk/monica_talk.rpy` | `OpcionEspecialTalk` `monica_tareas` |
| `game/script/characters/jasmine/talk/jasmine_talk.rpy` | `OpcionEspecialTalk` `jasmine_entrenar` |
| `game/tl/english/script/core/talk/talksystem_strings.rpy` | Traducciones al inglés de las 3 opciones |

---

## 14. Talk — soporte completo para idioma inglés

### Problema

Al jugar con idioma inglés, el texto resultado de la interacción Talk no se mostraba. Además, la oración dinámica de la Parte 1 (horario + locación + NPC) tiene una estructura diferente en inglés (posesivo: "Violet's room" en lugar de "la habitación de Violet"), por lo que no bastaba con traducir strings.

---

### Cambios aplicados

1. **Detección de idioma** en `talksystem_labels.rpy`:
   ```python
   $ _t_en = (renpy.game.preferences.language or "") == "english"
   ```

2. **Construcción separada de Parte 1** según idioma:
   - Español: `"Aprovechaste la {horario} para hablar con {NPC} en {locación}."`
   - Inglés: `"You spent the {horario} talking to {NPC} in {locación}."` con locaciones en inglés y posesivo (`"Violet's room"`)

3. **`renpy.translate_string()`** en Partes 2, 3 y 4 para que Ren'Py aplique la traducción dinámica a strings construidos en Python.

4. **Stubs auto-generados corregidos** en `game/tl/english/script/core/talk/talksystem_labels.rpy`:
   - Ren'Py genera stubs vacíos (`""`) que silenciosamente sobreescriben el contenido dinámico
   - Corregidos para que pasen el valor real: `"[_t_resultado_texto]"`, `piensa "[_msg_r]"`, `"[_t_intro_tr]" (interact=False)`, etc.

5. **Archivo de traducciones nuevo**: `game/tl/english/script/core/talk/talksystem_strings.rpy` con todos los strings del sistema Talk: opciones base, textos de menú de opciones especiales, mensajes de opciones, intros de estado (3 NPCs), mensajes de estado, resoluciones y resoluciones especiales.

---

### Archivos modificados/creados

| Archivo | Cambio |
|---|---|
| `game/script/core/talk/talksystem_core.rpy` | Agregados `_TALK_HORARIO_NOMBRES_EN` y `_TALK_LOCACIONES_NOMBRES_EN` |
| `game/script/core/talk/talksystem_labels.rpy` | Detección de idioma, construcción separada Parte 1, `renpy.translate_string()` en partes 2-4 |
| `game/tl/english/script/core/talk/talksystem_labels.rpy` | Stubs corregidos para pasar valores dinámicos |
| `game/tl/english/script/core/talk/talksystem_strings.rpy` | **[NUEVO]** Todas las traducciones al inglés del sistema Talk |

---

## 15. Tutorial — nuevas traducciones al inglés

Se completaron 3 stubs de traducción vacíos en `game/tl/english/script/story/intro/tutorial.rpy` correspondientes a las nuevas líneas agregadas al tutorial sobre el sistema de Talk:

- Descripción del estado de ánimo diario de los NPCs
- Ventaja del atributo carisma / inteligencia en el menú de Talk
- Descripción del texto resultado que aparece al finalizar la interacción

---

## 16. Pantalla de ingreso de nombre — eliminación del botón Cancelar

El botón "Cancelar" fue removido de la pantalla `name_input_screen`. No cumplía ninguna función (no había acción de cancelar implementada). La pantalla ahora tiene solo el botón "Confirmar" centrado.

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/_init/config_globals.rpy` | Reemplazado `hbox` con Confirmar+Cancelar por `textbutton` único con `xalign 0.5` |
| `game/tl/english/script/_init/config_globals.rpy` | Eliminada la entrada `old "Cancelar" / new "Cancel"` |

---

## 17. Sistema de Condiciones de Entrega de Mensajes

### Qué es

Antes de este cambio, los mensajes de chat disparados por quests o eventos (`disparar_por_trigger()`) aparecían inmediatamente en el historial. El nuevo sistema agrega un mecanismo de espera con 3 condiciones que deben cumplirse antes de que el mensaje se entregue.

---

### Las 3 condiciones (en orden)

1. **Bloqueo global**: si hay una `RestriccionQuest` activa con `mensajes_bloqueados=True`, los mensajes no se entregan.
2. **Momento del NPC emisor**: el NPC debe estar en una locación y horario específicos (`momento_locacion`, `momento_horario` en `GrupoMensajes`). Si no están configurados, esta condición siempre es verdadera.
3. **No compartir locación con el MC**: el NPC emisor no debe estar en la misma locación que el jugador al momento de enviar.

---

### Nuevos campos en `GrupoMensajes`

| Parámetro | Tipo | Descripción |
|---|---|---|
| `momento_locacion` | `str \| None` | Locación donde debe estar el NPC para enviar |
| `momento_horario` | `int \| None` | Horario requerido: 0=Mañana, 1=Tarde, 2=Noche |

Si ambos son `None`, el grupo no tiene condiciones de entrega y se comporta igual que antes.

---

### Nuevo campo en `RestriccionQuest`

| Parámetro | Tipo | Descripción |
|---|---|---|
| `mensajes_bloqueados` | `bool` | Si es `True`, bloquea la entrega de mensajes en espera |

---

### Hooks de verificación

Los mensajes en espera se verifican automáticamente en 3 momentos:
- Al avanzar el horario (`avanzar_horario()`)
- Al dormir (`dormir()`)
- Al moverse de locación (`accion_hotspot_move`, `accion_ir_a_locacion`)

---

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `game/script/core/messages/messagesystem_core.rpy` | Nuevos campos en `GrupoMensajes`, lista `_grupos_en_espera`, métodos `_intentar_entrega`, `_entregar_grupo`, `verificar_mensajes_en_espera` |
| `game/script/core/quests/restriccion_quest_system.rpy` | Nuevo campo `mensajes_bloqueados` en `RestriccionQuest`, función `mensajes_estan_bloqueados()` |
| `game/script/core/time/timesystem_core.rpy` | Hooks en `avanzar_horario()` y `dormir()` |
| `game/script/core/npcs/npcsystem_interactions.rpy` | Hooks en `accion_hotspot_move` y `accion_ir_a_locacion` |

---

### Ejemplo de uso

```python
# Chat con condiciones de entrega
chat_violet_quest8 = GrupoMensajes(
    id="violet_quest8_chat",
    npc_id="violet",
    mensaje_inicial="Mira lo que encontré...",
    trigger_id="violet_quest8_chat",
    momento_locacion="casa_hviolet",  # Violet debe estar en su habitación
    momento_horario=2,                # Debe ser de noche
    pasos=[...]
)

# Restricción que bloquea mensajes en espera
$ activar_restriccion(
    locaciones_permitidas=["casa_living"],
    mensajes_bloqueados=True,
)
```
