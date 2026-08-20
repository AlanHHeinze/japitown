################################################################################
## Violet — VENTAJA "Ropa Nueva" · el controlador
################################################################################
## Ventaja del hito de amor 30. Estando en su habitacion, el menu de Violet
## ofrece que se pruebe algo nuevo: se elige la prenda de un menu y cada una
## corre su propia escena.
##
## DIFERENCIA CON JUEGOS NUEVOS: aquel solo ENUMERA lo que falta (cada juego se
## juega por su via). Acá la prenda se juega desde la charla, asi que cada una
## registra ademas su LABEL.
##
## COMO AGREGAR UNA PRENDA: crear su `rn_<nombre>.rpy` en esta carpeta con su
## label y su flag, y llamar a registrar_prenda_nueva() desde su init 5.
## ESTE ARCHIVO NO SE TOCA.
##
##     characters/violet/ventajas/ropanueva/
##     ├── ropanueva_violet.rpy   ← esto
##     └── rn_vestido.rpy         ← una prenda


init python:

    # [(orden, reg, prenda_id, nombre, label, fn_vista)]
    ROPA_NUEVA_VIOLET = []

    def registrar_prenda_nueva(prenda_id, nombre, label, vista, orden=0):
        """
        Registra una prenda que Violet se puede probar.

        Args:
            prenda_id: id unico (ej. "vestido")
            nombre: como aparece en el menu. Se traduce al mostrarlo.
            label: label de la escena. Es CONTENIDO, asi que cierra con
                jump game_loop.
            vista: funcion de MODULO sin argumentos → True si ya se la probo.
            orden: menor primero. A igual orden, orden de registro.
        """
        ROPA_NUEVA_VIOLET.append((orden, len(ROPA_NUEVA_VIOLET),
                                  prenda_id, nombre, label, vista))

    def ropa_nueva_pendientes_violet():
        """
        Prendas que todavia no se probo, ya ordenadas → [(nombre, label)].

        Una prenda cuya funcion `vista` reviente se considera NO vista y se
        sigue ofreciendo: es preferible que se repita a que el menu se corte por
        una prenda mal escrita.
        """
        _pendientes = []
        for _orden, _reg, _pid, _nom, _lbl, _fn in sorted(ROPA_NUEVA_VIOLET,
                                                          key=lambda p: (p[0], p[1])):
            try:
                if _fn():
                    continue
            except Exception:
                pass
            _pendientes.append((_nom, _lbl))
        return _pendientes

    def _violet_boton_ropa_nueva():
        """
        Condicion del boton del menu de Violet.

        Pide que este en su habitacion: el menu solo se abre clickeando su
        sprite, asi que eso ya implica que el MC tambien esta ahi.
        """
        if not npc_tiene_ventaja("violet", "ropa_nueva"):
            return False
        return tracker_locacion_npc("violet") == "casa_hviolet"


################################################################################
## La charla
################################################################################

label violet_ropa_nueva:

    $ ocultar_hud()
    window show

    $ _rn_loc_hv = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _rn_bg = _rn_loc_hv.background if _rn_loc_hv else "#1a1a1a"
    scene expression _rn_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: de noche esta en pijama.
    $ _rn_cuerpo = cuerpo_activo("violet")
    if _rn_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "¿Te compraste algo nuevo?"
    # (Mc boca neutral)
    show mc_parado_base b_none

    $ _rn_pendientes = ropa_nueva_pendientes_violet()

    if not _rn_pendientes:
        # (Violet boca hablando)
        show violet_parada b_hablando
        violet "Ahora no tengo nada nuevo para probarme (Más contenido en futuras actualizaciones)"
        # (Violet boca neutral)
        show violet_parada b_none

        hide mc_parado_base
        hide violet_parada
        with dissolve

        window hide
        $ mostrar_hud()
        jump game_loop

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Sí, algo tengo. ¿Qué querés que me pruebe?"
    # (Violet boca neutral)
    show violet_parada b_none

    # display_menu y NO un bloque `menu:`: las opciones salen del registro, y el
    # bloque estatico no se puede armar en runtime. Mismo recurso que usa el
    # sistema de talk (talksystem_labels).
    #
    # Los nombres se traducen ANTES de armar el menu: salen de una variable, y
    # el `menu` no pasa por el sistema de traduccion por id.
    python:
        _rn_items = [(renpy.translate_string(_nom), _lbl)
                     for _nom, _lbl in _rn_pendientes]
        _rn_items.append((renpy.translate_string("Volver"), None))

    $ _rn_elegido = renpy.display_menu(_rn_items)

    hide mc_parado_base
    hide violet_parada
    with dissolve

    if _rn_elegido is None:
        window hide
        $ mostrar_hud()
        jump game_loop

    window hide
    jump expression _rn_elegido
