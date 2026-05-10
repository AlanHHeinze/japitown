################################################################################
## HUD de Navegación
################################################################################
## Interfaz visual para el sistema de navegación con información de tiempo


# Variable para controlar visibilidad del modo debug/desarrollo
default mostrar_debug_hud = False

# Variable para controlar si el contenido del HUD se renderiza.
# El screen siempre esta activo (para que las teclas funcionen),
# pero el contenido visual se oculta/muestra con esta variable.
default hud_contenido_visible = True

# Delay para ocultar sprites de NPCs durante la transicion de bg al cambiar horario
default hud_npc_delay_horario = False

# Labels especiales para el panel de debug (eventos y labels no registrados en sistema_events)
define _debug_labels_especiales = [
    {"nombre": "Violet: Evento 1 (primera vez)", "label": "evento1_violet"},
    {"nombre": "Violet: Evento 1 (repetir)", "label": "evento1_violet_repetir"},
    {"nombre": "Violet: Evento 2 (primera vez)", "label": "evento2_violet"},
    {"nombre": "Violet: Evento 2 (repetir)", "label": "evento2_violet_repetir"},
    {"nombre": "Violet: Invitar VR", "label": "invitar_violet_vr"},
    {"nombre": "Casco VR: Usar", "label": "usar_casco_vr"},
    {"nombre": "Casco VR: Repetir", "label": "usar_casco_vr_repetir"},
]

# Variable para el botón de test simple
default test_contador = 0

# Variables para herramienta de posicionamiento de sprites
default modo_posicionamiento = False
default sprite_posicion_actual = {"npc": None, "x": 0, "y": 0}

# Variables para herramienta de posicionamiento
# Pestañas disponibles: "sprites", "hotspots", "screen"
default modo_posicionamiento_tipo = "sprites"
default hotspot_seleccionado_id = None  # ID del hotspot actualmente seleccionado
default hotspot_posicion_actual = {"id": None, "x": 0, "y": 0, "w": 100, "h": 100}
default hotspots_guardados = []  # Lista de hotspots modificados (legado, se mantiene para compatibilidad)
default pos_hotspot_tipo_filtro = "MOVE"  # Filtro de tipo en tab Hotspots: "MOVE", "ACTION", "TODOS"

# Variables para creación de nuevos hotspots
default modo_crear_hotspot = False  # True cuando estamos creando un nuevo hotspot
default hotspots_temporales = []  # Lista de hotspots creados en esta sesión
default hotspot_nuevo_datos = {"id": "", "nombre": "", "tipo": "MOVE", "destino": ""}
default hotspot_nuevo_nombre = "Nuevo"  # Nombre para el input

# Variables para pestaña "Screen" (elementos posicionables agrupados por screen)
default pos_otros_elemento_id = None          # ID del elemento seleccionado
default pos_otros_posicion_actual = {"id": None, "x": 0, "y": 0, "xanchor": 0.5, "yanchor": 1.0}
default pos_screen_filtro = ""                # Screen activo como filtro ("" = ninguno)
# Sistema de registro de sesión
default pos_sesion_cambios = []              # Lista de cambios confirmados esta sesión
default pos_sesion_undo    = []              # Stack de estados previos (para deshacer)

# Variable para el preview de locación destino al hacer hover
# Guarda dict con: nombre, x, y, w, h del hotspot
default hover_destino_locacion = None

