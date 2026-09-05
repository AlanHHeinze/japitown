# PLANTILLA DE QUEST — JAPITOWN
# Completá cada campo y pasámelo para crear la quest sin preguntas adicionales.
# Los campos marcados con * son obligatorios. Los demás son opcionales (escribir NINGUNO si no aplica).

---

## BLOQUE 1: IDENTIFICACIÓN *

**ID de la quest:** [violet_questprincipal_X]
# Formato estricto: {npc_id}_questprincipal_{numero}. Debe ser único en todo el proyecto.

**NPC principal:** [violet / jasmine / monica]

**Nombre visible:** [Nombre que ve el jugador en el HUD y menú de quests]

**Descripción:** [Una o dos oraciones desde la perspectiva del MC. Ej: "Violet me llama a su habitación de noche..."]

**Número de quest:** [X]
# Número secuencial dentro de la línea del NPC. Afecta el auto-incremento de Progreso al completar.

**Quest anterior (requisito):** [npc_questprincipal_X / NINGUNA]
# La quest anterior debe estar completada para que esta se active.

---

## BLOQUE 2: ACTIVACIÓN *

**Días de espera:** [0]
# Cuántos días totales (dias_totales) deben pasar desde que la quest anterior se completó.
# 0 = se activa en el mismo día que termina la anterior.

**Condición adicional de espera:** [NINGUNA]
# Lambda Python opcional que también debe cumplirse (además de los días).
# Ejemplo: lambda: horario_actual == 0
# Ejemplo: lambda: len(sistema_compras.verificar_entregas_hoy()) == 0

---

## BLOQUE 3: REQUISITOS — ETAPA_CONDICIONES
# Qué debe tener/hacer el jugador ANTES de que aparezca el botón "Listo".
# Si no hay requisitos, la quest salta directamente a ETAPA_BOTON_LISTO.

### Requisito 1
- **Tipo:** [amor / deseo / relacion / item / dinero / memoria / locacion / horario / dia / mensaje / npc_presente / NINGUNO]
- **Mensaje para el jugador:** ["Descripción de lo que falta. Ej: Necesito 20 de Amor con Violet"]
- **Parámetro:**
  # amor / deseo / relacion → cantidad mínima. Ej: 20
  # item → id del item. Ej: "mangas_violet"
  # dinero → cantidad. Ej: 500
  # memoria → clave="X", valor=True
  # locacion → locacion_id="casa_hviolet"
  # horario → horario_id=2  (0=Mañana, 1=Tarde, 2=Noche, 3=Trasnoche)
  # dia → dia_id=5  (0=Lunes, 1=Martes, ..., 5=Sábado, 6=Domingo)
  # mensaje → grupo_id="id_del_grupo_de_chat"
  # npc_presente → npc_id="violet", locacion_id="casa_hviolet"
  []

### Requisito 2 (agregar más bloques si hay más)
- **Tipo:** []
- **Mensaje para el jugador:** []
- **Parámetro:** []

---

## BLOQUE 4: VALIDACIÓN DEL BOTÓN LISTO — ETAPA_BOTON_LISTO → ETAPA_DESARROLLO
# Condiciones que deben cumplirse EN EL MOMENTO que el jugador presiona "Listo".
# Si alguna falla, el botón queda inactivo y muestra el mensaje.
# Mismos tipos que el Bloque 3.

### Validación 1
- **Tipo:** []
- **Mensaje para el jugador:** []
- **Parámetro:** []

### Validación 2 (agregar más bloques si hay más)
- **Tipo:** []
- **Mensaje para el jugador:** []
- **Parámetro:** []

---

## BLOQUE 5: RUTINAS DURANTE LA QUEST
# Qué NPC aparece dónde mientras la quest está activa.
# Solo aplica en los días/horarios especificados.

### Rutina del NPC principal
# Cuándo y dónde debe estar para que la quest pueda ejecutarse.

| Día (0=Lun...6=Dom, o "todos") | Horario (0-3) | Locación ID       | Sprite (ruta completa o NINGUNO)                  | Posición (x, y) o NINGUNA |
|--------------------------------|---------------|-------------------|---------------------------------------------------|---------------------------|
| [5]                            | [0]           | [casa_hviolet]    | [images/characters/casa/idle/idle_violet_...png]  | [(800, 700)]              |

