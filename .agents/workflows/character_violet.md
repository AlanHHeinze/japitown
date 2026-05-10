---
description: Guía de referencia completa del personaje Violet (Personalidad, Quests, Rutinas y Stats)
---

# Violet - Guía de Personaje y Referencia de Contenido

Este documento contiene toda la información técnica y narrativa sobre el personaje **Violet** en *Japitown*. Sirve como referencia unificada para expandir su contenido (quests, eventos, diálogos) sin necesidad de revisar todos los scripts individuales.

## 1. Perfil Básico

*   **Nombre:** Violet
*   **Edad:** 20 años
*   **Ocupación:** Estudiante universitaria
*   **Color de texto (Ren'Py):** `#956db3`
*   **ID del NPC:** `violet`

### Personalidad y Dinámica con el MC
*   **Característica principal:** Actitud sarcástica, un poco *tsundere*, le cuesta admitir cuando algo le gusta o avergüenza, pero en el fondo disfruta de la atención del MC.
*   **Dinámica (Banter):** Tiene un trato competitivo con el MC. Se pelean en chiste y el MC suele hacer comentarios sugerentes (ej. sobre su "trasero") que la avergüenzan y la hacen responder a la defensiva ("idiota", "pervertido").
*   **Intereses conocidos:** Videojuegos (especialmente de VR tipo Fruit Samurai donde es muy competitiva), Cosplay (aunque le da mucha vergüenza mostrarlo al principio).

---

## 2. Variables y Stats (Estado Guardable)

Violet no usa "amor" o "afección" genérica. Utiliza dos stats principales que miden distintas facetas de la relación:

*   `violet_complicidad`: Medida de qué tan bien se llevan, la confianza amistosa y el banter.
*   `violet_sumision`: Medida de la tensión sexual y qué tanto Violet cede a las insinuaciones o dominancia del MC. 
*   `violet_progreso`: Contador oculto general de progreso.

**Otras variables importantes (`store`):**
*   `violet_interacciones`: Dict `{"hablar": False, "coquetear": False}` (restablecido diariamente)
*   `violet_quest2_trajesexy`: Booleano para rastrear decisiones.
*   `violet_evento1_completado` / `violet_evento1_repetir`: Tracker del evento de VR.
*   `vq4_rama_a/b/c` y `vq5_rama_a/b/c`: Rastreo de decisiones en los chats de WhatsApp de los Quests 4 y 5.

---

## 3. Rutinas Semanales y Posiciones

Violet tiene una rutina estricta de lunes a domingo.

*   **Lunes a Viernes:**
    *   Mañana (0): Cocina -> `(765, 1060)`
    *   Tarde (1): Su Habitación (leyendo) -> `(721, 793)`
    *   Noche (2): Su Habitación (en pijama) -> `(1558, 988)`
    *   Trasnoche (3): Su Habitación -> `(725, 862)`
*   **Sábados:**
    *   Mañana (0): Su Habitación -> `(728, 815)`
    *   Tarde (1): Living (leyendo) -> `(648, 816)`
    *   Noche (2): Su Habitación -> `(1558, 988)`
    *   Trasnoche (3): Su Habitación -> `(725, 862)`
*   **Domingos:**
    *   Mañana (0): Cocina -> `(765, 1060)`
    *   Tarde (1): Su Habitación -> `(721, 793)`
    *   Noche (2): Living -> `(648, 994)`
    *   Trasnoche (3): Su Habitación -> `(725, 862)`

---

## 4. Estructura de Quests (Arco del Cosplay)

La línea principal de quests de Violet gira en torno a descubrir su afición secreta por el cosplay y lograr la confianza (sumisión) suficiente para que se lo muestre al MC.

| ID de Quest | Nombre | Requisito Principal | Resumen |
|:---|:---|:---|:---|
| `violet_questprincipal_0` | ¿Que le pasa a Violet? | Tarde en H. Violet | Misión inicial para romper el hielo. |
| `violet_questprincipal_1` | Un paquete misterioso | 3 días después | Entrega pendiente. |
| `violet_questprincipal_3` | Limpieza del Sábado | Mensaje de Monica, Sábado mañana | Despertar a Violet para limpiar la casa. |
| `violet_questprincipal_7` | El cosplay de Violet | 3 días después | MC le pregunta a Violet sobre el cosplay. |
| `violet_questprincipal_8` | El cosplay de Violet II | **Sumisión 20** + Mensaje de WhatsApp | Violet confiesa vergüenza por su cuerpo; chat intenso. |
| `violet_questprincipal_7` | El cosplay de Violet III| **Sumisión 25** + Mensaje de WhatsApp | Violet envía fotos pero se queja de que le "aprieta la cola". |
| `violet_questprincipal_8` | El cosplay de Violet IV | **Sumisión 30** + Mensaje de WhatsApp | Intercambio de mensajes negociando ver más fotos a cambio de que el MC deje de molestarla. |
| `violet_questprincipal_11` | Los ruidos nocturnos | Item: `conjunto_cosplays` (1) | Comprarle conjuntos y sorprenderla a la noche. |
| `violet_questprincipal_12` | Visita nocturna | Mensaje de WhatsApp | Violet pide que el MC pase por su cuarto de noche. |

---

## 5. Eventos y Minijuegos

### Evento 1: Casco VR (`evento1_violet`)
*   **Desbloqueo:** Después de Quest 0, "Libre Mercado" avisa que el "Casco VR" está disponible en la tienda.
*   **Ejecución:** En `casa_noche_hmc`, Violet entra a quejarse del ruido pero termina pidiendo probar el VR. Juegan a un juego de cortar frutas.
*   **Interacciones destacadas:** Violet es extremadamente competitiva y se burla del MC por hacer pocos puntos (10120 vs 6500). El MC piensa en voz alta sobre su ropa ("short corto") lo que genera momentos de tensión cómica.
*   **Repetición:** Se agrega una opción extra al menú de Violet: *"Invitar a jugar VR"* que activa `evento1_violet_repetir` de noche.

---

## 6. Convenciones de Código y Assets

*   **Llamadas al NPC en UI:** `$ _npc_actual = obtener_npc("violet")`
*   **Sprites Base:** Mayormente `violet_parada`, pero para el evento de VR usa `violet_evento_01_violetvr`.
*   **Sprites de Cara (Expressions):** Siguen el estándar del juego: `o_felices` (ojos), `b_hablando` (boca). Si no mira a cámara usa el sufijo `nm` (ej. `o_felicesnm`).
*   **Archivos Importantes:**
    *   `definition_violet.rpy`: Setup base, rutinas y variables default.
    *   `quests/quest_violet.rpy`: Definición en código de todas las misiones.
    *   `chat/chat_violet.rpy`: Todos los guiones de mensajes de WhatsApp de Violet.
    *   `events/evento1_violet.rpy`: Lógica del evento del VR.
    *   `interaction/interactions_violet.rpy`: Opciones extra inyectadas dinámicamente en el menú de interacción base.
