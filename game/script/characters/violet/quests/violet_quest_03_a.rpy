################################################################################
## Violet Quest 03_A — Devolver los mangas
################################################################################

image vq3a_ropero   = "images/quest/violet/quest4/violet_quest04_ropero.jpg"
image vq3a_cajonera = "images/quest/violet/quest4/violet_quest04_cajonera.webp"

default vq3a_peluches_hecho  = False
default vq3a_pc_hecho        = False
default vq3a_manga_hecho     = False
default vq3a_muñecos_hecho   = False
default vq3a_mochila_hecho   = False
default vq3a_ropero_hecho    = False
default vq3a_cajonera_hecho  = False

# Flags de visibilidad de las acciones (registradas en init en actions_catalog.rpy;
# registrarlas en runtime rompía la quest al cargar un save a mitad del segmento)
default vq3a_fase1_activa = False
default vq3a_fase2_activa = False

# Skin evaluado al inicio — persiste en save para sub-labels
default vq3a_cuerpo = "c_rbase"


################################################################################
## LABEL: Pista desde interaccion NPC (fuera de la habitacion)
################################################################################

label vq3a_devolver_fuera:
    $ ocultar_hud()
    window show
    piensa "Tendría que esperar a que esté en su habitación para devolvérselos."
    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## LABEL PRINCIPAL — Entrada (desde door access)
################################################################################

label quest_violet_questprincipal_03_a:

    $ vq3a_cuerpo = cuerpo_activo("violet")

    $ ocultar_hud()
    hide screen hud_navegacion
    window show

    violet "Pasa"

    $ _loc_hviolet_03a = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet_03a = _loc_hviolet_03a.background if _loc_hviolet_03a else None
    if _bg_hviolet_03a:
        scene expression _bg_hviolet_03a with fade

    if vq3a_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right with dissolve
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda with dissolve

    show mc_parado_base b_hablando
    mc "Te traigo los mangas"
    show mc_parado_base b_none

    if vq3a_cuerpo == "c_pijama":
        show violet_parada b_hablandochica c_pijama_pensando with sprite_normal
    else:
        show violet_parada b_hablandochica c_rbase_pensando with sprite_normal
    violet "¿Ya los leíste todos?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Sí, ya los terminé de leer"
    show mc_parado_base b_none

    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3
    show mc_parado_base c_rbase_mangas with sprite_normal

    show mc_parado_base b_hablando
    mc "Toma"
    show mc_parado_base b_none

    show mc_parado_base c_rbase_base with sprite_normal
    if vq3a_cuerpo == "c_pijama":
        show violet_parada c_pijama_mangas with sprite_normal
        pause 0.3
        show violet_parada c_pijama_mangas at right_a_salir with sprite_normal
        pause 1.0
        show violet_parada c_pijama_base at entrar_a_right with sprite_normal
    else:
        show violet_parada c_rbase_mangas with sprite_normal
        pause 0.3
        show violet_parada c_rbase_mangas at right_a_salir with sprite_normal
        pause 1.0
        show violet_parada c_rbase_base at entrar_a_right with sprite_normal
    pause 0.5

    show violet_parada b_hablandochica
    violet "Bueno, listo, ya te puedes ir"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando
    mc "Ehhh, espera"
    show mc_parado_base b_abiertachica c_rbase_cuestionando with sprite_normal
    mc "¿Acaso no te interesa saber qué me pareció?"
    show mc_parado_base b_none

    if violet_recuerdo_mangas == "deseo":
        jump vq03a_rama_deseo
    else:
        jump vq03a_rama_amor


################################################################################
## RAMA: Recuerdo — Deseo
################################################################################

