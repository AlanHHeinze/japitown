################################################################################
## Herramienta de Posicionamiento de Idles — Versión Simple
################################################################################
## Uso:   tecla P (con MODO_DEV = True) o botón "📐 Posicionar" en panel de debug (F1).
## Guarda: tools/posiciones_idle.txt (append, nunca sobreescribe).
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

# ── Modo ZONAS ──────────────────────────────────────────────────────────────
# Rectangulos invisibles del juego (hotspots, botones de minijuego). No tienen
# imagen: son area y nada mas, asi que la unica forma de acomodarlos es verlos
# dibujados encima del fondo y arrastrarlos.
default _hpos_modo          = "sprite"  # "sprite" | "zonas"
default _hpos_zonas         = []        # [{"id","x","y","w","h"}]
default _hpos_zona_sel      = None      # indice de la zona seleccionada
default _hpos_zona_paso     = 10        # cuanto mueve cada +/- de tamaño

################################################################################
## Lógica Python
################################################################################

init python:

    # Las tres listas de la herramienta son EXCLUYENTES: una imagen aparece en
    # una sola. Fondos es la base sobre la que se acomoda todo lo demas, asi que
    # meter ahi las piezas sueltas de un minijuego llenaba el desplegable de
    # cosas que no son fondos.

    _HPOS_EXT = (".png", ".jpg", ".webp")

    def _hpos_es_contenido(f):
        """True si el path vive en las carpetas de quests o minijuegos."""
        return (f.startswith("images/quest/")
                or f.startswith("images/minijuegos/"))

    def _hpos_es_fondo_de_contenido(f):
        """
        True si una imagen de quest/minijuego es la BASE de su escena.

        Se reconoce por el nombre: `cama_fondo`, `ducha_fondo`, etc. Es una
        convencion y no una carpeta aparte porque el arte de una escena llega
        junto y separarlo en dos lugares se olvida.
        """
        return "fondo" in f.rsplit("/", 1)[-1].lower()

    def _hpos_lista_fondos():
        """
        Fondos: todo images/bg/ mas las bases de escena de quests y minijuegos.
        """
        try:
            return sorted([
                f for f in renpy.list_files()
                if f.lower().endswith(_HPOS_EXT)
                and (f.startswith("images/bg/")
                     or (_hpos_es_contenido(f) and _hpos_es_fondo_de_contenido(f)))
            ])
        except Exception:
            return []

    def _hpos_lista_assets():
        """
        Assets: las piezas sueltas de una quest o minijuego — sudores, ropa,
        props, zonas de interaccion.

        Es todo lo que vive en esas carpetas y NO es ni la base de la escena ni
        un idle (esos ya tienen su propia lista). Asi las piezas de un minijuego
        nuevo aparecen solas, sin tocar la herramienta.
        """
        try:
            return sorted([
                f for f in renpy.list_files()
                if f.lower().endswith(_HPOS_EXT)
                and _hpos_es_contenido(f)
                and not _hpos_es_fondo_de_contenido(f)
                and "/idle_" not in f
            ])
        except Exception:
            return []

    def _hpos_lista_idles():
        """Retorna lista de paths de idles de personajes, imágenes de movimiento y props de quest, ordenados."""
        try:
            return sorted([
                f for f in renpy.list_files()
                if (
                    (f.startswith("images/characters/") and "/idle/" in f)
                    or f.startswith("images/bg/casa/idle_movimiento/")
                    or (f.startswith("images/quest/") and "/idle_" in f)
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

    # ── Zonas ────────────────────────────────────────────────────────────────

    def _hpos_zona_nueva():
        """Agrega una zona nueva en el centro y la deja seleccionada."""
        store._hpos_zonas.append({
            "id": "zona_{}".format(len(store._hpos_zonas) + 1),
            "x": 760, "y": 440, "w": 400, "h": 200,
        })
        store._hpos_zona_sel = len(store._hpos_zonas) - 1

    def _hpos_zona_borrar():
        """Borra la zona seleccionada."""
        _i = store._hpos_zona_sel
        if _i is None or _i >= len(store._hpos_zonas):
            return
        del store._hpos_zonas[_i]
        store._hpos_zona_sel = (len(store._hpos_zonas) - 1) if store._hpos_zonas else None

    def _hpos_zona_medir(campo, delta):
        """Cambia el ancho o el alto de la zona seleccionada. Minimo 10 px."""
        _i = store._hpos_zona_sel
        if _i is None or _i >= len(store._hpos_zonas):
            return
        store._hpos_zonas[_i][campo] = max(10, store._hpos_zonas[_i][campo] + delta)

    def _hpos_zona_al_soltar(drags, drop):
        """Callback de drag: la esquina superior-izquierda es la posicion."""
        if not drags:
            return None
        _d = drags[0]
        try:
            _i = int(_d.drag_name.split("_")[-1])
        except (ValueError, AttributeError):
            return None
        if _i < len(store._hpos_zonas):
            store._hpos_zonas[_i]["x"] = int(_d.x)
            store._hpos_zonas[_i]["y"] = int(_d.y)
            store._hpos_zona_sel = _i
        return None

    def _hpos_ruta_salida():
        """
        Archivo donde se acumulan las posiciones exportadas.

        Va en tools/ y no en la raiz para no dejar nada suelto ahi. La carpeta
        se crea si no esta: el archivo lo escribe el juego, asi que no puede
        depender de que alguien la haya creado antes.
        """
        import os
        _dir = os.path.join(config.basedir, "tools")
        if not os.path.isdir(_dir):
            os.makedirs(_dir)
        return os.path.join(_dir, "posiciones_idle.txt")

    def _hpos_zonas_guardar():
        """
        Escribe las zonas en tools/posiciones_idle.txt, en el mismo formato de
        lista que usa el codigo del juego: (id, x, y, w, h).
        """
        if not store._hpos_zonas:
            return
        import datetime
        ruta = _hpos_ruta_salida()
        ts   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n")
            f.write("# ZONAS — {}\n".format(ts))
            f.write("# fondo: {}\n".format(store._hpos_bg_path or "(ninguno)"))
            f.write("ZONAS = [\n")
            for _z in store._hpos_zonas:
                f.write('    ("{}", {}, {}, {}, {}),\n'.format(
                    _z["id"], _z["x"], _z["y"], _z["w"], _z["h"]))
            f.write("]\n")
        renpy.notify("Guardadas {} zonas".format(len(store._hpos_zonas)))

    def _hpos_guardar():
        """
        Añade la posición actual al archivo tools/posiciones_idle.txt.
        Formato listo para copiar al código fuente del juego.
        """
        if not store._hpos_idle_path:
            return
        import datetime
        nombre  = store._hpos_idle_path.split("/")[-1].rsplit(".", 1)[0]
        ruta    = _hpos_ruta_salida()
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
    if _hpos_modo == "sprite" and _hpos_idle_path:
        draggroup:
            drag:
                drag_name ("idle_{}".format(_hpos_idle_id))
                xpos 0
                ypos 0
                draggable True
                droppable False
                dragged _hpos_al_soltar
                add _hpos_idle_path

    # ── 3b. Zonas arrastrables ────────────────────────────────────────────────
    # Cada zona es un rectangulo translucido con su id encima. En el juego el
    # boton va con `background None` y no se ve; acá se pinta SOLO para poder
    # agarrarlo. La seleccionada va en naranja para distinguirla del resto.
    if _hpos_modo == "zonas":
        draggroup:
            for _zi, _z in enumerate(_hpos_zonas):
                drag:
                    drag_name ("zona_{}".format(_zi))
                    xpos _z["x"]
                    ypos _z["y"]
                    draggable True
                    droppable False
                    dragged _hpos_zona_al_soltar
                    clicked SetVariable("_hpos_zona_sel", _zi)

                    fixed:
                        xysize (_z["w"], _z["h"])

                        frame:
                            xfill True
                            yfill True
                            background ("#ff980055" if _zi == _hpos_zona_sel else "#4fc3f744")
                            padding (0, 0)

                        text _z["id"]:
                            size 15
                            color "#ffffff"
                            outlines [(2, "#000000", 0, 0)]
                            xpos 6
                            ypos 4

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

                ## Botón Assets — piezas sueltas de quests y minijuegos.
                ## Se arrastran igual que un sprite y exportan las mismas
                ## coordenadas: comparten _hpos_idle_path.
                button:
                    yalign 0.5
                    background ("#3a6186" if _hpos_menu_abierto == "assets" else "#2d2d45")
                    hover_background "#4a7196"
                    padding (16, 8)
                    action SetVariable("_hpos_menu_abierto",
                        None if _hpos_menu_abierto == "assets" else "assets")
                    text "Assets" size 17 color "#cccccc" yalign 0.5

                ## Modo Zonas — para rectangulos invisibles (hotspots, botones
                ## de minijuego). Convive con el modo sprite: el fondo elegido
                ## es el mismo.
                button:
                    yalign 0.5
                    background ("#c66a00" if _hpos_modo == "zonas" else "#2d2d45")
                    hover_background "#e08020"
                    padding (16, 8)
                    action [
                        SetVariable("_hpos_menu_abierto", None),
                        SetVariable("_hpos_modo",
                            "sprite" if _hpos_modo == "zonas" else "zonas"),
                    ]
                    text "Zonas" size 17 color "#cccccc" yalign 0.5

                ## Nombre del sprite activo
                if _hpos_modo == "sprite" and _hpos_idle_path:
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

                ## Modo zonas: crear / borrar / medir / guardar
                if _hpos_modo == "zonas":
                    button:
                        yalign 0.5
                        background "#2d2d45"
                        hover_background "#4a7196"
                        padding (12, 8)
                        action Function(_hpos_zona_nueva)
                        text "+ Zona" size 16 color "#cccccc" yalign 0.5

                    if _hpos_zona_sel is not None and _hpos_zona_sel < len(_hpos_zonas):
                        $ _zsel = _hpos_zonas[_hpos_zona_sel]

                        frame:
                            yalign 0.5
                            background "#000000"
                            padding (10, 8)
                            text ("x={:4d} y={:4d}  w={:4d} h={:4d}".format(
                                    _zsel["x"], _zsel["y"], _zsel["w"], _zsel["h"])):
                                size 15
                                color "#ffffff"

                        ## Ancho y alto con pasos de _hpos_zona_paso
                        for _campo, _et in (("w", "W"), ("h", "H")):
                            button:
                                yalign 0.5
                                background "#2d2d45"
                                hover_background "#4a7196"
                                padding (9, 8)
                                action Function(_hpos_zona_medir, _campo, -_hpos_zona_paso)
                                text ("−" + _et) size 15 color "#cccccc" yalign 0.5
                            button:
                                yalign 0.5
                                background "#2d2d45"
                                hover_background "#4a7196"
                                padding (9, 8)
                                action Function(_hpos_zona_medir, _campo, _hpos_zona_paso)
                                text ("+" + _et) size 15 color "#cccccc" yalign 0.5

                        ## Paso: 1 para afinar, 10 para grueso
                        button:
                            yalign 0.5
                            background "#2d2d45"
                            hover_background "#4a7196"
                            padding (9, 8)
                            action SetVariable("_hpos_zona_paso",
                                1 if _hpos_zona_paso == 10 else 10)
                            text ("paso {}".format(_hpos_zona_paso)):
                                size 15
                                color "#cccccc"
                                yalign 0.5

                        button:
                            yalign 0.5
                            background "#7f0000"
                            hover_background "#c62828"
                            padding (9, 8)
                            action Function(_hpos_zona_borrar)
                            text "Borrar" size 15 color "#ffffff" yalign 0.5

                    button:
                        yalign 0.5
                        background "#2e7d32"
                        hover_background "#388e3c"
                        padding (14, 8)
                        action Function(_hpos_zonas_guardar)
                        text "Guardar" size 17 color "#ffffff" yalign 0.5

                ## Caja de coordenadas + botón Guardar (solo si hay sprite)
                elif _hpos_idle_path:
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
                    text "×" size 18 color "#ffffff" yalign 0.5

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

    # ── 6. Dropdown Sprites / Assets ──────────────────────────────────────────
    # Comparten el mismo cuerpo: los dos eligen la imagen arrastrable, solo
    # cambia de que lista salen.
    if _hpos_menu_abierto in ("sprites", "assets"):
        if _hpos_menu_abierto == "assets":
            $ _hpos_idles_lista = _hpos_lista_assets()
        else:
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
