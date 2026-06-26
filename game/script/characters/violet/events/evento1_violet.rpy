################################################################################
## Evento 1 de Violet - Casco VR
################################################################################
## Al completar quest 0 de Violet, se desbloquea el casco VR en la tienda y
## el contacto "Libre Mercado" envia un mensaje avisando.
## Cuando el jugador usa el casco de noche en su habitacion y Violet esta en
## la suya, se dispara este evento.
## Despues de la primera vez, el jugador puede invitar a Violet desde el menu
## de interaccion para activar la repeticion.

################################################################################
## Imagenes
################################################################################

image bg_casa_noche_hmc_zoom = "images/bg/casa/bg_casa_noche_hmc_zoom.png"

layeredimage mc_base_parado_vr:
    group pose:
        attribute vr1 default:
            "images/eventos/violet/evento1/mc_base_parado_vr1.png"
        attribute vr2:
            "images/eventos/violet/evento1/mc_base_parado_vr2.png"
        attribute vr3:
            "images/eventos/violet/evento1/mc_base_parado_vr3.png"

layeredimage violet_evento_01_jugandosolo:
    group pose:
        attribute j1 default:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo1.png"
        attribute j2:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo2.png"
        attribute j3:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo3.png"
        attribute j4:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo4.png"
        attribute j5:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo5.png"
        attribute j6:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo6.png"
        attribute j7:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo7.png"

layeredimage violet_evento_01_violetvr:
    group pose:
        attribute vr1 default:
            "images/eventos/violet/evento1/violet_evento_01_violetvr1.png"
        attribute vr2:
            "images/eventos/violet/evento1/violet_evento_01_violetvr2.png"
        attribute vr3:
            "images/eventos/violet/evento1/violet_evento_01_violetvr3.png"
        attribute vr4:
            "images/eventos/violet/evento1/violet_evento_01_violetvr4.png"
        attribute vr5:
            "images/eventos/violet/evento1/violet_evento_01_violetvr5.png"
        attribute vr6:
            "images/eventos/violet/evento1/violet_evento_01_violetvr6.png"
        attribute vr7:
            "images/eventos/violet/evento1/violet_evento_01_violetvr7.png"
        attribute vr8:
            "images/eventos/violet/evento1/violet_evento_01_violetvr8.png"
        attribute vr9:
            "images/eventos/violet/evento1/violet_evento_01_violetvr9.png"
        attribute vr10:
            "images/eventos/violet/evento1/violet_evento_01_violetvr10.png"
        attribute vr11:
            "images/eventos/violet/evento1/violet_evento_01_violetvr11.png"
        attribute vr12:
            "images/eventos/violet/evento1/violet_evento_01_violetvr12.png"
    group boca:
        attribute b_hablando:
            "images/eventos/violet/evento1/violet_evento_01_violetvrhablando.png"
        attribute b_none default:
            Null()

################################################################################
## Variables guardables
################################################################################

default violet_evento1_completado = False
default violet_evento1_repetir = False

################################################################################
## Funcion post-completar quest 0
################################################################################

init python:

    def post_completar_violet_quest0():
        """Se llama al completar quest 0 de Violet.
        Envia mensaje de Libre Mercado y desbloquea stock del casco VR."""
        sistema_mensajes.inicializar_chat("libre_mercado")
        sistema_mensajes.chats["libre_mercado"].agregar_mensaje(
            "libre_mercado",
            "El casco VR de su lista de deseados ahora esta disponible"
        )
        store.stock_tienda["casco_realidad_virtual"] = 1

################################################################################
## Labels
################################################################################

