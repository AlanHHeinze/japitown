################################################################################
## Herramienta Dev — Completar Quests
################################################################################

init python:

    def dev_listar_quests():
        items = []
        for npc_id in ["violet", "jasmine", "monica"]:
            qs = sorted(
                [q for q in store.sistema_quests.quests.values() if q.npc_id == npc_id],
                key=lambda q: q.numero_quest
            )
            if not qs:
                continue
            items.append(("header", npc_id.capitalize(), npc_id))
            for q in qs:
                items.append(("quest", q.id, q.nombre, q.numero_quest, q.completada, q.activa, npc_id))
        return items


label dev_completar_quest_label(npc_id):
    $ completar_quest_actual(npc_id)
    return


screen herramienta_quests():
    zorder 289
    modal True

    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        background "#00000066"
        action Hide("herramienta_quests")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 780
        ysize 660
        background "#0d0d1eFF"
        padding (0, 0)

        vbox:
            xfill True
            yfill True

            frame:
                xfill True
                background "#1a1a3aFF"
                padding (20, 14)
                hbox:
                    xfill True
                    yalign 0.5
                    text "Dev — Completar Quests" size 20 color "#4FC3F7" bold True yalign 0.5 xfill True
                    textbutton "Cerrar":
                        action Hide("herramienta_quests")
                        background "#FF5252AA"
                        hover_background "#FF5252FF"
                        text_color "#ffffff"
                        text_size 16
                        padding (14, 6)

            viewport:
                xfill True
                yfill True
                scrollbars "vertical"
                mousewheel True
                yinitial 0.0

                vbox:
                    xfill True
                    spacing 2

                    $ _dq_items = dev_listar_quests()

                    for _dq_item in _dq_items:

                        if _dq_item[0] == "header":
                            null height 4
                            frame:
                                xfill True
                                background "#1e1e3aFF"
                                padding (14, 6)
                                text _dq_item[1] size 16 color "#FFB74D" bold True

                        else:
                            $ _dq_nombre = _dq_item[2]
                            $ _dq_num    = _dq_item[3]
                            $ _dq_done   = _dq_item[4]
                            $ _dq_activa = _dq_item[5]
                            $ _dq_npcid  = _dq_item[6]
                            $ _dq_label  = (_dq_nombre + "  (Q" + str(_dq_num) + ")")

                            if _dq_done:
                                frame:
                                    xfill True
                                    background "#0f2b0fCC"
                                    padding (14, 10)
                                    text ("✓  " + _dq_label) size 15 color "#4CAF50"

                            elif _dq_activa:
                                textbutton ("▶  " + _dq_label + "  — Completar"):
                                    xfill True
                                    action Call("dev_completar_quest_label", _dq_npcid)
                                    background "#1a3a1aCC"
                                    hover_background "#2a5a2aCC"
                                    text_color "#88DD88"
                                    text_hover_color "#ffffff"
                                    text_size 15
                                    text_xalign 0.0
                                    padding (14, 10)

                            else:
                                frame:
                                    xfill True
                                    background "#111122CC"
                                    padding (14, 10)
                                    text ("○  " + _dq_label) size 15 color "#555577"
