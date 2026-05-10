################################################################################
## Herramienta de Ajuste Celular - Modelo de Datos
################################################################################
## Permite ajustar posicion, tamaño y layout de los menus del celular
## en tiempo real, y exportar los cambios para aplicar al codigo.

default modo_ajuste_celular = False
default ajuste_cel_screen_actual = "menu_celular"
default ajuste_cel_tab = "container"
default ajuste_cel_elemento_id = None
default ajuste_cel_sesion_cambios = []
default ajuste_cel_undo = []
default ajuste_cel_input_activo = None
default ajuste_cel_input_valor = ""

# Area de trabajo
default ajuste_cel_area_x = 630
default ajuste_cel_area_y = 0
default ajuste_cel_area_w = 660
default ajuste_cel_area_h = 1080
default ajuste_cel_area_orig_x = 630
default ajuste_cel_area_orig_y = 0
default ajuste_cel_area_orig_w = 660
default ajuste_cel_area_orig_h = 1080

init -5 python:
    import copy

    class ContainerCelular:
        """Representa el frame exterior de una pantalla del celular."""
        def __init__(self, screen_name, nombre, archivo,
                     xalign=0.5, yalign=0.5, xoffset=0, yoffset=0,
                     width=None, height=None,
                     min_width=None, min_height=None,
                     max_width=None, max_height=None,
                     padding_x=40, padding_y=30, spacing=20,
                     background="#1a1a2eEE",
                     grid_cols=None, grid_rows=None):
            self.screen_name = screen_name
            self.nombre = nombre
            self.archivo = archivo
            self.xalign = xalign
            self.yalign = yalign
            self.xoffset = xoffset
            self.yoffset = yoffset
            self.width = width
            self.height = height
            self.min_width = min_width
            self.min_height = min_height
            self.max_width = max_width
            self.max_height = max_height
            self.padding_x = padding_x
            self.padding_y = padding_y
            self.spacing = spacing
            self.background = background
            self.grid_cols = grid_cols
            self.grid_rows = grid_rows
            self._save_original()

        def _save_original(self):
            self.orig_xalign = self.xalign
            self.orig_yalign = self.yalign
            self.orig_xoffset = self.xoffset
            self.orig_yoffset = self.yoffset
            self.orig_width = self.width
            self.orig_height = self.height
            self.orig_min_width = self.min_width
            self.orig_min_height = self.min_height
            self.orig_max_width = self.max_width
            self.orig_max_height = self.max_height
            self.orig_padding_x = self.padding_x
            self.orig_padding_y = self.padding_y
            self.orig_spacing = self.spacing
            self.orig_grid_cols = self.grid_cols
            self.orig_grid_rows = self.grid_rows

        def fue_modificado(self):
            return (self.xalign != self.orig_xalign or
                    self.yalign != self.orig_yalign or
                    self.xoffset != self.orig_xoffset or
                    self.yoffset != self.orig_yoffset or
                    self.width != self.orig_width or
                    self.height != self.orig_height or
                    self.min_width != self.orig_min_width or
                    self.min_height != self.orig_min_height or
                    self.max_width != self.orig_max_width or
                    self.max_height != self.orig_max_height or
                    self.padding_x != self.orig_padding_x or
                    self.padding_y != self.orig_padding_y or
                    self.spacing != self.orig_spacing or
                    self.grid_cols != self.orig_grid_cols or
                    self.grid_rows != self.orig_grid_rows)

        def resetear(self):
            self.xalign = self.orig_xalign
            self.yalign = self.orig_yalign
            self.xoffset = self.orig_xoffset
            self.yoffset = self.orig_yoffset
            self.width = self.orig_width
            self.height = self.orig_height
            self.min_width = self.orig_min_width
            self.min_height = self.orig_min_height
            self.max_width = self.orig_max_width
            self.max_height = self.orig_max_height
            self.padding_x = self.orig_padding_x
            self.padding_y = self.orig_padding_y
            self.spacing = self.orig_spacing
            self.grid_cols = self.orig_grid_cols
            self.grid_rows = self.orig_grid_rows


    class ElementoInterno:
        """Representa un elemento interno de un menu del celular."""
        def __init__(self, id, nombre, container_screen,
                     xoffset=0, yoffset=0, size_w=None, size_h=None):
            self.id = id
            self.nombre = nombre
            self.container_screen = container_screen
            self.xoffset = xoffset
            self.yoffset = yoffset
            self.size_w = size_w
            self.size_h = size_h
            self._save_original()

        def _save_original(self):
            self.orig_xoffset = self.xoffset
            self.orig_yoffset = self.yoffset
            self.orig_size_w = self.size_w
            self.orig_size_h = self.size_h

        def fue_modificado(self):
            return (self.xoffset != self.orig_xoffset or
                    self.yoffset != self.orig_yoffset or
                    self.size_w != self.orig_size_w or
                    self.size_h != self.orig_size_h)

        def resetear(self):
            self.xoffset = self.orig_xoffset
            self.yoffset = self.orig_yoffset
            self.size_w = self.orig_size_w
            self.size_h = self.orig_size_h


    class SistemaAjusteCelular:
        """Registro central para todos los elementos ajustables del celular."""
        def __init__(self):
            self.containers = {}
            self.elementos = {}

        def registrar_container(self, **kwargs):
            c = ContainerCelular(**kwargs)
            self.containers[c.screen_name] = c

        def registrar_elemento(self, **kwargs):
            e = ElementoInterno(**kwargs)
            self.elementos[e.id] = e

        def obtener_container(self, screen_name):
            return self.containers.get(screen_name)

        def obtener_elementos_de(self, screen_name):
            return [e for e in self.elementos.values()
                    if e.container_screen == screen_name]

        def containers_modificados(self):
            return [c for c in self.containers.values() if c.fue_modificado()]

        def elementos_modificados(self):
            return [e for e in self.elementos.values() if e.fue_modificado()]

        def hay_cambios(self):
            return len(self.containers_modificados()) > 0 or len(self.elementos_modificados()) > 0

        def tomar_snapshot(self):
            for c in self.containers.values():
                c._save_original()
            for e in self.elementos.values():
                e._save_original()

        def resetear_todo(self):
            for c in self.containers.values():
                c.resetear()
            for e in self.elementos.values():
                e.resetear()

        def obtener_estado(self):
            """Retorna una copia profunda del estado actual para undo."""
            estado = {}
            for k, c in self.containers.items():
                estado["c_" + k] = {
                    "xalign": c.xalign, "yalign": c.yalign,
                    "xoffset": c.xoffset, "yoffset": c.yoffset,
                    "width": c.width, "height": c.height,
                    "min_width": c.min_width, "min_height": c.min_height,
                    "max_width": c.max_width, "max_height": c.max_height,
                    "padding_x": c.padding_x, "padding_y": c.padding_y,
                    "spacing": c.spacing,
                    "grid_cols": c.grid_cols, "grid_rows": c.grid_rows
                }
            for k, e in self.elementos.items():
                estado["e_" + k] = {
                    "xoffset": e.xoffset, "yoffset": e.yoffset,
                    "size_w": e.size_w, "size_h": e.size_h
                }
            return estado

        def restaurar_estado(self, estado):
            """Restaura un estado previamente guardado."""
            for k, c in self.containers.items():
                datos = estado.get("c_" + k)
                if datos:
                    c.xalign = datos["xalign"]
                    c.yalign = datos["yalign"]
                    c.xoffset = datos["xoffset"]
                    c.yoffset = datos["yoffset"]
                    c.width = datos["width"]
                    c.height = datos["height"]
                    c.min_width = datos["min_width"]
                    c.min_height = datos["min_height"]
                    c.max_width = datos["max_width"]
                    c.max_height = datos["max_height"]
                    c.padding_x = datos["padding_x"]
                    c.padding_y = datos["padding_y"]
                    c.spacing = datos["spacing"]
                    c.grid_cols = datos.get("grid_cols", c.grid_cols)
                    c.grid_rows = datos.get("grid_rows", c.grid_rows)
            for k, e in self.elementos.items():
                datos = estado.get("e_" + k)
                if datos:
                    e.xoffset = datos["xoffset"]
                    e.yoffset = datos["yoffset"]
                    e.size_w = datos["size_w"]
                    e.size_h = datos["size_h"]

        def lista_screens(self):
            """Retorna lista ordenada de (screen_name, nombre) para el selector."""
            return sorted([(c.screen_name, c.nombre) for c in self.containers.values()],
                         key=lambda x: x[1])


