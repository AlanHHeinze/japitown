# Revisión y testeo — Fixes E01–E06

> Análisis de qué se modificó para corregir cada error del `errores_registro.md`,
> el riesgo de regresión de cada cambio, **qué testear** y **dónde** podrían
> aparecer problemas. Nada de esto está commiteado todavía.
>
> Convención de riesgo: 🟢 bajo · 🟡 medio · 🔴 alto (o solo verificable al buildear).

---

## 1. Archivos modificados (solo E01–E06)

| Archivo | Fix | Naturaleza del cambio |
|---|---|---|
| `core/talk/talksystem_labels.rpy` | E01 | rename de variable de loop (`_p`→`_t_p`) |
| `core/utils/sistema_reporte_errores.rpy` | E02, E04 | `style.rebuild()` al continuar + pantalla de conexión + rewrite del screen de error |
| `core/quests/questsystem_core.rpy` | E03 | guard `has_label` antes del `jump expression` |
| `characters/violet/interaction/interactions_violet.rpy` | E03 | gate `has_label` en el auto-trigger |
| `characters/monica/interaction/interactions_monica.rpy` | E03 | gate `has_label` en el auto-trigger |
| `characters/jasmine/interaction/interactions_jasmine.rpy` | E03 | gate `has_label` en el auto-trigger |
| `ui/base/options.rpy` | E04 | `build.classify(... 'archive')` (solo build) |
| `characters/violet/quests/violet_quest_0_b.rpy` | E05 | `_ruta_vq0`→`default vq0b_ruta` |
| `characters/violet/quests/violet_quest_01_b.rpy` | E05, E06 | `_ruta_vq01b`→`default vq01b_ruta` + `del`→`pop` |
| `characters/violet/quests/violet_quest_11.rpy` | E06 | guard del consumo de `conjunto_cosplays` |

> **Cambio relacionado de esta ronda (NO E01–E06 pero afecta el testeo):** el
> *fix del leak de frames* tocó el control de flujo de **"Hablar"**
> (`menu_interaction.rpy`: `Call`→`Return`), de `ejecutar_quest_activa` y de varios
> labels de quest (`jump game_loop`→`return`). E03 se construyó sobre ese cambio,
> así que conviene testearlo junto. Ver sección 8.

---

## 2. E01 — rename `_p`→`_t_p` (talksystem_labels.rpy) 🟢

**Qué cambió:** la variable de loop `for _i, _p in enumerate(...)` pasó a `_t_i`,
`_t_p`. La lógica interna (`rstrip(".,")`, minúscula inicial) es idéntica.

**Riesgo:** mínimo — es un rename puro, sin cambio de lógica.

**Qué testear:**
- Usar **"Hablar"** con Violet, Mónica y Jasmine y leer el texto de resultado:
  debe verse bien armado (sin punto final sobrante, la 2ª parte en minúscula).
- Confirmar que el bug ya no ocurre: hablar → cambiar idioma (o empezar partida) →
  no debe crashear.

**Dónde podría aparecer un problema:** solo en el **texto de resultado del talk**.
Si algo se ve raro ahí (mayúsculas/puntuación), sería este cambio.

---

## 3. E02 — `style.rebuild()` al continuar (sistema_reporte_errores.rpy) 🟡

**Qué cambió:** en `_jp_error_context`, si el jugador toca **"Continuar"**
(`_return == "ignore"`), se llama `renpy.style.rebuild()` (envuelto en try/except).

**Riesgo:** medio — corre **después de CUALQUIER error** en el que el jugador
continúe. `renpy.style.rebuild()` es la API estándar de Ren'Py, pero reconstruye
todos los estilos.

**Qué testear:**
- Forzar un error (cheat **💥 Forzar error**) → **"Continuar"** → el juego debe
  seguir normal, con el HUD y los diálogos (namebox) intactos.
- Repetir un par de veces seguidas (continuar sobre el mismo error).

**Dónde podría aparecer un problema:** justo **al continuar tras un error** —
si algún estilo custom se viera distinto, o si hubiera un pequeño “parpadeo”/lag
al reconstruir. No debería, pero es el punto a mirar.

