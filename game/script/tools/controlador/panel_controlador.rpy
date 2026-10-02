################################################################################
## Dev — Panel del controlador (en vivo)
################################################################################
## Muestra, por quest activa, en que capa esta y por que: capa 1 (espera para
## nacer detras de X), capa 2 (conflicto: reserva ajena, consumos de otra,
## restriccion ajena), o el mundo en dos partes —tiempo y lugar— con lo que
## se cumple y lo que no. Mas las reservas vigentes y la restriccion activa.
##
## Solo lee estado (el predictor ejecuta el cuerpo de la screen): usa las
## partes puras de la capa 2, nunca puede_activarse().
##
## USO: jp_panel_controlador() en la consola (Shift+O), o el boton "Panel del
## controlador (en vivo)" del menu de cheats. Toggle.

init python:

    def jp_panel_controlador():
        if renpy.get_screen("panel_controlador"):
            renpy.hide_screen("panel_controlador")
        else:
            renpy.show_screen("panel_controlador")
        renpy.restart_interaction()

    _PP_ETAPAS = {1: "INIT", 2: "ESPERA", 3: "CONDIC", 4: "RUTINA", 5: "LISTA", 8: "MEM", 9: "FIN"}

    def _pp_lineas():
        """
        Lineas del panel. SOLO LECTURAS (el predictor ejecuta el cuerpo de la
        screen): usa las partes puras de la capa 2, no puede_activarse().
        """
        out = []
        out.append(("hdr", "dia %s · %s · h%s   restriccion: %s" % (
            getattr(store, "dias_totales", "?"),
            ["lun", "mar", "mie", "jue", "vie", "sab", "dom"][getattr(store, "dia_semana_actual", 0) % 7],
            getattr(store, "horario_actual", "?"),
            getattr(getattr(store, "restriccion_quest_activa", None), "duenio", None) or "-")))
        for res in getattr(store, "planificador_reservas", None) or []:
            if _pl_reserva_es_vida(res):
                out.append(("res", "reserva %s -> %s hasta completar  (VIGENTE)" % (
                    res["quest_id"], res["npc"])))
            else:
                _vig = "VIGENTE" if _pl_reserva_vigente_ahora(res) else "pendiente"
                out.append(("res", "reserva %s -> %s dia %s h %s  (%s)" % (
                    res["quest_id"], res["npc"], res["dia_total"], res["horario"], _vig)))
        for q in sorted(store.sistema_quests.quests.values(), key=lambda x: x.id):
            if not q.activa or q.completada:
                continue
            _et = _PP_ETAPAS.get(q.etapa_actual, str(q.etapa_actual))
            _nar = " NARR" if getattr(q, "narrativa_activa", False) else ""
            _dc = " DC" if getattr(q, "de_corrido", False) else ""
            if q.etapa_actual == ETAPA_CONDICIONES and getattr(q, "esperando_desde", None) is not None:
                _estado = "capa 1: espera detras de %s" % (getattr(q, "bloqueada_por", None) or "secuencia en curso")
                _tono = "warn"
            elif q.etapa_actual == ETAPA_BOTON_LISTO and not getattr(q, "narrativa_activa", False) and getattr(q, "planificada", False):
                _c = _pl_conflicto_activacion(q)
                if _c:
                    _estado, _tono = "capa 2: " + _c, "warn"
                else:
                    # Mundo en dos partes: cada una dice si se cumple o que falla.
                    _tm, _lg, _ext = _pl_mundo_detalle(q)
                    _estado = "tiempo: %s · lugar: %s" % (_tm or "OK", _lg or "OK")
                    _tono = "ok" if not (_tm or _lg) else "dim"
            elif getattr(q, "narrativa_activa", False):
                _estado, _tono = "en narrativa", "ok"
            else:
                _estado, _tono = "", "dim"
            out.append((_tono, "%-32s %-6s%s%s  %s" % (q.id, _et, _dc, _nar, _estado)))
        return out


screen panel_controlador():
    zorder 250

    frame:
        xalign 1.0
        yalign 0.0
        xoffset -10
        yoffset 110
        xsize 760
        background "#000000B0"
        padding (10, 8)

        vbox:
            spacing 2
            hbox:
                xfill True
                text "CONTROLADOR" size 13 color "#4FC3F7" bold True xfill True
                textbutton "x" action Function(jp_panel_controlador) text_size 12
            for _tono, _linea in _pp_lineas():
                if _tono == "hdr":
                    text _linea size 12 color "#ffffff" bold True
                elif _tono == "res":
                    text _linea size 12 color "#FFB74D"
                elif _tono == "warn":
                    text _linea size 12 color "#FF8A80"
                elif _tono == "ok":
                    text _linea size 12 color "#B9F6CA"
                else:
                    text _linea size 12 color "#9e9e9e"
