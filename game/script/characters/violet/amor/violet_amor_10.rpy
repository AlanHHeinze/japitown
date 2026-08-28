################################################################################
## Violet — Amor 10 · "Buena relación"
################################################################################
##     archivo   violet_amor_10.rpy
##     quest     violet_amor_02          (quests_amor_violet.rpy)
##     label     quest_violet_amor_02    (lo fija el motor: "quest_" + id)
##
## Es la quest que otorga el HITO "Buena relación" (violet_hito_amor_01).
##
## DISPARADOR UNICO: un trigger de game_loop. La escena salta sola al entrar al
## living por la mañana con Violet y Monica ahi. Por eso esta quest esta
## excluida del boton generico "Charlar un rato" del menu de interaccion.
##
## LAS DOS ESTAN EN EL LIVING porque la quest les cambia la rutina mientras esta
## activa (_VIOLET_AMOR_RUTINAS en quests_amor_violet.rpy). En la practica casi
## no se nota —al entrar al living salta la escena y no da tiempo a ver el
## fondo— pero hace que el mundo sea coherente: si el jugador pasa antes por la
## cocina, no las encuentra ahi para despues verlas aparecer en el living.
##
## PUESTA EN ESCENA: Monica en right, Violet en center mirando hacia ella
## (flip), el MC en su posicion de siempre. Cuando Monica se va, Violet se corre
## a right y se da vuelta para hablar de frente con el MC.


init python:

    def _gl_trigger_violet_amor_10():
        """
        Trigger de game_loop: la escena arranca al ENTRAR al living por la
        mañana, con las dos presentes.

        Se piden las dos en casa_living y no "en la casa": la rutina de la quest
        ya las pone ahi, asi que si alguna falta es porque algo la saco (una
        restriccion, otra quest) y en ese caso la escena no deberia dispararse.
        """
        if not quest_lista_para_boton("violet_amor_02"):
            return None
        if store.horario_actual != 0:
            return None

        _loc_a10 = store.sistema_locaciones.locacion_actual
        if _loc_a10 is None or _loc_a10.id != "casa_living":
            return None

        for _npc_id_a10 in ("violet", "monica"):
            _npc_a10 = obtener_npc(_npc_id_a10)
            if not _npc_a10 or not _npc_a10.esta_en_locacion("casa_living"):
                return None
            if npc_esta_oculto(_npc_id_a10):
                return None

        return "quest_violet_amor_02"


init 5 python:

    registrar_trigger_game_loop("violet_amor_10_encuentro",
                                _gl_trigger_violet_amor_10)


label quest_violet_amor_02:

    $ ocultar_hud()
    window show

    # Living con el fondo del horario actual: el trigger solo salta estando ahi.
    $ _va10_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va10_bg

    # Las dos ya estaban charlando cuando el MC sube: entran sin transicion.
    show monica_parada c_rbase_base o_base b_none at right

    # Violet al centro, espejada para quedar mirando hacia Monica.
    show violet_parada c_rbase_brazoscruzados ca_base o_base b_none at center:
        xzoom -1.0

    # El MC con sprite_normal: es el que acaba de entrar.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    show violet_parada b_hablando 
    violet "Te dije que yo no fui esta vez..."
    show violet_parada b_none

    show mc_parado_base b_hablando 
    mc "¿Que paso?"
    show mc_parado_base b_none

    show monica_parada b_hablando c_rbase_brazoscruzados with sprite_fast
    monica "Alguien se levanto con habre a la noche y dejo toda la cocina sucia"
    show monica_parada b_hablandochica
    monica "¿Fuiste vos [mc_name]?"
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_asustado with sprite_fast
    mc "No, solo baje por un vaso de agua"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando c_rbase_pensando with sprite_fast
    violet "Ayer Jasmine entreno mucho y eso le suele dar mucho hambre"
    show violet_parada b_none c_rbase_base with sprite_fast

    piensa "Jajaja fue ella, siempre le solia echar la culpa de todo a Jasmine"

    show monica_parada b_hablandochica 
    monica "Si hay algo que no es Jasmine, es desordenada"
    show monica_parada b_none

    show violet_parada b_hablando 
    violet "Entonces no te vas a enojar con ella por la unica vez que hace algo asi, quizas estaba muy dormida"
    show violet_parada b_none

    show monica_parada b_hablandochica c_rbase_brazoscintura with sprite_fast
    monica "..."
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_idea with sprite_fast
    mc "Cuando yo subia ella estaba bajando y se la veia bastante dormida"
    show mc_parado_base b_abiertachica c_rbase_base with sprite_fast
    mc "Pero no te preocupes ahora nos encargamos de ordenar todo nosotros"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_idea with sprite_fast
    violet "Si Jasmine siempre hace todo por nosotros"
    show violet_parada b_hablandochica 
    violet "Es lo minimo que podemos hacer por ella"
    show violet_parada b_none

    show monica_parada b_hablandochica with sprite_fast
    monica "Jajajajaja no cambiaron nada"
    show monica_parada b_hablando
    monica "Siempre culpaban a Jasmine por sus macanas, limpien todo ahora y yo me olvido del tema"
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_fast
    mc "Si"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando c_rbase_ok with sprite_fast
    violet "Si, nos encargamos de todo"
    show violet_parada b_none c_rbase_base with sprite_fast

    # Monica se va.
    hide monica_parada with dissolve

    # Violet se corre del centro a right y gira: deja de mirar hacia donde
    # estaba Monica y queda de frente al MC.
    show violet_parada at centro_a_right_y_giro

    show violet_parada b_hablando 
    violet "Bueno, vamos a ordenar el desastre de Jasmine"
    show violet_parada b_none

    show mc_parado_base b_hablando 
    mc "¿De Jasmine? ... ¿Segura?"
    show mc_parado_base b_none

    show violet_parada b_hablando 
    violet "Gracias, te debo una"
    show violet_parada b_none

    show mc_parado_base b_hablando 
    mc "¿Como antes?"
    show mc_parado_base b_none

    show violet_parada b_hablando 
    violet "Solo si me ayudas a limpiar"
    show violet_parada b_none

    show mc_parado_base b_hablando 
    mc "Jajaja dale, vamos"
    show mc_parado_base b_none

    hide violet_parada
    hide mc_parado_base
    with dissolve

    # Se van juntos y la escena cierra mas tarde, en la cocina. El trigger exige
    # horario 0 (mañana), asi que este avance siempre deja el juego en la tarde:
    # no hay forma de que caiga en trasnoche ni de que se tope con el tope de
    # avanzar_horario.
    $ avanzar_horario()
    $ sistema_locaciones.mover_a_locacion("casa_cocina")

    # El fondo se pide DESPUES de mover y de avanzar: `background` resuelve el
    # path con la locacion y el horario del momento, asi que pedirlo antes
    # traeria el living por la mañana.
    $ _va10_bg_final = sistema_locaciones.locacion_actual.background
    scene expression _va10_bg_final with fade

    $ completar_quest_actual("violet", quest_id="violet_amor_02")

    window hide
    $ mostrar_hud()
    jump game_loop
