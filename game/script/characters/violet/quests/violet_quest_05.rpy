################################################################################
## Quest 5 de Violet — Solo en casa
################################################################################
## Se activa automaticamente al despertar cuando se cumplen las condiciones.
## Todas las chicas estan fuera. MC piensa en aprovechar el dia libre.
## Flujo: habitacion MC → living (tv) → label TV → habitacion Violet →
##        ropero/cajonera → pasillo → baño (3 opciones) → cierre
################################################################################

# =============================================================================
# VARIABLES
# =============================================================================
default violet_quest5_inicio_pendiente = False
default violet_quest5_tiene_pijama = False
default violet_quest5_ropainterior = False

# Estado de elementos en habitacion de Violet (True = aun visible/pendiente)
default vq4_compu_pendiente = True
default vq4_mangas_pendiente = True
default vq4_mochila_pendiente = True
default vq4_muñecos_pendiente = True
default vq4_peluches_pendiente = True

# Fondos originales para restaurar al final
default vq4_bg_original_living = ""
default vq4_bg_original_hviolet = ""
default vq4_bg_original_pasilloarriba = ""

# Posiciones de elementos interactivos (ajustables con herramienta de posicionamiento)
default vq4_pos_sillon = (880, 1024)
default vq4_pos_cajonera = (234, 1080)
default vq4_pos_compu = (1636, 775)
default vq4_pos_mangas = (1680, 496)
default vq4_pos_mochila = (1249, 896)
default vq4_pos_muñecos = (1867, 812)
default vq4_pos_peluches = (830, 767)
default vq4_pos_ropero = (234, 908)

# Posiciones dentro del ropero
default vq4_pos_caja = (1185, 1078)
default vq4_pos_pijama = (821, 824)

# Posiciones dentro de la cajonera
default vq4_pos_grande = (816, 491)
default vq4_pos_normal = (338, 482)
default vq4_pos_tanga = (507, 879)


# =============================================================================
# IMAGENES
# =============================================================================

# --- Layeredimage: violet_mojada ---
layeredimage violet_mojada:
    group cuerpo:
        attribute base default:
            "images/quest/violet/quest4/violet_parada_mojada.png"

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/quest/violet/quest4/violet_parada_mojada_hablando.png"

# --- Fondos y escenas ---
image vq4_hviolet_tormenta = "images/quest/violet/quest4/violet_quest04_hviolet_tormenta.png"
image vq4_ducha = "images/quest/violet/quest4/violet_quest04_ducha.png"
image vq4_duchaescena = "images/quest/violet/quest4/violet_quest04_duchaescena.png"
image vq4_livinglloviendo = "images/quest/violet/quest4/violet_quest04_livinglloviendo.png"
image vq4_livingnublado = "images/quest/violet/quest4/violet_quest04_livingnublado.png"
image vq4_livingtormenta = "images/quest/violet/quest4/violet_quest04_livingtormenta.png"
image vq4_livingtormenta1 = "images/quest/violet/quest4/violet_quest04_livingtormenta1.png"
image vq4_livingtormenta2 = "images/quest/violet/quest4/violet_quest04_livingtormenta2.png"
image vq4_livingtormentacerrado = "images/quest/violet/quest4/violet_quest04_livingtormentacerrado.png"

# --- MC ---
image vq4_mcmirandotv = "images/quest/violet/quest4/violet_quest04_mcmirantotv.png"

# --- TV ---
image vq4_tv1 = "images/quest/violet/quest4/violet_quest04_tv1.png"
image vq4_tv2 = "images/quest/violet/quest4/violet_quest04_tv2.png"
image vq4_tv3 = "images/quest/violet/quest4/violet_quest04_tv3.png"
image vq4_tv4 = "images/quest/violet/quest4/violet_quest04_tv4.png"
image vq4_tv5 = "images/quest/violet/quest4/violet_quest04_tv5.png"

# --- Ropero y cajonera ---
image vq4_ropero = "images/quest/violet/quest4/violet_quest04_ropero.png"
image vq4_cajonera = "images/quest/violet/quest4/violet_quest04_cajonera.png"

