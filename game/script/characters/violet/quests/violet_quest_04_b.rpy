################################################################################
## Violet Quest 04_B — Hablar con Violet (perdón)
################################################################################
## Se dispara automáticamente al entrar en una locación donde esté Violet,
## o al golpear la puerta de su habitacion (Violet sale al pasillo).


################################################################################
## QUEST 04_B — Label principal
################################################################################

label quest_violet_questprincipal_04_b:

    $ desactivar_restriccion()
    $ ocultar_hud()
    window show

    # Fondo de la locación actual (funciona tanto en pasillo como en otras locaciones)
    $ _bg_conv = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_conv

    show violet_parada c_rbase_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show violet_parada b_hablandochica
    violet "Hola..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Hola, justo estaba pensando en ir a verte"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Paso algo?"
    show violet_parada b_none

    show mc_parado_base b_hablando o_abajonm c_rbase_perdon with sprite_fast
    mc "Te quería pedir perdón por la situación de la otra vez y por mirar tus cosas"
    show mc_parado_base b_none o_base c_rbase_base with sprite_fast

    show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_fast
    violet "Espera, te quiero hacer una pregunta primero"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, dime"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Por qué me trajiste ese regalo?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "Mmmmm la verdad no lo pensé mucho, simplemente sentí que ese era el regalo"
    show mc_parado_base b_abiertachica 
    mc "Y pensé que te gustaría"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica c_rbase_base with sprite_fast
    violet "¿Lo viste antes de comprarlo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, estaba en un maniqui, sé que es uno de tus personajes favoritos y quería que el regalo no fuera algo generico"
    show mc_parado_base b_abiertachica
    mc "Aparte de eso pronto se va a hacer la Japicon y pensé que seria un buen cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_pensando with sprite_fast
    violet "¿No hay otro tipo de intenciones detrás del regalo?"
    show violet_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_hablando
    mc "No ¿Qué puede haber detrás de eso? es solo un cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "El tipo de cosplay que es, es un traje digamos que muy..."
    show violet_parada b_hablando o_base ot_avergonzada
    violet "Apretado"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_fast
    mc "Pero es así el traje, no tiene nada de raro"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablandochica c_rbase_dedolabio with sprite_fast
    violet "No creo que todos sean así..." 
    show violet_parada b_hablando ot_none c_rbase_brazoscruzados with sprite_fast
    violet "Y ya te digo que no hay posibilidades que vaya a usarlo en un evento"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Por qué no me muestras que tal esta? Y te doy mi opion, seguro estas exagerando"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm c_rbase_pensando with sprite_fast
    violet "Lo voy a pensar"
    show violet_parada b_none o_base c_rbase_base with sprite_fast

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet")

    # Devolver a Violet a su rutina base (sale del pasillo para siempre)
    python:
        _nv = obtener_npc("violet")
        if _nv:
            # Limpiar todos los overrides de mañana que dejó la quest
            if hasattr(_nv, 'rutinas_quest'):
                for _d in range(7):
                    _nv.rutinas_quest.pop((_d, 0), None)
            # Forzar ubicación al valor base del dia actual
            _loc_base = _nv.rutinas.get((dia_semana_actual, horario_actual))
            _nv.locacion_actual = _loc_base if _loc_base else "casa_hviolet"

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## CHECK LOCACIÓN — Auto-trigger al entrar en locación donde esté Violet
################################################################################

label violet_quest04b_check_locacion:
    $ _violet_npc_04b = obtener_npc("violet")
    $ _loc_actual_04b = sistema_locaciones.locacion_actual.id if sistema_locaciones.locacion_actual else None
    if _violet_npc_04b and _violet_npc_04b.locacion_actual == _loc_actual_04b:
        jump quest_violet_questprincipal_04_b
    return


################################################################################
## PUERTA — Violet sale al pasillo cuando el MC golpea
################################################################################

label violet_quest04b_puerta:

    $ ocultar_hud()
    window show

    play sound "audio/sfx/door_knock_3.ogg"
    pause 0.5

    mc "Soy yo"

    violet "Ahí salgo"

    pause 0.5

    jump quest_violet_questprincipal_04_b
