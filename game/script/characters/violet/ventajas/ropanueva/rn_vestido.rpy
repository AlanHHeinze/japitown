################################################################################
## Ropa Nueva · Violet — VESTIDO
################################################################################
## Primera prenda del sistema. ⚠️ PLACEHOLDER: la escena todavia no esta escrita
## y el sprite es el cuerpo de siempre — al llegar el arte del vestido hay que
## declararlo en el layeredimage `violet_parada` (seccion propia del grupo
## `cuerpo`, como pijama y tanga) y cambiar el `show` de acá.

default rn_vestido_visto = False


init python:

    def _rn_vestido_visto():
        return getattr(store, 'rn_vestido_visto', False)


init 5 python:

    registrar_prenda_nueva(
        "vestido",
        "Vestido",
        "violet_rn_vestido",
        _rn_vestido_visto,
    )

    registrar_contenido_ventaja(
        "ropa_nueva", "vestido", "violet",
        "Vestido",
        "Elige Ropa Nueva en su menú y pídele el vestido.",
        vista=_rn_vestido_visto,
        orden=10,
    )


label violet_rn_vestido:

    $ ocultar_hud()
    window show

    $ _rnv_loc = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _rnv_bg = _rnv_loc.background if _rnv_loc else "#1a1a1a"
    scene expression _rnv_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # ⚠️ Sprite PLACEHOLDER: todavia no hay vestido.
    # (Violet cuerpo base ojos base boca neutral)
    show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la escena del vestido
    # =========================================================================

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Contenido de prueba"
    # (Violet boca neutral)
    show violet_parada b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    # A partir de acá deja de ofrecerse en el menu (lo lee _rn_vestido_visto).
    $ rn_vestido_visto = True

    window hide
    $ mostrar_hud()
    jump game_loop
