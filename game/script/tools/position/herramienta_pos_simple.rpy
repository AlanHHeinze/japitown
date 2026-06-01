################################################################################
## Herramienta de Posicionamiento de Idles — Versión Simple
################################################################################
## Uso:   tecla P (con MODO_DEV = True) o botón "📐 Posicionar" en panel de debug (F1).
## Guarda: posiciones_idle.txt en la raíz del proyecto (append, nunca sobreescribe).
##
## Anclaje registrado: xanchor=0.0, yanchor=0.0 (esquina superior-izquierda).
## Esto coincide exactamente con cómo los idles se posicionan en el código del juego.

################################################################################
## Estado de la herramienta
################################################################################

default _hpos_bg_path       = None   # Background activo (solo referencia visual)
default _hpos_idle_path     = None   # Idle activo (el arrastrable)
default _hpos_idle_x        = 0      # Coord X del idle al soltarlo (= xpos en código)
default _hpos_idle_y        = 0      # Coord Y del idle al soltarlo (= ypos en código)
default _hpos_menu_abierto  = None   # Dropdown activo: "fondos" | "sprites" | None
default _hpos_idle_id       = 0      # Incrementa al elegir nuevo sprite → resetea drag

################################################################################
## Lógica Python
################################################################################

init python:

    def _hpos_lista_fondos():
        """Retorna lista de paths de fondos en images/bg/, ordenados."""
        try:
            return sorted([
                f for f in renpy.list_files()
                if f.startswith("images/bg/")
                and f.lower().endswith((".png", ".jpg", ".webp"))
            ])
        except Exception:
            return []

    def _hpos_lista_idles():
        """Retorna lista de paths de idles de personajes e imágenes de movimiento, ordenados."""
        try:
            return sorted([
                f for f in renpy.list_files()
                if (
                    (f.startswith("images/characters/") and "/idle/" in f)
                    or f.startswith("images/bg/casa/idle_movimiento/")
                )
                and f.lower().endswith((".png", ".jpg", ".webp"))
            ])
        except Exception:
            return []

    def _hpos_seleccionar_idle(path):
        """
        Selecciona un nuevo idle y resetea la posición a (0, 0).
        Incrementa _hpos_idle_id para que el drag_name cambie y Ren'Py
        cree un drag nuevo desde (0, 0), evitando heredar la posición anterior.
        """
        store._hpos_idle_path = path
        store._hpos_idle_x    = 0
        store._hpos_idle_y    = 0
        store._hpos_idle_id  += 1

    def _hpos_es_sprite_personaje():
        """Retorna True si el sprite activo es un idle de personaje (xanchor=0.5, yanchor=1.0)."""
        p = store._hpos_idle_path or ""
        return p.startswith("images/characters/")

    def _hpos_al_soltar(drags, drop):
        """
        Callback de drag: actualiza las coordenadas al soltar el idle.
        Personajes (images/characters/): convierte top-left a centro-inferior (xanchor=0.5, yanchor=1.0).
        Resto (idle_movimiento, etc.): guarda top-left tal cual (xanchor=0.0, yanchor=0.0).
        """
        if drags:
            d = drags[0]
            if _hpos_es_sprite_personaje() and store._hpos_idle_path:
                try:
                    w, h = renpy.image_size(store._hpos_idle_path)
                    store._hpos_idle_x = int(d.x + w / 2)
                    store._hpos_idle_y = int(d.y + h)
                except Exception:
                    store._hpos_idle_x = int(d.x)
                    store._hpos_idle_y = int(d.y)
            else:
                store._hpos_idle_x = int(d.x)
                store._hpos_idle_y = int(d.y)
        return None

    def _hpos_guardar():
        """
        Añade la posición actual al archivo posiciones_idle.txt.
        Formato listo para copiar al código fuente del juego.
        """
        if not store._hpos_idle_path:
            return
        import os
        import datetime
        nombre  = store._hpos_idle_path.split("/")[-1].rsplit(".", 1)[0]
        ruta    = os.path.join(config.basedir, "posiciones_idle.txt")
        ts      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        es_npc  = _hpos_es_sprite_personaje()
        anchor  = "xanchor=0.5  yanchor=1.0" if es_npc else "xanchor=0.0  yanchor=0.0"
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write("# {} — {}\n".format(nombre, ts))
            f.write("# path: {}\n".format(store._hpos_idle_path))
            f.write("xpos {}  ypos {}  # {}\n".format(
                store._hpos_idle_x, store._hpos_idle_y, anchor))
        renpy.notify("Guardado  x={}  y={}".format(
            store._hpos_idle_x, store._hpos_idle_y))


################################################################################
## Screen principal
################################################################################