define sistema_ajuste_cel = SistemaAjusteCelular()

################################################################################
## Registro de pantallas del celular
################################################################################

init 1 python:

    # Menu principal
    sistema_ajuste_cel.registrar_container(
        screen_name="menu_celular",
        nombre="Menu Celular (Principal)",
        archivo="game/script/ui/hud/hud_celular.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        background="#1a1a2eEE",
        grid_cols=3, grid_rows=5,
        width=50, height=50
    )

    # Elementos internos del menu principal (9 botones)
    _btn_celular = [
        ("relaciones", "Boton Relaciones"),
        ("pistas", "Boton Pistas"),
        ("stats", "Boton Stats"),
        ("comprar", "Boton Comprar"),
        ("cheats", "Boton Cheats"),
        ("mensajes", "Boton Mensajes"),
        ("galeria", "Boton Galeria"),
        ("hot", "Boton Hot"),
        ("banco", "Boton Banco"),
    ]
    for _btn_id, _btn_nombre in _btn_celular:
        sistema_ajuste_cel.registrar_elemento(
            id="menu_celular_btn_{}".format(_btn_id),
            nombre=_btn_nombre,
            container_screen="menu_celular",
            size_w=150, size_h=150
        )

    # Lista de contactos (mensajes)
    sistema_ajuste_cel.registrar_container(
        screen_name="lista_contactos_mensajes",
        nombre="Lista Contactos",
        archivo="game/script/ui/hud/hud_mensajes.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=30, padding_y=25, spacing=15,
        min_width=500, min_height=400,
        background="#1a1a2eEE"
    )

    # Chat individual
    sistema_ajuste_cel.registrar_container(
        screen_name="pantalla_chat",
        nombre="Chat",
        archivo="game/script/ui/hud/hud_mensajes.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=0, padding_y=0, spacing=0,
        width=550, height=650,
        background="#1a1a2eF5"
    )

    # Selector de respuesta
    sistema_ajuste_cel.registrar_container(
        screen_name="selector_respuesta",
        nombre="Selector Respuesta",
        archivo="game/script/ui/hud/hud_mensajes.rpy",
        xalign=0.5, yalign=0.7,
        padding_x=25, padding_y=20, spacing=12,
        min_width=450, min_height=150,
        max_width=500, max_height=500,
        background="#1a1a2eF5"
    )

    # Resumen de recompensas
    sistema_ajuste_cel.registrar_container(
        screen_name="resumen_recompensas",
        nombre="Resumen Recompensas",
        archivo="game/script/ui/hud/hud_mensajes.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=30, padding_y=25, spacing=15,
        background="#1a1a2eF5"
    )

    # Galeria
    sistema_ajuste_cel.registrar_container(
        screen_name="panel_galeria",
        nombre="Galeria",
        archivo="game/script/ui/hud/hud_galeria.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=30, padding_y=25, spacing=15,
        min_width=600, min_height=450,
        max_width=700, max_height=550,
        background="#1a1a2eEE"
    )

    # Stats del MC
    sistema_ajuste_cel.registrar_container(
        screen_name="panel_stats_mc",
        nombre="Stats MC",
        archivo="game/script/ui/hud/hud_stats.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        min_width=400, min_height=300,
        background="#1a1a2eEE"
    )

    # Tienda
    sistema_ajuste_cel.registrar_container(
        screen_name="panel_tienda",
        nombre="Tienda",
        archivo="game/script/ui/hud/hud_stats.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        max_width=900, max_height=700,
        background="#2d1f3dEE"
    )

    # Inventario
    sistema_ajuste_cel.registrar_container(
        screen_name="panel_inventario",
        nombre="Inventario",
        archivo="game/script/ui/hud/hud_stats.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        min_width=450, min_height=300,
        background="#1a2e1aEE"
    )

    # Pistas
    sistema_ajuste_cel.registrar_container(
        screen_name="panel_pistas",
        nombre="Pistas",
        archivo="game/script/ui/hud/hud_pistas.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        min_width=650, min_height=350,
        background="#1a1a2eEE"
    )

    # Estadisticas NPCs
    sistema_ajuste_cel.registrar_container(
        screen_name="estadisticas_npcs",
        nombre="Estadisticas NPCs",
        archivo="game/script/ui/menus/menu_interaction.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        background="#0288D1EE"
    )

    # Cheats
    sistema_ajuste_cel.registrar_container(
        screen_name="menu_cheats",
        nombre="Cheats",
        archivo="game/script/ui/menus/menu_cheats.rpy",
        xalign=0.5, yalign=0.5,
        padding_x=40, padding_y=30, spacing=20,
        background="#000000DD"
    )


