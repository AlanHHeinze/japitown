################################################################################
## Quest 0_c de Mónica — La batería de la notebook
################################################################################
## Se dispara al usar el item "notebook_monica" en la habitacion del MC.
## El MC descubre que el problema es la batería y hay que comprar una nueva.

# =============================================================================
# USO DEL ITEM "notebook_monica" — dispara la quest 0_c
# =============================================================================
# La condicion_uso del item ya garantiza que el MC esté en su habitacion; si no
# lo está, el inventario muestra "Deberia revisarlo en mi habitacion".

label revisar_notebook_monica:
    if quest_lista_para_boton("monica_questprincipal_0_c"):
        jump quest_monica_questprincipal_0_c

    # Ya se revisó la notebook: recordatorio
    $ ocultar_hud()
    window show
    piensa "La batería está algo hinchada, parecería ser ese el problema"
    piensa "Podría comprar una nueva y cambiársela"
    window hide
    $ mostrar_hud()
    jump game_loop


# =============================================================================
# QUEST 0_C — Label principal
# =============================================================================

label quest_monica_questprincipal_0_c:

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    # MC en su habitacion
    $ _bg_m0c = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_m0c with fade
    show mc_parado_base c_rbase_pensando o_base b_none at center with dissolve

    piensa "A ver qué tiene esta notebook..."
    piensa "Probé encenderla y no da señales de vida"
    show mc_parado_base o_arribanm
    piensa "Por suerte el problema parece ser la batería, está algo hinchada. Con comprar una nueva debería solucionarse... o eso creo"
    show mc_parado_base o_base

    hide mc_parado_base with dissolve

    tutorial "Dentro del celular tendrás una App llamada Tienda en la que podrás encontrar todos los objetos del juego"
    tutorial "Al comprar un objeto tendrás que esperar los días de entrega, una vez llegue, podrás recibirlo por la mañana en el frente o si pasa el tiempo el objeto aparecerá sobre tu cama"

    window hide
    $ mostrar_hud()

    # Habilitar la batería en la tienda (1 unidad)
    $ stock_tienda["bateria_nt520"] = 1

    # Completar la quest
    $ completar_quest_actual("monica", quest_id="monica_questprincipal_0_c")

    $ mostrar_hud()
    jump game_loop


# =============================================================================
# USO DEL ITEM "bateria_nt520" — contenido en desarrollo
# =============================================================================
# La condicion_uso del item garantiza que el MC esté en su habitacion.

label usar_bateria_nt520:
    $ ocultar_hud()
    window show
    "Contenido en desarrollo"
    window hide
    $ mostrar_hud()
    jump game_loop