# --- Interacciones ---
image vq4_interaccion_caja = "images/quest/violet/quest4/violet_quest04_interaccion_caja.png"
image vq4_interaccion_cajonera = "images/quest/violet/quest4/violet_quest04_interaccion_cajonera.png"
image vq4_interaccion_compu = "images/quest/violet/quest4/violet_quest04_interaccion_compu.png"
image vq4_interaccion_grande = "images/quest/violet/quest4/violet_quest04_interaccion_grande.png"
image vq4_interaccion_mangas = "images/quest/violet/quest4/violet_quest04_interaccion_mangas.png"
image vq4_interaccion_mochila = "images/quest/violet/quest4/violet_quest04_interaccion_mochila.png"
image vq4_interaccion_muñecos = "images/quest/violet/quest4/violet_quest04_interaccion_muñecos.png"
image vq4_interaccion_normal = "images/quest/violet/quest4/violet_quest04_interaccion_normal.png"
image vq4_interaccion_peluches = "images/quest/violet/quest4/violet_quest04_interaccion_peluches.png"
image vq4_interaccion_pijama = "images/quest/violet/quest4/violet_quest04_interaccion_pijama.png"
image vq4_interaccion_ropero = "images/quest/violet/quest4/violet_quest04_interaccion_ropero.png"
image vq4_interaccion_tanga = "images/quest/violet/quest4/violet_quest04_interaccion_tanga.png"
image vq4_interaccionsillon = "images/quest/violet/quest4/violet_quest04_interaccionsillon.png"

image vq4_ducha = "images/quest/violet/quest4/violet_quest04_ducha.png"
image vq4_duchaescena = "images/quest/violet/quest4/violet_quest04_duchaescena.png"


################################################################################
## LABEL PRINCIPAL — Auto-inicio al despertar
################################################################################

