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
## PUESTA EN ESCENA: Monica en right, Violet en el centro, el MC en su posicion
## de siempre. Monica nunca se gira (los dos le quedan a la izquierda). Violet
## mira a Monica (centro_npc_flip) cuando le habla o la discute, y al MC
## (centro_npc) cuando el toma la conversacion. Cuando Monica se va, Violet se
## corre a right y se da vuelta para hablar de frente con el MC.
##
## LA COCINA ES UNA ESCENA (imagenes de pantalla completa), no sprites: al
## llegar se ve el desastre con Violet sola (`base`), el MC habla desde afuera
## del cuadro, y cuando ella lo mira (`mirando`) contesta con la boca de la
## escena. Despues de "Una limpieza mas tarde" vuelven los sprites, ya de tarde.


# La escena de la cocina. Por RUTA EXPLICITA y con nombre propio (ver amor 5).
# Van en master sin prefijo de personaje: una escena no se tiñe por horario.
image va10_cocina_base = "images/quest/violet/amor10/escena_cocina_amor10_base.jpg"
image va10_cocina_mirando = "images/quest/violet/amor10/escena_cocina_amor10_mirando.jpg"
image va10_cocina_boca = "images/quest/violet/amor10/escena_cocina_amor10_boca.webp"


init python:

    def _gl_trigger_violet_amor_10():
        """
        Trigger de game_loop: la escena arranca al ENTRAR al living por la
        mañana, con las dos presentes.

        Se piden las dos en casa_living y no "en la casa": la rutina de la quest
        ya las pone ahi, asi que si alguna falta es porque algo la saco (una
        restriccion, otra quest) y en ese caso la escena no deberia dispararse.
        """
        # Mañana, MC en el living, Violet y Monica en el living y no ocultas:
        # demandas de la quest, las aplica la capa 2.
        if not quest_lista_para_boton("violet_amor_02"):
            return None
        return "quest_violet_amor_02"


init 5 python:

    registrar_trigger_game_loop("violet_amor_10_encuentro",
                                _gl_trigger_violet_amor_10,
                                quest_id="violet_amor_02")