**Prioridad de rutina:** [0]
# 0 por defecto. Si hay conflicto con otra quest activa simultánea, gana el número más alto.

### Rutinas de otros NPCs durante la quest
# Útil para sacar NPCs de una habitación o reposicionarlos.

| NPC       | Día | Horario | Locación      |
|-----------|-----|---------|---------------|
| [monica]  | [5] | [0]     | [fuera]       |
| [jasmine] | [5] | [0]     | [fuera]       |

---

## BLOQUE 6: PISTAS Y MENSAJES POR ETAPA
# Textos que ve el jugador en el HUD según en qué etapa está la quest.
# Los campos marcados con (λ) admiten función lambda si el texto es dinámico.

### Etapa ESPERA
- **Pista HUD:** ["Violet parece estar ocupada..."]
- **Qué hacer:** ["Darle unos días"]
- **Mensaje al despertar:** [NINGUNO]
- **Trigger de chat al ENTRAR a esta etapa:** [NINGUNO / ("id_grupo_chat", "npc_id")]

### Etapa CONDICIONES (esperando requisitos)
- **Pista HUD (λ):** ["Necesito X para continuar"]
- **Qué hacer (λ):** ["Conseguir X"]
- **Mensaje al despertar (λ):** [NINGUNO]
- **Trigger de chat al ENTRAR a esta etapa:** [NINGUNO / ("id_grupo_chat", "npc_id")]

### Etapa BOTON LISTO
- **Pista HUD (λ):** ["Todo listo"]
- **Qué hacer (λ):** ["Ir a la habitación de Violet el sábado por la mañana"]
- **Mensaje al despertar (λ):** [NINGUNO / "Hoy parece que será un día especial..."]
  # Aparece en el pop-up al despertar ese día si la quest está en esta etapa.
- **Trigger de chat al ENTRAR a esta etapa:** [NINGUNO / ("id_grupo_chat", "npc_id")]
- **Acción Python al ENTRAR a esta etapa:** [NINGUNA]
  # Función Python a ejecutar cuando se entra a ETAPA_BOTON_LISTO.
  # Ej: lambda: setattr(store, 'violet_questX_pendiente', True)

---

## BLOQUE 7: FALLO (opcional)
# Condición que puede ocurrir una vez por día y "falla" la quest sin terminarla.
# Se resetea y el jugador puede reintentarlo.

**Tiene fallo:** [SÍ / NO]

# Si SÍ, completar:
- **Condición:** [lambda: dia_semana_actual == 5 and horario_actual == 1]
  # Se evalúa una vez por cada avance de horario. Si es True se ejecuta el fallo.
- **Trigger de chat al fallar:** [NINGUNO / ("id_grupo_chat_fallo", "npc_id")]
- **Cambio de stat al fallar:** [NINGUNO / (npc_id, cantidad)]
  # Ej: ("violet", -1) — baja 1 punto de amor a Violet
- **Pista después del fallo:** ["Violet está molesta..."]
- **Qué hacer después del fallo (λ):** ["Intentarlo de nuevo mañana"]

---

## BLOQUE 8: RETORNO AL COMPLETAR
# Cómo queda el juego después de que el label narrativo llama completar_quest_actual().

- **Avanzar al día siguiente al completar:** [SÍ / NO]
- **Locación donde queda el jugador:** [NINGUNA (queda donde estaba) / casa_living]
- **Horario donde queda el jugador:** [NINGUNO / 0-3]
- **Día de la semana donde queda el jugador:** [NINGUNO / 0-6]

---

## BLOQUE 9: MENSAJES DE CHAT ASOCIADOS
# Grupos de chat que se disparan durante la quest.