label quest_violet_questprincipal_5:

    # === SETUP INICIAL ===
    $ ocultar_hud()
    window show

    # === ESCENA: MC en su habitacion pensando ===
    scene expression "images/bg/casa/bg_casa_mañana_hmc.png" with fade

    show mc_parado_base c_rbase_base o_base b_none at center with dissolve

    show mc_parado_base o_base
    piensa "Hoy las chicas salieron temprano..."

    show mc_parado_base o_abajonm
    piensa "Parece que voy a estar solo en la casa todo el dia."

    show mc_parado_base o_base
    piensa "Podria aprovechar el dia libre."

    hide mc_parado_base with dissolve

    # === FASE 1: Modo restringido — libre por la casa, no avanzar tiempo ===
    # El jugador puede moverse por toda la casa pero no puede avanzar el tiempo
    # El sillon en el living es interactuable (igual que en quest 3)
    $ activar_restriccion(
        locaciones_permitidas=["casa_hmc", "casa_hviolet", "casa_hmonica", "casa_hjasmine", "casa_pasilloarriba", "casa_pasilloabajo", "casa_living", "casa_cocina", "casa_comedor", "casa_patio", "casa_banioarriba", "casa_banioabajo", "casa_garage", "casa_gym"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("No puedo salir de la casa ahora"),
        mensajes_acciones={
            "avanzar_tiempo": _("No tengo ganas de hacer nada productivo"),
            "dormir": _("No tengo sueño"),
            "entrenar": _("No tengo ganas de entrenar"),
            "trabajar": _("No tengo ganas de trabajar"),
            "usar_item": _("No tengo ganas de usar eso ahora"),
            "comprar": _("No tengo ganas de comprar nada"),
        },
        mensaje_npc_bloqueado=_("No hay nadie en la casa"),
        celular_bloqueado=False,
        mensaje_celular="",
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para cuando el jugador entre al living (mensaje recordatorio)
    $ restriccion_quest_activa.registrar_label_locacion("casa_living", "violet_quest4_living_mensaje")

    # Mover al jugador a su habitacion
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## LIVING — Mensaje al entrar + screen con sillon
################################################################################

label violet_quest4_living_mensaje:
    # Mostrar mensaje forzado 2 segundos (no se puede saltar)
    $ store._msg_restriccion_texto = "Podria mirar la tele."
    show screen mensaje_restriccion
    $ renpy.pause(0.5, hard=True)
    hide screen mensaje_restriccion
    # Mostrar el screen del sillon sobre el living (HUD y navegacion siguen visibles)
    show screen vq4_sillon_living
    return


################################################################################
## MIRANDO TV — Label del sillon (contenido pendiente)
################################################################################

label violet_quest4_mirando_tv:

    hide screen vq4_sillon_living
    $ ocultar_hud()
    window show

    scene bg_casa_mañana_living with dissolve
    show vq4_mcmirandotv
    show vq4_tv1

    mc "La gente hablo bien de este documental pero lo unico que veo son animales tomando agua hace 20 min"

    scene vq4_livingnublado 
    show vq4_mcmirandotv
    show vq4_tv2

    mc "Mi amigo Sifirus debe estar bastante molesto con que los piratas se esten volviendo de moda"
    mc "..."
    mc "Parece que se nublo un poco, pero no decia nada de que iba a llover"

    scene vq4_livinglloviendo 
    show vq4_mcmirandotv
    show vq4_tv3

    mc "Y llueve nomas, espero que sea una lluvia pasajera al menos"
    mc "Justo hoy salieron las 3"

    scene vq4_livingtormenta 
    show vq4_mcmirandotv
    show vq4_tv4

    mc "No es una lluvia pasajera tampoco..."
    mc "Y... ¿Que carajo estoy mirando?"

    scene vq4_livingtormenta1 
    show vq4_mcmirandotv
    show vq4_tv5

    mc "Uno la critica pero Veloces y Enojados siempre cumple con su cuota de accion sin sentido"

    "Ruido en la entrada"

    scene vq4_livingtormenta2 
    show vq4_tv5

    show mc_parado_base c_rbase_base o_base at mc_izquierda
    show violet_mojada at right

    show mc_parado_base b_hablando
    mc "Veo que tu pronostico tampoco decia que iba a llover"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Me gustaría culpar al pronóstico pero ni lo miré"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "Estas lo suficientemente mojada para que no sea gracioso"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Agradezco que no te rias"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "Anda a darte una ducha caliente"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Si"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "¿Quieres que te alcance algo de ropa"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Si, mi pijama por favor"
    show violet_mojada b_none

    show mc_parado_base b_hablando
    mc "Subí que ahora te lo llevo"
    show mc_parado_base b_none

    show violet_mojada b_hablando
    violet "Gracias"
    show violet_mojada b_none

    hide violet_mojada

    piensa "Pobre Violet no tenía ánimos ni para pelear"

    hide mc_parado_base

    # --- CONTENIDO PENDIENTE: Escena mirando TV ---

    # --- FIN CONTENIDO PENDIENTE ---

    # === FASE 2: Post-TV — Restriccion: solo pasillo arriba y habitacion violet ===
    # Cambiar fondos a version tormenta
    $ loc_living = sistema_locaciones.obtener_locacion("casa_living")
    $ loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ loc_pasilloarriba = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    $ vq4_bg_original_living = loc_living.background_base
    $ vq4_bg_original_hviolet = loc_hviolet.background_base
    $ vq4_bg_original_pasilloarriba = loc_pasilloarriba.background_base
    $ loc_living.background_base = "images/quest/violet/quest4/violet_quest04_livingtormentacerrado.png"
    $ loc_hviolet.background_base = "images/quest/violet/quest4/violet_quest04_hviolet_tormenta.png"
    $ loc_pasilloarriba.background_base = "images/bg/casa/bg_casa_noche_pasilloarriba.png"

    $ desactivar_restriccion()
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_hviolet"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Deberia llevarle ropa a Violet"),
        mensajes_acciones={
            "avanzar_tiempo": _("Deberia llevarle ropa a Violet"),
            "dormir": _("Deberia llevarle ropa a Violet"),
            "entrenar": _("Deberia llevarle ropa a Violet"),
            "trabajar": _("Deberia llevarle ropa a Violet"),
            "usar_item": _("Deberia llevarle ropa a Violet"),
            "comprar": _("Deberia llevarle ropa a Violet"),
        },
        mensaje_npc_bloqueado=_("No hay nadie en la casa"),
        celular_bloqueado=True,
        mensaje_celular=_("Deberia llevarle ropa a Violet"),
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para cuando entre a la habitacion de Violet
    # (bypass door access porque hay label registrado para esa locacion)
    $ restriccion_quest_activa.registrar_label_locacion("casa_hviolet", "violet_quest4_entrar_hviolet")

    # Registrar label para cuando salga al pasillo (verifica si tiene pijama)
    $ restriccion_quest_activa.registrar_label_locacion("casa_pasilloarriba", "violet_quest4_check_salida_hviolet")

    # Mover al jugador al pasillo arriba
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## ENTRAR A HABITACION DE VIOLET
################################################################################

label violet_quest4_entrar_hviolet:
    # Mostrar mensaje forzado (mismo formato que el living)
    $ store._msg_restriccion_texto = "Hace mucho que no estoy acá."
    show screen mensaje_restriccion
    $ renpy.pause(0.5, hard=True)
    hide screen mensaje_restriccion

label violet_quest4_mostrar_habitacion:
    # Ocultar HUD, mostrar fondo y screen de exploracion con su propio loop
    $ ocultar_hud()
    scene vq4_hviolet_tormenta with fade
    show screen vq4_habitacion_violet
    $ _vq4_en_habitacion = True
    while _vq4_en_habitacion:
        $ _resultado_hab = ui.interact()
        if _resultado_hab == "compu":
            hide screen vq4_habitacion_violet
            $ vq4_compu_pendiente = False
            window show
            piensa "La computadora de Violet... mejor no tocar nada."
            window hide
            show screen vq4_habitacion_violet
        elif _resultado_hab == "mangas":
            hide screen vq4_habitacion_violet
            $ vq4_mangas_pendiente = False
            window show
            piensa "Violet tiene bastantes mangas... no sabia que le gustaban tanto."
            window hide
            show screen vq4_habitacion_violet
        elif _resultado_hab == "mochila":
            hide screen vq4_habitacion_violet
            $ vq4_mochila_pendiente = False
            window show
            piensa "Su mochila del colegio... no deberia revisar sus cosas."
            window hide
            show screen vq4_habitacion_violet
        elif _resultado_hab == "muñecos":
            hide screen vq4_habitacion_violet
            $ vq4_muñecos_pendiente = False
            window show
            piensa "Tiene una coleccion de muñecos... algunos son bastante raros."
            window hide
            show screen vq4_habitacion_violet
        elif _resultado_hab == "peluches":
            hide screen vq4_habitacion_violet
            $ vq4_peluches_pendiente = False
            window show
            piensa "Un montón de peluches... típico de Violet."
            window hide
            show screen vq4_habitacion_violet
        elif _resultado_hab == "ropero":
            # Ir al ropero (tiene su propio loop, vuelve aqui al terminar)
            hide screen vq4_habitacion_violet
            call violet_quest4_click_ropero from _call_violet_quest4_click_ropero
            show screen vq4_habitacion_violet
        elif _resultado_hab == "cajonera":
            # Ir a la cajonera (tiene su propio loop, vuelve aqui al terminar)
            hide screen vq4_habitacion_violet
            call violet_quest4_click_cajonera from _call_violet_quest4_click_cajonera
            show screen vq4_habitacion_violet
        elif _resultado_hab == "salir":
            # Verificar si tiene el pijama
            if not violet_quest5_tiene_pijama:
                hide screen vq4_habitacion_violet
                window show
                piensa "Debo buscar la ropa de Violet."
                window hide
                show screen vq4_habitacion_violet
            else:
                $ _vq4_en_habitacion = False
        elif _resultado_hab == "fuera":
            # Click fuera de elementos — ignorar silenciosamente
            pass
    hide screen vq4_habitacion_violet
    # Tiene el pijama — avanzar a fase 3
    jump violet_quest4_salir_hviolet


################################################################################
## ROPERO — Screen con caja y pijama
################################################################################

label violet_quest4_click_ropero:
    # Cambiar escena al ropero
    scene vq4_ropero with fade
    show screen vq4_screen_ropero
    $ _vq4_en_ropero = True
    while _vq4_en_ropero:
        $ _resultado_ropero = ui.interact()
        if _resultado_ropero == "caja":
            hide screen vq4_screen_ropero
            window show
            mc "Le tendría que preguntar a Violet por el cosplay."
            window hide
            show screen vq4_screen_ropero
        elif _resultado_ropero == "pijama":
            hide screen vq4_screen_ropero
            window show
            mc "Esto es lo que necesitaba."
            $ violet_quest5_tiene_pijama = True
            window hide
            $ _vq4_en_ropero = False
        elif _resultado_ropero == "volver":
            $ _vq4_en_ropero = False
        elif _resultado_ropero == "fuera":
            hide screen vq4_screen_ropero
            window show
            mc "Violet me pidió su pijama rosa."
            window hide
            show screen vq4_screen_ropero
    hide screen vq4_screen_ropero
    # Volver a la habitacion
    scene vq4_hviolet_tormenta with fade
    return


################################################################################
## CAJONERA — Screen con grande, normal y tanga
################################################################################

label violet_quest4_click_cajonera:
    # Cambiar escena a la cajonera
    scene vq4_cajonera with fade
    show screen vq4_screen_cajonera
    $ _vq4_en_cajonera = True
    while _vq4_en_cajonera:
        $ _resultado_cajonera = ui.interact()
        if _resultado_cajonera in ["grande", "normal", "tanga"]:
            hide screen vq4_screen_cajonera
            window show
            menu:
                "Llevarle esto a Violet?"

                "Si":
                    $ violet_quest5_ropainterior = True
                    $ _vq4_en_cajonera = False
                "No":
                    pass
            window hide
            if _vq4_en_cajonera:
                show screen vq4_screen_cajonera
        elif _resultado_cajonera == "volver":
            $ _vq4_en_cajonera = False
        elif _resultado_cajonera == "fuera":
            hide screen vq4_screen_cajonera
            window show
            mc "¿Debería llevarle ropa interior también?"
            window hide
            show screen vq4_screen_cajonera
    hide screen vq4_screen_cajonera
    # Volver a la habitacion
    scene vq4_hviolet_tormenta with fade
    return


################################################################################
## CHECK SALIDA AL PASILLO — Verificar pijama antes de avanzar
################################################################################

label violet_quest4_check_salida_hviolet:
    if not violet_quest5_tiene_pijama:
        $ store._msg_restriccion_texto = "Debo buscar la ropa de Violet."
        show screen mensaje_restriccion
        $ renpy.pause(0.5, hard=True)
        hide screen mensaje_restriccion
        return
    jump violet_quest4_salir_hviolet


################################################################################
## SALIR DE HABITACION VIOLET — Verificar pijama
################################################################################

label violet_quest4_salir_hviolet:
    # El jugador ya tiene el pijama (verificado en violet_quest4_check_salida_hviolet)
    # === FASE 3: Restriccion — solo pasillo arriba y baño arriba ===
    $ desactivar_restriccion()
    $ activar_restriccion(
        locaciones_permitidas=["casa_pasilloarriba", "casa_banioarriba"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar"],
        mensaje_movimiento=_("Debo llevarle la ropa a Violet"),
        mensajes_acciones={
            "avanzar_tiempo": _("Debo llevarle la ropa a Violet"),
            "dormir": _("Debo llevarle la ropa a Violet"),
            "entrenar": _("Debo llevarle la ropa a Violet"),
            "trabajar": _("Debo llevarle la ropa a Violet"),
            "usar_item": _("Debo llevarle la ropa a Violet"),
            "comprar": _("Debo llevarle la ropa a Violet"),
        },
        mensaje_npc_bloqueado=_("No hay nadie mas en la casa"),
        celular_bloqueado=True,
        mensaje_celular=_("Debo llevarle la ropa a Violet"),
        npcs_ocultos=["monica", "jasmine", "violet"],
    )

    # Registrar label para interceptar al intentar entrar al baño
    $ restriccion_quest_activa.registrar_label_locacion("casa_banioarriba", "violet_quest4_puerta_banio")

    # Mover al jugador al pasillo arriba
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## PUERTA DEL BAÑO — Menu de 3 opciones
################################################################################

label violet_quest4_puerta_banio:

    # Volver al pasillo (el sistema ya movio al baño, lo revertimos)
    $ sistema_locaciones.locacion_actual = sistema_locaciones.locaciones.get("casa_pasilloarriba", sistema_locaciones.locacion_actual)

    # Ocultar HUD y mostrar menu modal (mismo patron que door_access_system)
    $ ocultar_hud()
    call screen vq4_menu_puerta_banio

    # Procesar resultado del menu
    if _return == "entrar":
        jump violet_quest4_banio_entrar
    elif _return == "golpear":
        jump violet_quest4_banio_golpear

    # "volver" — restaurar HUD y volver al game loop
    $ mostrar_hud()
    jump game_loop


################################################################################
## RAMAS DEL BAÑO
################################################################################

# --- Entrar ---
label violet_quest4_banio_entrar:

    $ ocultar_hud()

    scene vq4_ducha with fade

    # +5 deseo
    $ obtener_npc("violet").modificar_stat2(5)

    piensa "Entre directamente sin pensarlo"
    piensa "Parece que Violet no se dio cuenta"
    piensa "No veo muy bien por el vapor"
    piensa "Podria acercarme mas..."

    menu:
        "Si":
            jump violet_quest4_banio_entrar_si

        "No":
            jump violet_quest4_banio_entrar_no

label violet_quest4_banio_entrar_si:

    scene vq4_duchaescena with fade

    piensa "No puedo creer que me este atreviendo a hacer esto"
    piensa "Pero no me arrepiento"
    piensa "Tengo que irme antes de que se de cuenta"


    jump violet_quest4_cierre

label violet_quest4_banio_entrar_no:

    piensa "Mejor le dejo las cosas aca y me voy antes de que se de cuenta"

    jump violet_quest4_cierre

# --- Golpear ---
label violet_quest4_banio_golpear:

    $ ocultar_hud()

    "Toc Toc Toc"
    "Toc Toc Toc"
    violet "¿Que pasa?"
    mc "Te traje tu pijama, te dejo todo en la puerta y me voy"
    violet "Gracias"

    # +5 amor
    $ obtener_npc("violet").modificar_stat1(5)

    jump violet_quest4_cierre


################################################################################
## CIERRE DE LA QUEST
################################################################################

label violet_quest4_cierre:

    # Restaurar fondos originales
    $ loc_living = sistema_locaciones.obtener_locacion("casa_living")
    $ loc_hviolet = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ loc_pasilloarriba = sistema_locaciones.obtener_locacion("casa_pasilloarriba")
    if vq4_bg_original_living:
        $ loc_living.background_base = vq4_bg_original_living
    if vq4_bg_original_hviolet:
        $ loc_hviolet.background_base = vq4_bg_original_hviolet
    if vq4_bg_original_pasilloarriba:
        $ loc_pasilloarriba.background_base = vq4_bg_original_pasilloarriba

    # Desactivar restriccion
    $ desactivar_restriccion()

    # Avanzar el tiempo en 1
    $ avanzar_horario()

    # Completar la quest
    $ completar_quest_actual("violet")

    # Volver al game loop en la habitacion del MC
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    window hide
    $ mostrar_hud()
    jump game_loop
