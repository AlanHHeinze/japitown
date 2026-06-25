################################################################################
## Quest 06_a — Las entradas
################################################################################

# Imágenes de la quest 06
image beso_amor = "images/quest/violet/quest06/beso_amor.png"
image beso_deseo = "images/quest/violet/quest06/beso_deseo.png"


################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_06_a:
    jump violet_quest06a_hablar


################################################################################
## PUERTA — MC entra a la habitación de Violet
################################################################################

label violet_quest06a_puerta:

    $ ocultar_hud()
    window show

    mc "Violet..."
    violet "¿Qué?"
    mc "Tengo que contarte algo. ¿Puedo pasar?"
    violet "Pasá"

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet with fade

    jump violet_quest06a_habitacion


################################################################################
## HABLAR — Acceso directo desde dentro de la habitación
################################################################################

label violet_quest06a_hablar:

    $ ocultar_hud()
    window show

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet

    jump violet_quest06a_habitacion


################################################################################
## HABITACIÓN — Conversación inicial con evaluación de stat al final
################################################################################

label violet_quest06a_habitacion:

    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base b_hablando
    mc "Violet, compré las entradas"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_pijama_base with sprite_fast
    violet "¿Las entradas?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Para la Japicon. No hace falta que uses ningún cosplay, quiero que vayamos juntos"
    show mc_parado_base b_none

    show violet_parada o_abiertos b_none ot_avergonzada with sprite_normal

    pause 0.5

    show violet_parada b_hablandochica
    violet "Últimamente estás actuando un poco impulsivo..."
    show violet_parada b_none

    show violet_parada b_hablandochica 
    violet "No te entiendo ¿Por qué lo hacés?"
    show violet_parada b_none

    if obtener_stat1("violet") >= obtener_stat2("violet"):
        jump violet_quest06a_camino_amor
    else:
        jump violet_quest06a_camino_deseo


################################################################################
## CAMINO AMOR — stat1 (Amor) mayor o igual a stat2 (Deseo)
################################################################################

label violet_quest06a_camino_amor:

    show mc_parado_base b_hablando
    mc "Quiero compartir momentos con vos, la Japicon es uno de esos momentos y no lo voy a dejar pasar por un error"
    show mc_parado_base b_abiertachica
    mc "Quiero que lo de los cosplay quede atras"
    show mc_parado_base b_none

    # Beso amor — refrescar la escena con fade y cargar el sprite del beso centrado
    window hide
    scene expression _bg_hviolet
    show beso_amor at center
    with fade
    pause 2.0

    # Refrescar de nuevo con fade: vuelven los layered de Violet y el MC como estaban
    scene expression _bg_hviolet
    show violet_parada c_pijama_verguenza ca_pijama o_abiertos b_contenta ot_avergonzada at right
    show mc_parado_base c_rbase_base o_base b_felizcerrada  at mc_izquierda
    with fade

    piensa "No puedo creer que di el paso, fue un impulso y no se como va a reaccionar Violet"

    show violet_parada b_hablandochica o_abiertos 
    violet "Está bien... Voy a ir con vos a la Japicon"
    show violet_parada b_contenta

    show mc_parado_base b_abiertachica
    mc "Bueno nos vemos luego"
    show mc_parado_base b_none

    $ cambiar_stat1("violet", 8)
    jump violet_quest06a_cierre


################################################################################
## CAMINO DESEO — stat2 (Deseo) mayor a stat1 (Amor)
################################################################################

label violet_quest06a_camino_deseo:

    show mc_parado_base b_hablando
    mc "Hoy de nuevo en la casa, compartiendo momentos con vos, entendí que me equivoqué al enojarme cuando me fui y arruine la relación"
    show mc_parado_base b_abiertachica
    mc "No voy a dejar que pase eso otra vez"
    show mc_parado_base b_none

    # Beso deseo — refrescar la escena con fade y cargar el sprite del beso centrado
    window hide
    scene expression _bg_hviolet
    show beso_deseo at center
    with fade
    pause 2.0

    # Refrescar de nuevo con fade: vuelven los layered de Violet y el MC como estaban
    scene expression _bg_hviolet
    show violet_parada c_pijama_verguenza ca_pijama o_abiertos b_contenta ot_avergonzada at right
    show mc_parado_base c_rbase_base o_base b_felizcerrada  at mc_izquierda
    with fade

    piensa "No puedo creer que di el paso, fue un impulso y no se como va a reaccionar Violet"

    show violet_parada b_hablandochica o_abiertos 
    violet "Está bien... Voy a ir con vos a la Japicon"
    show violet_parada b_none

    show mc_parado_base b_abiertachica
    mc "Bueno nos vemos luego"
    show mc_parado_base b_none

    $ cambiar_stat2("violet", 4)
    jump violet_quest06a_cierre


################################################################################
## CIERRE — El MC huye a su habitación
################################################################################

label violet_quest06a_cierre:

    # Mover al MC a su habitación
    $ sistema_locaciones.mover_a_locacion("casa_hmc")

    # Mostrar la habitación con el MC en el centro
    $ _bg_hmc = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_hmc with fade
    
    show mc_parado_base c_rbase_base at center with dissolve
    pause 0.5
    show mc_parado_base c_rbase_facepalm o_abajonm b_seria with sprite_fast
    piensa "Soy un idiota, luego de darle un beso ¿mi mejor plan es huir?"
    piensa "Ahora voy a estar a la espectativa de la reaccion de Violet"

    # Completar la quest
    $ completar_quest_actual("violet")

    window hide
    $ mostrar_hud()
    jump game_loop