label evento1_violet:
    # Evento 1 de Violet (primera vez)
    $ ocultar_hud()
    hide screen hud_navegacion
    window show
    scene bg_casa_noche_hmc_zoom with fade

    # Violet entra enojada por el ruido
    show violet_parada c_pijama_brazoscruzados ca_pijama o_enojados b_hablando at right
    violet "¡Podes dejar de hacer tanto ruido!"
    show violet_parada b_none
    pause 0.3

    # Violet ve al MC en el piso
    show violet_parada o_abiertos b_abiertachica
    violet "¿Qué haces en el piso?"
    show violet_parada b_none o_enojados
    mc "Me cai"

    # Violet nota el casco VR - curiosidad
    show violet_parada o_abiertos b_hablando
    violet "¿Eso es un casco vr?"
    show violet_parada b_none
    mc "Sí"

    # Violet quiere probarlo - entusiasmo
    show violet_parada o_felices b_feliz
    violet "¿Lo puedo usar? Siempre quise probar uno"
    show violet_parada b_none o_base
    mc "Espera que me pare"

    # MC se para y le da el casco
    show mc_parado_base c_rbase_vr o_base b_seria at mc_izquierda with dissolve
    pause 0.3
    show mc_parado_base b_hablando
    mc "Toma"
    show mc_parado_base b_seria c_rbase_base
    hide violet_parada

    # Violet se pone el casco - emocionada
    show violet_evento_01_violetvr vr1 with dissolve
    show violet_evento_01_violetvr b_hablando
    violet "Es genial"
    show violet_evento_01_violetvr b_none

    # MC advierte sobre el mareo
    show mc_parado_base o_felicesnm b_hablando
    mc "Marea un poco"
    show mc_parado_base b_seria o_base

    # Violet pregunta por los juegos
    show violet_evento_01_violetvr b_hablando
    violet "No parece, ¿Qué juegos tienes?"
    show violet_evento_01_violetvr b_none
    show mc_parado_base b_hablando
    mc "Hay varios que ya vienen integrados"
    show mc_parado_base b_seria

    # Violet elige un juego
    show violet_evento_01_violetvr b_hablando
    violet "Voy a probar este"
    show violet_evento_01_violetvr b_none
    show violet_evento_01_violetvr vr2 with dissolve
    violet "Este se ve interesante"

    show mc_parado_base o_felices b_felizabierta
    mc "Prueba el que quieras"
    show mc_parado_base b_seria o_base

    # Violet navega los menus
    show violet_evento_01_violetvr vr3 with dissolve
    violet "Mmmmm"
    show violet_evento_01_violetvr vr4 with dissolve
    violet "Ya entendi"

    # MC pregunta que va a jugar
    show mc_parado_base o_aburridos b_hablando
    mc "¿Qué vas a jugar?"
    show mc_parado_base b_seria o_base
    violet "Uno de cortar frutas"
    show mc_parado_base o_molestosnm b_hablando
    mc "Supongo que es valido"
    show mc_parado_base b_seria o_base

    # Violet empieza a jugar - animacion de cortes
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr7 with dissolve

    # Violet se emociona
    violet "¡Wooo!"
    show mc_parado_base o_felices b_felizabierta
    mc "¿Te gusta?"
    show mc_parado_base b_felizcerrada

    # Sigue jugando emocionada
    show violet_evento_01_violetvr vr4 with dissolve
    violet "Sí, es genial"

    # Mas animacion de cortes
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr7 with dissolve

    # Violet quiere volver a jugar
    violet "Voy a venir a jugar seguido"

    # MC hace un comentario imprudente
    show mc_parado_base o_aburridosnm b_hablando
    mc "Mientras no vengas con ese short corto vamos a estar bien"
    show mc_parado_base b_seria

    # Violet no escucho
    show violet_evento_01_violetvr vr4 with dissolve
    violet "¿Qué? No te escuche"

    # MC se da cuenta de lo que dijo
    show mc_parado_base o_asustados b_asustada c_rbase_avergonzado
    piensa "¿Lo dije en voz alta?"
    show mc_parado_base o_felicesnm b_hablando c_rbase_base
    mc "Nada, nada"
    show mc_parado_base b_felizcerrada o_base

    # Viene la sandia
    show violet_evento_01_violetvr vr7 with dissolve
    violet "Ahí viene la sandia"
    show violet_evento_01_violetvr vr8 with dissolve
    pause 0.3

    # Violet ataca la sandia
    show violet_evento_01_violetvr vr9 with dissolve
    violet "¡Muere maldita sandiaaaaa!"

    # MC se rie
    show mc_parado_base o_felicescerrados b_felizabierta
    mc "Jajajajaja"
    show mc_parado_base b_felizcerrada o_felices

    # Violet hace poses de victoria
    show violet_evento_01_violetvr vr10 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr11 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr12 with dissolve

    # Violet presume su golpe
    violet "¿Te gusto mi golpe final?"
    show mc_parado_base o_felices b_felizabierta
    mc "Sí, fue genial"
    show mc_parado_base b_felizcerrada

    # Violet esta agotada
    violet "Quede agotada"
    show mc_parado_base o_base b_hablando
    mc "¿Quieres algo de tomar?"
    show mc_parado_base b_seria

    # Violet menciona ropa comoda - MC se pone nervioso
    violet "No, gracias... Otro día volvemos a jugar y con ropa más comoda"
    show mc_parado_base o_sorprendidos b_hablando
    mc "Eso es lo que decía yo"
    show mc_parado_base b_seria o_base
    violet "¿Eso decias tú?"

    # MC penso en voz alta otra vez
    show mc_parado_base o_asustados b_asustada c_rbase_avergonzado
    piensa "Tengo que dejar de pensar en voz alta"
    show mc_parado_base o_felicesnm b_hablando c_rbase_base
    mc "Nada, nada"
    show mc_parado_base b_felizcerrada o_base

    # Violet se despide
    show violet_evento_01_violetvr vr1 with dissolve
    show violet_evento_01_violetvr b_hablando
    violet "Bueno, me voy a dormir, gracias por dejarme jugar"
    show mc_parado_base o_felices b_felizabierta
    mc "De nada, que descanses"
    show mc_parado_base b_none
    show violet_evento_01_violetvr b_none
    hide violet_evento_01_violetvr
    hide mc_parado_base

    $ avanzar_horario()
    $ violet_evento1_completado = True
    $ _ev1 = sistema_events.obtener_event("violet_evento_01")
    $ _ev1 and _ev1.completar()
    jump game_loop