init python:
    def ocultar_hud():
        """Oculta el contenido visual del HUD sin destruir el screen."""
        store.hud_contenido_visible = False
        renpy.restart_interaction()

    def mostrar_hud():
        """Muestra el contenido visual del HUD."""
        store.hud_contenido_visible = True
        renpy.restart_interaction()

    def actualizar_posicion_sprite(drags, drop):
        """
        Callback que se ejecuta cuando se arrastra un sprite.
        Actualiza las coordenadas en tiempo real.

        El sprite usa xanchor=0.5 (centro) y yanchor=1.0 (abajo), así que:
        - x final = posición izquierda del drag + ancho/2
        - y final = posición superior del drag + alto (para obtener el borde inferior)
        """
        if drags:
            d = drags[0]
            # Calcular posición ajustada para los anchors del sprite
            # d.x, d.y son la esquina superior-izquierda
            # d.w, d.h son el ancho y alto del elemento arrastrado
            x_centro = int(d.x + d.w / 2)  # Centro horizontal
            y_abajo = int(d.y + d.h)        # Borde inferior
            
            store.sprite_posicion_actual["x"] = x_centro
            store.sprite_posicion_actual["y"] = y_abajo
            store.sprite_posicion_actual["npc"] = d.drag_name
        return None
    
    def actualizar_posicion_hotspot(drags, drop):
        """
        Callback que se ejecuta cuando se arrastra un hotspot.
        Actualiza las coordenadas en tiempo real.
        """
        if drags:
            d = drags[0]
            # La posición del hotspot es la esquina superior-izquierda
            store.hotspot_posicion_actual["x"] = int(d.x)
            store.hotspot_posicion_actual["y"] = int(d.y)
            store.hotspot_posicion_actual["id"] = d.drag_name
        return None
    
    def _registrar_cambio_drag(elem, x_nuevo, y_nuevo):
        """Registra un cambio de drag en pos_sesion_cambios sin deseleccionar."""
        import time
        loc = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "desconocida"
        cambio = {
            "tipo": "otro",
            "timestamp": time.strftime("%d/%m/%Y %H:%M:%S"),
            "locacion": loc,
            "id": elem.id,
            "nombre": elem.nombre,
            "grupo": elem.grupo,
            "imagen": elem.imagen,
            "x_original": elem.x_original,
            "y_original": elem.y_original,
            "x_nuevo": x_nuevo,
            "y_nuevo": y_nuevo,
            "xanchor": elem.xanchor,
            "yanchor": elem.yanchor,
        }
        for i, c in enumerate(store.pos_sesion_cambios):
            if c["tipo"] == "otro" and c["id"] == elem.id:
                store.pos_sesion_cambios[i] = cambio
                return
        store.pos_sesion_cambios.append(cambio)

    def actualizar_posicion_otros(drags, drop):
        """
        Callback para drag de elementos del tab Screen (sistema_pos).
        Usa el tamanio real de la imagen (no del drag/frame) para calcular
        el punto de anclaje correcto, igual que calcular_top_left_desde_ancla.
        """
        if drags:
            d = drags[0]
            elem = sistema_pos.obtener(d.drag_name)
            if elem:
                # Usar tamanio de la IMAGEN, no del drag (que incluye frame/padding/texto)
                img_w, img_h = obtener_tamanio_imagen_seguro(elem.imagen)
                # El top-left del drag = top-left de la imagen (calcular_top_left_desde_ancla)
                # Punto de anclaje = top-left + tamanio_imagen * anchor
                x_ancla = int(d.x + img_w * elem.xanchor)
                y_ancla = int(d.y + img_h * elem.yanchor)
                # Seleccionar el elemento si no estaba seleccionado
                if store.pos_otros_elemento_id != d.drag_name:
                    store.pos_otros_elemento_id = d.drag_name
                store.pos_otros_posicion_actual["x"] = x_ancla
                store.pos_otros_posicion_actual["y"] = y_ancla
                store.pos_otros_posicion_actual["id"] = d.drag_name
                store.pos_otros_posicion_actual["xanchor"] = elem.xanchor
                store.pos_otros_posicion_actual["yanchor"] = elem.yanchor
                # Actualizar posición en el registro del sistema
                sistema_pos.actualizar_posicion(d.drag_name, x_ancla, y_ancla)
                # Registrar cambio en la sesión para que se exporte
                _registrar_cambio_drag(elem, x_ancla, y_ancla)
                renpy.notify("{}: ({}, {})".format(elem.nombre, x_ancla, y_ancla))
                # Forzar posición visual del drag usando tamanio de imagen
                tl_x = x_ancla - int(img_w * elem.xanchor)
                tl_y = y_ancla - int(img_h * elem.yanchor)
                d.snap(tl_x, tl_y)
                renpy.restart_interaction()
        return None
    
    def seleccionar_hotspot(hotspot):
        """Selecciona un hotspot y carga sus datos en el panel."""
        store.hotspot_seleccionado_id = hotspot.id
        store.hotspot_posicion_actual["id"] = hotspot.id
        store.hotspot_posicion_actual["x"] = hotspot.x
        store.hotspot_posicion_actual["y"] = hotspot.y
        store.hotspot_posicion_actual["w"] = hotspot.w
        store.hotspot_posicion_actual["h"] = hotspot.h
    
    def modificar_dimension_hotspot(dimension, delta):
        """Modifica una dimensión del hotspot seleccionado y actualiza la vista."""
        if dimension == "w":
            store.hotspot_posicion_actual["w"] = max(20, store.hotspot_posicion_actual["w"] + delta)
        elif dimension == "h":
            store.hotspot_posicion_actual["h"] = max(20, store.hotspot_posicion_actual["h"] + delta)
        renpy.restart_interaction()  # Actualizar visualización inmediatamente
    
    def guardar_hotspot_actual():
        """Guarda el hotspot actual en la lista de hotspots guardados."""
        if not store.hotspot_posicion_actual["id"]:
            pass
            return
        
        # Crear copia del hotspot actual
        datos = {
            "locacion": sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "desconocida",
            "id": store.hotspot_posicion_actual["id"],
            "x": store.hotspot_posicion_actual["x"],
            "y": store.hotspot_posicion_actual["y"],
            "w": store.hotspot_posicion_actual["w"],
            "h": store.hotspot_posicion_actual["h"]
        }
        
        # Buscar si ya existe y actualizar, o agregar nuevo
        encontrado = False
        for i, h in enumerate(store.hotspots_guardados):
            if h["locacion"] == datos["locacion"] and h["id"] == datos["id"]:
                store.hotspots_guardados[i] = datos
                encontrado = True
                break
        
        if not encontrado:
            store.hotspots_guardados.append(datos)
        
        pass
    
    def exportar_hotspots_guardados():
        """Exporta los hotspots guardados a un archivo de texto."""
        if not store.hotspots_guardados:
            pass
            return
        
        import os
        ruta = os.path.join(config.basedir, "hotspots_exportados.txt")
        
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("# Hotspots Exportados\n")
            f.write("# Copia este código en locations_house.rpy\n\n")
            
            # Agrupar por locación
            locaciones = {}
            for h in store.hotspots_guardados:
                loc = h["locacion"]
                if loc not in locaciones:
                    locaciones[loc] = []
                locaciones[loc].append(h)
            
            for loc, hotspots in locaciones.items():
                f.write(f"# Locación: {loc}\n")
                for h in hotspots:
                    nombre = h.get('nombre', '')
                    tipo = h.get('tipo', 'MOVE')
                    destino = h.get('destino', '')
                    f.write(f"# Hotspot: {h['id']}\n")
                    f.write(f"# Nombre: {nombre}, Tipo: {tipo}, Destino: {destino}\n")
                    f.write(f"Hotspot(\"{h['id']}\", \"{tipo}\", {h['x']}, {h['y']}, {h['w']}, {h['h']}, destino=\"{destino}\", nombre=\"{nombre}\")\n\n")
        
        pass
    
    def limpiar_hotspots_guardados():
        """Limpia la lista de hotspots guardados."""
        store.hotspots_guardados = []
        pass
    
    def centrar_hotspot_en_pantalla(hotspot):
        """Centra un hotspot existente en el centro de la pantalla."""
        store.hotspot_seleccionado_id = hotspot.id
        store.hotspot_posicion_actual["id"] = hotspot.id
        store.hotspot_posicion_actual["x"] = 860  # Centro horizontal (1920/2 - 100)
        store.hotspot_posicion_actual["y"] = 490  # Centro vertical (1080/2 - 50)
        store.hotspot_posicion_actual["w"] = hotspot.w
        store.hotspot_posicion_actual["h"] = hotspot.h
        pass
        renpy.restart_interaction()
    
    def obtener_lista_locaciones():
        """Retorna lista de IDs de todas las locaciones registradas."""
        return list(sistema_locaciones.locaciones.keys())
    
    def crear_hotspot_nuevo():
        """Crea un nuevo hotspot temporal en el centro de la pantalla."""
        import time
        
        # Usar el nombre del input o generar uno por defecto
        nombre_hotspot = store.hotspot_nuevo_nombre if store.hotspot_nuevo_nombre else "Nuevo"
        nuevo_id = f"{nombre_hotspot}_{int(time.time()) % 10000}"
        
        # Crear objeto Hotspot temporal
        nuevo = Hotspot(
            id=nuevo_id,
            tipo=store.hotspot_nuevo_datos.get("tipo", "MOVE"),
            x=860,
            y=490,
            w=200,
            h=100,
            destino=store.hotspot_nuevo_datos.get("destino", ""),
            nombre=nombre_hotspot
        )
        
        # Agregar a la locación actual (no elimina los anteriores)
        if sistema_locaciones.locacion_actual:
            sistema_locaciones.locacion_actual.agregar_hotspot(nuevo)
            store.hotspots_temporales.append(nuevo_id)
            
            # Seleccionar el nuevo automáticamente (los anteriores siguen visibles)
            store.hotspot_seleccionado_id = nuevo_id
            store.hotspot_posicion_actual["id"] = nuevo_id
            store.hotspot_posicion_actual["x"] = 860
            store.hotspot_posicion_actual["y"] = 490
            store.hotspot_posicion_actual["w"] = 200
            store.hotspot_posicion_actual["h"] = 100
            
            pass
        
        # Resetear nombre para el siguiente
        store.hotspot_nuevo_nombre = "Nuevo"
        store.modo_crear_hotspot = False
        renpy.restart_interaction()
    
    def actualizar_destino_hotspot(destino_id):
        """Actualiza el destino del hotspot seleccionado."""
        store.hotspot_nuevo_datos["destino"] = destino_id
        renpy.restart_interaction()
    
    def actualizar_tipo_hotspot(tipo):
        """Actualiza el tipo del hotspot (MOVE o ACTION)."""
        store.hotspot_nuevo_datos["tipo"] = tipo
        renpy.restart_interaction()
    
    def guardar_hotspot_completo():
        """Guarda el hotspot actual, lo fija en su lugar y lo deselecciona."""
        if not store.hotspot_posicion_actual["id"]:
            pass
            return
        
        hotspot_id = store.hotspot_posicion_actual["id"]
        loc_actual = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "loc"
        destino = store.hotspot_nuevo_datos.get("destino", "")
        
        # Generar nombre automático: locacionactual_locaciondestino
        nombre_auto = f"{loc_actual}_{destino}" if destino else f"{loc_actual}_sin_destino"
        
        # Buscar el hotspot real y aplicar cambios
        for hotspot in sistema_locaciones.locacion_actual.hotspots:
            if hotspot.id == hotspot_id:
                # Aplicar posición y tamaño final
                hotspot.x = store.hotspot_posicion_actual["x"]
                hotspot.y = store.hotspot_posicion_actual["y"]
                hotspot.w = store.hotspot_posicion_actual["w"]
                hotspot.h = store.hotspot_posicion_actual["h"]
                hotspot.destino = destino
                hotspot.nombre = nombre_auto
                break
        
        # Crear registro para exportar
        datos = {
            "locacion": loc_actual,
            "id": nombre_auto,
            "nombre": nombre_auto,
            "tipo": store.hotspot_nuevo_datos.get("tipo", "MOVE"),
            "destino": destino,
            "x": store.hotspot_posicion_actual["x"],
            "y": store.hotspot_posicion_actual["y"],
            "w": store.hotspot_posicion_actual["w"],
            "h": store.hotspot_posicion_actual["h"]
        }
        
        # Agregar a lista de guardados
        store.hotspots_guardados.append(datos)
        
        # IMPORTANTE: Deseleccionar el hotspot para que el siguiente sea independiente
        store.hotspot_seleccionado_id = None
        store.hotspot_posicion_actual = {"id": None, "x": 0, "y": 0, "w": 100, "h": 100}
        store.hotspot_nuevo_datos = {"id": "", "nombre": "", "tipo": "MOVE", "destino": ""}
        
        pass
        renpy.restart_interaction()
    
    def aplicar_cambios_hotspot():
        """Aplica los cambios de posición y tamaño al hotspot real."""
        if not store.hotspot_posicion_actual["id"]:
            pass
            return

        hotspot_id = store.hotspot_posicion_actual["id"]

        # Buscar el hotspot en la locación actual
        for hotspot in sistema_locaciones.locacion_actual.hotspots:
            if hotspot.id == hotspot_id:
                # Aplicar cambios al objeto real
                hotspot.x = store.hotspot_posicion_actual["x"]
                hotspot.y = store.hotspot_posicion_actual["y"]
                hotspot.w = store.hotspot_posicion_actual["w"]
                hotspot.h = store.hotspot_posicion_actual["h"]

                # Actualizar destino si está configurado
                if store.hotspot_nuevo_datos.get("destino"):
                    hotspot.destino = store.hotspot_nuevo_datos["destino"]

                pass
                renpy.restart_interaction()
                return

        pass

    # =========================================================================
    # FUNCIONES: Pestaña "Otros" (elementos genéricos del sistema_pos)
    # =========================================================================

    def seleccionar_elemento_otros(elem_id):
        """Selecciona un elemento posicionable para moverlo en el panel Otros."""
        elem = sistema_pos.obtener(elem_id)
        if elem:
            store.pos_otros_elemento_id = elem_id
            store.pos_otros_posicion_actual["id"] = elem_id
            store.pos_otros_posicion_actual["x"] = elem.x
            store.pos_otros_posicion_actual["y"] = elem.y
            store.pos_otros_posicion_actual["xanchor"] = elem.xanchor
            store.pos_otros_posicion_actual["yanchor"] = elem.yanchor
        renpy.restart_interaction()

    def deseleccionar_elemento_otros():
        """Deselecciona el elemento actual en el panel Otros."""
        store.pos_otros_elemento_id = None
        store.pos_otros_posicion_actual = {"id": None, "x": 0, "y": 0, "xanchor": 0.5, "yanchor": 1.0}
        renpy.restart_interaction()

    def modificar_coordenada_otros(eje, delta):
        """
        Modifica la coordenada X o Y del elemento seleccionado en tab Otros.
        eje: "x" o "y"
        delta: cantidad a sumar (puede ser negativa)
        """
        elem_id = store.pos_otros_elemento_id
        if not elem_id:
            return
        elem = sistema_pos.obtener(elem_id)
        if not elem:
            return
        if eje == "x":
            nuevo = elem.x + delta
            elem.x = nuevo
            store.pos_otros_posicion_actual["x"] = nuevo
        elif eje == "y":
            nuevo = elem.y + delta
            elem.y = nuevo
            store.pos_otros_posicion_actual["y"] = nuevo
        renpy.restart_interaction()

    # =========================================================================
    # FUNCIONES: Sistema de registro de sesión de posicionamiento
    # =========================================================================

    def guardar_cambio_sesion_sprite():
        """
        Guarda el estado actual del sprite seleccionado en el registro de sesión.
        Se llama desde el botón 'Guardar' de la pestaña Sprites.
        """
        import time
        if not store.sprite_posicion_actual["npc"]:
            return
        _push_undo_state()

        npc_id = store.sprite_posicion_actual["npc"]
        x_nuevo = store.sprite_posicion_actual["x"]
        y_nuevo = store.sprite_posicion_actual["y"]
        loc = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "desconocida"

        cambio = {
            "tipo": "sprite",
            "timestamp": time.strftime("%d/%m/%Y %H:%M:%S"),
            "locacion": loc,
            "id": npc_id,
            "nombre": npc_id,
            "grupo": "npc_sprite",
            "x_nuevo": x_nuevo,
            "y_nuevo": y_nuevo,
            "xanchor": 0.5,
            "yanchor": 1.0,
        }

        # Reemplazar si ya hay un cambio para este NPC en esta sesión
        for i, c in enumerate(store.pos_sesion_cambios):
            if c["tipo"] == "sprite" and c["id"] == npc_id:
                store.pos_sesion_cambios[i] = cambio
                renpy.restart_interaction()
                return
        store.pos_sesion_cambios.append(cambio)
        renpy.restart_interaction()

    def guardar_cambio_sesion_hotspot():
        """
        Guarda el estado actual del hotspot seleccionado en el registro de sesión.
        Se llama desde el botón 'Guardar' de la pestaña Hotspots.
        Aplica también los cambios al objeto real.
        """
        import time
        if not store.hotspot_posicion_actual["id"]:
            return
        _push_undo_state()

        guardar_hotspot_completo()  # Aplica cambios y agrega a hotspots_guardados (legado)

        hotspot_id = store.hotspot_posicion_actual["id"] if store.hotspot_posicion_actual["id"] else (
            store.hotspots_guardados[-1]["id"] if store.hotspots_guardados else None)
        if not hotspot_id:
            return

        loc = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "desconocida"

        # Obtener datos del último guardado (guardar_hotspot_completo ya los procesó)
        for h in reversed(store.hotspots_guardados):
            if h.get("locacion") == loc:
                cambio = {
                    "tipo": "hotspot",
                    "timestamp": time.strftime("%d/%m/%Y %H:%M:%S"),
                    "locacion": loc,
                    "id": h["id"],
                    "nombre": h.get("nombre", ""),
                    "grupo": "hotspot_" + h.get("tipo", "MOVE").lower(),
                    "tipo_hotspot": h.get("tipo", "MOVE"),
                    "destino": h.get("destino", ""),
                    "x_nuevo": h["x"],
                    "y_nuevo": h["y"],
                    "w": h["w"],
                    "h_dim": h["h"],
                }
                # Reemplazar si ya existe
                for i, c in enumerate(store.pos_sesion_cambios):
                    if c["tipo"] == "hotspot" and c["id"] == cambio["id"]:
                        store.pos_sesion_cambios[i] = cambio
                        renpy.restart_interaction()
                        return
                store.pos_sesion_cambios.append(cambio)
                renpy.restart_interaction()
                return

    def guardar_cambio_sesion_otros():
        """
        Guarda el estado actual del elemento 'Otros' seleccionado en el registro de sesión.
        Se llama desde el botón 'Guardar' de la pestaña Otros.
        """
        import time
        elem_id = store.pos_otros_posicion_actual.get("id")
        if not elem_id:
            return

        elem = sistema_pos.obtener(elem_id)
        if not elem:
            return
        _push_undo_state()

        loc = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "desconocida"
        x_nuevo = store.pos_otros_posicion_actual["x"]
        y_nuevo = store.pos_otros_posicion_actual["y"]

        cambio = {
            "tipo": "otro",
            "timestamp": time.strftime("%d/%m/%Y %H:%M:%S"),
            "locacion": loc,
            "id": elem_id,
            "nombre": elem.nombre,
            "grupo": elem.grupo,
            "imagen": elem.imagen,
            "x_original": elem.x_original,
            "y_original": elem.y_original,
            "x_nuevo": x_nuevo,
            "y_nuevo": y_nuevo,
            "xanchor": elem.xanchor,
            "yanchor": elem.yanchor,
        }

        # Actualizar posición en el elemento real
        sistema_pos.actualizar_posicion(elem_id, x_nuevo, y_nuevo)

        # Reemplazar si ya existe en la sesión
        for i, c in enumerate(store.pos_sesion_cambios):
            if c["tipo"] == "otro" and c["id"] == elem_id:
                store.pos_sesion_cambios[i] = cambio
                # Deseleccionar tras guardar
                deseleccionar_elemento_otros()
                return
        store.pos_sesion_cambios.append(cambio)
        # Deseleccionar tras guardar
        deseleccionar_elemento_otros()

    def exportar_sesion_posicionamiento():
        """
        Exporta todos los cambios de la sesión actual a un archivo .txt.
        - Crea un archivo con timestamp único para la sesión
        - Hace APPEND al historial global acumulativo
        """
        import os
        import time

        if not store.pos_sesion_cambios:
            return

        ts = time.strftime("%Y_%m_%d_%H%M%S")
        ts_legible = time.strftime("%d/%m/%Y %H:%M:%S")
        loc = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else "desconocida"
        loc_nombre = sistema_locaciones.locacion_actual.nombre if sistema_locaciones.locacion_actual else "Desconocida"

        # Separar cambios por tipo
        sprites  = [c for c in store.pos_sesion_cambios if c["tipo"] == "sprite"]
        hotspots = [c for c in store.pos_sesion_cambios if c["tipo"] == "hotspot"]
        otros    = [c for c in store.pos_sesion_cambios if c["tipo"] == "otro"]

        lineas = []
        lineas.append("# ============================================================")
        lineas.append("# REGISTRO DE POSICIONAMIENTO - {}".format(ts_legible))
        lineas.append("# Locacion: {} ({})".format(loc_nombre, loc))
        lineas.append("# Cambios confirmados: {}".format(len(store.pos_sesion_cambios)))
        lineas.append("# ============================================================")
        lineas.append("")

        if sprites:
            lineas.append("## SPRITES MODIFICADOS")
            lineas.append("# " + "\u2500" * 61)
            for c in sprites:
                lineas.append("# NPC: {}".format(c["id"]))
                lineas.append("add \"{}\" xpos {} ypos {}  # xanchor {} yanchor {}".format(
                    c["id"], c["x_nuevo"], c["y_nuevo"],
                    c.get("xanchor", 0.5), c.get("yanchor", 1.0)))
                lineas.append("")

        if hotspots:
            lineas.append("## HOTSPOTS MODIFICADOS")
            lineas.append("# " + "\u2500" * 61)
            for c in hotspots:
                lineas.append("# ID: {}  |  Tipo: {}  |  Destino: {}".format(
                    c["id"], c.get("tipo_hotspot", "MOVE"), c.get("destino", "")))
                lineas.append("Hotspot(\"{}\", \"{}\", {}, {}, {}, {}, destino=\"{}\", nombre=\"{}\")".format(
                    c["id"], c.get("tipo_hotspot", "MOVE"),
                    c["x_nuevo"], c["y_nuevo"], c.get("w", 100), c.get("h_dim", 100),
                    c.get("destino", ""), c.get("nombre", "")))
                lineas.append("")

        if otros:
            # Agrupar por grupo
            grupos_otros = {}
            for c in otros:
                g = c.get("grupo", "sin_grupo")
                if g not in grupos_otros:
                    grupos_otros[g] = []
                grupos_otros[g].append(c)

            for grupo, items in grupos_otros.items():
                lineas.append("## OTROS MODIFICADOS  (grupo: {})".format(grupo))
                lineas.append("# " + "\u2500" * 61)
                for c in items:
                    lineas.append("# ID: {}  |  Nombre: {}".format(c["id"], c.get("nombre", "")))
                    if c.get("x_original") is not None:
                        lineas.append("#   Antes: ({}, {})".format(c["x_original"], c["y_original"]))
                    lineas.append("#   Ahora:  ({}, {})  xanchor {}  yanchor {}".format(
                        c["x_nuevo"], c["y_nuevo"],
                        c.get("xanchor", 0.5), c.get("yanchor", 1.0)))
                    lineas.append("xpos {} ypos {}  # xanchor {} yanchor {}".format(
                        c["x_nuevo"], c["y_nuevo"],
                        c.get("xanchor", 0.5), c.get("yanchor", 1.0)))
                    if c.get("imagen"):
                        lineas.append("# imagen: {}".format(c["imagen"]))
                    lineas.append("")

        contenido = "\n".join(lineas)

        # Escribir archivo de sesión
        ruta_sesion = os.path.join(config.basedir, "posicionamiento_sesion_{}.txt".format(ts))
        with open(ruta_sesion, "w", encoding="utf-8") as f:
            f.write(contenido)

        # Append al historial global
        ruta_historial = os.path.join(config.basedir, "posicionamiento_historial.txt")
        with open(ruta_historial, "a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(contenido)

        # Notificar en juego
        n = len(store.pos_sesion_cambios)
        renpy.notify("Exportados {} cambio{} - {}".format(n, "s" if n != 1 else "", ts))

    def _push_undo_state():
        """
        Guarda una copia del estado actual de pos_sesion_cambios en el stack de undo.
        Llamar ANTES de cualquier operación de guardado para permitir deshacerla.
        Limita el stack a 20 estados para no consumir demasiada memoria.
        """
        import copy
        snapshot = copy.deepcopy(store.pos_sesion_cambios)
        store.pos_sesion_undo.append(snapshot)
        if len(store.pos_sesion_undo) > 20:
            store.pos_sesion_undo.pop(0)

    def deshacer_ultimo_cambio():
        """
        Deshace el último guardado, restaurando el estado previo de la sesión.
        Si el cambio era en 'Otros', también restaura la posición en sistema_pos.
        """
        if not store.pos_sesion_undo:
            return

        estado_previo = store.pos_sesion_undo.pop()

        # Identificar qué cambio se va a deshacer (el último de la lista actual)
        if store.pos_sesion_cambios:
            ultimo = store.pos_sesion_cambios[-1]
            # Restaurar posición en sistema_pos si era de tipo "otro"
            if ultimo.get("tipo") == "otro":
                x_orig = ultimo.get("x_original")
                y_orig = ultimo.get("y_original")
                if x_orig is not None:
                    sistema_pos.actualizar_posicion(ultimo["id"], x_orig, y_orig)

        store.pos_sesion_cambios = estado_previo
        renpy.restart_interaction()

    def limpiar_sesion_posicionamiento():
        """Limpia todos los cambios de la sesión actual y vacía el stack de undo."""
        store.pos_sesion_cambios = []
        store.pos_sesion_undo = []
        renpy.restart_interaction()

    def iniciar_modo_posicionamiento():
        """
        Activa el modo posicionamiento tomando snapshot de posiciones actuales.
        Llamar al activar la herramienta.
        """
        sistema_pos.tomar_snapshot()
        store.modo_posicionamiento = True
        renpy.show_screen("panel_posicionamiento_completo", _zorder=9999)
        renpy.restart_interaction()

    def cerrar_modo_posicionamiento():
        """Desactiva el modo posicionamiento y limpia selecciones."""
        store.modo_posicionamiento = False
        store.pos_otros_elemento_id = None
        store.pos_otros_posicion_actual = {"id": None, "x": 0, "y": 0, "xanchor": 0.5, "yanchor": 1.0}
        store.pos_screen_filtro = ""
        store.hotspot_seleccionado_id = None
        store.hotspot_posicion_actual = {"id": None, "x": 0, "y": 0, "w": 100, "h": 100}
        renpy.hide_screen("panel_posicionamiento_completo")
        renpy.restart_interaction()

    def obtener_tamanio_imagen_seguro(imagen):
        """
        Retorna (ancho, alto) de una imagen de forma segura.
        Intenta con renpy.image_size, fallback a (0, 0) si falla.
        Funciona con rutas de archivo y con tags de imagen Ren'Py.
        """
        try:
            return renpy.image_size(imagen)
        except Exception:
            return (0, 0)

    def calcular_top_left_desde_ancla(elem):
        """
        Dado un ElementoPosicionable, calcula la posición top-left
        para usar como xpos/ypos del drag (que no tiene anchor).
        El drag posiciona por top-left, pero el juego usa el punto de anclaje.
        """
        w, h = obtener_tamanio_imagen_seguro(elem.imagen)
        dx = int(w * elem.xanchor)
        dy = int(h * elem.yanchor)
        return (elem.x - dx, elem.y - dy)


################################################################################
## Transforms de animación para el HUD
################################################################################

# Hexágonos (día, estación): Escalan sutilmente al hover
transform hud_hex_hover:
    zoom 0.75
    on idle:
        ease 0.3 zoom 0.75
    on hover:
        ease 0.3 zoom 0.80

# Botón de horario (centro): escala sutil al hover
transform hud_horario_hover:
    zoom 0.75 alpha 1.0
    on idle:
        ease 0.2 zoom 0.75 alpha 1.0
    on hover:
        ease 0.2 zoom 0.80 alpha 1.0
    on insensitive:
        ease 0.2 alpha 0.6 zoom 0.75

# Botones de acción (cama, mochila, celu, mapa): suben al hover
transform hud_action_hover:
    zoom 0.75 yoffset 0
    on idle:
        ease 0.2 yoffset 0 zoom 0.75
    on hover:
        ease 0.2 yoffset -6 zoom 0.78

# Badge de notificaciones: bounce infinito
transform hud_badge_bounce:
    yoffset 0
    block:
        ease 0.4 yoffset -5
        ease 0.4 yoffset 0
        pause 1.0
        repeat

# Panel de entrenamiento: fade-in con slide
transform hud_panel_fadein:
    alpha 0.0 yoffset -15
    easein 0.4 alpha 1.0 yoffset 0

# Botones de entrenamiento: suben al hover
transform hud_train_hover:
    yoffset 0
    on idle:
        ease 0.15 yoffset 0
    on hover:
        ease 0.15 yoffset -4


default _hud_horario_hover = False
default _hud_estacion_hover = False

screen hud_navegacion():
    """HUD que se muestra durante la navegación por locaciones"""
    
    # Ocultar el cuadro de diálogo de Ren'Py
    $ renpy.hide_screen("say")



    # Teclas T, C, P — movidas a boton_posicionamiento_overlay
    # para que funcionen incluso con el HUD oculto

    # =========================================================================
    # CENTRO SUPERIOR - Icono de horario (click para avanzar)
    # =========================================================================
    $ _horario_imgs = {
        0: "images/hud/horario_mañana.png",
        1: "images/hud/horario_tarde.png",
        2: "images/hud/horario_noche.png",
        3: "images/hud/horario_trasnoche.png"
    }
    $ _horario_img = _horario_imgs.get(horario_actual, "images/hud/horario_mañana.png")
    $ _horario_img_next = _horario_imgs.get(horario_actual + 1, _horario_img)
    $ _horario_nombres = ["Mañana", "Tarde", "Noche", "Trasnoche"]
    $ _horario_texto_actual = renpy.translate_string(_horario_nombres[horario_actual]) if horario_actual < len(_horario_nombres) else ""
    $ _horario_texto_next = renpy.translate_string(_horario_nombres[horario_actual + 1]) if horario_actual + 1 < len(_horario_nombres) else _horario_texto_actual
    fixed:
        xalign 0.5
        yalign 0.0
        yoffset 5
        xsize 96
        ysize 96

        button:
            xysize (96, 96)
            xalign 0.5
            yalign 0.5
            action Call("accion_avanzar_tiempo")
            if horario_actual == 3:
                sensitive False
            hovered SetVariable("_hud_horario_hover", True)
            unhovered SetVariable("_hud_horario_hover", False)
            at hud_horario_hover

            fixed:
                xysize (96, 96)
                # Icono idle o siguiente en hover
                if not _hud_horario_hover:
                    add _horario_img xalign 0.5 yalign 0.5
                else:
                    add _horario_img_next xalign 0.5 yalign 0.5

                # Texto del horario centrado sobre el icono
                frame:
                    xalign 0.5
                    xoffset -5
                    yalign 0.5
                    background None
                    padding (0, 0)
                    if not _hud_horario_hover:
                        text _horario_texto_actual size 26 color "#ffffff" bold True xalign 0.5 outlines [(2, "#000000", 0, 0)]
                    else:
                        text _horario_texto_next size 26 color "#ffffff" bold True xalign 0.5 outlines [(2, "#000000", 0, 0)]


    # =========================================================================
    # SUPERIOR IZQUIERDO - Dia de la semana (capa inferior) + Estacion (capa superior)
    # =========================================================================
    $ _es_ingles = _preferences.language == "english"
    $ _dias_hud = {
        0: "images/hud/monday_hud.png" if _es_ingles else "images/hud/lunes_hud.png",
        1: "images/hud/tuesday_hud.png" if _es_ingles else "images/hud/martes_hud.png",
        2: "images/hud/wednesday_hud.png" if _es_ingles else "images/hud/miercoles_hud.png",
        3: "images/hud/thursday_hud.png" if _es_ingles else "images/hud/jueves_hud.png",
        4: "images/hud/friday_hud.png" if _es_ingles else "images/hud/viernes_hud.png",
        5: "images/hud/saturday_hud.png" if _es_ingles else "images/hud/sabado_hud.png",
        6: "images/hud/sunday_hud.png" if _es_ingles else "images/hud/domingo_hud.png"
    }
    $ _estaciones_hud = {
        0: "images/hud/primavera_hud.png",
        1: "images/hud/verano_hud.png",
        2: "images/hud/otoño_hud.png",
        3: "images/hud/invierno_hud.png"
    }

    # Capa inferior: dia de la semana (con hover scale)
    imagebutton:
        idle _dias_hud.get(dia_semana_actual, "images/hud/lunes_hud.png")
        hover _dias_hud.get(dia_semana_actual, "images/hud/lunes_hud.png")
        xalign 0.0 yalign 0.0
        action NullAction()
        at hud_hex_hover

    # Capa superior: estacion (con hover scale)
    $ _nombre_estacion = obtener_estacion()
    imagebutton:
        idle _estaciones_hud.get(estacion_actual, "images/hud/verano_hud.png")
        hover _estaciones_hud.get(estacion_actual, "images/hud/verano_hud.png")
        xalign 0.0 yalign 0.0
        action NullAction()
        hovered SetVariable("_hud_estacion_hover", True)
        unhovered SetVariable("_hud_estacion_hover", False)
        at hud_hex_hover

    # Nombre de la estacion al hacer hover
    if _hud_estacion_hover:
        text "[_nombre_estacion]":
            xpos 120
            ypos 38
            color "#ffffff"
            size 36
            bold True
    
    # =========================================================================
    # SUPERIOR DERECHO - Iconos de acceso rápido (independientes)
    # =========================================================================
    # Cada botón en su propio frame para que las animaciones no afecten a los demás
    # Imágenes originales: 128x128px, zoom 0.75 = 96x96px. Spacing: 12px
    # Posiciones desde la derecha: mapa(0), celu(108), mochila(216), cama(324)

    # Cama - Ir a mi habitación
    imagebutton:
        idle "images/hud/cama_base.png"
        hover "images/hud/cama_hover.png"
        action [SetVariable("_locacion_temp", "casa_hmc"), Call("accion_ir_a_locacion")]
        xalign 1.0 yalign 0.0
        xoffset -344 yoffset 10
        at hud_action_hover

    # Mochila - Inventario
    imagebutton:
        idle "images/hud/mochila_base.png"
        hover "images/hud/mochila_hover.png"
        action Show("panel_inventario")
        xalign 1.0 yalign 0.0
        xoffset -236 yoffset 10
        at hud_action_hover

    # Celular - Menú del celular (con badge de mensajes)
    fixed:
        xalign 1.0 yalign 0.0
        xoffset -128 yoffset 10
        xsize 96 ysize 96

        imagebutton:
            if celular_esta_bloqueado():
                action Call("pensar_mensaje", celular_esta_bloqueado())
            else:
                action [SetVariable("menu_celular_abierto", True), Show("menu_celular")]
            idle "images/hud/celu_base.png"
            hover "images/hud/celu_hover.png"
            at hud_action_hover

        $ _total_msg_sin_leer = sistema_mensajes.obtener_pendientes_total()
        if _total_msg_sin_leer > 0:
            frame:
                xalign 1.0
                yalign 0.0
                xoffset -4
                yoffset 6
                background "#FF4444"
                xsize 32 ysize 32
                padding (0, 0)
                at hud_badge_bounce
                text "[_total_msg_sin_leer]" size 20 color "#ffffff" bold True xalign 0.5 yalign 0.5

    # Mapa - Contenido en desarrollo
    imagebutton:
        idle "images/hud/mapa_base.png"
        hover "images/hud/mapa_hover.png"
        action Call("narrar_mensaje", "Contenido en desarrollo")
        xalign 1.0 yalign 0.0
        xoffset -20 yoffset 10
        at hud_action_hover
    
    # =========================================================================
    # PANEL DEBUG UNIFICADO (inferior izquierdo) - Solo visible cuando debug activo
    # =========================================================================
    if mostrar_debug_hud:
        frame:
            xalign 0.0
            yalign 1.0
            xoffset 10
            yoffset -10
            background "#2E7D32DD"
            padding (15, 10)
            
            viewport:
                xysize (320, 400)
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 4
                    xsize 300
                    
                    # --- Ubicación ---
                    text "📍 Ubicación" size 14 color "#888888"
                    
                    if sistema_locaciones.locacion_actual:
                        text "[sistema_locaciones.locacion_actual.nombre]" size 20 color "#ffffff" bold True
                        text "ID: [sistema_locaciones.locacion_actual.id]" size 11 color "#aaaaaa"
                    else:
                        text "Desconocida" size 20 color "#ffffff"
                    
                    # --- Tiempo ---
                    null height 8
                    text "DEBUG Tiempo:" size 13 color "#ffff00"
                    if hasattr(store, 'DIAS_SEMANA') and hasattr(store, 'dia_semana_actual'):
                        text "Día: [DIAS_SEMANA[dia_semana_actual]] ([dia_semana_actual])" size 11 color "#ffffff"
                    else:
                        text "Día: N/A" size 11 color "#ffffff"
                    
                    if hasattr(store, 'HORARIOS') and hasattr(store, 'horario_actual'):
                        text "Horario: [HORARIOS[horario_actual]] ([horario_actual])" size 11 color "#ffffff"
                    else:
                        text "Horario: N/A" size 11 color "#ffffff"
                    
                    text "Día del mes: [dia_actual]" size 11 color "#ffffff"
                    
                    # --- Quest ---
                    null height 8
                    text "DEBUG Quest:" size 13 color "#ffff00"
                    text "Quest actual: [quest_actual]" size 11 color "#ffffff"
                    
                    $ quest_activa = sistema_quests.obtener_quest_activa()
                    if quest_activa:
                        text "Quest activa: [quest_activa.nombre]" size 11 color "#00ff00"
                        text "Quest activa ID: [quest_activa.id]" size 11 color "#00ff00"
                    else:
                        text "Quest activa: Ninguna" size 11 color "#ffffff"
                    
                    $ quests_monica = sistema_quests.obtener_quests_disponibles("monica")
                    text "Quests disponibles Mónica: [len(quests_monica)]" size 11 color "#ffffff"
                    
                    $ pista = obtener_pista_quest()
                    if pista:
                        text "Pista: [pista['npc_nombre']] en [pista['locacion']]" size 11 color "#ffff00"
                    else:
                        text "Pista: No disponible" size 11 color "#ffffff"
                    
                    # --- Relaciones ---
                    null height 8
                    text "DEBUG Relaciones:" size 13 color "#ffff00"
                    text "Mónica: A[monica_amor] D[monica_deseo] P[monica_progreso]" size 11 color "#ffffff"
                    text "Jasmine: A[jasmine_amor] D[jasmine_deseo] P[jasmine_progreso]" size 11 color "#ffffff"
                    text "Violet: A[violet_amor] D[violet_deseo] P[violet_progreso]" size 11 color "#ffffff"
    
    # Herramientas de debug (esquina inferior derecha) - Solo visible cuando debug está activo
    if mostrar_debug_hud:
        frame:
            xalign 1.0
            yalign 1.0
            xoffset -10
            yoffset -10
            background "#4FC3F7DD"
            padding (15, 10)
            
            vbox:
                spacing 8
                
                # Botón de TEST: Crear checkpoint
                textbutton "💾 TEST Checkpoint":
                    action Jump("test_checkpoint")
                    style "hud_button"
                    text_color "#ff0000"
                
                # Botón de TEST SIMPLE
                textbutton "🔢 TEST Simple ([test_contador])":
                    action SetVariable("test_contador", test_contador + 1)
                    style "hud_button"
                    text_color "#00ff00"
                
                null height 5
                
                # Botón para modo posicionamiento
                $ pos_btn_color = "#00ff00" if modo_posicionamiento else "#ffffff"
                textbutton ("📐 Posicionar [[ON]]" if modo_posicionamiento else "📐 Posicionar"):
                    action (Function(cerrar_modo_posicionamiento) if modo_posicionamiento else Function(iniciar_modo_posicionamiento))
                    style "hud_button"
                    text_color pos_btn_color
                
                # Botón para saltar a labels de quests/events
                textbutton "🎯 Saltar a Label":
                    action Show("panel_debug_labels")
                    style "hud_button"
                    text_color "#FFD700"

                # Botón para completar quests
                textbutton "📋 Completar Quest":
                    action Show("menu_completar_quests")
                    style "hud_button"
                    text_color "#FFD700"

################################################################################
## Panel de Debug: Salto a Labels
################################################################################

screen panel_debug_labels():
    """Panel para saltar directamente a labels de quests y eventos."""
    
    modal True
    
    # Fondo semi-transparente
    add Solid("#000000AA")
    
    # Panel central
    frame:
        xalign 0.5
        yalign 0.5
        xysize (500, 600)
        background "#1E1E1EEE"
        padding (20, 20)
        
        vbox:
            spacing 10
            xfill True
            
            # Header
            hbox:
                xfill True
                text "🎯 Saltar a Label" size 24 color "#FFD700" bold True
                textbutton "✕ Cerrar":
                    action Hide("panel_debug_labels")
                    xalign 1.0
                    text_size 16
                    text_color "#FF5722"
                    background None
            
            null height 10
            
            # Contenido scrollable
            viewport:
                xysize (460, 500)
                scrollbars "vertical"
                mousewheel True
                
                vbox:
                    spacing 8
                    xsize 440
                    
                    # === SECCIÓN QUESTS ===
                    text "📜 QUESTS" size 18 color "#4CAF50" bold True
                    null height 5
                    
                    # Obtener quests del sistema
                    for quest_id, quest in sistema_quests.quests.items():
                        $ estado_icon = "✅" if quest.completada else ("▶️" if quest.activa else "⬜")
                        $ label_name = quest.label_quest
                        
                        hbox:
                            spacing 5
                            xfill True
                            
                            text estado_icon size 14
                            
                            textbutton "[quest.npc_id.capitalize()]: [quest.nombre]":
                                action [Hide("panel_debug_labels"), Hide("navegacion_locaciones_con_hud"), Hide("hud_navegacion"), Jump(label_name)]
                                text_size 14
                                text_color "#FFFFFF"
                                background "#333333"
                                hover_background "#4CAF50"
                                padding (8, 4)
                                xsize 380
                    
                    null height 15
                    
                    # === SECCIÓN EVENTS ===
                    text "⚡ EVENTS" size 18 color "#2196F3" bold True
                    null height 5
                    
                    # Obtener events del sistema
                    for event_id, event in sistema_events.events.items():
                        if event.label_efecto:
                            $ estado_icon = "✅" if event.estado == ESTADO_EVENT_COMPLETADO else ("▶️" if event.estado == ESTADO_EVENT_ACTIVO else "⬜")
                            $ label_name = event.label_efecto
                            
                            hbox:
                                spacing 5
                                xfill True
                                
                                text estado_icon size 14
                                
                                textbutton "[event.nombre]":
                                    action [Hide("panel_debug_labels"), Hide("navegacion_locaciones_con_hud"), Hide("hud_navegacion"), Jump(label_name)]
                                    text_size 14
                                    text_color "#FFFFFF"
                                    background "#333333"
                                    hover_background "#2196F3"
                                    padding (8, 4)
                                    xsize 380

                    null height 15

                    # === SECCIÓN LABELS ESPECIALES ===
                    text "🔧 LABELS ESPECIALES" size 18 color "#FF9800" bold True
                    null height 5

                    for _label_info in _debug_labels_especiales:
                        $ _sl_nombre = _label_info["nombre"]
                        $ _sl_label = _label_info["label"]

                        hbox:
                            spacing 5
                            xfill True

                            text "🔹" size 14

                            textbutton "[_sl_nombre]":
                                action [Hide("panel_debug_labels"), Hide("navegacion_locaciones_con_hud"), Hide("hud_navegacion"), Jump(_sl_label)]
                                text_size 14
                                text_color "#FFFFFF"
                                background "#333333"
                                hover_background "#FF9800"
                                padding (8, 4)
                                xsize 380


################################################################################
## Screen de animación de dormir
################################################################################

screen animacion_dormir():
    """Animación que se muestra al dormir"""
    
    # Bloquear interacción con elementos de fondo
    modal True
    
    # Timer para cerrar automáticamente la pantalla y retornar
    timer 2.0 action Return()
    
    # Fondo negro con fade
    add Solid("#000000")
    
    # Texto central
    frame:
        xalign 0.5
        yalign 0.5
        background None
        
        vbox:
            spacing 20
            xalign 0.5
            
            text "💤" size 80 xalign 0.5
            text _("Durmiendo...") size 40 color "#ffffff" xalign 0.5
            text "Zzz..." size 30 color "#888888" xalign 0.5

################################################################################
## Estilos para el HUD
################################################################################

style hud_button is button:
    background "#0288D1"  # Azul profundo veraniego
    hover_background "#FFB74D"  # Naranja atardecer al hover
    padding (12, 8)
    
style hud_button_text is button_text:
    size 18
    color "#FFFFFF"
    hover_color "#5D4037"  # Marrón al hover para contraste
    bold True

################################################################################
## Screen de navegación actualizado con HUD
################################################################################

screen navegacion_locaciones_con_hud():
    """Screen de navegación con HUD integrado"""

    # Sin modal — se usa un boton fullscreen dentro del if para capturar clicks
    # Esto permite que cuando el contenido esta oculto, los clicks pasen al say/otros screens

    # Teclas de debug desactivadas para build de release

    # Contenido visual del HUD (se oculta con ocultar_hud())
    if hud_contenido_visible and sistema_locaciones.locacion_actual:
        # Boton fullscreen invisible — captura clicks en areas sin interaccion (reemplaza modal)
        button:
            xpos 0
            ypos 0
            xsize 1920
            ysize 1080
            background None
            action NullAction()

        # Obtener NPCs presentes (necesario antes de hotspots y sprites)
        $ npcs_aqui = npcs_en_locacion_actual()
        
        # =====================================================================
        # CAPA 1: Hotspots interactivos (se renderizan primero, quedan detrás)
        # =====================================================================
        
        # En modo posicionamiento de hotspots, usar draggroup para hotspots arrastrables
        if modo_posicionamiento and modo_posicionamiento_tipo == "hotspots":
            # Filtrar hotspots según el sub-filtro: MOVE, ACTION o TODOS
            if pos_hotspot_tipo_filtro == "TODOS":
                $ hotspots_filtrados = sistema_locaciones.locacion_actual.obtener_hotspots_habilitados()
            else:
                $ hotspots_filtrados = [h for h in sistema_locaciones.locacion_actual.obtener_hotspots_habilitados() if h.tipo == pos_hotspot_tipo_filtro]
            
            draggroup:
                for hotspot in hotspots_filtrados:
                    # Determinar posición y tamaño (usa valores editados si está seleccionado)
                    $ h_x = hotspot_posicion_actual["x"] if hotspot.id == hotspot_seleccionado_id else hotspot.x
                    $ h_y = hotspot_posicion_actual["y"] if hotspot.id == hotspot_seleccionado_id else hotspot.y
                    $ h_w = hotspot_posicion_actual["w"] if hotspot.id == hotspot_seleccionado_id else hotspot.w
                    $ h_h = hotspot_posicion_actual["h"] if hotspot.id == hotspot_seleccionado_id else hotspot.h
                    $ is_selected = hotspot.id == hotspot_seleccionado_id
                    $ hotspot_name = hotspot.nombre if hotspot.nombre else hotspot.id
                    
                    # Hotspot arrastrable con visualización
                    drag:
                        drag_name hotspot.id
                        xpos h_x
                        ypos h_y
                        xysize (h_w, h_h)
                        draggable True
                        droppable False
                        dragged actualizar_posicion_hotspot
                        clicked Function(seleccionar_hotspot, hotspot)
                        
                        # Visualización del hotspot: fondo semi-transparente con texto
                        frame:
                            xysize (h_w, h_h)
                            padding (0, 0)
                            
                            # Fondo según estado: dorado seleccionado, azul MOVE, verde ACTION
                            if is_selected:
                                background "#FFD70088"  # Dorado para seleccionado
                            elif hotspot.tipo == "MOVE":
                                background "#2196F366"  # Azul para MOVE
                            else:
                                background "#4CAF5066"  # Verde para ACTION
                            
                            # Nombre del hotspot centrado
                            text hotspot_name:
                                size 14
                                color "#FFFFFF"
                                outlines [(2, "#000000", 0, 0)]
                                xalign 0.5
                                yalign 0.5
            
            # Panel lateral izquierdo: Lista de hotspots de la locación
            frame:
                xpos 10
                ypos 180
                xysize (180, 200)
                background "#1E1E1ECC"
                padding (8, 8)
                
                vbox:
                    spacing 4
                    xsize 164
                    
                    # Título con filtro activo
                    text "📋 Hotspots ([pos_hotspot_tipo_filtro]):" size 11 color "#FFD700" bold True
                    
                    # Lista scrollable de hotspots (filtrada por tipo)
                    viewport:
                        xysize (164, 150)
                        scrollbars "vertical"
                        mousewheel True
                        
                        vbox:
                            spacing 3
                            xsize 150
                            
                            for hotspot in hotspots_filtrados:
                                $ h_bg = "#FFD70044" if hotspot.id == hotspot_seleccionado_id else "#33333388"
                                $ h_tipo_icon = "🚪" if hotspot.tipo == "MOVE" else "⚡"
                                
                                hbox:
                                    spacing 3
                                    
                                    frame:
                                        background h_bg
                                        padding (4, 2)
                                        xsize 120
                                        
                                        hbox:
                                            spacing 3
                                            text h_tipo_icon size 10
                                            text hotspot.id size 10 color "#FFFFFF"
                                    
                                    # Botón centrar
                                    textbutton "📍":
                                        action Function(centrar_hotspot_en_pantalla, hotspot)
                                        text_size 10
                                        background "#2196F3"
                                        hover_background "#64B5F6"
                                        padding (4, 2)
            
            # Panel selector de locaciones destino (cuando modo_crear_hotspot está activo)
            if modo_crear_hotspot:
                frame:
                    xpos 1700
                    ypos 300
                    xysize (200, 380)
                    background "#1E1E1EEE"
                    padding (8, 8)
                    
                    vbox:
                        spacing 4
                        xsize 184
                        
                        hbox:
                            spacing 5
                            text "✏️ Nombre:" size 11 color "#FFD700" bold True
                            textbutton "✕":
                                action SetVariable("modo_crear_hotspot", False)
                                text_size 10
                                background "#F44336"
                                padding (4, 2)
                        
                        # Input para nombre del hotspot
                        input:
                            value VariableInputValue("hotspot_nuevo_nombre")
                            size 12
                            color "#FFFFFF"
                            pixel_width 170
                        
                        null height 5
                        text "🎯 Destino:" size 11 color "#FFD700" bold True
                        
                        # Lista scrollable de locaciones
                        viewport:
                            xysize (184, 260)
                            scrollbars "vertical"
                            mousewheel True
                            
                            vbox:
                                spacing 2
                                xsize 170
                                
                                $ lista_locs = obtener_lista_locaciones()
                                for loc_id in lista_locs:
                                    $ loc_obj = sistema_locaciones.obtener_locacion(loc_id)
                                    $ loc_nombre = loc_obj.nombre if loc_obj else loc_id
                                    $ is_dest = hotspot_nuevo_datos.get("destino", "") == loc_id
                                    $ loc_bg = "#4CAF5088" if is_dest else "#33333388"
                                    
                                    textbutton "[loc_nombre]":
                                        action [Function(actualizar_destino_hotspot, loc_id), SetVariable("modo_crear_hotspot", False)]
                                        text_size 10
                                        background loc_bg
                                        hover_background "#66BB6A"
                                        padding (4, 2)
                                        xsize 170
        else:
            for hotspot in sistema_locaciones.locacion_actual.obtener_hotspots_habilitados():
                
                # Calcular nombre destino para hotspots MOVE (antes del button)
                $ loc_destino = sistema_locaciones.obtener_locacion(hotspot.destino) if hotspot.tipo == "MOVE" else None
                $ nombre_destino = renpy.translate_string(loc_destino.nombre) if loc_destino else (hotspot.destino if hotspot.tipo == "MOVE" else "")
                # Crear dict con info del hotspot para mostrar mensaje en su posición
                $ hover_info = {"nombre": nombre_destino, "x": hotspot.x, "y": hotspot.y, "w": hotspot.w, "h": hotspot.h}
                
                # Área clickeable del hotspot
                button:
                    xpos hotspot.x
                    ypos hotspot.y
                    xysize (hotspot.w, hotspot.h)
                    background None
                    hover_background None

                    # Bloquear acciones mientras la herramienta de posicionamiento esté activa
                    if modo_posicionamiento:
                        action NullAction()
                    elif hotspot.tipo == "MOVE":
                        action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_move")]
                        # Al hacer hover, guardar info del destino y posición
                        hovered SetVariable("hover_destino_locacion", hover_info)
                        unhovered SetVariable("hover_destino_locacion", None)
                    elif hotspot.tipo == "ACTION":
                        action [SetVariable("_hotspot_temp", hotspot), Call("accion_hotspot_action")]

                    if hotspot.nombre:
                        tooltip renpy.translate_string(hotspot.nombre)
                    else:
                        tooltip hotspot.id
        
        # =====================================================================
        # CAPA 2: Sprites de NPCs (se renderizan después, quedan arriba)
        # =====================================================================

        # Timer que revela los NPCs al terminar la transicion del bg
        if hud_npc_delay_horario:
            timer 1.5 action SetVariable("hud_npc_delay_horario", False)

        if npcs_aqui and not hud_npc_delay_horario:
            # Obtener posiciones para los NPCs
            $ posiciones = obtener_posiciones_npcs(len(npcs_aqui))
            
            # Modo posicionamiento de SPRITES: usar draggroup para sprites arrastrables
            if modo_posicionamiento and modo_posicionamiento_tipo == "sprites":
                draggroup:
                    for i, npc in enumerate(npcs_aqui):
                        # Determinar sprite y posición
                        if npc.id == "monica":
                            $ sprite_actual = obtener_sprite_rutina_monica()
                            $ posicion_rutina = obtener_posicion_rutina_monica()
                            if not sprite_actual:
                                $ sprite_actual = npc.sprite
                            if posicion_rutina:
                                $ pos_x = posicion_rutina[0]
                                $ pos_y = posicion_rutina[1]
                            elif i < len(posiciones):
                                $ pos = posiciones[i]
                                $ pos_x = int(pos[0] * 1920)
                                $ pos_y = 1080
                            else:
                                $ pos_x = 960
                                $ pos_y = 1080
                        elif npc.id == "violet":
                            $ sprite_actual = obtener_sprite_rutina_violet()
                            $ posicion_rutina = obtener_posicion_rutina_violet()
                            if not sprite_actual:
                                $ sprite_actual = npc.sprite
                            if posicion_rutina:
                                $ pos_x = posicion_rutina[0]
                                $ pos_y = posicion_rutina[1]
                            elif i < len(posiciones):
                                $ pos = posiciones[i]
                                $ pos_x = int(pos[0] * 1920)
                                $ pos_y = 1080
                            else:
                                $ pos_x = 960
                                $ pos_y = 1080
                        elif npc.id == "jasmine":
                            $ sprite_actual = obtener_sprite_rutina_jasmine()
                            $ posicion_rutina = obtener_posicion_rutina_jasmine()
                            if not sprite_actual:
                                $ sprite_actual = npc.sprite
                            if posicion_rutina:
                                $ pos_x = posicion_rutina[0]
                                $ pos_y = posicion_rutina[1]
                            elif i < len(posiciones):
                                $ pos = posiciones[i]
                                $ pos_x = int(pos[0] * 1920)
                                $ pos_y = 1080
                            else:
                                $ pos_x = 960
                                $ pos_y = 1080
                        else:
                            $ sprite_actual = npc.sprite
                            if i < len(posiciones):
                                $ pos = posiciones[i]
                                $ pos_x = int(pos[0] * 1920)
                                $ pos_y = 1080
                            else:
                                $ pos_x = 960
                                $ pos_y = 1080
                        
                        if sprite_actual:
                            # Sprite arrastrable
                            drag:
                                drag_name npc.id
                                xpos pos_x
                                ypos pos_y
                                xanchor 0.5
                                yanchor 1.0
                                draggable True
                                droppable False
                                dragged actualizar_posicion_sprite
                                
                                # Sprite a escala original con borde de selección
                                fixed:
                                    fit_first True
                                    
                                    add sprite_actual
                                    
                                    # Borde visual para indicar modo arrastrable
                                    add Solid("#00ff0044")
            else:
                # Modo normal: sprites estáticos
                # Filtrar NPCs ocultos por restricción de quest/evento
                $ _npcs_visibles = [n for n in npcs_aqui if not npc_esta_oculto(n.id)]
                for i, npc in enumerate(_npcs_visibles):
                    # Determinar sprite y posición (rutina específica o default)
                    if npc.id == "monica":
                        # Prioridad 1: Sprite de quest activa
                        $ sprite_actual = obtener_sprite_quest_npc("monica")
                        $ posicion_rutina = obtener_posicion_quest_npc("monica")
                        
                        # Prioridad 2: Sprite de rutina visual
                        if not sprite_actual:
                            $ sprite_actual = obtener_sprite_rutina_monica()
                            $ posicion_rutina = obtener_posicion_rutina_monica()
                        
                        # Fallback al sprite default si no hay rutina visual
                        if not sprite_actual:
                            $ sprite_actual = npc.sprite
                        
                        # Usar posición de rutina o calcular posición default
                        if posicion_rutina:
                            $ pos_x = posicion_rutina[0]
                            $ pos_y = posicion_rutina[1]
                        elif i < len(posiciones):
                            $ pos = posiciones[i]
                            $ pos_x = int(pos[0] * 1920)
                            $ pos_y = 1080
                        else:
                            $ pos_x = 960
                            $ pos_y = 1080
                    elif npc.id == "violet":
                        # Prioridad 1: Sprite de quest activa
                        $ sprite_actual = obtener_sprite_quest_npc("violet")
                        $ posicion_rutina = obtener_posicion_quest_npc("violet")
                        
                        # Prioridad 2: Sprite de rutina visual
                        if not sprite_actual:
                            $ sprite_actual = obtener_sprite_rutina_violet()
                            $ posicion_rutina = obtener_posicion_rutina_violet()
                        
                        # Fallback al sprite default si no hay rutina visual
                        if not sprite_actual:
                            $ sprite_actual = npc.sprite
                        
                        # Usar posición de rutina o calcular posición default
                        if posicion_rutina:
                            $ pos_x = posicion_rutina[0]
                            $ pos_y = posicion_rutina[1]
                        elif i < len(posiciones):
                            $ pos = posiciones[i]
                            $ pos_x = int(pos[0] * 1920)
                            $ pos_y = 1080
                        else:
                            $ pos_x = 960
                            $ pos_y = 1080
                    elif npc.id == "jasmine":
                        # Prioridad 1: Sprite de quest activa
                        $ sprite_actual = obtener_sprite_quest_npc("jasmine")
                        $ posicion_rutina = obtener_posicion_quest_npc("jasmine")
                        
                        # Prioridad 2: Sprite de rutina visual
                        if not sprite_actual:
                            $ sprite_actual = obtener_sprite_rutina_jasmine()
                            $ posicion_rutina = obtener_posicion_rutina_jasmine()
                        
                        # Fallback al sprite default si no hay rutina visual
                        if not sprite_actual:
                            $ sprite_actual = npc.sprite
                        
                        # Usar posición de rutina o calcular posición default
                        if posicion_rutina:
                            $ pos_x = posicion_rutina[0]
                            $ pos_y = posicion_rutina[1]
                        elif i < len(posiciones):
                            $ pos = posiciones[i]
                            $ pos_x = int(pos[0] * 1920)
                            $ pos_y = 1080
                        else:
                            $ pos_x = 960
                            $ pos_y = 1080
                    else:
                        # NPCs sin rutina visual: usar sprite y posición default
                        $ sprite_actual = npc.sprite
                        if i < len(posiciones):
                            $ pos = posiciones[i]
                            $ pos_x = int(pos[0] * 1920)
                            $ pos_y = 1080
                        else:
                            $ pos_x = 960
                            $ pos_y = 1080
                    
                    if sprite_actual:
                        # Imagebutton: el área clickeable coincide con el tamaño del sprite
                        imagebutton:
                            idle sprite_actual
                            hover sprite_actual
                            xpos pos_x
                            ypos pos_y
                            xanchor 0.5  # Centrar horizontalmente
                            yanchor 1.0  # Alinear desde la parte inferior
                            mouse "hand"
                            # Bloquear interacción mientras la herramienta de posicionamiento esté activa
                            if modo_posicionamiento:
                                action NullAction()
                            elif npc_interactuable(npc.id):
                                action Call("interaccion_" + npc.id)
                            else:
                                action Call("pensar_mensaje", mensaje_npc_bloqueado())
        
        # =====================================================================
        # CAPA 2.5: Elementos dinámicos de quest/evento
        # =====================================================================
        if hay_restriccion_activa() and sistema_locaciones.locacion_actual:
            $ _elems_quest = obtener_elementos_escena(sistema_locaciones.locacion_actual.id)
            for _elem in _elems_quest:
                if _elem.get("tipo") == "imagebutton":
                    imagebutton:
                        idle _elem["imagen"]
                        hover _elem["imagen"]
                        xpos _elem["pos"][0]
                        ypos _elem["pos"][1]
                        if _elem.get("anchor"):
                            xanchor _elem["anchor"][0]
                            yanchor _elem["anchor"][1]
                        mouse "hand"
                        # En modo posicionamiento no ejecutar el label (para poder arrastrar)
                        if modo_posicionamiento:
                            action NullAction()
                        else:
                            action Call(_elem["label"])
        
        # =====================================================================
        # CAPA 3: Elementos "Otros" del sistema_pos — modo normal (idles, props)
        # NOTA: el drag de posicionamiento se gestiona en boton_posicionamiento_overlay
        # (zorder 200) para funcionar incluso dentro de screens de quest.
        # =====================================================================

        # Repartidor en frente de la casa (mañana de entrega)
        if repartidor_presente and sistema_locaciones.locacion_actual.id == "casa_frente":
            $ _rep = sistema_pos.obtener("casa_frente_repartidor")
            $ _rep_x = _rep.x if _rep else 1270
            $ _rep_y = _rep.y if _rep else 540
            imagebutton:
                idle "idle_repartidor_puerta"
                hover "idle_repartidor_puerta"
                xpos _rep_x
                ypos _rep_y
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action Jump("interaccion_repartidor")

        # Paquete en la habitación del MC (entrega perdida)
        if paquete_en_habitacion and sistema_locaciones.locacion_actual.id == "casa_hmc":
            $ _paq = sistema_pos.obtener("casa_hmc_paquete")
            $ _paq_x = _paq.x if _paq else 1000
            $ _paq_y = _paq.y if _paq else 530
            imagebutton:
                idle "idle_paquete_hmc"
                hover "idle_paquete_hmc"
                xpos _paq_x
                ypos _paq_y
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action Jump("recoger_paquete_habitacion")
        
        # Debug info unificado en el panel inferior izquierdo del HUD
        # (se eliminó el panel superpuesto aquí para evitar conflicto con el panel de fecha)
        
        # Panel de coordenadas para modo posicionamiento
        use panel_posicionamiento_completo
    
    if hud_contenido_visible:
        # Mostrar panel de entrenamiento si estamos en la habitación del MC
        use panel_entrenamiento

        # =====================================================================
        # Preview de destino al hacer hover sobre hotspots de movimiento
        # =====================================================================
        if hover_destino_locacion:
            # Calcular posición centrada dentro del hotspot
            $ preview_x = hover_destino_locacion["x"] + hover_destino_locacion["w"] // 2
            $ preview_y = hover_destino_locacion["y"] + hover_destino_locacion["h"] // 2

            frame:
                xpos preview_x
                ypos preview_y
                xanchor 0.5
                yanchor 0.5
                background "#0288D1EE"
                padding (25, 12)

                text hover_destino_locacion["nombre"] size 28 color "#FFFFFF" bold True outlines [(2, "#1565C0", 0, 0)]

        # Mostrar el HUD
        use hud_navegacion

################################################################################
## Labels de control actualizados
################################################################################

# Este label ya no se usa - el loop principal está en intro.rpy
# Se mantiene por compatibilidad pero redirige al loop principal
label iniciar_navegacion_con_hud:
    jump game_loop


################################################################################
## Screen overlay permanente — Botón de posicionamiento
## Siempre visible, incluso dentro de screens de quest
################################################################################

init python:
    if "boton_posicionamiento_overlay" not in config.overlay_screens:
        config.overlay_screens.append("boton_posicionamiento_overlay")

screen boton_posicionamiento_overlay():
    zorder 300  # Por encima de todo, incluyendo screens de quest

    # Teclas de debug ahora viven en navegacion_locaciones_con_hud (siempre activo)

    # ─── Elementos del screen seleccionado visibles en pantalla ──────────────
    # Cuando la pestaña Screen está activa y hay un screen seleccionado,
    # muestra TODOS sus elementos en sus posiciones reales.
    # Click para seleccionar, drag en el seleccionado.
    if modo_posicionamiento and modo_posicionamiento_tipo == "screen" and pos_screen_filtro:
        $ _ov_elems = sistema_pos.obtener_por_screen(pos_screen_filtro)

        draggroup:
            for _ov_elem in _ov_elems:
                $ _ov_tl = calcular_top_left_desde_ancla(_ov_elem)
                $ _ov_es_sel = (_ov_elem.id == pos_otros_elemento_id)
                $ _ov_bg = "#E65100CC" if _ov_es_sel else "#33333388"
                $ _ov_txt_color = "#ffffff" if _ov_es_sel else "#aaaaaa"
                $ _ov_txt_size = 11 if _ov_es_sel else 10

                drag:
                    drag_name _ov_elem.id
                    pos (_ov_tl[0], _ov_tl[1])
                    draggable True
                    droppable False
                    dragged actualizar_posicion_otros
                    clicked Function(seleccionar_elemento_otros, _ov_elem.id)

                    frame:
                        background _ov_bg
                        padding (3, 3)
                        vbox:
                            spacing 2
                            add _ov_elem.imagen
                            text "[_ov_elem.nombre]" size _ov_txt_size color _ov_txt_color xalign 0.5

    # Solo visible en modo debug
    if mostrar_debug_hud:

        # Botón toggle — esquina inferior derecha
        frame:
            xalign 1.0
            yalign 1.0
            xoffset -20
            yoffset -20
            background None
            
            $ _pos_color = "#00ff00" if modo_posicionamiento else "#cccccc"
            textbutton ("📐 [[ON]]" if modo_posicionamiento else "📐 Posicionar"):
                action (Function(cerrar_modo_posicionamiento) if modo_posicionamiento else Function(iniciar_modo_posicionamiento))
                text_size 15
                text_color _pos_color
                background ("#1a1a1aCC" if not modo_posicionamiento else "#1a3a1aCC")
                hover_background "#2a2a2aCC"
                padding (12, 8)


################################################################################
## Sub-screen: Panel de posicionamiento — Barra superior horizontal
################################################################################

screen panel_posicionamiento_completo():
    zorder 9999
    modal False

    if modo_posicionamiento:
        frame:
            xpos 0
            ypos 0
            xsize 1920
            ysize 100
            background "#1A1A2EF0"
            padding (10, 5)

            hbox:
                spacing 8
                yalign 0.5

                # ─── COL 1: Titulo + Tabs ────────────────────────────────
                vbox:
                    spacing 3
                    yalign 0.5
                    xsize 160

                    text "📐 POSICIONAR" size 12 color "#ffffff" bold True

                    $ _tab_sprites  = "#4CAF50" if modo_posicionamiento_tipo == "sprites"  else "#333333"
                    $ _tab_hotspots = "#2196F3" if modo_posicionamiento_tipo == "hotspots" else "#333333"
                    $ _tab_screen   = "#FF9800" if modo_posicionamiento_tipo == "screen"   else "#333333"

                    hbox:
                        spacing 3
                        textbutton "Sprites":
                            action SetVariable("modo_posicionamiento_tipo", "sprites")
                            text_size 10 background _tab_sprites padding (6, 3)
                        textbutton "Hotspots":
                            action SetVariable("modo_posicionamiento_tipo", "hotspots")
                            text_size 10 background _tab_hotspots padding (6, 3)
                        textbutton "Screen":
                            action SetVariable("modo_posicionamiento_tipo", "screen")
                            text_size 10 background _tab_screen padding (6, 3)

                # Separador vertical
                frame:
                    xsize 1
                    ysize 80
                    yalign 0.5
                    background "#444444"

                # ─── COL 2: Contenido de la pestaña activa ───────────────

                # ═══ SPRITES ═══
                if modo_posicionamiento_tipo == "sprites":
                    $ _spr_npc = sprite_posicion_actual["npc"]
                    $ _spr_guardado = any(c["tipo"] == "sprite" and c["id"] == _spr_npc for c in pos_sesion_cambios) if _spr_npc else False

                    hbox:
                        spacing 12
                        yalign 0.5

                        vbox:
                            spacing 1
                            text "NPC" size 10 color "#90CAF9"
                            if _spr_npc:
                                text "[_spr_npc]" size 14 color "#ffffff" bold True
                            else:
                                text "(arrastra)" size 11 color "#666666"

                        vbox:
                            spacing 1
                            text "X" size 10 color "#90CAF9"
                            text "[sprite_posicion_actual['x']]" size 16 color "#00E676" bold True

                        vbox:
                            spacing 1
                            text "Y" size 10 color "#90CAF9"
                            text "[sprite_posicion_actual['y']]" size 16 color "#00E676" bold True

                        if _spr_npc:
                            vbox:
                                spacing 2
                                yalign 0.5
                                frame:
                                    background "#0D1117CC"
                                    padding (6, 3)
                                    text "xpos [sprite_posicion_actual['x']] ypos [sprite_posicion_actual['y']]" size 10 color "#E6DB74"
                                textbutton ("💾 Actualizar" if _spr_guardado else "💾 Guardar"):
                                    action Function(guardar_cambio_sesion_sprite)
                                    text_size 11
                                    background ("#1565C0" if _spr_guardado else "#2E7D32")
                                    hover_background ("#1976D2" if _spr_guardado else "#4CAF50")
                                    padding (8, 3)

                # ═══ HOTSPOTS ═══
                elif modo_posicionamiento_tipo == "hotspots":
                    $ _hs_id = hotspot_posicion_actual["id"]
                    $ _hs_guardado = any(c["tipo"] == "hotspot" and c["id"] == _hs_id for c in pos_sesion_cambios) if _hs_id else False

                    hbox:
                        spacing 8
                        yalign 0.5

                        # Filtro tipo
                        vbox:
                            spacing 2
                            $ _fmove   = "#0288D1" if pos_hotspot_tipo_filtro == "MOVE"   else "#333333"
                            $ _faction = "#43A047" if pos_hotspot_tipo_filtro == "ACTION" else "#333333"
                            $ _ftodos  = "#7B1FA2" if pos_hotspot_tipo_filtro == "TODOS"  else "#333333"
                            hbox:
                                spacing 2
                                textbutton "MOVE":
                                    action SetVariable("pos_hotspot_tipo_filtro", "MOVE")
                                    text_size 9 background _fmove padding (5, 2)
                                textbutton "ACTION":
                                    action SetVariable("pos_hotspot_tipo_filtro", "ACTION")
                                    text_size 9 background _faction padding (5, 2)
                                textbutton "TODOS":
                                    action SetVariable("pos_hotspot_tipo_filtro", "TODOS")
                                    text_size 9 background _ftodos padding (5, 2)

                        # ID + coords
                        vbox:
                            spacing 1
                            text "Hotspot" size 10 color "#90CAF9"
                            if _hs_id:
                                text "[_hs_id]" size 11 color "#ffffff" bold True
                            else:
                                text "(selecciona)" size 10 color "#666666"

                        vbox:
                            spacing 1
                            text "X" size 10 color "#90CAF9"
                            text "[hotspot_posicion_actual['x']]" size 14 color "#00E676" bold True

                        vbox:
                            spacing 1
                            text "Y" size 10 color "#90CAF9"
                            text "[hotspot_posicion_actual['y']]" size 14 color "#00E676" bold True

                        # W/H
                        vbox:
                            spacing 1
                            text "W" size 10 color "#90CAF9"
                            hbox:
                                spacing 2
                                textbutton "-10":
                                    action Function(modificar_dimension_hotspot, "w", -10)
                                    text_size 9 background "#C62828" padding (4, 2)
                                text "[hotspot_posicion_actual['w']]" size 12 color "#00E676" bold True yalign 0.5
                                textbutton "+10":
                                    action Function(modificar_dimension_hotspot, "w", 10)
                                    text_size 9 background "#2E7D32" padding (4, 2)

                        vbox:
                            spacing 1
                            text "H" size 10 color "#90CAF9"
                            hbox:
                                spacing 2
                                textbutton "-10":
                                    action Function(modificar_dimension_hotspot, "h", -10)
                                    text_size 9 background "#C62828" padding (4, 2)
                                text "[hotspot_posicion_actual['h']]" size 12 color "#00E676" bold True yalign 0.5
                                textbutton "+10":
                                    action Function(modificar_dimension_hotspot, "h", 10)
                                    text_size 9 background "#2E7D32" padding (4, 2)

                        # Botones
                        vbox:
                            spacing 2
                            yalign 0.5
                            hbox:
                                spacing 3
                                textbutton "🔄 Aplicar":
                                    action Function(aplicar_cambios_hotspot)
                                    text_size 10 background "#7B1FA2" padding (6, 3)
                                textbutton ("💾 Act." if _hs_guardado else "💾 Guardar"):
                                    action Function(guardar_cambio_sesion_hotspot)
                                    text_size 10
                                    background ("#1565C0" if _hs_guardado else "#2E7D32")
                                    padding (6, 3)
                                textbutton "➕ Nuevo":
                                    action Function(crear_hotspot_nuevo)
                                    text_size 10 background "#0277BD" padding (6, 3)

                # ═══ SCREEN ═══
                elif modo_posicionamiento_tipo == "screen":

                    hbox:
                        spacing 8
                        yalign 0.5

                        # Lista de screens disponibles
                        vbox:
                            spacing 2
                            xsize 340

                            hbox:
                                spacing 3
                                text "Screen:" size 10 color "#90CAF9" yalign 0.5

                            $ _screens_disp = sistema_pos.obtener_screens_disponibles()

                            if _screens_disp:
                                viewport:
                                    xysize (340, 55)
                                    scrollbars "vertical"
                                    mousewheel True

                                    vbox:
                                        spacing 2
                                        xsize 320
                                        for _sid in _screens_disp:
                                            $ _s_sel = (_sid == pos_screen_filtro)
                                            $ _s_bg = "#E65100AA" if _s_sel else "#1E1E1E99"
                                            $ _s_count = len(sistema_pos.obtener_por_screen(_sid))
                                            textbutton "[_sid] ([_s_count])":
                                                action SetVariable("pos_screen_filtro", _sid)
                                                text_size 10
                                                text_color ("#FFD700" if _s_sel else "#ffffff")
                                                background _s_bg
                                                padding (4, 2)
                                                xsize 320

                        # Separador
                        frame:
                            xsize 1
                            ysize 80
                            yalign 0.5
                            background "#444444"

                        # Coordenadas del elemento seleccionado
                        if pos_otros_posicion_actual["id"]:
                            $ _eid = pos_otros_posicion_actual["id"]
                            $ _eobj = sistema_pos.obtener(_eid)

                            vbox:
                                spacing 2
                                yalign 0.5

                                hbox:
                                    spacing 6
                                    text "[_eid]" size 11 color "#ffffff" bold True yalign 0.5
                                    if _eobj:
                                        text "([_eobj.screen])" size 9 color "#aaaaaa" yalign 0.5

                                # X
                                hbox:
                                    spacing 2
                                    yalign 0.5
                                    text "X" size 10 color "#90CAF9" yalign 0.5
                                    textbutton "-10":
                                        action Function(modificar_coordenada_otros, "x", -10)
                                        text_size 9 background "#C62828" padding (4, 2)
                                    textbutton "-5":
                                        action Function(modificar_coordenada_otros, "x", -5)
                                        text_size 9 background "#D32F2F" padding (4, 2)
                                    textbutton "-1":
                                        action Function(modificar_coordenada_otros, "x", -1)
                                        text_size 9 background "#E53935" padding (4, 2)
                                    frame:
                                        background "#0D1117"
                                        padding (6, 2)
                                        text "[pos_otros_posicion_actual['x']]" size 12 color "#00E676" bold True
                                    textbutton "+1":
                                        action Function(modificar_coordenada_otros, "x", 1)
                                        text_size 9 background "#2E7D32" padding (4, 2)
                                    textbutton "+5":
                                        action Function(modificar_coordenada_otros, "x", 5)
                                        text_size 9 background "#388E3C" padding (4, 2)
                                    textbutton "+10":
                                        action Function(modificar_coordenada_otros, "x", 10)
                                        text_size 9 background "#43A047" padding (4, 2)

                                # Y
                                hbox:
                                    spacing 2
                                    yalign 0.5
                                    text "Y" size 10 color "#90CAF9" yalign 0.5
                                    textbutton "-10":
                                        action Function(modificar_coordenada_otros, "y", -10)
                                        text_size 9 background "#C62828" padding (4, 2)
                                    textbutton "-5":
                                        action Function(modificar_coordenada_otros, "y", -5)
                                        text_size 9 background "#D32F2F" padding (4, 2)
                                    textbutton "-1":
                                        action Function(modificar_coordenada_otros, "y", -1)
                                        text_size 9 background "#E53935" padding (4, 2)
                                    frame:
                                        background "#0D1117"
                                        padding (6, 2)
                                        text "[pos_otros_posicion_actual['y']]" size 12 color "#00E676" bold True
                                    textbutton "+1":
                                        action Function(modificar_coordenada_otros, "y", 1)
                                        text_size 9 background "#2E7D32" padding (4, 2)
                                    textbutton "+5":
                                        action Function(modificar_coordenada_otros, "y", 5)
                                        text_size 9 background "#388E3C" padding (4, 2)
                                    textbutton "+10":
                                        action Function(modificar_coordenada_otros, "y", 10)
                                        text_size 9 background "#43A047" padding (4, 2)

                            # Separador
                            frame:
                                xsize 1
                                ysize 80
                                yalign 0.5
                                background "#444444"

                            # Botones guardar/deseleccionar
                            vbox:
                                spacing 3
                                yalign 0.5
                                textbutton "💾 Guardar":
                                    action Function(guardar_cambio_sesion_otros)
                                    text_size 10 background "#2E7D32" hover_background "#4CAF50" padding (6, 3)
                                textbutton "✕ Deselec.":
                                    action Function(deseleccionar_elemento_otros)
                                    text_size 10 background "#424242" hover_background "#616161" padding (6, 3)
                        else:
                            if pos_screen_filtro:
                                text "Click en un elemento en pantalla" size 11 color "#666666" yalign 0.5
                            else:
                                text "Selecciona un screen" size 11 color "#666666" yalign 0.5

                # ─── COL 3: Sesion + Cerrar (siempre visible) ────────────
                # Separador
                frame:
                    xsize 1
                    ysize 80
                    yalign 0.5
                    background "#444444"

                vbox:
                    spacing 2
                    yalign 0.5
                    xsize 170

                    if len(pos_sesion_cambios) > 0:
                        text "💾 [len(pos_sesion_cambios)] cambio(s)" size 10 color "#FFD700"
                    else:
                        text "Sin cambios" size 10 color "#555555"

                    hbox:
                        spacing 5
                        textbutton "↩️ Deshacer":
                            action Function(deshacer_ultimo_cambio)
                            text_size 13
                            background ("#1565C0" if len(pos_sesion_undo) > 0 else "#1A1A1A")
                            padding (10, 6)
                            sensitive len(pos_sesion_undo) > 0
                        textbutton "📤 Exportar":
                            action Function(exportar_sesion_posicionamiento)
                            text_size 13
                            background ("#E65100" if len(pos_sesion_cambios) > 0 else "#333333")
                            padding (10, 6)
                            sensitive len(pos_sesion_cambios) > 0
                        textbutton "🗑️ Limpiar":
                            action Function(limpiar_sesion_posicionamiento)
                            text_size 13 background "#333333" padding (10, 6)
                            sensitive len(pos_sesion_cambios) > 0
                        textbutton "❌ Cerrar":
                            action Function(cerrar_modo_posicionamiento)
                            text_size 13 background "#C62828" padding (10, 6)


################################################################################
## Screen: Mensaje de restricción (auto-dismiss 1.5s)
################################################################################
## Muestra un mensaje en el cuadro de texto del juego sin requerir click.
## Se usa en lugar de renpy.notify() para mensajes del sistema de restricciones.

default _msg_restriccion_texto = ""

screen mensaje_restriccion():
    zorder 150
    
    # Fondo del cuadro de diálogo (parte inferior de pantalla)
    frame:
        xalign 0.5
        yalign 0.98
        xsize 1400
        ypadding 20
        xpadding 40
        background "#1a1a1aCC"
        
        text _msg_restriccion_texto:
            xalign 0.5
            color "#CCCCCC"
            italic True
            size 32
            outlines [(2, "#000000", 0, 0)]
    
    # Timer: cierra el screen automáticamente después de 1.5 segundos
    timer 1.5 action [Hide("mensaje_restriccion"), Return()]


################################################################################
## Label helper: mostrar mensaje de restricción
################################################################################

label mostrar_mensaje_restriccion(texto):
    $ store._msg_restriccion_texto = texto
    show screen mensaje_restriccion
    $ renpy.pause(1.5, hard=True)
    hide screen mensaje_restriccion
    return

################################################################################
## Label helper: pensar un mensaje (usa piensa)
################################################################################

label pensar_mensaje(msg):
    $ msg = renpy.translate_string(msg)
    piensa "[msg]"
    return

################################################################################
## Label helper: narrar un mensaje (usa narrator)
################################################################################

label narrar_mensaje(msg):
    $ msg = renpy.translate_string(msg)
    "[msg]"
    return
