################################################################################
## Sistema de Notificaciones de Stats
################################################################################
## Muestra notificaciones flotantes estilo debug cuando un stat cambia.
## Usa el enfoque de llamada explícita: la función notificar_cambio_stat()
## se invoca desde los puntos centralizados que modifican stats.

# Registrar screen como overlay persistente
init python:
    if "notificaciones_stats" not in config.overlay_screens:
        config.overlay_screens.append("notificaciones_stats")

init python:
    import time as _time_module

    # Cola de notificaciones activas
    # Cada entrada: {"texto": str, "icono": str, "color": str, "timestamp": float, "positivo": bool}
    _notificaciones_stats = []

    # Duración en segundos que cada notificación permanece visible
    _NOTIF_DURACION = 2.5

    # Iconos para cada tipo de stat
    _NOTIF_ICONOS = {
        # Stats del MC
        "fuerza": "💪",
        "carisma": "💬",
        "destreza": "🎯",
        "inteligencia": "🧠",
        "dinero": "💰",
        # Stats de NPC
        "amor": "❤️",
        "deseo": "💋",

        "progreso": "⭐",
    }

    # Colores para cada tipo de stat
    _NOTIF_COLORES = {
        "fuerza": "#FF6B6B",
        "carisma": "#FFB74D",
        "destreza": "#4FC3F7",
        "inteligencia": "#81C784",
        "dinero": "#4CAF50",
        "amor": "#FF4081",
        "deseo": "#E040FB",

        "progreso": "#FFC107",
    }

    def notificar_cambio_stat(tipo, cantidad, npc_nombre=None):
        """
        Agrega una notificación de cambio de stat a la cola.

        Args:
            tipo: ID del stat ("fuerza", "carisma", "dinero", "amor", "deseo", etc.)
            cantidad: Cambio numérico (positivo o negativo)
            npc_nombre: Nombre del NPC (opcional, para stats de NPC)
        """
        if cantidad == 0:
            return

        positivo = cantidad > 0
        signo = "+" if positivo else "-"
        icono = _NOTIF_ICONOS.get(tipo, "📊")
        color = _NOTIF_COLORES.get(tipo, "#ffffff")

        # Construir texto
        if npc_nombre:
            texto = "{}{} {}".format(signo, abs(cantidad), npc_nombre)
        elif tipo == "dinero":
            texto = "{}${}".format(signo, abs(cantidad))
        else:
            texto = "{}{}".format(signo, abs(cantidad))

        notif = {
            "texto": texto,
            "icono": icono,
            "color": color,
            "timestamp": _time_module.time(),
            "positivo": positivo,
            "id_str": "{}_{}_{}".format(tipo, cantidad, _time_module.time()),
            "delay": len(store._notificaciones_stats) * 0.15,
        }

        _limpiar_notificaciones_expiradas()
        store._notificaciones_stats.append(notif)

        # Limitar cola a 6 notificaciones máximo
        if len(store._notificaciones_stats) > 6:
            store._notificaciones_stats.pop(0)

    def _limpiar_notificaciones_expiradas():
        """Remueve notificaciones que ya expiraron."""
        ahora = _time_module.time()
        store._notificaciones_stats = [
            n for n in store._notificaciones_stats
            if ahora - n["timestamp"] < _NOTIF_DURACION
        ]


################################################################################
## Transform para animación de notificación
################################################################################

# Entrada: slide desde la derecha + fade in, luego fade out al final
transform notif_stat_aparecer(delay=0.0):
    on show:
        alpha 0.0 xoffset 30
        pause delay
        easein 0.3 alpha 1.0 xoffset 0
        pause (_NOTIF_DURACION - 0.6)
        easeout 0.3 alpha 0.0 xoffset 30


################################################################################
## Screen de notificaciones (siempre activo, se superpone al HUD)
################################################################################

screen notificaciones_stats():
    zorder 150
    layer "overlay"

    $ _notifs_actuales = [n for n in _notificaciones_stats if _time_module.time() - n["timestamp"] < _NOTIF_DURACION]

    if _notifs_actuales:
        vbox:
            xalign 1.0
            ypos 120
            spacing 10

            for _notif in _notifs_actuales:
                frame:
                    id "notif_" + _notif["id_str"]
                    background "#00000099"
                    padding (18, 9, 24, 9)
                    at notif_stat_aparecer(_notif["delay"])

                    hbox:
                        spacing 12
                        yalign 0.5

                        text _notif["icono"] size 33 yalign 0.5
                        text _notif["texto"]:
                            size 30
                            color _notif["color"]
                            bold True
                            yalign 0.5
                            outlines [(1, "#000000", 0, 0)]


################################################################################
## Sistema de Notificaciones de Recuerdos
################################################################################
## Notificaciones flotantes en el lado IZQUIERDO para eventos de memoria.
##
## Funciones disponibles:
##   $ notificar_recuerdo_activado()          → "Recuerdo activado"
##   $ notificar_recordara("violet")          → "Violet recordará esto"

# Registrar screen como overlay persistente
init python:
    if "notificaciones_recuerdos" not in config.overlay_screens:
        config.overlay_screens.append("notificaciones_recuerdos")