### Grupo 1
- **ID del grupo:** [violet_questX_chat_nombre]
- **NPC que envía:** [violet / jasmine / monica]
- **Cuándo se dispara:** [Al entrar a ETAPA_CONDICIONES / Al entrar a ETAPA_BOTON_LISTO / Desde el label narrativo]
- **Condiciones de entrega del mensaje:**
  - momento_locacion: [NINGUNA / casa_hviolet]
  - momento_horario: [NINGUNO / 2]
    # 0=Mañana, 1=Tarde, 2=Noche. La NPC debe estar en esa locación y horario para enviar.
- **¿Es requisito para avanzar la quest?:** [SÍ (tipo "mensaje" en Bloque 3 o 4) / NO]
- **Propósito narrativo:** [Violet le manda un mensaje diciéndole X]

### Grupo 2 (si hay más)
- **ID del grupo:** []
- **NPC que envía:** []
- **Cuándo se dispara:** []
- **Condiciones de entrega:** momento_locacion: [], momento_horario: []
- **¿Es requisito?:** []
- **Propósito narrativo:** []

---

## BLOQUE 10: LABEL NARRATIVO — ESTRUCTURA
# Describir en detalle el flujo de la escena que se ejecuta al presionar "Listo".

### Datos del archivo
- **Nombre del label principal:** [quest_violet_questprincipal_X]
- **Archivo:** [game/script/characters/violet/quests/violet_quest_XX.rpy]

---

### ESCENA 1

**Fondo:**
- Locación/ID: [casa_pasilloarriba / imagen custom]
- Si es custom: [images/quest/violet/questX/nombre.png]
- Horario del fondo: [el actual / mañana / tarde / noche]

**NPCs presentes en pantalla:**
- NPC: [] — Sprite: [] — Posición: (x, y) — Expresión/pose: []
- NPC: [] — Sprite: [] — Posición: (x, y) — Expresión/pose: []
# Escribir NINGUNO si no hay NPCs en pantalla.

**Música:** [NINGUNA / la actual / nueva: audio/...]

**¿Se activa una restricción en esta escena?:** [SÍ → ver Bloque 11, Restricción N° / NO]

**Resumen de lo que pasa:**
[Describir en detalle el diálogo y acciones. Ej:
  - El MC llega al pasillo
  - Golpea la puerta de Violet
  - Violet responde con desgano
  - El MC pregunta si está bien
  - Aparece menú con dos opciones]

**Menú de opciones:** [SÍ / NO]
- Opción A: "[Texto de la opción A]"
  → Qué pasa: [descripción de consecuencias]
  → Stats: [(violet, amor, +5) / NINGUNO]
  → Sub-label o continúa en la misma escena: []
- Opción B: "[Texto de la opción B]"
  → Qué pasa: [descripción de consecuencias]
  → Stats: [(violet, deseo, +3) / NINGUNO]
  → Sub-label o continúa en la misma escena: []

**Stats que se modifican en esta escena:** [(violet, amor, +5) / NINGUNO]

**¿Se avanza el horario en esta escena?:** [SÍ / NO]

---

### ESCENA 2 (copiar bloque para cada escena adicional)

**Fondo:** []
**NPCs presentes:** []
**Música:** []
**¿Restricción?:** []
**Resumen:** []
**Menú:** []
**Stats:** []
**¿Avanza horario?:** []

---

### ESCENA FINAL / CIERRE

**Cómo termina la quest:**
[Describir el cierre narrativo]

**¿Se guarda algún recuerdo (decisión) del jugador?:** [SÍ / NO]
# Si SÍ: clave="nombre_decision", valor=True/False/"opcionA"

**¿Se activa un estado especial en el NPC al terminar?:** [NINGUNO / activar_estado_especial_npc("violet", "id_estado")]

**Dónde queda el jugador al terminar:** [casa_hviolet / casa_living / game_loop]

**¿La restricción se desactiva antes de completar?:** [SÍ / NO (se desactiva automáticamente con completar)]

---

## BLOQUE 11: RESTRICCIONES DURANTE EL LABEL
# Descripción de cada restricción que se activa en el label narrativo.
# Puede haber varias (activadas y desactivadas en distintos momentos de la escena).

### Restricción 1
**Se activa en:** [Escena 1, al inicio / después del primer diálogo / al entrar a Escena 2]

