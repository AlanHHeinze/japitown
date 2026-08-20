################################################################################
## Juego Nuevo — CASCO VR
################################################################################
## Primer juego del sistema "Juegos Nuevos" (ventaja del hito de amor 20).
##
## ANTES ERA UN EVENTO (`violet_evento_01`, en events/evento1_violet.rpy) que
## aparecia a los 20 de amor y se disparaba usando el item. El sistema de Juegos
## Nuevos cubre ese rol mejor, asi que el Event se retiro y todo su contenido
## —imagenes, escenas, el uso del item y el desbloqueo de la tienda— vive acá.
##
## COMO SE JUEGA: Violet lo menciona en la charla de "Juegos Nuevos" mientras no
## se haya jugado. El casco se compra en la tienda (el stock lo abre el hito de
## amor 20, mas abajo) y se usa de NOCHE en la habitacion del MC — ahi arranca
## la escena. Despues de la primera vez se la puede invitar desde su menu.
##
## ⚠️ LOS FLAGS CONSERVAN EL NOMBRE VIEJO (`violet_evento1_*`) A PROPOSITO.
## Renombrar un `default` no migra el valor: una partida a mitad del casco
## volveria a cero y el juego figuraria como no jugado. Se leen desde
## _jn_cascovr_jugado().


################################################################################
## Imagenes
################################################################################

image bg_casa_noche_hmc_zoom = "images/bg/casa/bg_casa_noche_hmc_zoom.jpg"

layeredimage mc_base_parado_vr:
    group pose:
        attribute vr1 default:
            "images/eventos/violet/evento1/mc_base_parado_vr1.webp"
        attribute vr2:
            "images/eventos/violet/evento1/mc_base_parado_vr2.webp"
        attribute vr3:
            "images/eventos/violet/evento1/mc_base_parado_vr3.webp"

layeredimage violet_evento_01_jugandosolo:
    group pose:
        attribute j1 default:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo1.webp"
        attribute j2:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo2.webp"
        attribute j3:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo3.webp"
        attribute j4:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo4.webp"
        attribute j5:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo5.webp"
        attribute j6:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo6.webp"
        attribute j7:
            "images/eventos/violet/evento1/violet_evento_01_jugandosolo7.webp"

layeredimage violet_evento_01_violetvr:
    group pose:
        attribute vr1 default:
            "images/eventos/violet/evento1/violet_evento_01_violetvr1.webp"
        attribute vr2:
            "images/eventos/violet/evento1/violet_evento_01_violetvr2.webp"
        attribute vr3:
            "images/eventos/violet/evento1/violet_evento_01_violetvr3.webp"
        attribute vr4:
            "images/eventos/violet/evento1/violet_evento_01_violetvr4.webp"
        attribute vr5:
            "images/eventos/violet/evento1/violet_evento_01_violetvr5.webp"
        attribute vr6:
            "images/eventos/violet/evento1/violet_evento_01_violetvr6.webp"
        attribute vr7:
            "images/eventos/violet/evento1/violet_evento_01_violetvr7.webp"
        attribute vr8:
            "images/eventos/violet/evento1/violet_evento_01_violetvr8.webp"
        attribute vr9:
            "images/eventos/violet/evento1/violet_evento_01_violetvr9.webp"
        attribute vr10:
            "images/eventos/violet/evento1/violet_evento_01_violetvr10.webp"
        attribute vr11:
            "images/eventos/violet/evento1/violet_evento_01_violetvr11.webp"
        attribute vr12:
            "images/eventos/violet/evento1/violet_evento_01_violetvr12.webp"
    group boca:
        attribute b_hablando:
            "images/eventos/violet/evento1/violet_evento_01_violetvrhablando.webp"
        attribute b_none default:
            Null()

################################################################################
## Variables guardables
################################################################################

default violet_evento1_completado = False
default violet_evento1_repetir = False

################################################################################
## Registro en Juegos Nuevos + apertura de la tienda
################################################################################

# True cuando ya se abrio el stock. Es `default` y no se deriva del hito porque
# el jugador puede comprar el casco y venderlo: sin este flag, el trigger le
# repondria stock cada vuelta del loop.
default jn_cascovr_tienda_abierta = False