label vq03a_rama_deseo:

    $ notificar_recuerdo_activado()

    if vq3a_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_juzgandonm c_pijama_brazoscruzados with sprite_normal
    else:
        show violet_parada b_hablandochica o_juzgandonm c_rbase_brazoscruzados with sprite_normal
    violet "¿Vamos a hablar del manga o de mi trasero?"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando c_rbase_base
    mc "Pensaba hablar del manga, pero... bueno, si quieres hablar de tu trasero también puedo hacerlo jajaja"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Listo te puedes ir"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando
    mc "No, espera, es un chiste, no lo dije en serio"
    show mc_parado_base b_none

    show violet_parada b_hablandochica o_arribanm
    violet "La otra vez no fue un chiste"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando
    mc "No te quedes encerrada en eso"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Me es complicado no hacerlo"
    show violet_parada b_none

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Veo que se lo tomó bastante a pecho"
    piensa "No sé si es el mejor momento para hablar de eso, voy a esperar hasta que esté un poco más tranquila"
    show mc_parado_base c_rbase_base o_base b_hablando with sprite_normal
    mc "Bueno, de verdad hablemos del manga, necesito descargar con alguien"
    show mc_parado_base b_none

    jump vq03a_comun


################################################################################
## RAMA: Recuerdo — Amor
################################################################################

label vq03a_rama_amor:

    $ notificar_recuerdo_activado()

    if vq3a_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_juzgandonm c_pijama_brazoscruzados with sprite_normal
    else:
        show violet_parada b_hablandochica o_juzgandonm c_rbase_brazoscruzados with sprite_normal
    violet "Sí, pero no quiero que te pongas sentimental como la otra vez"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando c_rbase_base
    mc "Perdón, solo dije lo que pensé, no sabía que te iba a molestar"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "No me molestó, solo que no quiero hablar de eso"
    show violet_parada b_none o_base

    show mc_parado_base b_hablando
    mc "No te quedes encerrada en eso"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "Me es complicado no hacerlo"
    show violet_parada b_none

    show mc_parado_base c_rbase_pensando o_arribanm with sprite_normal
    piensa "Veo que se lo tomó bastante a pecho"
    piensa "No sé si es el mejor momento para hablar de eso, voy a esperar hasta que esté un poco más tranquila"
    show mc_parado_base c_rbase_base o_tristesnm b_hablando with sprite_normal
    mc "Bueno, de verdad hablemos del manga, necesito descargar con alguien"
    show mc_parado_base b_none

    jump vq03a_comun


################################################################################
## PUNTO COMUN — Convergencia de ramas
################################################################################