################################################################################
## Funciones de control
################################################################################

init python:

    def activar_ajuste_celular():
        store.modo_ajuste_celular = True
        sistema_ajuste_cel.tomar_snapshot()
        store.ajuste_cel_sesion_cambios = []
        store.ajuste_cel_undo = []
        store.ajuste_cel_screen_actual = "menu_celular"
        store.ajuste_cel_tab = "container"
        store.ajuste_cel_elemento_id = None
        # Snapshot del area de trabajo
        store.ajuste_cel_area_orig_x = store.ajuste_cel_area_x
        store.ajuste_cel_area_orig_y = store.ajuste_cel_area_y
        store.ajuste_cel_area_orig_w = store.ajuste_cel_area_w
        store.ajuste_cel_area_orig_h = store.ajuste_cel_area_h
        renpy.show_screen("panel_ajuste_celular")
        renpy.show_screen("menu_celular")
        renpy.restart_interaction()

    def desactivar_ajuste_celular():
        store.modo_ajuste_celular = False
        sistema_ajuste_cel.resetear_todo()
        # Resetear area de trabajo
        store.ajuste_cel_area_x = store.ajuste_cel_area_orig_x
        store.ajuste_cel_area_y = store.ajuste_cel_area_orig_y
        store.ajuste_cel_area_w = store.ajuste_cel_area_orig_w
        store.ajuste_cel_area_h = store.ajuste_cel_area_orig_h
        store.ajuste_cel_elemento_id = None
        renpy.hide_screen("panel_ajuste_celular")
        # Ocultar la pantalla activa (puede no ser menu_celular)
        _scr = store.ajuste_cel_screen_actual
        if renpy.get_screen(_scr):
            renpy.hide_screen(_scr)
        store.menu_celular_abierto = False
        renpy.restart_interaction()

    def ajuste_cel_cambiar_screen(nuevo_screen):
        """Cambia la pantalla visible en modo ajuste."""
        viejo = store.ajuste_cel_screen_actual
        if viejo == nuevo_screen:
            return
        # Ocultar la pantalla vieja
        if renpy.get_screen(viejo):
            renpy.hide_screen(viejo)
        # Mostrar la nueva
        store.ajuste_cel_screen_actual = nuevo_screen
        store.ajuste_cel_elemento_id = None
        renpy.show_screen(nuevo_screen)
        renpy.restart_interaction()

    def toggle_ajuste_celular():
        if store.modo_ajuste_celular:
            desactivar_ajuste_celular()
        else:
            activar_ajuste_celular()

    def _push_undo_cel():
        estado = sistema_ajuste_cel.obtener_estado()
        # Incluir area de trabajo en el estado de undo
        estado["_area"] = {
            "x": store.ajuste_cel_area_x,
            "y": store.ajuste_cel_area_y,
            "w": store.ajuste_cel_area_w,
            "h": store.ajuste_cel_area_h
        }
        store.ajuste_cel_undo.append(estado)
        if len(store.ajuste_cel_undo) > 20:
            store.ajuste_cel_undo.pop(0)

    def deshacer_ajuste_cel():
        if store.ajuste_cel_undo:
            estado = store.ajuste_cel_undo.pop()
            sistema_ajuste_cel.restaurar_estado(estado)
            # Restaurar area de trabajo
            area = estado.get("_area")
            if area:
                store.ajuste_cel_area_x = area["x"]
                store.ajuste_cel_area_y = area["y"]
                store.ajuste_cel_area_w = area["w"]
                store.ajuste_cel_area_h = area["h"]
            renpy.restart_interaction()

    def ajuste_cel_modificar(attr, valor, es_elemento=False):
        """Modifica un atributo del container o elemento seleccionado."""
        _push_undo_cel()
        if es_elemento and store.ajuste_cel_elemento_id:
            elem = sistema_ajuste_cel.elementos.get(store.ajuste_cel_elemento_id)
            if elem:
                val_actual = getattr(elem, attr, 0) or 0
                nuevo = val_actual + valor
                if attr in ("size_w", "size_h") and nuevo < 10:
                    nuevo = 10
                setattr(elem, attr, nuevo)
        else:
            c = sistema_ajuste_cel.obtener_container(store.ajuste_cel_screen_actual)
            if c:
                val_actual = getattr(c, attr, 0) or 0
                nuevo = val_actual + valor
                if attr in ("xalign", "yalign"):
                    nuevo = round(max(0.0, min(1.0, nuevo)), 2)
                elif attr in ("padding_x", "padding_y", "spacing"):
                    nuevo = max(0, nuevo)
                elif attr in ("width", "height", "min_width", "min_height", "max_width", "max_height"):
                    if nuevo < 50:
                        nuevo = 50
                elif attr in ("grid_cols", "grid_rows"):
                    nuevo = max(1, int(nuevo))
                setattr(c, attr, nuevo)
        renpy.restart_interaction()

    def exportar_ajuste_celular():
        """Exporta los cambios a un archivo .txt listo para copiar-pegar."""
        import time
        timestamp = time.strftime("%Y_%m_%d_%H%M%S")
        fecha = time.strftime("%d/%m/%Y %H:%M:%S")

        lineas = []
        lineas.append("# ============================================================")
        lineas.append("# AJUSTE CELULAR - {}".format(fecha))
        lineas.append("# ============================================================")
        lineas.append("")

        containers_mod = sistema_ajuste_cel.containers_modificados()
        elementos_mod = sistema_ajuste_cel.elementos_modificados()
        _area_mod = _area_fue_modificada()

        if not containers_mod and not elementos_mod and not _area_mod:
            lineas.append("# Sin cambios.")
        else:
            # Area de trabajo
            if _area_mod:
                lineas.append("## AREA DE TRABAJO")
                lineas.append("# Antes: xpos {}  ypos {}  ancho {}  alto {}".format(
                    store.ajuste_cel_area_orig_x, store.ajuste_cel_area_orig_y,
                    store.ajuste_cel_area_orig_w, store.ajuste_cel_area_orig_h))
                lineas.append("# Ahora: xpos {}  ypos {}  ancho {}  alto {}".format(
                    store.ajuste_cel_area_x, store.ajuste_cel_area_y,
                    store.ajuste_cel_area_w, store.ajuste_cel_area_h))
                lineas.append("")
            for c in containers_mod:
                lineas.append("## CONTAINER: {}".format(c.nombre))
                lineas.append("# Screen: {}".format(c.screen_name))
                lineas.append("# Archivo: {}".format(c.archivo))

                antes = []
                antes.append("xalign {}".format(c.orig_xalign))
                antes.append("yalign {}".format(c.orig_yalign))
                if c.orig_xoffset: antes.append("xoffset {}".format(c.orig_xoffset))
                if c.orig_yoffset: antes.append("yoffset {}".format(c.orig_yoffset))
                antes.append("padding ({}, {})".format(c.orig_padding_x, c.orig_padding_y))
                antes.append("spacing {}".format(c.orig_spacing))
                if c.orig_width: antes.append("width {}".format(c.orig_width))
                if c.orig_height: antes.append("height {}".format(c.orig_height))
                if c.orig_min_width: antes.append("min_width {}".format(c.orig_min_width))
                if c.orig_min_height: antes.append("min_height {}".format(c.orig_min_height))
                if c.orig_max_width: antes.append("max_width {}".format(c.orig_max_width))
                if c.orig_max_height: antes.append("max_height {}".format(c.orig_max_height))
                lineas.append("# Antes: {}".format("  ".join(antes)))

                lineas.append("# Ahora:")
                lineas.append("frame:")
                lineas.append("    xalign {}".format(c.xalign))
                lineas.append("    yalign {}".format(c.yalign))
                if c.xoffset: lineas.append("    xoffset {}".format(c.xoffset))
                if c.yoffset: lineas.append("    yoffset {}".format(c.yoffset))
                lineas.append("    background \"{}\"".format(c.background))
                lineas.append("    padding ({}, {})".format(c.padding_x, c.padding_y))
                if c.width and c.height:
                    lineas.append("    xysize ({}, {})".format(c.width, c.height))
                elif c.width:
                    lineas.append("    xsize {}".format(c.width))
                elif c.height:
                    lineas.append("    ysize {}".format(c.height))
                if c.min_width and c.min_height:
                    lineas.append("    minimum ({}, {})".format(c.min_width, c.min_height))
                elif c.min_width:
                    lineas.append("    xminimum {}".format(c.min_width))
                elif c.min_height:
                    lineas.append("    yminimum {}".format(c.min_height))
                if c.max_width and c.max_height:
                    lineas.append("    maximum ({}, {})".format(c.max_width, c.max_height))
                elif c.max_width:
                    lineas.append("    xmaximum {}".format(c.max_width))
                elif c.max_height:
                    lineas.append("    ymaximum {}".format(c.max_height))
                lineas.append("    # spacing en vbox: {}".format(c.spacing))
                if c.grid_cols:
                    lineas.append("    # grid_cols: {}".format(c.grid_cols))
                if c.grid_rows:
                    lineas.append("    # grid_rows: {}".format(c.grid_rows))
                lineas.append("")

            # Agrupar elementos por screen
            screens_con_elementos = {}
            for e in elementos_mod:
                if e.container_screen not in screens_con_elementos:
                    screens_con_elementos[e.container_screen] = []
                screens_con_elementos[e.container_screen].append(e)

            for screen_name, elems in screens_con_elementos.items():
                c = sistema_ajuste_cel.obtener_container(screen_name)
                nombre_screen = c.nombre if c else screen_name
                lineas.append("## ELEMENTOS: {} ({})".format(nombre_screen, screen_name))
                for e in elems:
                    partes = []
                    if e.xoffset != e.orig_xoffset:
                        partes.append("xoffset {} -> {}".format(e.orig_xoffset, e.xoffset))
                    if e.yoffset != e.orig_yoffset:
                        partes.append("yoffset {} -> {}".format(e.orig_yoffset, e.yoffset))
                    if e.size_w != e.orig_size_w or e.size_h != e.orig_size_h:
                        partes.append("xysize ({}, {}) -> ({}, {})".format(
                            e.orig_size_w, e.orig_size_h, e.size_w, e.size_h))
                    lineas.append("# {}: {}".format(e.nombre, "  |  ".join(partes)))
                    lineas.append("#   xoffset {}  yoffset {}  xysize ({}, {})".format(
                        e.xoffset, e.yoffset, e.size_w, e.size_h))
                lineas.append("")

        contenido = "\n".join(lineas)

        # Guardar sesion
        nombre_sesion = "ajuste_celular_sesion_{}.txt".format(timestamp)
        with open(os.path.join(config.basedir, nombre_sesion), "w", encoding="utf-8") as f:
            f.write(contenido)

        # Appendear al historial
        with open(os.path.join(config.basedir, "ajuste_celular_historial.txt"), "a", encoding="utf-8") as f:
            f.write("\n\n" + contenido)

        renpy.notify("Exportado: {}".format(nombre_sesion))

    def ajuste_cel_abrir_input(attr, es_elemento=False):
        """Abre el input de texto para un atributo."""
        if es_elemento and store.ajuste_cel_elemento_id:
            elem = sistema_ajuste_cel.elementos.get(store.ajuste_cel_elemento_id)
            if elem:
                val = getattr(elem, attr, 0) or 0
                store.ajuste_cel_input_valor = str(val)
        else:
            c = sistema_ajuste_cel.obtener_container(store.ajuste_cel_screen_actual)
            if c:
                val = getattr(c, attr, 0) or 0
                store.ajuste_cel_input_valor = str(val)
        store.ajuste_cel_input_activo = (attr, es_elemento)
        renpy.restart_interaction()

    def ajuste_cel_aplicar_input():
        """Aplica el valor del input de texto al atributo activo."""
        if not store.ajuste_cel_input_activo:
            return
        attr, es_elemento = store.ajuste_cel_input_activo
        texto = store.ajuste_cel_input_valor.strip()
        if not texto:
            store.ajuste_cel_input_activo = None
            renpy.restart_interaction()
            return
        try:
            if attr in ("xalign", "yalign"):
                nuevo = float(texto)
                nuevo = round(max(0.0, min(1.0, nuevo)), 2)
            else:
                nuevo = int(float(texto))
                if attr in ("size_w", "size_h", "width", "height", "min_width", "min_height", "max_width", "max_height"):
                    if nuevo < 10:
                        nuevo = 10
                elif attr in ("padding_x", "padding_y", "spacing"):
                    nuevo = max(0, nuevo)
                elif attr in ("grid_cols", "grid_rows"):
                    nuevo = max(1, nuevo)
                elif attr in ("area_w", "area_h"):
                    nuevo = max(100, nuevo)
                elif attr in ("area_x", "area_y"):
                    nuevo = max(0, nuevo)
        except ValueError:
            store.ajuste_cel_input_activo = None
            renpy.restart_interaction()
            return
        _push_undo_cel()
        if es_elemento == "area":
            mapa = {
                "area_x": "ajuste_cel_area_x",
                "area_y": "ajuste_cel_area_y",
                "area_w": "ajuste_cel_area_w",
                "area_h": "ajuste_cel_area_h"
            }
            var = mapa.get(attr)
            if var:
                setattr(store, var, nuevo)
        elif es_elemento and store.ajuste_cel_elemento_id:
            elem = sistema_ajuste_cel.elementos.get(store.ajuste_cel_elemento_id)
            if elem:
                setattr(elem, attr, nuevo)
        else:
            c = sistema_ajuste_cel.obtener_container(store.ajuste_cel_screen_actual)
            if c:
                setattr(c, attr, nuevo)
        store.ajuste_cel_input_activo = None
        renpy.restart_interaction()

    def ajuste_cel_cancelar_input():
        """Cancela el input de texto."""
        store.ajuste_cel_input_activo = None
        renpy.restart_interaction()

    def limpiar_ajuste_cel():
        """Resetea todos los cambios sin exportar."""
        sistema_ajuste_cel.resetear_todo()
        # Resetear area de trabajo
        store.ajuste_cel_area_x = store.ajuste_cel_area_orig_x
        store.ajuste_cel_area_y = store.ajuste_cel_area_orig_y
        store.ajuste_cel_area_w = store.ajuste_cel_area_orig_w
        store.ajuste_cel_area_h = store.ajuste_cel_area_orig_h
        store.ajuste_cel_undo = []
        store.ajuste_cel_elemento_id = None
        renpy.restart_interaction()

    def _area_fue_modificada():
        """Retorna True si el area de trabajo fue modificada."""
        return (store.ajuste_cel_area_x != store.ajuste_cel_area_orig_x or
                store.ajuste_cel_area_y != store.ajuste_cel_area_orig_y or
                store.ajuste_cel_area_w != store.ajuste_cel_area_orig_w or
                store.ajuste_cel_area_h != store.ajuste_cel_area_orig_h)

    def ajuste_cel_area_modificar(attr, valor):
        """Modifica un atributo del area de trabajo."""
        _push_undo_cel()
        mapa = {
            "area_x": "ajuste_cel_area_x",
            "area_y": "ajuste_cel_area_y",
            "area_w": "ajuste_cel_area_w",
            "area_h": "ajuste_cel_area_h"
        }
        var = mapa.get(attr)
        if var:
            val_actual = getattr(store, var, 0)
            nuevo = val_actual + valor
            if attr in ("area_w", "area_h"):
                nuevo = max(100, nuevo)
            if attr in ("area_x", "area_y"):
                nuevo = max(0, nuevo)
            setattr(store, var, int(nuevo))
        renpy.restart_interaction()

    def ajuste_cel_area_abrir_input(attr):
        """Abre el input de texto para un atributo del area."""
        mapa = {
            "area_x": "ajuste_cel_area_x",
            "area_y": "ajuste_cel_area_y",
            "area_w": "ajuste_cel_area_w",
            "area_h": "ajuste_cel_area_h"
        }
        var = mapa.get(attr)
        if var:
            store.ajuste_cel_input_valor = str(getattr(store, var, 0))
        store.ajuste_cel_input_activo = (attr, "area")
        renpy.restart_interaction()
