################################################################################
## QUEST 9 — Afinidad 30
################################################################################

label quest_violet_questprincipal_9:

    $ ocultar_hud()
    window show

    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    
    show mc_parado_base b_hablando
    mc "Violet te queria"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Hablar de mi trasero?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No, jajaja ¿Por que lo dices?"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¡Fue de lo único que hablaste!"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Me perdi en el cuando lo vi..."
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Sabia..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "En realidad te queria preguntar de que personaje si te gustaria ir"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No lo sé... me da vergüenza solo de pensarlo"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Pero podriamos buscar alguno no tan llamativo, aunque con ese trasero va a ser difícil jajajaja"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Callate!"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No te enojes, ahora se con que molestarte"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Ya no te metas mas con mi trasero"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Hey... no te metás en mi relación con tu trasero, yo lo quiero y el me quiere a mi"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando
    mc "Nosotros dos somos felices jajaja"
    show mc_parado_base b_none

    violet "..."

    show violet_parada b_hablandochica
    violet "Chau"
    show violet_parada b_none

    hide violet_parada with dissolve

    piensa "Se veia bastante avergonzada jajaja"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