label vq03a_comun:

    if vq3a_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_felicesnm c_pijama_brazoscruzados with sprite_normal
    else:
        show violet_parada b_hablandochica o_felicesnm c_rbase_brazoscruzados with sprite_normal
    violet "Jajaja es un trauma que va a quedar ahí para siempre"
    show violet_parada b_sonrisaleve o_base

    show mc_parado_base b_hablando o_base
    mc "Sí, empezó como algo solo de acción y tiros, pensé que iba a ser eso"
    show mc_parado_base b_abiertachica
    mc "Pero el desarrollo de los personajes y la historia me pareció fascinante, todavía sigo pensando en el final"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "A mí me gustó, refleja bastante bien el mundo y la idea de los finales felices"
    show violet_parada b_none o_base

    show mc_parado_base b_abiertachica
    mc "A mí también, pero duele jajaja"
    show mc_parado_base b_hablando
    mc "¿Cuál es tu personaje favorito?"
    show mc_parado_base b_none

    vozoff "Prrr Prrr Prrr"

    if vq3a_cuerpo == "c_pijama":
        show violet_parada o_abajonm c_pijama_celu with sprite_normal
    else:
        show violet_parada o_abajonm c_rbase_celu with sprite_normal
    pause 1.0
    show violet_parada o_base b_hablandochica
    violet "Mónica necesita que la ayude con algo, ahí vengo"
    show violet_parada b_hablando
    violet "Espérame y seguimos hablando"
    show violet_parada b_none

    hide violet_parada with dissolve

    piensa "Podría ver si hay algún otro manga que me interese mientras espero"
    piensa "Y chusmear un poco su habitación, capaz que encuentro algo más para conectar con ella"

    # Quitar mangas del inventario
    $ store.inventario["mangas_violet_mc"] = store.inventario.get("mangas_violet_mc", 1) - 1
    if store.inventario.get("mangas_violet_mc", 0) <= 0:
        $ store.inventario.pop("mangas_violet_mc", None)

    hide mc_parado_base with dissolve

    $ activar_restriccion(
        duenio="violet_03_a",
        locaciones_permitidas=["casa_hviolet"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento="Podría quedarme un momento más.",
        mensajes_acciones={
            "avanzar_tiempo": "No es momento",
            "dormir": "No es momento",
            "entrenar": "No es momento",
            "trabajar": "No es momento",
            "usar_item": "No es momento",
            "comprar": "No es momento",
            "cocinar": "No es momento",
            "ver_tv": "No es momento",
        },
        mensaje_npc_bloqueado="No hay nadie aquí",
        celular_bloqueado=True,
        mensaje_celular="Ahora no",
        npcs_ocultos=["violet", "monica", "jasmine"],
    )

    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    # Las acciones estan registradas en init (actions_catalog.rpy); este flag las muestra
    $ vq3a_fase1_activa = True

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## ACCIONES — FASE 1 (5 elementos)
################################################################################

label vq3a_accion_peluches:
    $ ocultar_hud()
    window show
    piensa "Violet y su obsesión con los Slime... desde pequeña que le gustan y los colecciona"
    window hide
    $ vq3a_peluches_hecho = True
    if vq3a_peluches_hecho and vq3a_pc_hecho and vq3a_manga_hecho and vq3a_muñecos_hecho and vq3a_mochila_hecho:
        jump vq3a_monologo
    $ mostrar_hud()
    return

label vq3a_accion_pc:
    $ ocultar_hud()
    window show
    piensa "PC master race, me pregunto qué estará jugando actualmente"
    window hide
    $ vq3a_pc_hecho = True
    if vq3a_peluches_hecho and vq3a_pc_hecho and vq3a_manga_hecho and vq3a_muñecos_hecho and vq3a_mochila_hecho:
        jump vq3a_monologo
    $ mostrar_hud()
    return

label vq3a_accion_manga:
    $ ocultar_hud()
    window show
    piensa "Tiene bastantes opciones, la próxima le voy a pedir alguno de sus favoritos"
    window hide
    $ vq3a_manga_hecho = True
    if vq3a_peluches_hecho and vq3a_pc_hecho and vq3a_manga_hecho and vq3a_muñecos_hecho and vq3a_mochila_hecho:
        jump vq3a_monologo
    $ mostrar_hud()
    return

label vq3a_accion_muñecos:
    $ ocultar_hud()
    window show
    piensa "Su colección de figuras, también tiene slimes aquí"
    window hide
    $ vq3a_muñecos_hecho = True
    if vq3a_peluches_hecho and vq3a_pc_hecho and vq3a_manga_hecho and vq3a_muñecos_hecho and vq3a_mochila_hecho:
        jump vq3a_monologo
    $ mostrar_hud()
    return

label vq3a_accion_mochila:
    $ ocultar_hud()
    window show
    piensa "Tiene una mochila japonesa... sé que esas son muy caras, me pregunto cuánto le habrá costado..."
    window hide
    $ vq3a_mochila_hecho = True
    if vq3a_peluches_hecho and vq3a_pc_hecho and vq3a_manga_hecho and vq3a_muñecos_hecho and vq3a_mochila_hecho:
        jump vq3a_monologo
    $ mostrar_hud()
    return


################################################################################
## MONOLOGO — Entre las dos fases
################################################################################

label vq3a_monologo:

    $ ocultar_hud()
    window show
    piensa "Esperaba encontrar un desorden, pero tiene todo bien acomodado, un poco me sorprende"
    piensa "Descontando la cantidad de slimes por todos lados, esta podría ser mi habitación"
    piensa "La verdad que tenemos gustos similares, no debería ser tan difícil conectar con ella"
    piensa "Ahora que estoy aquí, no vi el cosplay que le regalé por ningún lado, quizás esté guardado en su ropero"

    window hide

    # Fase 2: mostrar ropero/cajonera (registradas en init en actions_catalog.rpy)
    $ vq3a_fase1_activa = False
    $ vq3a_fase2_activa = True

    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## ACCIONES — FASE 2 (ropero y cajonera)
################################################################################

label vq3a_accion_ropero:

    $ ocultar_hud()
    scene vq3a_ropero with fade
    window show
    piensa "Ahí está guardado el cosplay que le regalé y sigue en la caja"
    piensa "¿Se lo habrá probado? No me dijo nada de si le gustó o no, podría preguntarle cuando vuelva"
    piensa "Tampoco veo aquí que tenga algún otro cosplay, pensé que sí iba a haber, quizás no le gustan..."
    window hide

    $ vq3a_ropero_hecho = True

    $ _loc_hviolet_r = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet_r = _loc_hviolet_r.background if _loc_hviolet_r else None
    if _bg_hviolet_r:
        scene expression _bg_hviolet_r with fade

    if vq3a_ropero_hecho and vq3a_cajonera_hecho:
        jump vq3a_final_escena

    $ mostrar_hud()
    return


label vq3a_accion_cajonera:

    $ ocultar_hud()
    scene vq3a_cajonera with fade
    window show
    piensa "No sé qué esperaba encontrar aquí, seguí mirando por instinto"
    piensa "Está toda su ropa interior, no me imaginé que Violet usara de este tipo"
    piensa "Tiene bastante variedad"
    window hide

    $ vq3a_cajonera_hecho = True

    $ _loc_hviolet_c = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet_c = _loc_hviolet_c.background if _loc_hviolet_c else None
    if _bg_hviolet_c:
        scene expression _bg_hviolet_c with fade

    if vq3a_ropero_hecho and vq3a_cajonera_hecho:
        jump vq3a_final_escena

    $ mostrar_hud()
    return


################################################################################
## ESCENA FINAL — Violet vuelve, conversacion, fin de quest
################################################################################

label vq3a_final_escena:

    $ ocultar_hud()

    $ _loc_hviolet_f = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _bg_hviolet_f = _loc_hviolet_f.background if _loc_hviolet_f else None
    if _bg_hviolet_f:
        scene expression _bg_hviolet_f with fade

    window show

    if vq3a_cuerpo == "c_pijama":
        show violet_parada c_pijama_base ca_pijama o_base b_none at right with dissolve
    else:
        show violet_parada c_rbase_base ca_base o_base b_none at right with dissolve
    show mc_parado_base c_rbase_tanga o_base b_none at mc_izquierda with dissolve

    if vq3a_cuerpo == "c_pijama":
        show violet_parada b_hablandochica o_enojados c_pijama_brazoscruzados
    else:
        show violet_parada b_hablandochica o_enojados c_rbase_brazoscruzados
    violet "¿Me voy un momento y te pones a revisar mis cosas?"
    show violet_parada b_aburrida

    show mc_parado_base b_hablando
    mc "No, no estaba revisando nada, solo cerré el cajón que estaba abierto"
    show mc_parado_base b_none

    show violet_parada b_hablandochica
    violet "¿Y eso estaba en el piso, entonces lo estabas guardando, no?"
    show violet_parada b_none

    show mc_parado_base o_abajonm
    piensa "Estoy muerto... sí, sí lo estoy"
    show mc_parado_base o_asustados b_asustada
    pause 0.5
    show mc_parado_base b_hablando
    mc "Espera, hay una explicación"
    show mc_parado_base b_asustada

    show mc_parado_base at mc_salir_izquierda with sprite_fast
    pause 0.7

    hide violet_parada with dissolve
    hide mc_parado_base


    $ _loc_hmc_3a = sistema_locaciones.obtener_locacion("casa_hmc")
    $ _bg_hmc_3a  = _loc_hmc_3a.background if _loc_hmc_3a else None
    if _bg_hmc_3a:
        scene expression _bg_hmc_3a with fade

    show mc_parado_base c_rbase_tanga o_base b_none at Transform(xalign=0.5, yalign=1.0) with dissolve

    piensa "Escapar creo que fue la mejor opción"
    show mc_parado_base o_abajonm
    piensa "¿Ahora qué hago con esto?"
    piensa "Mejor lo guardo y cuando encuentre el momento se lo devuelvo"

    $ agregar_al_inventario("tanga_violet")

    $ vq3a_fase2_activa = False
    $ desactivar_restriccion(duenio="violet_03_a")
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_03_a")
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


################################################################################
## Usar: Tanga de Violet
################################################################################

label usar_tanga_violet:
    $ ocultar_hud()
    window show
    piensa "Contenido en desarrollo"
    window hide
    $ mostrar_hud()
    jump game_loop
