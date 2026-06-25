################################################################################
## Visualizador de Hotspots de Movimiento
################################################################################
## Accion de locacion global (locacion_id=None) disponible en todas las
## locaciones. Al activarla muestra las imagenes de hover de todos los hotspots
## MOVE de la locacion actual: imagen propia si la tiene, flecha centrada si no.
## Un segundo toque la desactiva.

default visualizador_hotspot_activo = False
default config_mostrar_accion_movimiento = False


################################################################################
## Accion global
################################################################################

init python:
    def _cond_accion_movimiento():
        return getattr(store, 'config_mostrar_accion_movimiento', False)

init 5 python:
    sistema_acciones.registrar_accion(AccionLocacion(
        id="visualizador_hotspot",
        nombre="Ver salidas",
        icono=u"👁",
        locacion_id=None,
        label_generico="visualizador_hotspot_toggle",
        reseteo=None,
        condicion=_cond_accion_movimiento,
        color="#37474F",
        color_hover="#546E7A",
    ))


################################################################################
## Label toggle — se llama con call expression, termina en return
################################################################################

label visualizador_hotspot_toggle:
    $ visualizador_hotspot_activo = not visualizador_hotspot_activo
    return


################################################################################
## Screen overlay — muestra las imagenes de hover de todos los MOVE hotspots
################################################################################

screen visualizador_hotspot_overlay():

    if visualizador_hotspot_activo and config_mostrar_accion_movimiento and sistema_locaciones.locacion_actual:

        $ _vhs_hotspots = [
            h for h in sistema_locaciones.locacion_actual.obtener_hotspots_habilitados()
            if h.tipo == "MOVE"
        ]

        for _vhs_h in _vhs_hotspots:

            $ _vhs_img    = _IDLE_MOV_IMGS.get(_vhs_h.id)
            $ _vhs_flecha = _IDLE_MOV_FLECHAS.get(_vhs_h.id)
            $ _vhs_cx     = _vhs_h.x + _vhs_h.w // 2
            $ _vhs_cy     = _vhs_h.y + _vhs_h.h // 2

            if _vhs_img:
                # Hotspot con imagen propia: mostrar en su posicion con alpha visible
                add Transform(_vhs_img, alpha=0.75) xpos _vhs_h.x ypos _vhs_h.y xanchor 0.0 yanchor 0.0

            elif _vhs_flecha:
                if "flecha_abajo" in _vhs_flecha and _vhs_cy > 900:
                    add _vhs_flecha xpos _vhs_cx ypos 1070 xanchor 0.5 yanchor 1.0
                elif _vhs_h.id == "casa_living_casa_pasilloabajo":
                    add _vhs_flecha xpos _vhs_cx ypos 1022 xanchor 0.5 yanchor 0.5
                else:
                    add _vhs_flecha xpos _vhs_cx ypos _vhs_cy xanchor 0.5 yanchor 0.5