screen herramienta_pos_simple():
    modal True
    zorder 500

    # ── 1. Fondo negro (cubre el juego por debajo) ────────────────────────────
    add "#111111"

    # ── 2. Background seleccionado (solo referencia visual) ───────────────────
    if _hpos_bg_path:
        add _hpos_bg_path

    # ── 3. Idle arrastrable ───────────────────────────────────────────────────
    # Usar drag_name con _hpos_idle_id: al incrementar el ID al seleccionar
    # un nuevo sprite, Ren'Py crea un drag nuevo desde xpos=0 ypos=0.
    if _hpos_idle_path:
        draggroup:
            drag:
                drag_name ("idle_{}".format(_hpos_idle_id))
                xpos 0
                ypos 0
                draggable True
                droppable False
                dragged _hpos_al_soltar
                add _hpos_idle_path

    # ── 4. Barra de cabecera (máx 50 px, sobre todo lo demás) ─────────────────
    frame:
        xpos 0
        ypos 0
        xfill True
        ysize 50
        background "#111111f0"
        padding (0, 0)

        fixed:
            xfill True
            ysize 50

            ## Grupo izquierdo: botones + nombre del sprite
            hbox:
                xpos 10
                yalign 0.5
                spacing 8

                ## Botón Fondos
                button:
                    yalign 0.5
                    background ("#3a6186" if _hpos_menu_abierto == "fondos" else "#2d2d45")
                    hover_background "#4a7196"
                    padding (16, 8)
                    action SetVariable("_hpos_menu_abierto",
                        None if _hpos_menu_abierto == "fondos" else "fondos")
                    text "Fondos" size 17 color "#cccccc" yalign 0.5

                ## Botón Sprites
                button:
                    yalign 0.5
                    background ("#3a6186" if _hpos_menu_abierto == "sprites" else "#2d2d45")
                    hover_background "#4a7196"
                    padding (16, 8)
                    action SetVariable("_hpos_menu_abierto",
                        None if _hpos_menu_abierto == "sprites" else "sprites")
                    text "Sprites" size 17 color "#cccccc" yalign 0.5

                ## Nombre del sprite activo
                if _hpos_idle_path:
                    text (_hpos_idle_path.split("/")[-1].rsplit(".", 1)[0]):
                        size 13
                        color "#777777"
                        yalign 0.5
                        xmaximum 560

            ## Grupo derecho: coordenadas + Guardar + Cerrar
            hbox:
                xalign 1.0
                xoffset -10
                yalign 0.5
                spacing 8

                ## Caja de coordenadas + botón Guardar (solo si hay sprite)
                if _hpos_idle_path:
                    frame:
                        yalign 0.5
                        background "#000000"
                        padding (14, 8)
                        xminimum 200
                        text ("x={:5d}   y={:5d}".format(_hpos_idle_x, _hpos_idle_y)):
                            size 16
                            color "#ffffff"
                            xalign 0.5

                    button:
                        yalign 0.5
                        background "#2e7d32"
                        hover_background "#388e3c"
                        padding (16, 8)
                        action Function(_hpos_guardar)
                        text "Guardar" size 17 color "#ffffff" yalign 0.5

                ## Botón Cerrar
                button:
                    yalign 0.5
                    background "#7f0000"
                    hover_background "#c62828"
                    padding (14, 8)
                    action [
                        SetVariable("_hpos_menu_abierto", None),
                        Hide("herramienta_pos_simple"),
                    ]
                    text "✕" size 18 color "#ffffff" yalign 0.5

    # ── 5. Dropdown Fondos ────────────────────────────────────────────────────
    if _hpos_menu_abierto == "fondos":
        $ _hpos_fondos_lista = _hpos_lista_fondos()
        frame:
            xpos 10
            ypos 50
            xsize 420
            ysize 1030
            padding (0, 0)
            background "#1a1a2ef0"

            viewport id "vp_hpos_fondos":
                xsize 420
                ysize 1030
                mousewheel True
                scrollbars "vertical"
                yinitial 0.0

                vbox:
                    xsize 400
                    spacing 1

                    for _bg in _hpos_fondos_lista:
                        button:
                            xsize 400
                            background ("#3a6186" if _hpos_bg_path == _bg else "#1e1e35")
                            hover_background "#2d2d50"
                            padding (10, 7)
                            action [
                                SetVariable("_hpos_bg_path", _bg),
                                SetVariable("_hpos_menu_abierto", None),
                            ]
                            text (_bg.split("/")[-1]):
                                size 13
                                color "#cccccc"

    # ── 6. Dropdown Sprites ───────────────────────────────────────────────────
    if _hpos_menu_abierto == "sprites":
        $ _hpos_idles_lista = _hpos_lista_idles()
        frame:
            xpos 120
            ypos 50
            xsize 520
            ysize 1030
            padding (0, 0)
            background "#1a1a2ef0"

            viewport id "vp_hpos_sprites":
                xsize 520
                ysize 1030
                mousewheel True
                scrollbars "vertical"
                yinitial 0.0

                vbox:
                    xsize 500
                    spacing 1

                    for _sp in _hpos_idles_lista:
                        button:
                            xsize 500
                            background ("#3a6186" if _hpos_idle_path == _sp else "#1e1e35")
                            hover_background "#2d2d50"
                            padding (10, 7)
                            action [
                                Function(_hpos_seleccionar_idle, _sp),
                                SetVariable("_hpos_menu_abierto", None),
                            ]
                            text (_sp.split("/")[-1]):
                                size 13
                                color "#cccccc"
