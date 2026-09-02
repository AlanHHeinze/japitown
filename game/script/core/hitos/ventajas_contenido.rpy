################################################################################
## Hitos — Catálogo de CONTENIDO de una ventaja
################################################################################
## El panel de Desbloqueos dice QUE hace cada ventaja. Esto dice QUE HAY dentro:
## la lista de escenas, chats o prendas concretas que esa ventaja habilita, con
## el estado de cada una.
##
## En el panel, toda ventaja que tenga contenido registrado acá muestra un botón
## de ojo al lado; el ojo abre la subapp que lista sus entradas. El motor NO
## conoce ninguna ventaja por nombre: si un id no tiene entradas, no hay botón.
##
## TRES ESTADOS, y los decide cada entrada con sus dos predicados:
##
##   bloqueado  — `desbloqueada()` da False. Todavia no se puede llegar a esto
##                por una razon estructural (falta una ventaja, falta una rama
##                de otra escena). NO es para condiciones del momento: que
##                Violet no este en su pieza AHORA no bloquea nada, solo hay
##                que esperar.
##   pendiente  — se puede, pero el jugador no lo vio.
##   visto      — `vista()` da True.
##
## Un predicado que revienta se toma como False: una entrada mal escrita
## aparece como bloqueada/no vista, pero no rompe el panel.
##
## LA DESCRIPCION ES UNA PISTA, no un resumen. Tiene que orientar sobre COMO
## llegar a esa situacion ("Escribile de noche mientras se esta bañando"), que
## es para lo que el jugador abre esta pantalla.

init -1 python:

    # Los tres estados posibles de una entrada.
    VC_BLOQUEADO = "bloqueado"
    VC_PENDIENTE = "pendiente"
    VC_VISTO     = "visto"

    # Iconos y colores de cada estado. Se tocan SOLO acá: los usa la subapp para
    # las tres filas, asi que cambiar el emoji del ojo es una linea.
    VC_ICONO = {
        VC_BLOQUEADO: u"🔒",
        VC_PENDIENTE: u"🙈",
        VC_VISTO:     u"👁️",
    }
    VC_COLOR = {
        VC_BLOQUEADO: "#5a5a6e",    # gris oscuro, igual que una ventaja bloqueada
        VC_PENDIENTE: "#9aa8c0",    # gris claro
        VC_VISTO:     "#ffffff",    # blanco
    }


init python:

    # {ventaja_id: [(orden, reg, dict)]}
    CONTENIDO_VENTAJA = {}

    def registrar_contenido_ventaja(ventaja_id, entrada_id, npc_id, nombre,
                                    descripcion, vista, desbloqueada=None,
                                    orden=0):
        """
        Registra UNA situacion concreta que habilita una ventaja.

        Args:
            ventaja_id: la ventaja a la que cuelga (ver hitos_ventajas.rpy).
            entrada_id: id unico dentro de esa ventaja.
            npc_id: de quien es el contenido. La subapp filtra por esto, asi que
                una ventaja compartida por los tres NPCs lista lo que
                corresponde a cada ficha.
            nombre: como se llama la situacion. En español; se traduce al pintar.
            descripcion: PISTA de como llegar. En español; se traduce al pintar.
            vista: funcion de MODULO sin argumentos → True si el jugador ya la
                vio. Nunca lambda (regla anti-pickle del proyecto).
            desbloqueada: funcion de MODULO sin argumentos → False si todavia no
                se puede llegar. None = siempre alcanzable.
            orden: menor primero. A igual orden, orden de registro.
        """
        _lista = CONTENIDO_VENTAJA.setdefault(ventaja_id, [])
        _lista.append((orden, len(_lista), {
            "id":           entrada_id,
            "npc_id":       npc_id,
            "nombre":       nombre,
            "descripcion":  descripcion,
            "_vista":       vista,
            "_desbloqueada": desbloqueada,
        }))

    def _vc_llamar(fn, defecto):
        """Corre un predicado de entrada; si revienta, devuelve `defecto`."""
        if fn is None:
            return defecto
        try:
            return bool(fn())
        except Exception:
            return defecto

    def ventaja_tiene_contenido(ventaja_id, npc_id):
        """
        True si esta ventaja tiene entradas para este NPC.

        Lo consulta el panel de Desbloqueos para decidir si dibuja el ojo. Es
        una lectura pura: la llama una screen en cada frame.
        """
        for _orden, _reg, _e in CONTENIDO_VENTAJA.get(ventaja_id, []):
            if _e["npc_id"] == npc_id:
                return True
        return False

    def obtener_contenido_ventaja(ventaja_id, npc_id):
        """
        Las entradas de una ventaja para un NPC, ordenadas y ya resueltas.

        Devuelve dicts con nombre/desc YA TRADUCIDOS y su `estado`, que es lo
        unico que necesita la subapp: la screen no vuelve a llamar predicados.

        Returns:
            list[dict] — {"id", "nombre", "desc", "estado"}
        """
        _salida = []
        for _orden, _reg, _e in sorted(CONTENIDO_VENTAJA.get(ventaja_id, []),
                                       key=lambda c: (c[0], c[1])):
            if _e["npc_id"] != npc_id:
                continue

            if not _vc_llamar(_e["_desbloqueada"], True):
                _estado = VC_BLOQUEADO
            elif _vc_llamar(_e["_vista"], False):
                _estado = VC_VISTO
            else:
                _estado = VC_PENDIENTE

            _salida.append({
                "id":     _e["id"],
                "nombre": renpy.translate_string(_e["nombre"]),
                "desc":   renpy.translate_string(_e["descripcion"]),
                "estado": _estado,
            })
        return _salida

    def contar_contenido_ventaja(ventaja_id, npc_id):
        """(vistas, alcanzables) — el contador que encabeza la subapp.

        `alcanzables` no cuenta las bloqueadas a proposito: mostrar "2/9" con
        siete cosas que todavia no se pueden ni intentar desanima sin informar.
        """
        _entradas = obtener_contenido_ventaja(ventaja_id, npc_id)
        _vistas = len([_e for _e in _entradas if _e["estado"] == VC_VISTO])
        _alcanzables = len([_e for _e in _entradas if _e["estado"] != VC_BLOQUEADO])
        return _vistas, _alcanzables