---

## 4. E03 — guard/gate `has_label` (questsystem_core + 3 interactions) 🟡

**Qué cambió:**
- `ejecutar_quest_activa`: `jump expression label_quest` ahora dentro de
  `if renpy.has_label(label_quest)`.
- Los 3 auto-triggers (violet/monica/jasmine): se agregó `renpy.has_label("quest_"+id)`
  a la condición.

**Clave para el testeo:** el gate **NO cambia el comportamiento de ninguna quest que
tenga label** (todas dan `has_label=True` → disparan igual que antes). Solo evita que
disparen las quests **sin** label (que usan triggers custom y nunca debían auto-ejecutarse).

**Qué testear — que sigan disparando al hacer click en el NPC (tienen label):**
- **Violet:** `01_b`, `04_b`, `04_c`, `04_d`, `04_e`, `07_c`, `0_b`, `11`, `12`.
- **Mónica:** `0_c`.
- (Estas son las quests que realmente pasan por el auto-trigger. Para cada una que
  tengas activa en BOTON_LISTO, al clickear el NPC debe arrancar como siempre.)

**Qué testear — que NO crasheen y muestren el menú normal (sin label, triggers custom):**
- **Violet:** `01_a` (el bug original — click en Violet con 01_a lista → menú normal,
  sin crash), `0_a`, `02_a`, `02_c`, `04_a`.
- **Jasmine:** `0_a`, `0_b`, `0_c`.

**Dónde podría aparecer un problema:** si alguna quest con label **dejara de
dispararse** al clickear el NPC (no debería, por lo de arriba). Síntoma: hago click
en el NPC con la quest lista y aparece el menú normal en vez de arrancar la quest.

**Riesgo colateral (importante):** este fix se apoya en que `ejecutar_quest_activa`
ahora hace `return` (del fix de leak). Ver sección 8.

---

## 5. E04 — pantalla de conexión + rewrite del screen (sistema_reporte_errores.rpy) 🟡

**Qué cambió:** el handler detecta el download error (`_jp_es_descarga`) y el screen
`jp_error_screen` ahora tiene **dos ramas**: vista de "Problema de conexión"
(descarga) vs. el reporte de error normal (todo lo demás). El screen se **reescribió**
para meter el `if/else`.

**Riesgo:** medio — se tocó el screen que usan **TODOS** los errores. Si la rama
"normal" quedara mal, se rompería el reporte de bugs.

**Qué testear:**
- **Error normal** (cheat **💥**): debe salir la pantalla de siempre con **todos**
  los botones funcionando: **Reportar** (envía a Discord/Sentry), **Copiar**,
  **Reintentar**, **Continuar**, y **Salir** (solo desktop).
- **Download error:** difícil de simular a mano. Si podés forzar una desconexión en
  el build web mientras carga un fondo, debería salir "Problema de conexión" con
  **🔄 Reintentar** / "Continuar igual".

**Dónde podría aparecer un problema:** en la **pantalla de error en sí** (cualquier
error la usa). Mirar que los 5 botones de la rama normal estén y funcionen.

---

## 6. E04 (infra) — archivado de assets en `.rpa` (options.rpy) 🔴 (solo al buildear)

**Qué cambió:** `build.classify('game/**.png'/'.jpg'/'.webp', 'archive')` + re-exclusión
de `game/images/test/**` DESPUÉS (para que la exclusión gane sobre el archive).

**Riesgo:** solo se verifica **generando un build**. No afecta correr desde el SDK.

**Qué testear (al generar el build web):**
- Que el juego **cargue y ande** (los fondos/sprites se ven).
- Que los **sprites de prueba NO estén** en la distribución (confirmar que la
  re-exclusión funcionó).
- Comparar el **tiempo de carga inicial** con el build anterior (el trade-off).

**Dónde podría aparecer un problema:** al **empaquetar/publicar**. Si algo faltara,
serían "image not found" masivos, o test sprites colándose. **No testeable desde el editor.**

---

## 7. E05 y E06 — quests de Violet 🟢/🟡

