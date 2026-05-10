################################################################################
## Screens de la Quest 4 de Violet — Solo en casa
################################################################################
## Screens interactivos: sillon en living, habitacion de Violet,
## ropero (caja/pijama) y cajonera (grande/normal/tanga).
## Todos los elementos usan sistema_pos para ser editables con la herramienta.

# =============================================================================
# SCREEN: Sillon en el Living
# =============================================================================
# Se muestra sobre el living sin ocultar HUD ni navegacion.
# Click en el sillon dispara el label de la TV.

screen vq4_sillon_living():

    # Auto-ocultar si el jugador ya no esta en el living
    if getattr(store, 'sistema_locaciones', None) and store.sistema_locaciones.locacion_actual and store.sistema_locaciones.locacion_actual.id != "casa_living":
        on "show" action Hide("vq4_sillon_living")
        timer 0.01 action Hide("vq4_sillon_living")
    else:
        # Posicion leida desde sistema_pos (editable con herramienta → tab Screen)
        $ _sillon_elem = sistema_pos.obtener("casa_living_sillon_vq4")
        $ _sillon_x = _sillon_elem.x if _sillon_elem else vq4_pos_sillon[0]
        $ _sillon_y = _sillon_elem.y if _sillon_elem else vq4_pos_sillon[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccionsillon.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccionsillon.png"
            xpos _sillon_x
            ypos _sillon_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action [Hide("vq4_sillon_living"), Jump("violet_quest4_mirando_tv")]


# =============================================================================
# SCREEN: Habitacion de Violet — Exploracion
# =============================================================================
# Se usa con ui.interact() loop desde el label.
# Todos los elementos devuelven Return("id") al label que controla el loop.
# El HUD se oculta mientras este screen esta activo.

screen vq4_habitacion_violet():

    # Area clickeable de fondo (absorbe clicks fuera de elementos)
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        action Return("fuera")

    # --- Cajonera (se oculta si ya tomo ropa interior) ---
    if not violet_quest5_ropainterior:
        $ _cajonera_elem = sistema_pos.obtener("hviolet_cajonera_vq4")
        $ _cajonera_x = _cajonera_elem.x if _cajonera_elem else vq4_pos_cajonera[0]
        $ _cajonera_y = _cajonera_elem.y if _cajonera_elem else vq4_pos_cajonera[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_cajonera.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_cajonera.png"
            xpos _cajonera_x
            ypos _cajonera_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("cajonera")

    # --- Compu ---
    if vq4_compu_pendiente:
        $ _compu_elem = sistema_pos.obtener("hviolet_compu_vq4")
        $ _compu_x = _compu_elem.x if _compu_elem else vq4_pos_compu[0]
        $ _compu_y = _compu_elem.y if _compu_elem else vq4_pos_compu[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_compu.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_compu.png"
            xpos _compu_x
            ypos _compu_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("compu")

    # --- Mangas ---
    if vq4_mangas_pendiente:
        $ _mangas_elem = sistema_pos.obtener("hviolet_mangas_vq4")
        $ _mangas_x = _mangas_elem.x if _mangas_elem else vq4_pos_mangas[0]
        $ _mangas_y = _mangas_elem.y if _mangas_elem else vq4_pos_mangas[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_mangas.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_mangas.png"
            xpos _mangas_x
            ypos _mangas_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("mangas")

    # --- Mochila ---
    if vq4_mochila_pendiente:
        $ _mochila_elem = sistema_pos.obtener("hviolet_mochila_vq4")
        $ _mochila_x = _mochila_elem.x if _mochila_elem else vq4_pos_mochila[0]
        $ _mochila_y = _mochila_elem.y if _mochila_elem else vq4_pos_mochila[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_mochila.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_mochila.png"
            xpos _mochila_x
            ypos _mochila_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("mochila")

    # --- Muñecos ---
    if vq4_muñecos_pendiente:
        $ _muñecos_elem = sistema_pos.obtener("hviolet_muñecos_vq4")
        $ _muñecos_x = _muñecos_elem.x if _muñecos_elem else vq4_pos_muñecos[0]
        $ _muñecos_y = _muñecos_elem.y if _muñecos_elem else vq4_pos_muñecos[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_muñecos.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_muñecos.png"
            xpos _muñecos_x
            ypos _muñecos_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("muñecos")

    # --- Peluches ---
    if vq4_peluches_pendiente:
        $ _peluches_elem = sistema_pos.obtener("hviolet_peluches_vq4")
        $ _peluches_x = _peluches_elem.x if _peluches_elem else vq4_pos_peluches[0]
        $ _peluches_y = _peluches_elem.y if _peluches_elem else vq4_pos_peluches[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_peluches.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_peluches.png"
            xpos _peluches_x
            ypos _peluches_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("peluches")

    # --- Ropero (se oculta si ya tomo el pijama) ---
    if not violet_quest5_tiene_pijama:
        $ _ropero_elem = sistema_pos.obtener("hviolet_ropero_vq4")
        $ _ropero_x = _ropero_elem.x if _ropero_elem else vq4_pos_ropero[0]
        $ _ropero_y = _ropero_elem.y if _ropero_elem else vq4_pos_ropero[1]

        imagebutton:
            idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_ropero.png", alpha=0.0)
            hover "images/quest/violet/quest4/violet_quest04_interaccion_ropero.png"
            xpos _ropero_x
            ypos _ropero_y
            xanchor 0.5
            yanchor 1.0
            mouse "hand"
            if modo_posicionamiento:
                action NullAction()
            else:
                action Return("ropero")

    # --- Boton Salir (arriba al centro) ---
    button:
        xalign 0.5
        ypos 20
        background "#0288D1EE"
        hover_background "#4FC3F7"
        padding (30, 10)
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("salir")
        text "Salir" size 22 color "#ffffff" bold True


# =============================================================================
# SCREEN: Ropero — Caja y Pijama
# =============================================================================
# Fondo: vq4_ropero (se pone como scene antes de mostrar este screen)
# Boton "Volver" siempre visible arriba al centro

screen vq4_screen_ropero():

    # Area clickeable de fondo (click fuera de elementos)
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("fuera")

    # --- Caja ---
    $ _caja_elem = sistema_pos.obtener("hviolet_ropero_caja_vq4")
    $ _caja_x = _caja_elem.x if _caja_elem else vq4_pos_caja[0]
    $ _caja_y = _caja_elem.y if _caja_elem else vq4_pos_caja[1]

    imagebutton:
        idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_caja.png", alpha=0.0)
        hover "images/quest/violet/quest4/violet_quest04_interaccion_caja.png"
        xpos _caja_x
        ypos _caja_y
        xanchor 0.5
        yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("caja")

    # --- Pijama ---
    $ _pijama_elem = sistema_pos.obtener("hviolet_ropero_pijama_vq4")
    $ _pijama_x = _pijama_elem.x if _pijama_elem else vq4_pos_pijama[0]
    $ _pijama_y = _pijama_elem.y if _pijama_elem else vq4_pos_pijama[1]

    imagebutton:
        idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_pijama.png", alpha=0.0)
        hover "images/quest/violet/quest4/violet_quest04_interaccion_pijama.png"
        xpos _pijama_x
        ypos _pijama_y
        xanchor 0.5
        yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("pijama")

    # --- Boton Volver (siempre visible, arriba al centro) ---
    button:
        xalign 0.5
        ypos 20
        background "#0288D1EE"
        hover_background "#4FC3F7"
        padding (30, 10)
        action Return("volver")
        text "Volver" size 22 color "#ffffff" bold True


# =============================================================================
# SCREEN: Cajonera — Grande, Normal y Tanga
# =============================================================================
# Fondo: vq4_cajonera (se pone como scene antes de mostrar este screen)
# Boton "Volver" siempre visible arriba al centro

screen vq4_screen_cajonera():

    # Area clickeable de fondo (click fuera de elementos)
    button:
        xpos 0
        ypos 0
        xsize 1920
        ysize 1080
        background None
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("fuera")

    # --- Grande ---
    $ _grande_elem = sistema_pos.obtener("hviolet_cajonera_grande_vq4")
    $ _grande_x = _grande_elem.x if _grande_elem else vq4_pos_grande[0]
    $ _grande_y = _grande_elem.y if _grande_elem else vq4_pos_grande[1]

    imagebutton:
        idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_grande.png", alpha=0.0)
        hover "images/quest/violet/quest4/violet_quest04_interaccion_grande.png"
        xpos _grande_x
        ypos _grande_y
        xanchor 0.5
        yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("grande")

    # --- Normal ---
    $ _normal_elem = sistema_pos.obtener("hviolet_cajonera_normal_vq4")
    $ _normal_x = _normal_elem.x if _normal_elem else vq4_pos_normal[0]
    $ _normal_y = _normal_elem.y if _normal_elem else vq4_pos_normal[1]

    imagebutton:
        idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_normal.png", alpha=0.0)
        hover "images/quest/violet/quest4/violet_quest04_interaccion_normal.png"
        xpos _normal_x
        ypos _normal_y
        xanchor 0.5
        yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("normal")

    # --- Tanga ---
    $ _tanga_elem = sistema_pos.obtener("hviolet_cajonera_tanga_vq4")
    $ _tanga_x = _tanga_elem.x if _tanga_elem else vq4_pos_tanga[0]
    $ _tanga_y = _tanga_elem.y if _tanga_elem else vq4_pos_tanga[1]

    imagebutton:
        idle Transform("images/quest/violet/quest4/violet_quest04_interaccion_tanga.png", alpha=0.0)
        hover "images/quest/violet/quest4/violet_quest04_interaccion_tanga.png"
        xpos _tanga_x
        ypos _tanga_y
        xanchor 0.5
        yanchor 1.0
        mouse "hand"
        if modo_posicionamiento:
            action NullAction()
        else:
            action Return("tanga")

    # --- Boton Volver (siempre visible, arriba al centro) ---
    button:
        xalign 0.5
        ypos 20
        background "#0288D1EE"
        hover_background "#4FC3F7"
        padding (30, 10)
        action Return("volver")
        text "Volver" size 22 color "#ffffff" bold True


# =============================================================================
# SCREEN: Menu Puerta del Bano — Quest 4
# =============================================================================
# Mismo patron que menu_puerta_npc del door_access_system.
# Se usa con call screen, devuelve Return("id").

screen vq4_menu_puerta_banio():

    modal True

    # Fondo del pasillo de arriba (con horario actual)
    $ _bg_pasillo_banio = store.sistema_locaciones.obtener_locacion("casa_pasilloarriba").background if store.sistema_locaciones.obtener_locacion("casa_pasilloarriba") else None
    if _bg_pasillo_banio:
        add _bg_pasillo_banio

    # Overlay semi-transparente
    add Solid("#00000088")

    # Menu de opciones - Mismo layout que screen choice
    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Entrar":
            style "choice_button"
            action Return("entrar")

        textbutton "Golpear":
            style "choice_button"
            action Return("golpear")

        textbutton "Volver":
            style "choice_button"
            action Return("volver")
