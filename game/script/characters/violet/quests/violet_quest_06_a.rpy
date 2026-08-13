################################################################################
## Quest 06_a — Las entradas
################################################################################

# Secuencias del beso — un solo grupo por secuencia para pasar de un frame al
# siguiente sin hide ni reposicionar (mismo patrón que el layeredimage quest06).
# Uso: show beso_amor f1 / show beso_amor f2 ... con pausa entre cada frame.
layeredimage beso_amor:
    group secuencia:
        attribute f1 default:
            "images/quest/violet/quest06/beso_amor1.webp"
        attribute f2:
            "images/quest/violet/quest06/beso_amor2.webp"
        attribute f3:
            "images/quest/violet/quest06/beso_amor3.webp"
        attribute f4:
            "images/quest/violet/quest06/beso_amor4.webp"
        attribute f5:
            "images/quest/violet/quest06/beso_amor5.webp"
        attribute f6:
            "images/quest/violet/quest06/beso_amor6.webp"
        attribute f7:
            "images/quest/violet/quest06/beso_amor7.webp"

layeredimage beso_deseo:
    group secuencia:
        attribute f1 default:
            "images/quest/violet/quest06/beso_deseo1.webp"
        attribute f2:
            "images/quest/violet/quest06/beso_deseo2.webp"
        attribute f3:
            "images/quest/violet/quest06/beso_deseo3.webp"
        attribute f4:
            "images/quest/violet/quest06/beso_deseo4.webp"
        attribute f5:
            "images/quest/violet/quest06/beso_deseo5.webp"
        attribute f6:
            "images/quest/violet/quest06/beso_deseo6.webp"
        attribute f7:
            "images/quest/violet/quest06/beso_deseo7.webp"


################################################################################
## LABEL PRINCIPAL — llamado por el botón Listo del HUD
################################################################################

label quest_violet_questprincipal_06_a:
    jump violet_quest06a_hablar


################################################################################
## PUERTA — MC entra a la habitacion de Violet
################################################################################

label violet_quest06a_puerta:

    $ ocultar_hud()
    window show

    mc "Violet..."
    violet "¿Qué?"
    mc "Tengo que contarte algo. ¿Puedo pasar?"
    violet "Pasa"

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet with fade

    jump violet_quest06a_habitacion


################################################################################
## HABLAR — Acceso directo desde dentro de la habitacion
################################################################################

label violet_quest06a_hablar:

    $ ocultar_hud()
    window show

    $ _loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet = _loc_hviolet.background if _loc_hviolet else "#1a1a1a"
    scene expression _bg_hviolet

    jump violet_quest06a_habitacion


################################################################################
## HABITACIÓN — Conversacion inicial con evaluación de stat al final
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
    violet "No te entiendo ¿Por qué lo haces?"
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
    mc "Quiero compartir momentos contigo, la Japicon es uno de esos momentos y no lo voy a dejar pasar por un error"
    show mc_parado_base b_abiertachica
    mc "Quiero que lo de los cosplay quede atrás"
    show mc_parado_base b_none

    # Beso amor — la escena entra con fade en el primer frame y luego la secuencia
    # avanza frame a frame con show normal y una pausa de 0.5 entre cada uno.
    window hide
    scene expression _bg_hviolet
    show beso_amor f1 at center
    with fade
    pause 0.5
    show beso_amor f2 with sprite_normal
    pause 0.5
    show beso_amor f3 with sprite_normal
    pause 0.5
    show beso_amor f4 with sprite_normal
    pause 0.5
    show beso_amor f5 with sprite_normal
    pause 0.5
    show beso_amor f6 with sprite_normal
    pause 0.5
    show beso_amor f7 with sprite_normal
    pause 0.5

    # Refrescar de nuevo con fade: vuelven los layered de Violet y el MC como estaban
    scene expression _bg_hviolet
    show violet_parada c_pijama_verguenza ca_pijama o_abiertos b_contenta ot_avergonzada at right
    show mc_parado_base c_rbase_base o_base b_felizcerrada  at mc_izquierda
    with fade

    piensa "No puedo creer que di el paso, fue un impulso y no se como va a reaccionar Violet"

    show violet_parada b_hablandochica o_abiertos 
    violet "Está bien... Voy a ir contigo a la Japicon"
    show violet_parada b_contenta

    show mc_parado_base b_abiertachica
    mc "Bueno nos vemos luego"
    show mc_parado_base b_none

    $ cambiar_stat1("violet", 4, reserva=True)
    jump violet_quest06a_cierre


################################################################################
## CAMINO DESEO — stat2 (Deseo) mayor a stat1 (Amor)
################################################################################