label evento1_violet_repetir:
    # Evento 1 de Violet (repeticion)
    $ ocultar_hud()
    hide screen hud_navegacion
    window show
    scene bg_casa_noche_hmc_zoom with fade

    # Violet llega lista para jugar
    show violet_parada c_pijama_brazoscruzados ca_pijama o_felices b_feliz at right

    # MC le entrega el casco
    show mc_parado_base c_rbase_vr o_felices b_felizcerrada at mc_izquierda with dissolve
    pause 0.3
    show mc_parado_base b_hablando
    mc "Toma"
    show mc_parado_base b_seria c_rbase_base
    hide violet_parada

    # Violet se pone el casco - confiada
    show violet_evento_01_violetvr vr1 with dissolve
    show violet_evento_01_violetvr b_hablando
    violet "Esta vez voy a hacer muchos más puntos"
    show violet_evento_01_violetvr b_none

    # MC pregunta - curioso
    show mc_parado_base o_aburridos b_hablando
    mc "¿Vas a jugar a lo mismo?"
    show mc_parado_base b_seria o_base

    # Violet responde con su logica
    show violet_evento_01_violetvr b_hablando
    violet "Sí, hay que reutilizar los recursos"
    show violet_evento_01_violetvr b_none

    # MC confundido
    show mc_parado_base o_sorprendidos b_hablando
    mc "¿Qué?"
    show mc_parado_base b_seria o_base

    # Violet comienza
    show violet_evento_01_violetvr vr2 with dissolve
    violet "Voy a comenzar"

    # MC nota que no se cambio - molesto/divertido
    show mc_parado_base o_molestosnm b_hablando
    mc "Al final no te cambiaste la ropa..."
    show mc_parado_base b_seria o_base

    # Violet responde sarcastica
    show violet_evento_01_violetvr vr3 with dissolve
    violet "Que parte de que hay que reutilizar los recursos no entendiste?"
    show violet_evento_01_violetvr vr4 with dissolve

    # MC no entiende
    show mc_parado_base o_aburridosnm b_aburrida
    piensa "No se de que está hablando"
    show mc_parado_base b_hablando
    mc "Lo que digas..."
    show mc_parado_base b_seria o_base

    # Violet empieza a jugar - animacion de cortes
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr7 with dissolve

    # Violet va bien
    violet "Combo x8"
    show mc_parado_base o_felices b_felizabierta c_rbase_confianza
    mc "Vas mejorando, pero no me vas a superar jajaja"
    show mc_parado_base b_felizcerrada c_rbase_base

    # Violet sigue subiendo
    show violet_evento_01_violetvr vr4 with dissolve
    violet "Combo x12"

    # Mas animacion de cortes
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr5 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr6 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr7 with dissolve

    # Violet logra un puntaje alto
    violet "Siiii, 8655 puntos"

    # MC sorprendido
    show mc_parado_base o_sorprendidos b_hablando
    mc "¿Qué? ¿Más de 8000? Eso es imposible..."
    show mc_parado_base b_seria

    # Violet presume
    show violet_evento_01_violetvr vr4 with dissolve
    violet "Te lo dije y todavía no termine"

    # El golpe final
    show violet_evento_01_violetvr vr7 with dissolve
    violet "Golpe final y ... 10000 puntos"
    show violet_evento_01_violetvr vr8 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr9 with dissolve
    violet "¡10120 puntos! en tu cara [mc_name]"

    # MC derrotado
    show mc_parado_base o_asustados b_hablando
    mc "Es imposible, solo pude llegar a los 6500 puntos"
    show mc_parado_base b_triste o_tristesnm

    # Violet celebra
    show violet_evento_01_violetvr vr10 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr11 with dissolve
    pause 0.3
    show violet_evento_01_violetvr vr12 with dissolve
    violet "Listoooo, has sido destruido por la maestra del Fruit Samurai"

    # MC acepta la derrota con determinacion
    show mc_parado_base o_serios b_hablando
    mc "Voy a tener que practicar más"
    show mc_parado_base b_seria
    violet "Nunca vas a superar mi puntuacion"

    # MC competitivo
    show mc_parado_base o_enojados b_hablando c_rbase_confianza
    mc "Ya veremos"
    show mc_parado_base b_seria c_rbase_base o_base
    violet "Avisame si lo logras"
    show mc_parado_base o_felicesnm b_hablando
    mc "Lo hare"
    show mc_parado_base b_felizcerrada o_base

    # Violet se despide burlona
    show violet_evento_01_violetvr vr1 with dissolve
    show violet_evento_01_violetvr b_hablando
    violet "Bueno, me voy a dormir, hasta la poxima perdedor jajaja"

    # MC resignado pero con buen humor
    show mc_parado_base o_molestosnm b_hablando
    mc "... que descanses"
    show mc_parado_base b_none
    show violet_evento_01_violetvr b_none
    hide violet_evento_01_violetvr
    hide mc_parado_base

    $ avanzar_horario()

    jump game_loop


label invitar_violet_vr:
    # El jugador invita a Violet a jugar VR
    $ violet_evento1_repetir = True
    $ ocultar_hud()
    piensa "La invite a jugar con el casco de realidad virtual esta noche."
    jump game_loop
