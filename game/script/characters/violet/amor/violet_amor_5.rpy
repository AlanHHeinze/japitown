################################################################################
## Violet — Amor 5 · "¿Mejor?"
################################################################################
## Primera quest de la linea de amor. El archivo se llama por el UMBRAL (amor 5)
## porque es como se la nombra al hablar de ella; el id de la quest y el nombre
## del label van por numero de quest:
##
##     archivo   violet_amor_5.rpy
##     quest     violet_amor_01          (quests_amor_violet.rpy)
##     label     quest_violet_amor_01    (lo fija el motor: "quest_" + id)
##
## DISPARADOR UNICO: la opcion "Llamarla" del menu de puerta de Violet, que solo
## aparece por la tarde y con ella en su habitacion (ver puertas_violet.rpy).
## Por eso esta quest esta excluida del boton generico "Charlar un rato" del
## menu de interaccion: la escena asume el pasillo de arriba, y desde el menu se
## podria disparar en cualquier locacion.
##
## La escena entera pasa en el pasillo, en el horario actual: el MC la llama
## desde afuera, piensa un momento y ella sale.


label quest_violet_amor_01:

    $ ocultar_hud()
    window show

    # Pasillo de arriba con el fondo del horario actual. Se llega acá desde la
    # puerta, asi que el MC ya esta parado ahi.
    $ _va5_loc = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ _va5_bg = _va5_loc.background if _va5_loc else "#1a1a1a"
    scene expression _va5_bg

    # El MC en su posicion de conversacion: entra solo, pero se queda donde va a
    # estar cuando Violet salga, para no moverse a mitad de escena.
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    show mc_parado_base c_rbase_pensando with sprite_fast
    piensa "Bueno de a poco voy logrando avances con Violet cuando la cruzo en algun lugar de la casa"
    piensa "Pero no me suele responder cuando la llamo, quiero darle su espacio pero sinto que tambien es rendirme"
    piensa "Nos soliamos llevar muy bien como para que ahora las cosas esten asi"

    # Violet sale al pasillo. Ropa base: la escena es de tarde, nunca en pijama.
    show violet_parada c_rbase_base ca_base o_base b_none at right with sprite_normal
    
    show violet_parada b_hablando o_arribanm
    violet "¿Que queres ahora?"
    show violet_parada b_none o_base

    show mc_parado_base c_rbase_base with sprite_fast
    piensa "Pense que no iba a salir esta vez tampoco y ahora no se que decirle"

    show mc_parado_base b_hablando 
    mc "Hola ¿Como estas?"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_fast
    violet "... repito ... ¿Que queres ahora?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Nada en particular, queria saber como estabas"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "¿De verad me molestas por eso?"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_fast
    mc "No, bueno no pense que me ibas a responder..."
    show mc_parado_base b_abiertachica
    mc "Y no tenia un tema de conversacion pensado"
    show mc_parado_base b_none c_rbase_base with sprite_fast

    show violet_parada b_hablando c_rbase_pensando with sprite_fast
    violet "¿Y para que me llamaste si no tenias un tema de conversacion planeado?"
    show violet_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_hablando 
    mc "Para ver si me respondias"
    show mc_parado_base b_none

    show violet_parada b_hablando 
    violet "Raro..."
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_fast
    mc "Rara vos, sigo sin entender que te pasa y me vengo esforzando mucho para poder llevarnos como antes"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_pensando with sprite_fast
    violet "Si te es mucho esfuerzo entonces dejalo de hacer"
    show violet_parada b_none c_rbase_base with sprite_fast

    show mc_parado_base b_hablando
    mc "No, hasta que la situacion no cambie voy a seguir insistiendo"
    show mc_parado_base b_abiertachica
    mc "Vas a tener que vivir con eso"
    show mc_parado_base b_none

    violet "..."

    show mc_parado_base b_hablando
    mc "¿No vas a decir nada?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "No"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Bueno tendre que seguir intentandolo dia a dia"
    show mc_parado_base b_abiertachica
    mc "Nos vemos en el proximo intento"
    show mc_parado_base b_none

    hide mc_parado_base with dissolve
    hide violet_parada with dissolve

    #violet pensando


    $ completar_quest_actual("violet", quest_id="violet_amor_01")

    window hide
    $ mostrar_hud()
    jump game_loop