label quest_violet_amor_02:

    $ ocultar_hud()
    window show

    # Living con el fondo del horario actual: el trigger solo salta estando ahi.
    $ _va10_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va10_bg

    # Las dos ya estaban charlando cuando el MC sube: entran sin transicion.
    show monica_parada c_rbase_base o_base b_none at right

    # Violet al centro, mirando a Monica: estaban discutiendo. centro_npc_flip
    # y no un `xzoom` suelto, para que al volver a centro_npc no le quede el
    # espejado heredado.
    show violet_parada c_rbase_brazoscruzados ca_base o_base b_none at centro_npc_flip

    # `with None` cierra acá el fondo y las dos chicas, sin transicion.
    #
    # HACE FALTA: un `with` arrastra TODO lo pendiente desde la ultima
    # interaccion, asi que sin esta linea el sprite_normal de abajo se llevaba
    # tambien el fondo y a las dos, y entraban los tres juntos. Con el corte
    # acá, la transicion queda solo para el MC.
    with None

    # El MC con sprite_normal: es el unico que acaba de entrar.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with sprite_normal

    show violet_parada b_hablando
    violet "Te dije que yo no fui esta vez..."
    show violet_parada b_none

    # El MC toma la conversacion: Violet se da vuelta a mirarlo.
    show violet_parada at centro_npc
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "¿Qué pasó?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show monica_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    monica "Alguien se levantó con hambre a la noche y dejó toda la cocina sucia"
    show monica_parada b_hablandochica
    monica "¿Fuiste tú, [mc_name]?"
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_asustado with sprite_normal
    mc "No, solo bajé por un vaso de agua"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    # Le contesta a Monica (la excusa de Jasmine): la vuelve a mirar.
    show violet_parada at centro_npc_flip
    show violet_parada b_hablando c_rbase_pensando with sprite_normal
    violet "Ayer Jasmine entrenó mucho y eso le suele dar mucho hambre"
    show violet_parada b_none c_rbase_base with sprite_normal

    piensa "Jajaja fue ella, siempre le solía echar la culpa de todo a Jasmine"

    show monica_parada b_hablandochica
    monica "Si hay algo que no es Jasmine, es desordenada"
    show monica_parada b_none

    show violet_parada b_hablando
    violet "Entonces no te vas a enojar con ella por la única vez que hace algo así, quizás estaba muy dormida"
    show violet_parada b_none

    show monica_parada b_hablandochica c_rbase_brazoscintura with sprite_normal
    monica "¿En serio?"
    show monica_parada b_none

    # El MC se mete a defenderla: Violet lo mira.
    show violet_parada at centro_npc
    show mc_parado_base b_hablando c_rbase_idea with sprite_normal
    mc "Cuando yo subía ella estaba bajando y se la veía bastante dormida"
    show mc_parado_base b_abiertachica c_rbase_base with sprite_normal
    mc "Pero no te preocupes ahora nos encargamos de ordenar todo nosotros"
    show mc_parado_base b_none

    # Se suma, hablandole a Monica: la vuelve a mirar hasta que se va.
    show violet_parada at centro_npc_flip
    show violet_parada b_hablando c_rbase_idea with sprite_normal
    violet "Sí, Jasmine siempre hace todo por nosotros"
    show violet_parada b_hablandochica
    violet "Es lo mínimo que podemos hacer por ella"
    show violet_parada b_none

    show monica_parada b_hablandochica
    monica "Jajajajaja no cambiaron nada"
    show monica_parada b_hablando
    monica "Siempre culpaban a Jasmine por sus macanas, limpien todo ahora y yo me olvido del tema"
    show monica_parada b_none

    show mc_parado_base b_hablando c_rbase_confianza with sprite_normal
    mc "Sí, Mónica"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_ok with sprite_normal
    violet "Sí, nos encargamos de todo"
    show violet_parada b_none c_rbase_base with sprite_normal

    # Monica se va.
    hide monica_parada with dissolve

    # Violet se corre del centro a right y gira: deja de mirar hacia donde
    # estaba Monica y queda de frente al MC.
    show violet_parada at centro_a_right_y_giro

    show violet_parada b_hablando c_rbase_idea with sprite_normal
    violet "Bueno, vamos a ordenar el desastre de Jasmine"
    show violet_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿De Jasmine? ... ¿Segura?"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_parada b_hablando
    violet "Sí, de Jasmine"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Jajaja, dale, vamos"
    show mc_parado_base b_none

    # ── LA COCINA: la escena ─────────────────────────────────────────────────
    #
    # No caminan hasta la cocina: fundido a la escena. Sigue siendo la mañana.
    # La locacion se cambia ACA (escena=True: lo mueve la escena, no el
    # jugador) para que todo lo que sigue ya este en la cocina.

    hide violet_parada
    hide mc_parado_base
    with dissolve

    window hide
    $ sistema_locaciones.mover_a_locacion("casa_cocina", escena=True)
    scene va10_cocina_base with fade
    window show

    # El MC no se ve: habla desde afuera del cuadro.
    mc "No puedo creer el desastre que hay... ¿Qué hiciste?"

    # Violet lo mira y le contesta.
    scene va10_cocina_mirando with dissolve

    show va10_cocina_boca
    violet "Una receta que vi en Tok Tok, decía que era fácil y no resultó"
    hide va10_cocina_boca

    mc "¿Y limpiarlo en el momento tampoco funcionó?"

    show va10_cocina_boca
    violet "No, quedé estresada y de mal humor, me fui a dormir y dije me levanto temprano para limpiar todo"
    violet "Pero no me pude despertar"
    hide va10_cocina_boca

    # ── UNA LIMPIEZA MAS TARDE ───────────────────────────────────────────────
    #
    # El corte se come toda la limpieza. El cartel espera el CLICK y no un
    # `pause` con segundos: es un corte de tiempo, no un efecto — el jugador
    # decide cuando sigue.

    window hide
    scene black with fade
    show text Text(renpy.translate_string("Una limpieza más tarde"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause
    hide text with dissolve

    # ── LA COCINA, POR LA TARDE ──────────────────────────────────────────────
    #
    # El trigger exige horario 0 (mañana), asi que este avance siempre deja el
    # juego en la tarde: no hay forma de que caiga en trasnoche ni de que se
    # tope con el tope de avanzar_horario.
    $ avanzar_horario()

    # El fondo se pide DESPUES de avanzar: `background` resuelve el path con la
    # locacion y el horario del momento.
    $ _va10_bg_final = sistema_locaciones.locacion_actual.background
    scene expression _va10_bg_final

    # Los sprites vuelven JUNTO con el fondo: si el fade fuera del `scene` solo,
    # se veria la cocina vacia un frame antes que los sprites.
    show violet_parada c_rbase_base ca_base o_base b_none at right
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    with fade
    window show

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Ahora el que se quiere ir a dormir después de todo esto soy yo"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_ok with sprite_normal
    violet "Te debo una"
    show violet_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Puedo pedir lo que quiera?"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "No me mires con esa cara rara... no hay límites a lo que puedes pedir"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Cómo antes?"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_parada b_hablando c_rbase_pensando with sprite_normal
    violet "Mmmm... voy a intentarlo"
    show violet_parada b_none

    # El `with` de Violet va en su propia linea y no compartido con el del MC:
    # el `piensa` de abajo es una interaccion, asi que corta lo pendiente. Sin
    # esto, Violet desaparecia de golpe al aparecer el pensamiento y el dissolve
    # se lo llevaba solo el MC.
    hide violet_parada with dissolve

    piensa "De momento con que me deje de ignorar me conformo"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_02")

    window hide
    $ mostrar_hud()
    jump game_loop
