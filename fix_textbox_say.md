# Fix del textbox — dos bugs distintos de la screen `say`

> Investigación del 2026-08-20. Nada de esto está commiteado todavía.
> Base: commit `309f03b`.
>
> Se encontraron **dos bugs independientes** que se veían mezclados. Este
> documento deja qué se cambió, por qué, **cómo revertir cada cosa por separado**
> y qué testear.

---

## Resumen

| | Bug A — pestañeo | Bug B — el textbox desaparece |
|---|---|---|
| **Síntoma** | El cuadro se funde para afuera y para adentro en cada cambio de imagen | Al tocar cualquier botón del textbox se va el cuadro **y la botonera**; el click siguiente lo restaura con la línea posterior |
| **Dónde** | Labels con `scene` entre líneas de diálogo | Flujos de diálogo con el HUD escondido (mensajes al despertar, tutorial de la app de pistas, mensajes de bloqueo) |
| **Causa** | `config.window = "auto"` esconde el cuadro en cada `scene`, con `Dissolve(.2)` de ida y de vuelta | Un `$ renpy.hide_screen("say")` en el **cuerpo de una screen**, ejecutado por el predictor de Ren'Py |
| **Antigüedad** | Desde el commit inicial del proyecto | Idem — es el mismo mecanismo detrás de los problemas históricos de "los mensajes de bloqueo no se mostraban / se iban muy rápido" |
| **Riesgo del fix** | 🟡 medio (cambia cuándo se ve el cuadro) | 🟢 bajo (se borra una línea redundante) |

---

## Bug B — la causa raíz

En `screen hud_navegacion()` había:

```renpy
screen hud_navegacion():
    # Ocultar el cuadro de diálogo de Ren'Py
    $ renpy.hide_screen("say")
```

**Ren'Py predice las screens que podrían mostrarse pronto para precargarles las
imágenes, y predecir una screen significa ejecutar su cuerpo** — esté o no en
pantalla. Así que esa línea corría desde el predictor y destruía el cuadro de
diálogo activo.

Stack que lo probó:

```
core.py:2996   interact_core → self.idle_frame(expensive)
core.py:2262   idle_frame → self.prediction_coroutine.send(expensive)
predict.py:208 prediction_coroutine → predict_screen(name, ...)
screen.py:1445 predict_screen → d.update()
slast.py:1873  exec(self.code.bytecode, ...)
game/script/ui/hud/hud_navigation.rpy, line 173
    $ renpy.hide_screen("say")
```

Por qué encajaba con todo lo observado:

- **Solo con el HUD escondido.** Ren'Py no predice lo que ya está mostrado: con
  el HUD visible la línea nunca se disparaba. Por eso las quests andaban bien y
  el despertar y el tutorial no.
- **Solo después de que el texto termina de tipearse.** La predicción corre en
  `idle_frame`, o sea cuando la interacción queda ociosa.
- **El botón era inocente.** Los volcados muestran la screen `say` viva en
  `show_done` y `slow_done`, y ya ausente al registrar el click — antes de que
  la acción del botón ejecutara una línea. Lo que quedaba en pantalla era un
  render viejo; el primer redibujo lo borraba junto con la botonera (que cuelga
  de `screen say` vía `use jp_textbox_controles()`).
- **`additional_transient` seguía poblado** en ese momento: el desarme normal
  (`replace_transient()`) todavía no había corrido. Era un `hide_screen` por
  fuera del ciclo.

**Regla que se violó:** el cuerpo de una screen tiene que ser libre de efectos
secundarios, justamente porque Ren'Py lo ejecuta para predecir. Un escaneo del
proyecto confirmó que **era la única**: los demás `renpy.hide_screen` /
`restart_interaction` están dentro de labels, que es donde corresponde.

---

## Archivos modificados

### Bug B (1 archivo)

| Archivo | Cambio |
|---|---|
| `ui/hud/hud_navigation.rpy` | Se borra el `$ renpy.hide_screen("say")` de la línea 173. Queda un comentario largo explicando por qué no debe volver. |

Es redundante: el `game_loop` ya hace `window hide` en su primera instrucción
(`characters/mc/quests/intro_main.rpy`).

**Revertir:**
```
git checkout game/script/ui/hud/hud_navigation.rpy
```

**Si al sacarlo queda un cuadro colgado navegando:** la solución va con un
`window hide` en el LABEL que corresponda, **nunca** dentro de una screen.

### Bug A (8 archivos)

Se agrega `window show` al empezar cada tramo de diálogo, que apaga el modo auto
(`_window_auto = False`) y evita que cada `scene` esconda el cuadro. Cada tramo
cierra con el `window hide` que ya tenía, o con el del `game_loop`.

