# QUEST — [NOMBRE]

---

## IDENTIFICACIÓN

- **ID:** 
- **NPC:** violet / jasmine / monica
- **Nombre visible:** 
- **Descripción:** 
- **Número de quest:** 
- **Quest anterior:** 

---

## ACTIVACIÓN

- **Días de espera:** 
- **Condición adicional:** NINGUNA /

---

## REQUISITOS (antes de que aparezca el botón Listo)

| # | Tipo | Mensaje al jugador | Parámetro |
|---|------|--------------------|-----------|
| 1 |      |                    |           |
| 2 |      |                    |           |

*Tipos: amor · deseo · relacion · item · dinero · memoria · locacion · horario · dia · mensaje · npc_presente*

---

## VALIDACIÓN DEL BOTÓN LISTO

| # | Tipo | Mensaje al jugador | Parámetro |
|---|------|--------------------|-----------|
| 1 |      |                    |           |
| 2 |      |                    |           |

---

## RUTINAS DURANTE LA QUEST

**NPC principal**

| Día | Horario | Locación | Sprite | Posición |
|-----|---------|----------|--------|----------|
|     |         |          |        |          |

**Prioridad:** 0

**Otros NPCs**

| NPC | Día | Horario | Locación |
|-----|-----|---------|----------|
|     |     |         |          |

---

## PISTAS POR ETAPA

**ESPERA**
- Pista HUD: 
- Qué hacer: 
- Trigger de chat al entrar: NINGUNO /

**CONDICIONES**
- Pista HUD: 
- Qué hacer: 
- Trigger de chat al entrar: NINGUNO /

**BOTÓN LISTO**
- Pista HUD: 
- Qué hacer: 
- Mensaje al despertar: NINGUNO /
- Trigger de chat al entrar: NINGUNO /
- Acción Python al entrar: NINGUNA /

---

## FALLO

- **¿Tiene fallo?** SÍ / NO
- Condición: 
- Trigger de chat al fallar: NINGUNO /
- Cambio de stat al fallar: NINGUNO /
- Pista después del fallo: 
- Qué hacer después del fallo: 

---

## RETORNO AL COMPLETAR

- **Avanzar al día siguiente:** SÍ / NO
- **Locación donde queda el jugador:** NINGUNA /
- **Horario:** NINGUNO /
- **Día de la semana:** NINGUNO /

---

## MENSAJES DE CHAT

| ID grupo | NPC | Cuándo se dispara | momento_locacion | momento_horario | ¿Requisito? | Propósito |
|----------|-----|-------------------|------------------|-----------------|-------------|-----------|
|          |     |                   |                  |                 |             |           |

---

## LABEL NARRATIVO

- **Label principal:** quest_[npc]_questprincipal_X
- **Archivo:** game/script/characters/[npc]/quests/[npc]_quest_XX.rpy

### Escena 1
- **Fondo:** 
- **NPCs en pantalla:** 
- **Música:** 
- **Restricción activa:** SÍ (ver abajo) / NO
- **Resumen:**

  

- **Menú:** SÍ / NO
  - Opción A: "" → Qué pasa: / Stats:
  - Opción B: "" → Qué pasa: / Stats:
- **Stats que cambian:** NINGUNO /
- **¿Avanza horario?** SÍ / NO

---

### Escena 2
- **Fondo:** 
- **NPCs en pantalla:** 
- **Música:** 
- **Restricción activa:** SÍ / NO
- **Resumen:**

  

- **Menú:** SÍ / NO
- **Stats:** NINGUNO /
- **¿Avanza horario?** SÍ / NO

---

### Cierre
- **Cómo termina:** 
- **¿Se guarda decisión?** SÍ (clave= , valor= ) / NO
- **¿Estado especial al terminar?** NINGUNO /
- **Dónde queda el jugador:** 

---

## RESTRICCIONES

### Restricción 1 — se activa en: [Escena X / inicio / después del diálogo Y]

- **Locaciones permitidas:** TODAS /
- **Acciones bloqueadas:** avanzar_tiempo · dormir · entrenar · trabajar · usar_item · comprar
- **Mensaje de movimiento bloqueado:** 
- **Mensajes por acción bloqueada:**
  - avanzar_tiempo: 
  - dormir: 
  - entrenar: 
  - trabajar: 
  - usar_item: 
  - comprar: 
- **NPCs ocultos:** NINGUNO /
- **NPCs interactuables:** NINGUNO /
- **Mensaje NPC bloqueado:** 
- **Celular bloqueado:** SÍ / NO —
- **Mensajes bloqueados (chat en espera):** SÍ / NO
- **Labels por locación:**
  - [locacion_id → label]
- **¿Cuándo se desactiva?** 

---

## VARIABLES GUARDABLES

| Variable | Tipo | Valor inicial | Para qué sirve |
|----------|------|---------------|----------------|
|          |      |               |                |

---

## IMÁGENES CUSTOM

| ID Ren'Py | Ruta | Descripción visual |
|-----------|------|--------------------|
|           |      |                    |

*NINGUNA si solo se usan fondos existentes.*

---

## SCREENS INTERACTIVOS

- **¿Tiene screens?** SÍ / NO

*(Si SÍ, describir patrón A/B/C/D, screen name, locación, elementos clickeables)*

---

## NOTAS

