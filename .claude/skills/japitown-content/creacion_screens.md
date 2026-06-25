# Japitown — Screens Interactivos en Quests (complemento de `creacion.md`)

Patrones para objetos clickeables, exploración de habitaciones y mini-escenas dentro de quests.
Ejemplos reales: `violet_quest_04.rpy` + `violet_quest04_screens.rpy`.

**Regla universal:** todo botón/imagebutton verifica `modo_posicionamiento` →
`action NullAction()` cuando está activo.

---

## Patrón A — Overlay sobre el HUD (objeto sobre la locación)

El screen se muestra SOBRE el HUD sin ocultarlo; se auto-oculta si el jugador sale.

```renpy
screen mi_screen_quest():
    if sistema_locaciones.locacion_actual and sistema_locaciones.locacion_actual.id != "casa_living":
        timer 0.01 action Hide("mi_screen_quest")
    else:
        imagebutton:
            idle Transform("imagen.png", alpha=0.0)
            hover "imagen.png"
            xpos 500 ypos 400 xanchor 0.5 yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action [Hide("mi_screen_quest"), Jump("mi_label")]
```
```renpy
label mi_label_al_entrar:           # registrado con registrar_label_locacion
    show screen mi_screen_quest
    return                          # OBLIGATORIO
```

---

## Patrón B — Screen de exploración (reemplaza la interacción normal)

Múltiples elementos clickeables; el HUD sigue visible pero el screen captura clicks.

**Call vs Jump desde el screen:**
- Interacción simple (diálogo y volver): `action Call("label")` — el screen NO se oculta, el
  label hace `return` y el screen se re-evalúa.
- Interacción que cambia escena (ropero, cajonera): `action [Hide("screen"), Jump("label")]`.
- Salir: `action [Hide("screen"), Jump("label_verificar")]`.

```renpy
screen vq4_habitacion_violet():
    button:                          # fondo que absorbe clicks
        xpos 0 ypos 0 xsize 1920 ysize 1080
        background None
        action NullAction()

    if vq4_compu_pendiente:          # diálogo simple → Call
        imagebutton:
            idle Transform("compu.png", alpha=0.0)
            hover "compu.png"
            xpos 500 ypos 400 xanchor 0.5 yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Call("violet_quest4_click_compu")

    if not violet_quest4_tiene_pijama:   # cambia escena → Hide + Jump
        imagebutton:
            idle Transform("ropero.png", alpha=0.0)
            hover "ropero.png"
            xpos 234 ypos 908 xanchor 0.5 yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action [Hide("vq4_habitacion_violet"), Jump("violet_quest4_click_ropero")]

    button:                          # Salir con verificación
        xalign 0.5 ypos 20
        background "#0288D1EE" hover_background "#4FC3F7" padding (30,10)
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action [Hide("vq4_habitacion_violet"), Jump("violet_quest4_check_salida")]
        text "Salir" size 22 color "#ffffff" bold True
```
```renpy
label violet_quest4_click_compu:
    $ vq4_compu_pendiente = False
    window show
    piensa "Mejor no tocar nada."
    window hide
    return                          # vuelve al screen visible

label violet_quest4_mostrar_habitacion:
    show screen vq4_habitacion_violet
    return
```

---

## Patrón C — Screen con loop `ui.interact()` (mini-escena propia)

Para sub-escenas (ropero, cajonera): se oculta el HUD, se cambia el background y el screen usa
`Return(...)` con un loop `while/ui.interact()`.