| Archivo | Cambio |
|---|---|
| `ui/base/options.rpy` | Nota al lado de `config.window = "auto"` explicando el mecanismo y su contra |
| `characters/violet/quests/violet_quest_0_b.rpy` | 4 `window show` |
| `characters/mc/quests/intro_main.rpy` | 3 `window show` + **2 `window hide`** |
| `characters/monica/quests/monica_quest_0_a.rpy` | 1 `window show` |
| `characters/jasmine/quests/jasmine_quest_0_a.rpy` | 1 `window show` |
| `characters/jasmine/quests/jasmine_quest_0_c.rpy` | 1 `window show` |
| `characters/jasmine/events/event_jasmine_01.rpy` | 2 `window show` |
| `characters/otros/repartidor/historia_repartidor.rpy` | 3 `window show` |

**Los 2 `window hide` de la intro no son opcionales.** Con el modo auto apagado
el cuadro ya no se va solo, y los dos intertítulos sobre negro ("30 minutos más
tarde", "Más tarde...") quedarían con un cuadro vacío encima. Por eso el
`window show` de `intro_llegada_casa` va **después** del intertítulo, no al tope
del label.

**Revertir todo el bug A:**
```
git checkout game/script/ui/base/options.rpy \
  game/script/characters/violet/quests/violet_quest_0_b.rpy \
  game/script/characters/mc/quests/intro_main.rpy \
  game/script/characters/monica/quests/monica_quest_0_a.rpy \
  game/script/characters/jasmine/quests/jasmine_quest_0_a.rpy \
  game/script/characters/jasmine/quests/jasmine_quest_0_c.rpy \
  game/script/characters/jasmine/events/event_jasmine_01.rpy \
  game/script/characters/otros/repartidor/historia_repartidor.rpy
```

Los dos bugs son independientes: se puede revertir A sin tocar B y al revés.

---

## Instrumental (ya borrado)

Para encontrar el bug B se usó un diagnóstico temporal, **ya removido**:

- `game/script/tools/diag_textbox.rpy` — volcaba a `diag_textbox.txt` el ciclo
  de vida completo de cada línea de diálogo (`begin`/`show`/`show_done`/
  `slow_done`/`interact_done`/`end`) con el contenido de todas las capas, y
  envolvía `renpy.hide_screen` y `SceneLists.remove` para imprimir el stack de
  Python cuando el tag era `"say"`. Eso fue lo que nombró al culpable.
- Modificaciones temporales a `ui/hud/textbox_control.rpy` — revertidas con
  `git checkout`.

Si hace falta reconstruirlo, la pieza clave es envolver esas dos funciones
(son las únicas dos vías por las que una screen sale de una capa) y volcar
`traceback.format_stack()`.

---

## Hipótesis descartadas

Vale dejarlas anotadas para no volver a recorrerlas:

- **No era `_window`** — vale `True` tanto donde anda como donde falla.
- **No era el ruteo del click** — la línea avanza en los dos casos, o sea que el
  botón nunca consumió el evento.
- **No era `restart_interaction()`** — la screen ya estaba muerta antes.
- **No era texto plano vs transiciones `with`** — seis `mc "test"` seguidos
  dentro de una quest funcionan bien.
- **No era la salida temprana de `_window_show`** (`if store._window: return`) —
  forzar el camino completo con `window hide` + `window show` no cambió nada.
- **No era el `at Transform(alpha=...)` de `screen say`** — se probó con
  transforms nombrados y el pestañeo seguía.

---

## Qué testear

**Bug B** (lo que debería quedar arreglado):

1. Mensajes al despertar — tocar el ojo y los `+`/`−`: el cuadro y la botonera
   tienen que quedarse; el ojo esconde solo el texto.
2. Tutorial de la app de pistas — igual, en sus dos tramos (las 4 líneas antes
   de abrir el celular y las 3 de después de cerrarlo).
3. Mensajes de bloqueo — que se muestren y duren lo que tienen que durar.

**Bug A** (lo que cambia de aspecto):

4. **Intro completa** — los dos intertítulos sobre negro tienen que salir **sin
   cuadro vacío encima**. Es lo único que cambia de aspecto y no de
   comportamiento.
5. Quest 0 de Mónica — el corte al `bg_quest_monica_0_living_zoom`, entre
   "Vamos [mc_name], ven a olerlo" y "No seas tímido".
6. Quest 0_a de Jasmine — el negro del beso: el diálogo sigue sobre el negro, el
   cuadro tiene que quedarse visible.
7. Quest 0_b de Violet — la secuencia `cambiandose` / `cambiandose2` /
   `cambiandose3` (era el pestañeo más marcado).
8. Repartidor — las tres entregas (primera, 1-5, 5+).
9. Evento 1 de Jasmine — las dos variantes.

---

## Pendiente aparte

`event_jasmine_01.rpy` repite el mismo `scene bg_casa_tarde_gym_zoom with fade`
dos veces seguidas en sus dos variantes (líneas 23/26 y 220/223). Es
preexistente e inofensivo; no se tocó.