init python:
    # Cola de notificaciones de recuerdos activas
    # Cada entrada: {"texto": str, "timestamp": float, "delay": float, "id_str": str}
    _notificaciones_recuerdos = []

    # Duración en segundos
    _NOTIF_RECUERDO_DURACION = 2.5

    def _agregar_notif_recuerdo(texto, color="#ffffff"):
        """Agrega una notificación a la cola izquierda de recuerdos."""
        import time as _t
        _limpiar_notificaciones_recuerdos_expiradas()

        notif = {
            "texto":     texto,
            "color":     color,
            "timestamp": _t.time(),
            "delay":     len(store._notificaciones_recuerdos) * 0.15,
            "id_str":    "recuerdo_{}".format(_t.time()),
        }

        store._notificaciones_recuerdos.append(notif)

        if len(store._notificaciones_recuerdos) > 3:
            store._notificaciones_recuerdos.pop(0)

    def notificar_item_obtenido(item_id):
        """
        Muestra '{emoji_item} + Nombre del Item' a la izquierda.
            $ notificar_item_obtenido("golosinas")
        """
        info   = CATALOGO_ITEMS.get(item_id, {})
        nombre = info.get("nombre", item_id)
        emoji  = info.get("emoji", "📦")
        _agregar_notif_recuerdo("{} + {}".format(emoji, nombre), color="#ffffff")

    def notificar_item_perdido(item_id):
        """
        Muestra '{emoji_item} - Nombre del Item' en rojo a la izquierda.
            $ notificar_item_perdido("golosinas")
        """
        info   = CATALOGO_ITEMS.get(item_id, {})
        nombre = info.get("nombre", item_id)
        emoji  = info.get("emoji", "📦")
        _agregar_notif_recuerdo("{} - {}".format(emoji, nombre), color="#FF4444")

    def agregar_al_inventario(item_id, cantidad=1):
        """
        Agrega cantidad al inventario y dispara la notificación de obtención.
            $ agregar_al_inventario("golosinas")
            $ agregar_al_inventario("tanga_violet", 1)
        """
        store.inventario[item_id] = store.inventario.get(item_id, 0) + cantidad
        notificar_item_obtenido(item_id)

    def quitar_del_inventario(item_id, cantidad=1):
        """
        Quita cantidad del inventario y dispara la notificación de pérdida.
        Si llega a 0 o menos, elimina la entrada del dict.
            $ quitar_del_inventario("golosinas")
        """
        actual = store.inventario.get(item_id, 0)
        nuevo  = actual - cantidad
        if nuevo <= 0:
            store.inventario.pop(item_id, None)
        else:
            store.inventario[item_id] = nuevo
        notificar_item_perdido(item_id)

    def notificar_recuerdo_activado():
        """
        Muestra "Recuerdo activado" a la izquierda.
            $ notificar_recuerdo_activado()
        """
        _agregar_notif_recuerdo("Recuerdo activado")

    def notificar_recordara(npc_id):
        """
        Muestra "[Nombre] recordará esto" a la izquierda.
            $ notificar_recordara("violet")   →   "Violet recordará esto"

        Acepta el npc_id ("violet", "monica", "jasmine") y resuelve
        el nombre visible automáticamente desde el sistema de NPCs.
        """
        npc = obtener_npc(npc_id) if hasattr(store, 'sistema_npcs') else None
        nombre = npc.nombre if npc else npc_id.capitalize()
        _agregar_notif_recuerdo("{} recordará esto".format(nombre))

    def _limpiar_notificaciones_recuerdos_expiradas():
        """Remueve notificaciones de recuerdos que ya expiraron."""
        import time as _t
        store._notificaciones_recuerdos = [
            n for n in store._notificaciones_recuerdos
            if _t.time() - n["timestamp"] < _NOTIF_RECUERDO_DURACION
        ]


# Entrada: slide desde la izquierda + fade in, luego fade out a la izquierda
transform notif_recuerdo_aparecer(delay=0.0):
    on show:
        alpha 0.0 xoffset -30
        pause delay
        easein 0.3 alpha 1.0 xoffset 0
        pause (_NOTIF_RECUERDO_DURACION - 0.6)
        easeout 0.3 alpha 0.0 xoffset -30


screen notificaciones_recuerdos():
    zorder 150
    layer "overlay"

    python:
        import time as _t
        _notifs_recuerdos_act = [
            n for n in _notificaciones_recuerdos
            if _t.time() - n["timestamp"] < _NOTIF_RECUERDO_DURACION
        ]

    if _notifs_recuerdos_act:
        vbox:
            xalign 0.0
            ypos 120
            spacing 10

            for _nr in _notifs_recuerdos_act:
                frame:
                    id "notif_" + _nr["id_str"]
                    background "#00000099"
                    padding (24, 9, 18, 9)
                    at notif_recuerdo_aparecer(_nr["delay"])

                    text _nr["texto"]:
                        size 30
                        color _nr.get("color", "#ffffff")
                        bold True
                        yalign 0.5
                        outlines [(1, "#000000", 0, 0)]