```renpy
screen vq4_screen_ropero():
    button:
        xpos 0 ypos 0 xsize 1920 ysize 1080
        background None
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("fuera")
    imagebutton:
        idle Transform("pijama.png", alpha=0.0)
        hover "pijama.png"
        xpos 821 ypos 824 xanchor 0.5 yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("pijama")
    button:
        xalign 0.5 ypos 20
        background "#0288D1EE" hover_background "#4FC3F7" padding (30,10)
        action Return("volver")
        text "Volver" size 22 color "#ffffff" bold True
```
```renpy
label violet_quest4_click_ropero:
    hide screen vq4_habitacion_violet
    $ ocultar_hud()
    scene vq4_ropero with fade
    show screen vq4_screen_ropero
    $ _en_ropero = True
    while _en_ropero:
        $ _resultado = ui.interact()
        if _resultado == "pijama":
            hide screen vq4_screen_ropero
            window show
            mc "Esto necesitaba."
            $ violet_quest4_tiene_pijama = True
            window hide
            $ _en_ropero = False
        elif _resultado == "volver":
            $ _en_ropero = False
        else:                        # caja, fuera, etc.
            hide screen vq4_screen_ropero
            window show
            mc "..."
            window hide
            show screen vq4_screen_ropero
    hide screen vq4_screen_ropero
    scene vq4_hviolet_tormenta with fade
    $ mostrar_hud()
    jump violet_quest4_mostrar_habitacion
```
Dentro del loop: `hide screen` antes de diálogos → `window show`/diálogo/`window hide` →
`show screen` para seguir o `_en_loop=False` para salir.

---

## Patrón D — Verificación de salida

```renpy
label violet_quest4_check_salida:
    if not violet_quest4_tiene_pijama:
        window show
        piensa "Debo buscar la ropa de Violet."
        window hide
        jump violet_quest4_mostrar_habitacion
    jump violet_quest4_salir
```

---

## Ocultar elementos según estado

```renpy
default vq4_compu_pendiente = True
default violet_quest4_tiene_pijama = False
# en el screen:
if vq4_compu_pendiente: ...           # se oculta tras interactuar
if not violet_quest4_tiene_pijama: ...# se oculta al obtener el ítem
```

---

## Posiciones editables con `sistema_pos`

```renpy
default vq4_pos_compu = (1636, 775)   # fallback
# en el screen:
$ _elem = sistema_pos.obtener("hviolet_compu_vq4")
$ _x = _elem.x if _elem else vq4_pos_compu[0]
$ _y = _elem.y if _elem else vq4_pos_compu[1]
imagebutton:
    xpos _x ypos _y xanchor 0.5 yanchor 1.0
```
Registro en `tools/position/posicionamiento_elementos.rpy`:
```renpy
sistema_pos.registrar(id="hviolet_compu_vq4",
    imagen="images/quest/violet/quest4/...png", nombre="Compu - Habitacion VQ4",
    grupo="quest_elemento", screen="vq4_habitacion_violet",
    x=1636, y=775, xanchor=0.5, yanchor=1.0)
```
Ajustar en juego con la tecla P (modo debug) y copiar el `(x, y)` reportado.

---

## Sprites — Layered Images y notación de comentarios

Grupos: `a_` área · `ca_` cabeza · `b_` boca · `o_` ojos · `c_` cuerpo/ropa · `ot_` otros.
Cada `show` que cambia un sprite paramétrico lleva ENCIMA un comentario semántico con solo los
grupos presentes en ese show (sin prefijos, sin `at`/`with`/`xzoom`):

```renpy
# (Mc cuerpo base ojos base boca neutral)
show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
# (Violet boca hablando)
show violet_parada b_hablando
violet "Texto"
# (Violet boca aburrida)
show violet_parada b_aburrida
```
Mapeos: `b_none/c_none/o_none → neutral`, `ot_avergonzada → sonrojo`, `c_rbase_ → cuerpo `,
`c_pijama_ → cuerpo pijama `. Referencia completa: `expresiones_referencia.md`.

Convenciones de rutas:
```
Idle:        images/characters/casa/idle/idle_<npc>_casa_<locacion>_<horario>_<rutina>_<grupo>_<skin>.png
Menú skin:   images/characters/casa/menu/<npc>_menu_<grupo>_<variante>.png
Quest:       images/quest/<npc>/questX/<descriptivo>.png
Backgrounds: images/bg/casa/bg_casa_<horario>_<locacion>.png
```
Transiciones: `fade` (escena), `sprite_fast`/`sprite_normal` (sprite), `dissolve` (suave).