- **Locaciones permitidas:** [casa_pasilloarriba, casa_living, casa_cocina / TODAS]
- **Acciones bloqueadas:** [avanzar_tiempo, dormir, entrenar, trabajar, usar_item, comprar / NINGUNA]
  # Opciones disponibles: avanzar_tiempo, dormir, entrenar, trabajar, usar_item, comprar
- **Mensaje de movimiento bloqueado (ir a locación no permitida):** ["Tengo que resolver esto primero"]
- **Mensajes por acción bloqueada (dejar vacío si el mismo para todas):**
  - avanzar_tiempo: ["No puedo perder tiempo"]
  - dormir: ["No puedo dormir ahora"]
  - entrenar: ["Ahora no"]
  - trabajar: ["Ahora no"]
  - usar_item: ["Ahora no"]
  - comprar: ["Ahora no"]
- **NPCs ocultos (no se renderizan):** [monica, jasmine / NINGUNO]
- **NPCs que SÍ se pueden interactuar (los demás bloqueados):** [NINGUNO / violet]
- **Mensaje al intentar interactuar con NPC bloqueado:** ["No hay nadie más"]
- **Celular bloqueado:** [SÍ / NO]
- **Mensaje de celular bloqueado:** ["No puedo distraerme ahora"]
- **Entrega de mensajes de chat bloqueada:** [SÍ / NO]
- **Labels por locación** (se disparan automáticamente al entrar a esa locación):
  - [casa_cocina → nombre_del_label_a_disparar]
  - [casa_hviolet → otro_label]
  # El label disparado DEBE terminar en return.

**¿Cuándo se desactiva?:** [Al iniciar Escena 3 / Al llamar completar_quest_actual / NUNCA dentro del label]

### Restricción 2 (si hay más cambios de restricción)
(copiar el esquema completo de Restricción 1)

---

## BLOQUE 12: VARIABLES GUARDABLES
# Variables que la quest necesita guardar entre sesiones (default).

| Variable                        | Tipo    | Valor inicial | Para qué sirve                                     |
|---------------------------------|---------|---------------|----------------------------------------------------|
| [violet_questX_completada]      | [bool]  | [False]       | [Marcar si esta quest ya se completó]              |
| [violet_questX_opcion_elegida]  | [int]   | [0]           | [Qué opción eligió el jugador (0=ninguna, 1=A, 2=B)] |

---

## BLOQUE 13: IMÁGENES CUSTOM
# Imágenes específicas de esta quest que aún no existen en el proyecto.

| ID Ren'Py              | Ruta del archivo                                    | Descripción visual                   |
|------------------------|-----------------------------------------------------|--------------------------------------|
| [questX_fondo_pasillo] | [images/quest/violet/questX/fondo_pasillo.png]      | [Pasillo de arriba, tarde]           |
| [questX_violet_pose1]  | [images/quest/violet/questX/violet_sorprendida.png] | [Violet con expresión sorprendida]   |

# Si no hay imágenes custom y solo se usan los fondos de locación actuales, escribir NINGUNA.

---

## BLOQUE 14: SCREENS INTERACTIVOS (opcional)
# Solo si la quest tiene elementos clickeables sobre el fondo (objetos, pistas, etc.)

**¿Tiene screens interactivos?:** [SÍ / NO]

# Si SÍ, para cada elemento:

### Elemento 1
- **Nombre del screen:** [nombre_screen_questX]
- **Locación donde aparece:** [casa_hviolet]
- **Patrón** (ver skill de contenido para detalles):
  [A: overlay sobre HUD (elementos clickeables en la locación)
   B: exploración (reemplaza interacción normal, múltiples objetos)
   C: loop ui.interact (escena propia, resultado con Return())]
- **Elementos clickeables:**
  - Elemento: [Nombre/descripción] — Imagen: [ruta] — Posición: (x, y) — Qué hace: [label que llama / item que da]
- **¿Tiene botón Salir?:** [SÍ → verifica condición antes de salir / NO]

---

## BLOQUE 15: NOTAS ADICIONALES
# Cualquier detalle especial, excepción o comportamiento que no encaje en los bloques anteriores.

[Escribir aquí.]
