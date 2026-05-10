################################################################################
## Sistema de Talk — Screens
################################################################################

screen menu_talk_npc(npc, config, estado, especiales, preview_opcion, preview_resultado, npc_id, sprite_npc):
    modal True

    # Overlay que dimea el fondo y el sprite del MC (que están en master layer)
    add Solid("#00000077")

    # Sprite del NPC encima del overlay
    if sprite_npc:
        add sprite_npc:
            xalign 0.85
            yalign 1.0

    # Panel de opciones
    frame:
        xalign 0.25
        yalign 0.5
        background "#0288D1EE"
        padding (30, 20)

        vbox:
            spacing 15

            # Nombre del NPC
            text npc.nombre size 32 color "#FFF8E1" bold True xalign 0.5 outlines [(2, "#1565C0", 0, 0)]

            # Estado actual del NPC
            if estado:
                text estado.nombre size 18 color "#B3E5FC" xalign 0.5 italic True

            null height 5
            frame:
                xsize 300
                ysize 2
                background "#4FC3F7"
            null height 10

            # Stats del NPC
            $ _t_emojis = {"stat1": "❤️", "stat2": "💋"}
            hbox:
                spacing 20
                xalign 0.5
                hbox:
                    spacing 4
                    text "[_t_emojis['stat1']]" size 16
                    text "[npc.estado[npc.nombre_stat1]]" size 14 color "#66BB6A" bold True
                hbox:
                    spacing 4
                    text "[_t_emojis['stat2']]" size 16
                    text "[npc.estado[npc.nombre_stat2]]" size 14 color "#FFB74D" bold True

            null height 8

            # 5 opciones base
            vbox:
                spacing 8
                xsize 300

                for opcion_id in OPCIONES_BASE_IDS:
                    $ _tm = sistema_talk.consultar_memoria_mc(npc_id, estado.id if estado else "", opcion_id)
                    $ _tp = (opcion_id == preview_opcion)

                    button:
                        xfill True
                        background "#1565C0"
                        hover_background "#FFB74D"
                        padding (15, 10)
                        action Return(opcion_id)

                        hbox:
                            spacing 8
                            xfill True
                            text OPCIONES_BASE_TEXTO[opcion_id] size 18 color "#ffffff"
                            # Memoria del MC (verde): recuerda el resultado de este combo
                            if _tm:
                                text RESULTADO_TEXTO[_tm] size 13 color "#A5D6A7" italic True xalign 1.0
                            # Carisma preview (amarillo): resultado probable de esta opción
                            elif _tp and preview_resultado:
                                text RESULTADO_TEXTO[preview_resultado] size 13 color "#FFF176" italic True xalign 1.0

            # Opciones especiales (separador + botones adicionales)
            if especiales:
                null height 5
                frame:
                    xfill True
                    ysize 1
                    background "#00968844"
                null height 5

                for oesp in especiales:
                    button:
                        xfill True
                        background "#009688"
                        hover_background "#4DB6AC"
                        padding (15, 10)
                        action Return(("especial", oesp))
                        text oesp.texto size 18 color "#ffffff"

            null height 10

            textbutton "Cerrar":
                xalign 0.5
                action Return("cerrar")
                text_size 20
                text_color "#FFF8E1"
