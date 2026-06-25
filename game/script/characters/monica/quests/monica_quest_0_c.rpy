################################################################################
## Quest 0_c de Mónica — La batería de la notebook
################################################################################
## Se dispara al usar el item "notebook_monica" en la habitación del MC.
## El MC descubre que el problema es la batería y hay que comprar una nueva.

# =============================================================================
# USO DEL ITEM "notebook_monica" — dispara la quest 0_c
# =============================================================================
# La condicion_uso del item ya garantiza que el MC esté en su habitación; si no
# lo está, el inventario muestra "Deberia revisarlo en mi habitacion".

label revisar_notebook_monica:
    $ _q_m0c = sistema_quests.obtener_quest("monica_questprincipal_0_c")
    if _q_m0c and _q_m0c.activa and not _q_m0c.completada:
        $ _q_m0c.etapa_actual = ETAPA_DESARROLLO
        jump quest_monica_questprincipal_0_c

    # Ya se revisó la notebook: recordatorio
    $ ocultar_hud()
    window show
    piensa "La bateria esta algo hinchada pareceria ser ese el problema"
    piensa "Podria comprar una nueva y cambiarsela"
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

    # MC en su habitación
    $ _bg_m0c = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _bg_m0c with fade
    show mc_parado_base c_rbase_pensando o_base b_none at center with dissolve

    piensa "A ver qué tiene esta notebook..."
    piensa "Probé encenderla y no da señales de vida"
    show mc_parado_base o_arribanm
    piensa "Por suerte el problema parece ser la batería esta algo hinchadda. Con comprar una nueva debería solucionarse... o eso creo"
    show mc_parado_base o_base

    hide mc_parado_base with dissolve

    tutorial "Dentro del [colorear_quest('Celular')] hay una [colorear_quest('App Tienda')]	a donde podras conseguir todos los [colorear_quest('Objetos Comprables')] del juego"
    tutorial "Todos los articulos van a tener tres indicadores: Su [colorear_quest('Costo')], el [colorear_quest('Stock')] en tienda (la mayoria de los articulos se reponen nuevamente los lunes) y los [colorear_quest('Dias hasta la Entrega')]"
    tutorial "Cuando el [colorear_quest('Dia de Entrega')] llegue tendras un [colorear_quest('Recordatorio al Despertar')], podras salir por la mañana hasta el [colorear_locacion('Frente')] y recoger el pedido [colorear_quest('Interactuando con el Repartidor')]"
    tutorial "Si no lo haces alguien recogera el paquete por ti y lo dejara [colorear_quest('Sobre tu Cama por la Tarde')]"
    tutorial "Para conseguir mas [colorear_quest('Dinero')]	puedes hacer la [colorear_quest('Accion Trabajar')] disponible en [colorear_locacion('Tu Habitacion')]. Cada turno te da $20 y avanza el horario. Podés trabajar hasta 2 veces por día."
   
    window hide
    $ mostrar_hud()

    # Habilitar la batería en la tienda (1 unidad)
    $ stock_tienda["bateria_nt520"] = 1

    # Completar la quest
    $ completar_quest_actual("monica")

    $ mostrar_hud()
    jump game_loop


# =============================================================================
# USO DEL ITEM "bateria_nt520" — contenido en desarrollo
# =============================================================================
# La condicion_uso del item garantiza que el MC esté en su habitación.

label usar_bateria_nt520:
    $ ocultar_hud()
    window show
    "Contenido en desarrollo"
    window hide
    $ mostrar_hud()
    jump game_loop
