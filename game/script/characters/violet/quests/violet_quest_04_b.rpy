################################################################################
## Violet Quest 04_B — Hablar con Violet (perdón)
################################################################################
## Se dispara automáticamente al entrar en una locación donde esté Violet,
## o al golpear la puerta de su habitacion (Violet sale al pasillo).


################################################################################
## QUEST 04_B — Label principal
################################################################################

label quest_violet_questprincipal_04_b:

    $ desactivar_restriccion(duenio="violet_04_b")
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
    violet "¿Pasó algo?"
    show violet_parada b_none

    show mc_parado_base b_hablando o_abajonm c_rbase_perdon with sprite_normal
    mc "Te quería pedir perdón por la situación de la otra vez y por mirar tus cosas"
    show mc_parado_base b_none o_base c_rbase_base with sprite_normal

    show violet_parada b_hablandochica c_rbase_brazoscruzados with sprite_normal
    violet "Espera, te quiero hacer una pregunta primero"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, dime"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Por qué me trajiste ese regalo?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Mmmmm la verdad no lo pensé mucho, simplemente sentí que ese era el regalo"
    show mc_parado_base b_abiertachica
    mc "Y pensé que te gustaría"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica c_rbase_base with sprite_normal
    violet "¿Lo viste antes de comprarlo?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, estaba en un maniquí, sé que es uno de tus personajes favoritos y quería que el regalo no fuera algo genérico"
    show mc_parado_base b_abiertachica
    mc "Aparte de eso pronto se va a hacer la Japicon y pensé que sería un buen cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica c_rbase_pensando with sprite_normal
    violet "¿No hay otro tipo de intenciones detrás del regalo?"
    show violet_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base b_hablando
    mc "No, ¿qué puede haber detrás de eso? Es solo un cosplay"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "El tipo de cosplay que es, es un traje digamos que muy..."
    show violet_parada b_hablando o_base ot_avergonzada
    violet "Apretado"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Pero es así el traje, no tiene nada de raro"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablandochica c_rbase_dedolabio with sprite_normal
    violet "No creo que todos sean así..."
    show violet_parada b_hablando ot_none c_rbase_brazoscruzados with sprite_normal
    violet "Y ya te digo que no hay posibilidades de que vaya a usarlo en un evento"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Por qué no me muestras qué tal está? Y te doy mi opinión, seguro estás exagerando"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm c_rbase_pensando with sprite_normal
    violet "Lo voy a pensar"
    show violet_parada b_none o_base c_rbase_base with sprite_normal

    hide violet_parada with dissolve
    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_questprincipal_04_b")

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

## DISPARO DE LA QUEST — trigger de game_loop, registrado en init.
##
## Antes esto era `label violet_quest04b_check_locacion`, al que se llegaba por
## los registros que setup_restriccion_violet_quest04b metia en el objeto de
## restriccion. Ese objeto es un slot global unico (`restriccion_quest_activa`):
## cualquier `activar_restriccion` lo reemplaza entero y cualquier
## `desactivar_restriccion` lo borra — y hay decenas de llamadas a las dos en el
## proyecto. Como accion_al_entrar corre UNA sola vez, al pasar de etapa, el
## primer contenido que corriera despues se llevaba el disparo puesto y la quest
## quedaba muerta para siempre en el panel de pistas. Mismo bug que reportaron
## los jugadores en la 0_b de Monica.
##
## La condicion es la misma de antes: estar en la misma locacion que Violet,
## dentro de la lista de locaciones donde puede estar.

init python:

    _VQ04B_LOCACIONES = ["casa_hviolet", "casa_pasilloarriba", "casa_cocina",
                         "casa_living", "casa_gym"]

    def _gl_trigger_violet_04b():
        q = store.sistema_quests.obtener_quest("violet_questprincipal_04_b")
        if not (q and q.activa and not q.completada
                and q.etapa_actual == ETAPA_BOTON_LISTO):
            return None

        loc = store.sistema_locaciones.locacion_actual
        if not loc or loc.id not in _VQ04B_LOCACIONES:
            return None

        # Con Violet OCULTA por la restriccion de otro contenido no se dispara:
        # el jugador no la ve, y ademas el label de esta quest arranca con
        # desactivar_restriccion(duenio="violet_04_b") — dispararse en medio de la cadena de
        # evento03 (que vive el mismo tramo del juego) le pisaba la maquina de
        # estados y la dejaba trabada. Se mira la locacion cruda del NPC a
        # proposito (no el tracker): la escena la pone en el lugar igual.
        if npc_esta_oculto("violet"):
            return None
        npc = store.obtener_npc("violet")
        if npc and npc.locacion_actual == loc.id:
            return "quest_violet_questprincipal_04_b"
        return None


init 5 python:
    registrar_trigger_game_loop("violet_04b", _gl_trigger_violet_04b, duenio="violet_04_b")


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