### E05 — rutas guardables (`vq0b_ruta`, `vq01b_ruta`)
**Qué cambió:** las variables de rama dejaron de ser temp `_` y pasaron a `default`
guardables (renombradas). 0 referencias viejas restantes (verificado).

**Qué testear:**
- **Quest 0_b (Violet):** jugar la rama **"respeto"** y la **"confrontar"**; en cada
  una, **guardar después de elegir y antes de cocinar**, recargar, ir a cocinar →
  debe correr la rama correcta, **sin NameError**.
- **Quest 01_b (Violet):** las 3 ramas al dar el paquete (a / b1 / b2), idealmente
  guardando en el medio → el cierre debe tomar la rama correcta.

**Dónde podría aparecer un problema:** el **cierre de la quest** (aplicación de stats
por rama). Si la rama saliera equivocada, sería acá. **Saves viejos en pleno vuelo:**
la rama cae a `""` → se saltea el bonus de stats (esperado, no crash).

### E06 — borrado idempotente de inventario (`pop`)
**Qué cambió:** `del inventario["mangas_violet"]` (×3) → `pop(..., None)`; quest_11
`conjunto_cosplays` envuelto en `if get()>0`.

**Qué testear:**
- **Dar el paquete a Violet** (quest 01_b), por las 2 vías (sprite y puerta) y las 3
  ramas → el item se quita del inventario y la quest completa. Sin KeyError.
- **Quest 11 (Violet):** entregar el `conjunto_cosplays` → se consume bien.

**Dónde podría aparecer un problema:** al **entregar items de quest**. El riesgo es
casi nulo (el `pop` es idéntico cuando el item está).

---

## 8. Cambio transversal a re-testear: fix del leak de frames

E03 y varios de los tracebacks dependían del fix de leak (de esta misma ronda), que
cambió **control de flujo**. Conviene un pase de humo:

- **"Hablar"** con cada NPC → termina y **devuelve el HUD** (no queda colgado).
- **Cerrar** el menú de interacción con "Cerrar" sin elegir nada.
- **Disparar una quest** desde el menú del NPC (opciones "(Quest)") → arranca y al
  terminar vuelve el control.
- **Celular:** abrir Pistas y cerrar → completa la quest 0_b del MC y vuelve al juego.
- Síntoma de regresión: el juego se **queda sin devolver el control** (pantalla
  quieta) después de una de estas acciones.

---

## 9. Checklist priorizado

**🔴 Crítico (rompe el flujo si algo salió mal):**
- [ ] Pantalla de error normal: los 5 botones andan (E04/§5).
- [ ] Auto-trigger de quests con label sigue disparando (E03/§4): violet 01_b/04_b–e/07_c/0_b/11/12, monica 0_c.
- [ ] "Hablar" con cada NPC devuelve el control (leak/§8).

**🟡 Importante:**
- [ ] Click en Violet con 01_a lista → menú normal, sin crash (E03).
- [ ] Continuar tras un error deja el juego sano (E02).
- [ ] Quest 0_b: guardar entre elegir rama y cocinar, recargar, cocinar → rama correcta (E05).
- [ ] Dar paquete / conjunto → item se consume, sin KeyError (E06).

**🟢 Menor / verificación:**
- [ ] Texto de resultado de "Hablar" se ve bien (E01).
- [ ] (Al buildear) build web carga, sin test sprites, tiempo de carga OK (E04 infra).

---

## 10. Resumen de riesgo

| Fix | Riesgo | Testeable desde el editor |
|---|---|---|
| E01 rename `_p` | 🟢 | sí |
| E02 style.rebuild | 🟡 | sí |
| E03 has_label | 🟡 | sí |
| E04 pantalla conexión | 🟡 | parcial (el normal sí; el de descarga difícil) |
| E04 archive .rpa | 🔴 | **no** — solo al buildear |
| E05 rutas guardables | 🟢/🟡 | sí |
| E06 pop inventario | 🟢 | sí |

Los cambios de **código** son en su mayoría acotados y preservan comportamiento. El
punto que **solo** se valida buildando es el archivado de assets (§6).
