################################################################################
## Ropa Nueva · Violet — EL JEAN (volver a verlo)
################################################################################
## Repite la secuencia del jean de la quest de amor 30 (violet_amor_30.rpy), que
## es de donde sale esta ventaja: el jean es lo ultimo que le vio puesto, y esta
## prenda es para volver a verlo.
##
## NO SE GASTA. Las demas prendas desaparecen del menu una vez probadas —esa es
## la funcion `vista` que pide registrar_prenda_nueva—, pero acá el punto es
## justamente poder repetirla, asi que su `vista` devuelve False SIEMPRE y la
## opcion queda para siempre. El flag `rn_jean_visto` existe aparte y es solo
## para el ojo del panel de Desbloqueos.
##
## USA EL LAYEREDIMAGE `violet_q30a` (visual/sprites_violet.rpy), el mismo de la
## quest: trae la cabeza y la cara dibujadas, asi que no combina con los grupos
## del `violet_parada` de siempre.
##
## ⚠️ SIN DIALOGO Y CORTADA DONDE TERMINA EL ARTE. La secuencia va de corrido
## hasta `c_jean_bajando5`, que es el ultimo cuadro que existe hoy. Al llegar los
## sprites nuevos se agregan al final, antes del `hide`.

# Solo para el ojo del panel de Desbloqueos: la opcion del menu no se apaga.
default rn_jean_visto = False


init python:

    def _rn_jean_pendiente():
        """
        `vista` de la prenda — SIEMPRE False a proposito.

        Es lo que mantiene la opcion en el menu: ropa_nueva_pendientes_violet()
        saca las prendas cuya `vista` da True, y esta es para repetir.
        """
        return False

    def _rn_jean_visto():
        """`vista` del catalogo de contenido: si ya la corrio alguna vez."""
        return getattr(store, 'rn_jean_visto', False)


init 5 python:

    registrar_prenda_nueva(
        "jean",
        "El jean",
        "violet_rn_jean",
        _rn_jean_pendiente,
    )

    registrar_contenido_ventaja(
        "ropa_nueva", "jean", "violet",
        "El jean, otra vez",
        "Elige Ropa Nueva en su menú y pídele el jean. Si no están en su habitación, te cita allá.",
        vista=_rn_jean_visto,
        orden=20,
    )


label violet_rn_jean:

    $ ocultar_hud()
    window show

    # La escena pasa SI O SI en su habitacion: o el jugador ya estaba ahi, o
    # llego despues de la cita y la dispara el trigger de convocatoria. En los
    # dos casos la locacion actual es la correcta.
    $ _rnj_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _rnj_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo jean base boca neutral)
    show violet_q30a c_jean_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — el jean
    # =========================================================================
    #
    # El grupo `cuerpo` del layeredimage es uno solo, o sea que los atributos
    # son excluyentes: cada `show` reemplaza el cuadro anterior y no hay que
    # apagar nada.
    #
    # Cada cuadro entra con sprite_normal (Dissolve de 0.5) y se sostiene otro
    # medio segundo. Los `pause` van con duracion, asi que corren solos y la
    # secuencia se mira de corrido, sin clicks.

    # Se da vuelta.
    show violet_q30a c_jean_espalda with sprite_normal
    pause 0.5

    # Se toca el jean.
    show violet_q30a c_jean_tocando1 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_tocando2 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_tocando3 with sprite_normal
    pause 0.5

    # Y se lo baja.
    show violet_q30a c_jean_bajando1 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando2 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando3 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando4 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_bajando5 with sprite_normal
    pause 0.5

    # Con el jean abajo, se toca. Estos tres cuadros son propios de la ventaja:
    # la quest de amor 30 termina en bajando5.
    show violet_q30a c_jean_btocando1 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_btocando2 with sprite_normal
    pause 0.5

    show violet_q30a c_jean_btocando3 with sprite_normal
    pause 0.5

    # ⚠️ ACÁ SIGUE: los sprites nuevos van despues de este cuadro.

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_q30a
    with dissolve

    # No apaga la opcion del menu (la prenda se puede repetir): es solo el ojo
    # del panel de Desbloqueos.
    $ rn_jean_visto = True

    window hide
    $ mostrar_hud()
    jump game_loop