label violet_quest06a_camino_deseo:

    show mc_parado_base b_hablando
    mc "Hoy de nuevo en la casa, compartiendo momentos contigo, entendí que me equivoqué al enojarme cuando me fui y arruine la relación"
    show mc_parado_base b_abiertachica
    mc "No voy a dejar que pase eso otra vez"
    show mc_parado_base b_none

    # Beso deseo — la escena entra con fade en el primer frame y luego la secuencia
    # avanza frame a frame con show normal y una pausa de 0.5 entre cada uno.
    window hide
    scene expression _bg_hviolet
    show beso_deseo f1 at center
    with fade
    pause 0.5
    show beso_deseo f2 with sprite_normal
    pause 0.5
    show beso_deseo f3 with sprite_normal
    pause 0.5
    show beso_deseo f4 with sprite_normal
    pause 0.5
    show beso_deseo f5 with sprite_normal
    pause 0.5
    show beso_deseo f6 with sprite_normal
    pause 0.5
    show beso_deseo f7 with sprite_normal
    pause 0.5

    # Refrescar de nuevo con fade: vuelven los layered de Violet y el MC como estaban
    scene expression _bg_hviolet
    show violet_parada c_pijama_verguenza ca_pijama o_abiertos b_contenta ot_avergonzada at right
    show mc_parado_base c_rbase_base o_base b_felizcerrada  at mc_izquierda
    with fade

    piensa "No puedo creer que di el paso, fue un impulso y no se como va a reaccionar Violet"

    show violet_parada b_hablandochica o_abiertos 
    violet "Está bien... Voy a ir contigo a la Japicon"
    show violet_parada b_none

    show mc_parado_base b_abiertachica
    mc "Bueno nos vemos luego"
    show mc_parado_base b_none

    $ cambiar_stat2("violet", 4, reserva=True)
    jump violet_quest06a_cierre


################################################################################
## CIERRE — El MC huye a su habitacion
################################################################################

label violet_quest06a_cierre:

    # Mover al MC a su habitacion
    $ sistema_locaciones.mover_a_locacion("casa_hmc")

    # Mostrar la habitacion con el MC en el centro
    $ _bg_hmc = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_hmc with fade
    
    show mc_parado_base c_rbase_base at center with dissolve
    pause 0.5
    show mc_parado_base c_rbase_facepalm o_abajonm b_seria with sprite_fast
    piensa "Soy un idiota, luego de darle un beso ¿mi mejor plan es huir?"
    piensa "Ahora voy a estar a la espectativa de la reaccion de Violet"

    # Completar la quest
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_06_a")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## TEST — salto directo al contenido de la 06_a (desde el menú de cheats)
################################################################################

label test_quest06a_violet:
    # Cerrar el celular si quedó abierto
    $ renpy.hide_screen("menu_cheats")
    $ renpy.hide_screen("lista_contactos_mensajes")
    $ renpy.hide_screen("menu_celular")
    $ menu_celular_abierto = False

    # Restaurar backgrounds por si un test anterior (ej. 08_a) quedó a medias
    python:
        for _loc_id, _bg_orig in dict(getattr(store, 'vq8a_bgs_originales', {})).items():
            _loc_obj = sistema_locaciones.obtener_locacion(_loc_id)
            if _loc_obj:
                _loc_obj.background_base = _bg_orig
        store.vq8a_bgs_originales = {}

    # Limpiar restricción de un test previo
    $ desactivar_restriccion()

    # Forzar la 06_a como la ÚNICA quest activa de Violet, en ETAPA_BOTON_LISTO
    # (asi el cierre la completa correctamente con completar_quest_actual("violet", quest_id="violet_questprincipal_06_a"))
    python:
        for _q in sistema_quests.quests.values():
            if _q.npc_id == "violet" and _q.activa and _q.id != "violet_questprincipal_06_a":
                _q.activa = False
        _q06a = sistema_quests.obtener_quest("violet_questprincipal_06_a")
        if _q06a:
            _q06a.completada = False
            _q06a.activa = True
            _q06a.etapa_actual = ETAPA_BOTON_LISTO
            _q06a.dia_inicio = getattr(store, 'dias_totales', 1)

    # Contexto: Violet y el MC en la habitacion de Violet, de noche
    $ horario_actual = 2
    $ obtener_npc("violet").locacion_actual  = "casa_hviolet"
    $ obtener_npc("monica").locacion_actual  = "fuera"
    $ obtener_npc("jasmine").locacion_actual = "fuera"
    $ actualizar_rutinas_npcs()
    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    jump violet_quest06a_hablar
