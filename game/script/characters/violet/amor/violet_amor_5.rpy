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
    #
    # Entra YA pensando. Antes eran dos `show`: uno en c_rbase_base sin
    # transicion y otro en c_rbase_pensando con sprite_fast, asi que el primero
    # no llegaba a verse nunca.
    show mc_parado_base c_rbase_pensando o_base b_none at mc_izquierda

    piensa "Bueno, de a poco voy logrando avances con Violet cuando la cruzo en algún lugar de la casa"
    piensa "Pero no me suele responder cuando la llamo, quiero darle su espacio pero siento que también es rendirme"
    piensa "Nos solíamos llevar muy bien como para que ahora las cosas estén así"

    # Violet sale al pasillo. Ropa base: la escena es de tarde, nunca en pijama.
    show violet_parada c_rbase_base ca_base o_base b_none at right with sprite_normal

    show violet_parada b_hablando o_arribanm
    violet "¿Qué quieres ahora?"
    show violet_parada b_none o_base

    show mc_parado_base c_rbase_avergonzado with sprite_normal
    piensa "Pensé que no iba a salir esta vez tampoco y ahora no sé qué decirle"

    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Hola, ¿cómo estás?"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "... repito ... ¿Qué quieres ahora?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Nada en particular, quería saber cómo estabas"
    show mc_parado_base b_none

    show violet_parada b_hablando o_arribanm
    violet "¿De verdad me molestas por eso?"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "¿Hasta cuándo vas a seguir con este juego?"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_pensando with sprite_normal
    violet "No sé de qué juego me hablas"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "De ignorarme y hacerte la ofendida cuando te hablo"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "Simplemente tengo ganas de ignorarte y ya"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "Si tanto problema tienes conmigo, ¿por qué no me lo dices de una vez y terminamos con esto?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Desde que te fuiste no enviaste un mensaje, una llamada, ni siquiera un saludo, y ahora que vienes, ¿tenemos que ser mejores amigos?"
    show violet_parada b_hablandochica
    violet "Creo que no funciona así"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "¿Y yo solo estuve mal? ¿No aplica lo mismo para el otro lado?"
    show mc_parado_base b_abiertachica
    mc "Tampoco recuerdo un mensaje tuyo, pero haciéndome el ofendido no voy a solucionar nada"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "La verdad es que no tengo ganas de discutir esto ahora"
    show violet_parada b_none

    # Descruza los brazos: los tomo en la discusion (mas arriba) y sin esto se
    # los quedaba puestos hasta el final, incluso en los pensamientos de cierre.
    show mc_parado_base b_hablando c_rbase_base with sprite_normal
    mc "Bueno, voy a vivir por un largo tiempo en la casa, en algún momento se va a tener que hablar"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Adiós"
    show violet_parada b_none

    hide violet_parada with dissolve

    piensa "Bueno, al menos el problema está plantado, es el primer paso a resolverlo"
    piensa "Será cosa de seguir insistiendo y esperar a que ella esté lista"

    hide mc_parado_base with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_01")

    window hide
    $ mostrar_hud()
    jump game_loop