init python:

    def _jn_cascovr_jugado():
        """
        True si el casco ya se jugo con Violet.

        Lee el flag VIEJO del evento a proposito (ver la nota del encabezado):
        renombrarlo dejaria en cero a toda partida que ya lo hubiera jugado.
        """
        return getattr(store, 'violet_evento1_completado', False)

    def _jn_cascovr_trigger_tienda():
        """
        Trigger de game_loop: abre el casco en la tienda al llegar el hito de
        amor 20, y avisa por el chat de Libre Mercado.

        ANTES lo hacia post_completar_violet_quest0() al cerrar la quest 0 de
        Violet. Se movio acá porque ahora el casco es contenido de "Juegos
        Nuevos": no tiene sentido que este a la venta antes de que ella lo
        mencione. Devuelve siempre None — efecto python, el loop sigue.
        """
        if store.jn_cascovr_tienda_abierta:
            return None
        if not npc_tiene_ventaja("violet", "juegos_nuevos"):
            return None

        store.jn_cascovr_tienda_abierta = True
        store.stock_tienda["casco_realidad_virtual"] = 1
        sistema_mensajes.inicializar_chat("libre_mercado")
        sistema_mensajes.chats["libre_mercado"].agregar_mensaje(
            "libre_mercado",
            "El casco VR de su lista de deseados ahora esta disponible"
        )
        return None


init 5 python:

    registrar_juego_nuevo(
        "cascovr",
        "Siempre quise probar un casco de realidad virtual",
        _jn_cascovr_jugado,
    )

    registrar_trigger_game_loop("jn_cascovr_tienda", _jn_cascovr_trigger_tienda)


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
    violet "¡Puedes dejar de hacer tanto ruido!"
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
    # Marca el juego como jugado: a partir de acá Violet deja de proponerlo en
    # la charla de "Juegos Nuevos" (lo lee _jn_cascovr_jugado).
    $ violet_evento1_completado = True
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


label usar_casco_vr:

    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion

    # Si el evento 1 ya se completo
    if violet_evento1_completado:
        # Con invitacion activa → directo al evento repetir
        if violet_evento1_repetir:
            $ violet_evento1_repetir = False
            jump evento1_violet_repetir
        # Sin invitacion → narrativa corta de jugar solo
        jump usar_casco_vr_repetir

    # Primera vez: narrativa completa del casco VR
    scene bg_casa_noche_hmc_zoom with fade
    show mc_parado_base c_rbase_base o_base b_seria at center with dissolve
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_vr with sprite_normal
    pause 0.3

    show mc_parado_base b_hablando 
    mc "Al fin lo tengo"
    show mc_parado_base b_none
    pause 0.3
    show mc_parado_base b_hablando 
    mc "Voy a probar el X Fighters"
    show mc_parado_base b_none
    
    hide mc_parado_base with dissolve
    show mc_base_parado_vr vr1 at center with dissolve
    piensa "Tendria que ver como configurar esto"
    show mc_base_parado_vr vr2 at center with dissolve
    piensa "Creo que voy entendiendo"
    show mc_base_parado_vr vr3 at center with dissolve
    piensa "Ahí esta"
    show mc_base_parado_vr vr2 at center with dissolve
    pause 0.3
    show mc_base_parado_vr vr1 at center with dissolve
    
    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Un tiempo mas tarde...{/color}"
    scene bg_casa_noche_hmc_zoom with fade

    show violet_evento_01_jugandosolo j1 with dissolve
    piensa "Ya casi lo tengo, un golpe mas y destruyo al terrible Majin Freazing Cell Z"
    show violet_evento_01_jugandosolo j2 with dissolve
    piensa "¡Muereeeeeee!"
    show violet_evento_01_jugandosolo j3 with dissolve
    mc "AHHHHHHHH"
    show violet_evento_01_jugandosolo j4 with dissolve
    pause 0.3
    show violet_evento_01_jugandosolo j5 with dissolve
    pause 0.3
    show violet_evento_01_jugandosolo j6 with dissolve
    pause 0.3
    show violet_evento_01_jugandosolo j7 with dissolve
    pause 0.3
    mc "Estoy bien..."
    mc "Pero ya es suficiente de esto"
    mc "Me duele todo"
    hide violet_evento_01_jugandosolo with dissolve

    # Ocultar MC VR
    hide mc_base_parado_vr with dissolve

    # Post-narrativa primera vez: comprobar si Violet esta en su habitacion
    $ _violet_vr = obtener_npc("violet")
    if _violet_vr and _violet_vr.locacion_actual == "casa_hviolet":
        jump evento1_violet

    # Violet no esta → volver al game loop
    $ mostrar_hud()
    jump game_loop


################################################################################
## Label: Casco VR — Repetir (jugar solo, sin evento)
################################################################################

label usar_casco_vr_repetir:

    scene bg_casa_noche_hmc_zoom with fade

    show mc_base_parado_vr vr1 at center with dissolve
    piensa "Placeholder: Voy a jugar un rato con el casco."

    scene black with fade
    pause 1.0
    centered "{color=#FFFFFF}Un tiempo mas tarde...{/color}"

    show violet_evento_01_jugandosolo j1 with dissolve
    piensa "Placeholder: Estuvo bien la sesion de hoy."
    hide violet_evento_01_jugandosolo with dissolve

    $ mostrar_hud()
    jump game_loop
