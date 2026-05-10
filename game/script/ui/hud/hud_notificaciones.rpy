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
