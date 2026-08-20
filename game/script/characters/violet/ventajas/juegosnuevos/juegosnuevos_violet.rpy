################################################################################
## Violet — VENTAJA "Juegos Nuevos" · el controlador
################################################################################
## Ventaja del hito de amor 20. Agrega una opcion fija al menu de Violet donde
## el MC le pregunta si se le ocurre algo nuevo para jugar, y ella enumera los
## juegos que todavia no jugaron.
##
## LA CHARLA SOLO ENUMERA. Cada juego se juega por su propia via — el casco VR,
## por ejemplo, se compra en la tienda y se usa de noche en la habitacion del MC.
## Este label no dispara ninguna escena: cuenta que existen.
##
## COMO AGREGAR UN JUEGO: crear su archivo `jn_<nombre>.rpy` en esta carpeta y
## llamar a registrar_juego_nuevo() desde su init 5. ESTE ARCHIVO NO SE TOCA.
## Es la misma operativa que el resto de los registros del proyecto: el
## controlador itera, no conoce ningun juego por nombre.
##
##     characters/violet/ventajas/juegosnuevos/
##     ├── juegosnuevos_violet.rpy   ← esto
##     └── jn_cascovr.rpy            ← un juego


init python:

    # [(orden, juego_id, mensaje, fn_jugado)]
    JUEGOS_NUEVOS_VIOLET = []

    def registrar_juego_nuevo(juego_id, mensaje, jugado, orden=0):
        """
        Registra un juego para la charla de "Juegos Nuevos".

        Args:
            juego_id: id unico del juego (ej. "cascovr")
            mensaje: lo que dice Violet mientras el juego NO este jugado. Va en
                español; se traduce al mostrarlo.
            jugado: funcion de MODULO sin argumentos → True si ya se jugo. Nunca
                lambda: el registro se arma en init y la regla anti-pickle del
                proyecto vale igual por consistencia.
            orden: menor primero. A igual orden, orden de registro.
        """
        JUEGOS_NUEVOS_VIOLET.append((orden, len(JUEGOS_NUEVOS_VIOLET),
                                     juego_id, mensaje, jugado))

    def juegos_nuevos_pendientes_violet():
        """
        Los juegos que Violet todavia puede proponer, ya ordenados.

        Un juego cuya funcion `jugado` reviente se considera NO jugado y se
        sigue proponiendo: es preferible que se repita a que la charla se corte
        a la mitad por un juego mal escrito.
        """
        _pendientes = []
        for _orden, _reg, _jid, _msg, _fn in sorted(JUEGOS_NUEVOS_VIOLET,
                                                    key=lambda j: (j[0], j[1])):
            try:
                if _fn():
                    continue
            except Exception:
                pass
            _pendientes.append(_msg)
        return _pendientes

    def _violet_boton_juegos_nuevos():
        """Condicion del boton del menu de Violet (interactions_violet.rpy)."""
        return npc_tiene_ventaja("violet", "juegos_nuevos")


################################################################################
## La charla
################################################################################
## Pasa donde esten y con la ropa que tengan: la opcion esta siempre disponible,
## asi que no se puede asumir ni locacion ni atuendo.

label violet_juegos_nuevos:

    $ ocultar_hud()
    window show

    $ _jn_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _jn_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: de noche esta en pijama.
    $ _jn_cuerpo = cuerpo_activo("violet")
    if _jn_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "¿Se te ocurre algo nuevo para jugar?"
    # (Mc boca neutral)
    show mc_parado_base b_none

    $ _jn_pendientes = juegos_nuevos_pendientes_violet()

    # (Violet boca hablando)
    show violet_parada b_hablando

    if _jn_pendientes:
        # Un mensaje por juego. renpy.translate_string y NO _(): el texto sale
        # de una variable, y en `violet "[var]"` Ren'Py buscaria la traduccion
        # del literal "[var]" — hay que traducir ANTES de asignar.
        python:
            _jn_i = 0
        while _jn_i < len(_jn_pendientes):
            $ _jn_msg = renpy.translate_string(_jn_pendientes[_jn_i])
            violet "[_jn_msg]"
            $ _jn_i += 1
    else:
        violet "Ahora no se me ocurre ninguno (Más contenido en futuras actualizaciones)"

    # (Violet boca neutral)
    show violet_parada b_none

    hide mc_parado_base
    hide violet_parada
    with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop
