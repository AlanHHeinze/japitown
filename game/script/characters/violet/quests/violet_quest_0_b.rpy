# =============================================================================
# IMAGENES - Quest 0 Violet
# =============================================================================
image quest0_puertaviolet = "images/quest/violet/quest0/quest0_puertaviolet.jpg"
image quest0_violet = "images/quest/violet/quest0/quest0_violet.jpg"
image quest0_violet_amasando = "images/quest/violet/quest0/quest0_violet_amasando.jpg"
image quest0_violet_cambiandose = "images/quest/violet/quest0/quest0_violet_cambiandose.jpg"
image quest0_violet_cambiandose2 = "images/quest/violet/quest0/quest0_violet_cambiandose2.jpg"
image quest0_violet_cambiandose3 = "images/quest/violet/quest0/quest0_violet_cambiandose3.jpg"
image quest0_violet_esperando = "images/quest/violet/quest0/quest0_violet_esperando.jpg"
image quest0_violet_heladera = "images/quest/violet/quest0/quest0_violet_heladera.jpg"
image quest0_violet_pizzalista = "images/quest/violet/quest0/quest0_violet_pizzalista.jpg"
image quest0_violet_poniendopizza = "images/quest/violet/quest0/quest0_violet_poniendopizza.jpg"
image quest0_violet_puertahabitacion = "images/quest/violet/quest0/quest0_violet_puertahabitacion.jpg"
image quest0_violet_sacandopizza = "images/quest/violet/quest0/quest0_violet_sacandopizza.jpg"
image quest0_violet_cenando = "images/quest/violet/quest0/quest0_violet_cenando.jpg"

# =============================================================================

# True una vez que el jugador vio el tutorial de elecciones (compartido entre
# la quest 0_b de Violet y la 0_a de Jasmine — solo se muestra en la primera).
default tutorial_elecciones_visto = False

# Rama elegida ("respeto" | "confrontar"): se decide temprano y se lee mucho
# después, en el cierre (tras cocinar). DEBE ser `default` sin `_`: las variables
# con `_` no se guardan, así que si el jugador guardaba entre la decisión y el
# cierre, se perdía y crasheaba con NameError (E05). Antes era una temp `_`.
default vq0b_ruta = ""

# ⚠️ EL LISTENER DE "COCINAR" VIVE EN actions_catalog.rpy, EN INIT. Antes se
# registraba aca, en runtime, dentro de los dos labels de eleccion.
# `sistema_acciones` es `define` —no se guarda— asi que quien guardaba entre la
# eleccion y el cocinar cargaba sin listener: "Cocinar" corria el generico, la
# restriccion no se levantaba nunca y la partida quedaba trabada en la primera
# quest de Violet. Su condicion se DERIVA de `vq0b_ruta` y del estado de la
# quest (nada nuevo que guardar), asi que una partida que ya venia trabada se
# destraba sola al cargar. Auditoria 2026-09-10.

# Hito que habilita la tercera opcion de la decision ("Ya esta resuelto"): el
# primer hito de amor de Violet. Va como constante y no suelto en el screen para
# que el id se escriba UNA vez — la etiqueta y el `sensitive` tienen que mirar
# al mismo hito o la opcion queda gris con el nombre puesto, o al reves.
define VQ0B_HITO_RESUELTO = "violet_hito_amor_01"

# ⚠️ LA TERCERA OPCION ESTA ESCONDIDA hasta que su rama tenga contenido. Hoy
# elegirla solo mostraba "Este contenido se agregará en futuras
# actualizaciones" y volvia a la decision: con el hito ya ganado, el jugador la
# veia habilitada y no entendia por que no pasaba nada. Al escribir la rama,
# poner esto en True y la opcion vuelve tal cual (etiqueta con el hito, gris
# sin el hito).
define VQ0B_RESUELTO_DISPONIBLE = False


# QUEST 0 - El Muro de Cristal (Violet)
# =============================================================================
# Para activar un recuerdo y mostrar la notificación flotante, usar:
#   $ notificar_recuerdo_activado()
#   $ notificar_recordara("violet")
# =============================================================================
label quest_violet_questprincipal_0_b:
    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion

    # =========================================================================
    # ESCENA 1: Pasillo (Puerta Cerrada)
    # =========================================================================
    # Fija el cuadro de dialogo en todo el tramo (cierra con el `window hide`
    # del final): sin esto cada `scene` lo esconde y la linea siguiente lo
    # reaparece. Ver la nota de config.window en ui/base/options.rpy.
    window show

    scene quest0_violet_puertahabitacion with fade

    # (Mc espalda brazos cruzados)
    show mc_espalda_base brazoscruzados at mc_cerca:
        xzoom -1.0

    piensa "Conozco a Violet como para saber que está molesta por algo"
    piensa "Si no doy el primer paso para hablar, ella no lo va a hacer"

    # (Mc espalda golpeando puerta)
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    # (Mc espalda golpeando ruido)
    show mc_espalda_base golpeandoruido with sprite_normal
    "Toc Toc Toc"
    # (Mc espalda golpeando puerta)
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    # (Mc espalda golpeando ruido)
    show mc_espalda_base golpeandoruido with sprite_normal
    "Toc Toc Toc"
    pause 0.5

    violet "¿Quién?"

    # (Mc espalda brazos cruzados)
    show mc_espalda_base brazoscruzados
    mc "[mc_name]"

    violet "No hay nadie"

    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    pause 0.3
    # (Mc espalda rascandose 2)
    show mc_espalda_base rascarse2
    pause 0.3
    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    mc "¿Y quién me respondió?"
    pause 0.3

    # (Mc espalda brazos cruzados)
    show mc_espalda_base brazoscruzados
    mc "Vamos... solo quiero hablar contigo"

    violet "Yo no quiero"

    mc "¿Sabes que voy a estar viviendo en esta casa?"
    mc "En algún momento me vas a tener que hablar"

    violet "Puede que no sea necesario"

    mc "No seas caprichosa y ábreme la puerta"

    violet "No"

    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    pause 0.3
    # (Mc espalda rascandose 2)
    show mc_espalda_base rascarse2
    pause 0.3
    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    piensa "Está más terca de lo que la recuerdo"
    piensa "¿Qué debería hacer?"

    jump tutorial_elecciones_violet

label tutorial_elecciones_violet:

    # Tutorial de elecciones compartido con la quest 0_a de Jasmine.
    # Como no se sabe qué quest hará primero el jugador, solo se muestra una vez.
    if not tutorial_elecciones_visto:
        tutorial "A lo largo del desarrollo de la historia de un personaje nos iremos encontrando varias veces con distintas opciones para elegir. Estas representan la manera en la que nuestro personaje va a actuar ante la situación"
        tutorial "Estas elecciones afectan el desarrollo inmediato como también a largo plazo. Los personajes recordarán las elecciones elegidas y actuarán en relación a ello en ciertos momentos"
        $ tutorial_elecciones_visto = True

    jump elecciones_violet_continuar

# Menu de la decision. NO es un `menu:` de Ren'Py: la tercera opcion tiene que
# VERSE aunque no se pueda elegir, y un `menu:` esconde las opciones que no
# cumplen su condicion. Es el mismo screen propio que usan las otras elecciones
# especiales del juego (quests 05_c, 06_b y 08_a de Violet), con el layout y el
# estilo del `screen choice` para que se vea igual que cualquier otra eleccion.
screen vq0b_menu_elecciones():
    modal True

    vbox:
        xalign 0.5
        ypos 405
        yanchor 0.5
        spacing gui.choice_spacing

        textbutton "Quizás darle su espacio funcione":
            style "choice_button"
            action Return("respeto")

        textbutton "Lo mejor seria confrontarla":
            style "choice_button"
            action Return("confrontar")

        # Pide el primer hito de amor. La etiqueta se arma desde el catalogo de
        # hitos, asi que si el hito se renombra la opcion lo sigue sola.
        # Escondida mientras la rama no tenga contenido (ver
        # VQ0B_RESUELTO_DISPONIBLE, arriba).
        if VQ0B_RESUELTO_DISPONIBLE:
            textbutton etiqueta_opcion_hito("Ya esta resuelto", VQ0B_HITO_RESUELTO):
                style "choice_button"
                action Return("resuelto")
                sensitive hito_alcanzado(VQ0B_HITO_RESUELTO)


label elecciones_violet_continuar:

    call screen vq0b_menu_elecciones

    if _return == "respeto":
        jump quest_violet_0_opcion_respeto

    elif _return == "confrontar":
        jump quest_violet_0_opcion_entrar

    # "Ya esta resuelto": la rama todavia no esta escrita. Hoy no se llega
    # porque la opcion esta escondida (VQ0B_RESUELTO_DISPONIBLE); el aviso queda
    # como red si alguien la prende antes de escribirla.
    "Este contenido se agregará en futuras actualizaciones"

    jump elecciones_violet_continuar

# =============================================================================
# OPCIÓN A: RESPETO (+Relacion, +Empatía)
# =============================================================================
label quest_violet_0_opcion_respeto:

    # (Mc espalda brazos cruzados)
    show mc_espalda_base brazoscruzados
    mc "No sé cuál es el problema y tampoco sé si es conmigo"
    mc "En el momento que me quieras contar por qué y con quién estás enojada, voy a estar para escucharte"

    violet "No estoy enojada, de un momento para el otro tengo un extraño viviendo en mi casa"
    violet "Y no tengo nada que hablar con ese extraño"

    mc "¿Desde cuándo soy un extraño?"

    violet "¿Cuándo fue la última vez que hablamos?"

    mc "Hace algunos años supongo"

    violet "Eso hacen los extraños"

    piensa "Supongo que tiene un punto válido"
    piensa "Debería esforzarme en mejorar la relación y dejar de ser un extraño"
    piensa "¿Qué puedo hacer...?"

    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    pause 0.3
    # (Mc espalda rascandose 2)
    show mc_espalda_base rascarse2
    pause 0.3
    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    piensa "La conozco como para saber que la comida puede ser un buen punto para atacar"
    pause 0.3

    mc "Bueno, me voy y no te molesto más"

    violet "Gracias"

    mc "Estaba con ganas de cocinar pizzas para la cena, pero supongo que no quieres comer pizzas hechas por un extraño"

    violet "Sí quiero"

    mc "Jajaja, ¿eso sí?"

    violet "Es normal comer pizzas hechas por extraños"
    violet "No conozco a todos los vendedores de pizzas"

    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    pause 0.3
    # (Mc espalda rascandose 2)
    show mc_espalda_base rascarse2
    pause 0.3
    # (Mc espalda rascandose 1)
    show mc_espalda_base rascarse1
    piensa "Vuelve a tener un punto... de momento me voy a concentrar en la pizza"

    # (Mc espalda brazos cruzados)
    show mc_espalda_base brazoscruzados
    mc "Me voy a cocinar, te aviso cuando esté lista"

    violet "Bueno"

    mc "Por cierto, antes de que me olvide. El extraño que vive en tu casa te trajo un regalo"
    mc "Si no lo quieres, no hay problema"

    violet "Déjalo en la puerta, ahora estoy descambiada"

    #Poner animacion sacar el regalo
    $ quitar_del_inventario("regalo_violet")

    piensa "Creo que conseguí avanzar un poco en la relación"

    $ vq0b_ruta = "respeto"

    # =========================================================================
    # Modo restringido: el jugador debe ir a la cocina
    # =========================================================================
    piensa "Debería ir a la cocina a prepararlas, Mónica me dijo que había todo lo necesario"

    # validar_bloqueos: reloj libre — la salida ES cocinar
    $ activar_restriccion(
        duenio="violet_0_b",
        locaciones_permitidas=["casa_pasilloarriba", "casa_living", "casa_pasilloabajo", "casa_cocina"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar", "ver_tv"],
        mensaje_movimiento=_("Deberia ir a la cocina a preparar la pizza"),
        mensajes_acciones={
            "avanzar_tiempo": _("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
        },
        celular_bloqueado=True,
        mensaje_celular=_("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
        # Nadie se esconde: Monica y Jasmine siguen su rutina (se las ve, se
        # las cruza) pero estan RESERVADAS para esta quest — clickearlas
        # devuelve este mensaje. Violet esta en su pieza por la rutina de la
        # quest, fuera del recorrido permitido.
        mensaje_npc_bloqueado=_("Tengo que encargarme de las pizzas antes de hacer otra cosa"),
    )

    # El listener de "Cocinar" esta en init (actions_catalog.rpy) y se prende
    # solo con vq0b_ruta puesta y la quest activa. Nada se registra acá.

    # Mover al jugador al pasillo arriba (donde esta la puerta de Violet)
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


# =============================================================================
# OPCIÓN B: CONFRONTACIÓN (Entrar)
# =============================================================================
label quest_violet_0_opcion_entrar:

    # (Mc espalda brazos cruzados)
    show mc_espalda_base brazoscruzados
    mc "Violet, voy a entrar... No sé cuál es el problema, pero no quiero estar por la casa y que me estés esquivando"

    violet "No"

    mc "3"

    violet "Dije que no"

    mc "2"

    violet "Que no"

    mc "1"

    # Cambio de escena: Cuarto Violet
    # Fija el cuadro de dialogo en todo el tramo (cierra con el `window hide`
    # del final): sin esto cada `scene` lo esconde y la linea siguiente lo
    # reaparece. Ver la nota de config.window en ui/base/options.rpy.
    window show

    scene quest0_violet with fade

    # (Violet cuerpo brazos cruzados ojos enojada boca aburrida)
    show violet_parada c_rbase_brazoscruzados o_enojados b_aburrida at right
    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "¡¿Qué haces?! ¡Te dije que no podías entrar!"
    # (Violet boca aburrida)
    show violet_parada b_aburrida

    # (Mc ojos abajo)
    show mc_parado_base o_abajonm
    pause 0.5
    # (Mc ojos base)
    show mc_parado_base o_base
    pause 0.5
    # (Mc ojos arriba)
    show mc_parado_base o_arribanm
    pause 0.5
    # (Mc ojos base)
    show mc_parado_base o_base

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Recordaba tu habitación muy distinta... Pero me gusta el estilo nuevo"
    # (Mc boca sonrisa abierta)
    show mc_parado_base b_abiertachica
    mc "Te convertiste en toda una otaku, estoy orgulloso"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet cuerpo fuck you)
    show violet_parada c_rbase_fuckyou with sprite_normal
    pause 0.5
    # (Violet cuerpo brazos cruzados)
    show violet_parada c_rbase_brazoscruzados

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "¡Si no te vas ahora, voy a llamar a Mónica!"
    # (Violet boca aburrida)
    show violet_parada b_aburrida

    # (Mc boca hablando cuerpo pensando)
    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "Jajaja, ¿qué le vas a decir?"
    # (Mc boca sonrisa abierta)
    show mc_parado_base b_abiertachica
    mc "Pienso ignorar a [mc_name] el resto de mi vida y está aquí adelante mío hablándome ¿...?"
    # (Mc boca feliz cerrada ojos base cuerpo base)
    show mc_parado_base b_felizcerrada o_base c_rbase_base with sprite_normal

    # (Violet boca hablando ojos juzgando cuerpo pensando)
    show violet_parada b_hablando o_juzgandonm c_rbase_pensando with sprite_normal
    violet "Le voy a decir que te dije que no entres porque estaba descambiada y entraste igual"
    # (Violet boca neutral cuerpo brazos cruzados)
    show violet_parada b_none c_rbase_brazoscruzados with sprite_normal

    # (Mc boca hablando cuerpo señalando)
    show mc_parado_base b_hablando c_rbase_señalando with sprite_normal
    mc "No seas chiquilina, sabes que Mónica no te va a creer eso"
    # (Mc boca seria cuerpo base)
    show mc_parado_base b_seria c_rbase_base with sprite_normal

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "¿Qué quieres?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando cuerpo cuestionando)
    show mc_parado_base b_hablando c_rbase_cuestionando with sprite_normal
    mc "Hablar, cuando llegué ni me saludaste y cuando me acerco te vas"
    # (Mc boca sonrisa abierta)
    show mc_parado_base b_abiertachica
    mc "Solo quiero saber, ¿qué te pasa?"
    # (Mc boca seria cuerpo base)
    show mc_parado_base b_seria c_rbase_base with sprite_normal

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Nada"
    # (Violet boca hablando chica ojos arriba)
    show violet_parada b_hablandochica o_arribanm
    violet "¿Feliz?"
    # (Violet ojos base boca neutral)
    show violet_parada o_base b_none

    # (Mc boca hablando ojos molesto)
    show mc_parado_base b_hablando o_molestos
    mc "No, te dije que vamos a hablar y no me voy a ir hasta que hablemos"
    # (Mc boca seria)
    show mc_parado_base b_seria

    # (Violet ojos abiertos)
    show violet_parada o_abiertos
    pause 0.5

    # (Violet boca hablando ojos costado)
    show violet_parada b_hablando o_costadobase
    violet "No estoy enojada, de un momento para el otro tengo un extraño viviendo en mi casa"
    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "Y no tengo nada que hablar con ese extraño"
    # (Violet boca neutral ojos base)
    show violet_parada b_none o_base

    # (Mc boca hablando ojos base cuerpo pensando)
    show mc_parado_base b_hablando o_base c_rbase_pensando with sprite_normal
    mc "¿Desde cuándo soy un extraño?"
    # (Mc boca seria cuerpo base)
    show mc_parado_base b_seria c_rbase_base with sprite_normal

    # (Violet boca hablando ojos pensando)
    show violet_parada b_hablando o_pensando
    violet "¿Cuándo fue la última vez que hablamos?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando ojos abajo)
    show mc_parado_base b_hablando o_abajonm
    mc "Hace algunos años supongo"
    # (Mc boca seria)
    show mc_parado_base b_seria

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "Eso hacen los extraños"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc cuerpo pensando ojos arriba)
    show mc_parado_base c_rbase_pensando o_arribanm
    piensa "Supongo que tiene un punto válido"
    piensa "Pero no podemos seguir así para siempre"
    piensa "Algo tengo que hacer"
    # (Mc cuerpo base ojos base)
    show mc_parado_base c_rbase_base o_base

    # (Mc boca hablando cuerpo señalando)
    show mc_parado_base b_hablando c_rbase_señalando with sprite_normal
    mc "Ahora estamos hablando, ya dejamos de ser extraños, entonces si te hablo me respondes"
    # (Mc boca sonrisa abierta)
    show mc_parado_base b_abiertachica
    mc "¿Está bien?"
    # (Mc boca seria cuerpo brazos cruzados)
    show mc_parado_base b_seria c_rbase_brazoscruzados with sprite_normal

    # (Violet ojos abiertos sonrojo)
    show violet_parada o_abiertos ot_avergonzada

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "¿Se entendió?"
    # (Mc boca seria)
    show mc_parado_base b_seria

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Sí..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "¿Sí qué?"
    # (Mc boca seria)
    show mc_parado_base b_seria

    # (Violet boca hablando cuerpo vergüenza)
    show violet_parada b_hablando c_rbase_verguenza with sprite_normal
    violet "Sí, señor"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc cuerpo pensando)
    show mc_parado_base c_rbase_pensando with sprite_normal
    piensa "Eso fue raro..."
    # (Mc cuerpo base)
    show mc_parado_base c_rbase_base with sprite_normal

    # (Mc boca hablando cuerpo señalando)
    show mc_parado_base b_hablando c_rbase_señalando with sprite_normal
    mc "Entonces... ¿Nos vamos a empezar a llevar mejor?"
    # (Mc boca seria cuerpo brazos cruzados)
    show mc_parado_base b_seria c_rbase_brazoscruzados with sprite_normal

    # (Violet boca hablando chica cuerpo sorprendida)
    show violet_parada b_hablandochica c_rbase_sorprendido with sprite_normal
    violet "Sí..."
    # (Violet boca neutral)
    show violet_parada b_none

    piensa "Tenía razón, hablando la gente se entiende y parece que cambió un poco su actitud"
    piensa "Pero se la ve un poco tensa, vamos a cambiar el ambiente"

    # (Violet boca hablando chica)
    show violet_parada b_hablandochica
    violet "¿Qué pasa?"
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Me acordé de que te traje un regalo"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet ojos abiertos cuerpo base)
    show violet_parada o_abiertos c_rbase_base with sprite_normal

    # (Mc cuerpo mochila 1)
    show mc_parado_base c_rbase_mochila1 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 2)
    show mc_parado_base c_rbase_mochila2 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 3)
    show mc_parado_base c_rbase_mochila3 with sprite_normal
    pause 0.3
    # (Mc cuerpo mochila 4)
    show mc_parado_base c_rbase_mochila4 with sprite_normal
    pause 0.3

    # (Mc cuerpo regalo violet)
    show mc_parado_base c_rbase_cajacosplay with sprite_normal
    pause 0.3
    # (Mc boca hablando cuerpo base)
    show mc_parado_base b_hablando c_rbase_base with sprite_normal

    $ quitar_del_inventario("regalo_violet")

    # (Violet cuerpo recibiendo regalo)
    show violet_parada c_rbase_cajacosplay with sprite_normal
    mc "Toma"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Eh, gracias... ¿Qué es?"
    # (Violet boca sonrisa pequeña)
    show violet_parada b_sonrisapequeña

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Te va a gustar"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Mc ojos abajo cuerpo celular)
    show mc_parado_base o_abajonm c_rbase_celular with sprite_normal
    pause 1.5
    # (Mc ojos base cuerpo base)
    show mc_parado_base o_base c_rbase_base with sprite_normal

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Se me hizo tarde... Le dije a Mónica que iba a cocinar pizzas hoy"
    # (Mc boca neutral)
    show mc_parado_base b_none
    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Después me dices si te gustó el regalo"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando ojos feliz)
    show violet_parada b_hablando o_felices
    violet "Siiii pizza"
    # (Violet boca sonrisa pequeña ojos abiertos)
    show violet_parada b_sonrisapequeña o_abiertos

    # (Mc ojos abajo boca seria cuerpo facepalm)
    show mc_parado_base o_abajonm b_seria c_rbase_facepalm with sprite_normal
    piensa "Cierto, Violet es fanática de la pizza"
    piensa "Quizás podría haber empezado por ahí, hubiera sido más fácil"
    # (Mc ojos base boca neutral cuerpo base)
    show mc_parado_base o_base b_none c_rbase_base with sprite_normal

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "Te aviso cuando esté lista"
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "Está bien"
    # (Violet boca sonrisa leve)
    show violet_parada b_sonrisaleve

    $ vq0b_ruta = "confrontar"

    # =========================================================================
    # Modo restringido: el jugador debe ir a la cocina
    # =========================================================================
    $ ocultar_hud()
    hide screen hud_navegacion

    piensa "Bueno, voy a ir a preparar la pizza"

    # validar_bloqueos: reloj libre — la salida ES cocinar
    $ activar_restriccion(
        duenio="violet_0_b",
        locaciones_permitidas=["casa_pasilloarriba", "casa_living", "casa_pasilloabajo", "casa_cocina"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar", "ver_tv"],
        mensaje_movimiento=_("Deberia ir a la cocina a preparar la pizza"),
        mensajes_acciones={
            "avanzar_tiempo": _("Tengo que cocinar primero"),
        },
        celular_bloqueado=True,
        mensaje_celular=_("Tengo que cocinar primero"),
        # Idem rama "respeto": nadie oculto, Monica y Jasmine reservadas.
        mensaje_npc_bloqueado=_("Tengo que cocinar primero"),
    )

    # El listener de "Cocinar" esta en init (actions_catalog.rpy) y se prende
    # solo con vq0b_ruta puesta y la quest activa. Nada se registra acá.

    # Mover al jugador al pasillo arriba (donde esta la puerta de Violet)
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    # Devolver control al jugador
    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


# =============================================================================
# CIERRE: Se dispara al entrar a la cocina (ambas ramas llegan aqui)
# =============================================================================
label quest_violet_0_cierre:
    # Desactivar restriccion
    $ desactivar_restriccion(duenio="violet_0_b")

    # Ocultar HUD
    $ ocultar_hud()
    hide screen hud_navegacion

    # Mc hace pizzas
    # Fija el cuadro de dialogo en todo el tramo (cierra con el `window hide`
    # del final): sin esto cada `scene` lo esconde y la linea siguiente lo
    # reaparece. Ver la nota de config.window en ui/base/options.rpy.
    window show

    scene bg_casa_noche_cocina with fade

    mc "Debería ponerme a cocinar"

    show quest0_violet_heladera with sprite_normal
    piensa "Voy a tener que acercarme de a poco dándole espacio"
    piensa "Recurriendo a cosas que le gusten"

    show quest0_violet_amasando with sprite_normal
    piensa "También tendría que ver qué es lo que la tiene enfadada"
    piensa "Porque evidentemente es conmigo el problema"

    show quest0_violet_poniendopizza with sprite_normal
    piensa "Supongo que estaba cómoda con su vida y de la nada llega alguien a molestarme"
    piensa "Aunque no sea mi intención, en algún punto lo estoy haciendo"

    show quest0_violet_esperando with sprite_normal
    piensa "Ya veré cómo resolverlo"
    piensa "No quiero involucrar a Mónica, ya debe tener los suficientes problemas"

    show quest0_violet_sacandopizza with sprite_normal
    piensa "Espero que esta pizza ayude"

    show quest0_violet_pizzalista with sprite_normal
    piensa "Voy a llamarla para que baje a comer"

    $ avanzar_horario()

    $ activar_restriccion(
        duenio="violet_0_b",
        locaciones_permitidas=["casa_pasilloabajo", "casa_living", "casa_pasilloarriba", "casa_hviolet"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar", "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Debo avisarle a Violet que esta la comida"),
        celular_bloqueado=True,
        # Monica y Jasmine visibles y reservadas; Violet en su pieza (rutina
        # de la quest de noche), a donde hay que ir.
        mensaje_npc_bloqueado=_("Debo avisarle a Violet que esta la comida"),
    )

    # Al entrar a la habitacion de Violet se dispara la escena
    $ restriccion_quest_activa.registrar_label_locacion("casa_hviolet", "quest_violet_0_puerta")

    $ sistema_locaciones.mover_a_locacion("casa_pasilloabajo")

    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop


# =============================================================================
# PUERTA: Se dispara al ir a la habitacion de Violet
# =============================================================================
label quest_violet_0_puerta:
    $ desactivar_restriccion(duenio="violet_0_b")

    $ ocultar_hud()
    hide screen hud_navegacion

    # Fija el cuadro de dialogo en todo el tramo (cierra con el `window hide`
    # del final): sin esto cada `scene` lo esconde y la linea siguiente lo
    # reaparece. Ver la nota de config.window en ui/base/options.rpy.
    window show

    scene quest0_violet_puertahabitacion with fade

    # (Mc espalda golpeando puerta)
    show mc_espalda_base golpeando at mc_cerca:
        xzoom -1.0
    "Toc Toc Toc"
    pause 0.3
    # (Mc espalda golpeando ruido)
    show mc_espalda_base golpeandoruido with sprite_normal
    "Toc Toc Toc"
    # (Mc espalda golpeando puerta)
    show mc_espalda_base golpeando with sprite_normal
    pause 0.3
    # (Mc espalda golpeando ruido)
    show mc_espalda_base golpeandoruido with sprite_normal
    piensa "Me está ignorando de nuevo... Esta vez voy a entrar y decirle las cosas"

    scene quest0_violet_cambiandose with fade
    mc "..."
    scene quest0_violet_cambiandose2 with dissolve
    mc "Eh... perdón"
    scene quest0_violet_cambiandose3 with dissolve
    mc "Me voy..."

    scene quest0_violet_cenando with fade
    vozoff "En la cena Violet se sentó en la punta de la mesa, lejos de mí y no me habló en toda la noche"
    pause 0.3

    # Evaluar ruta elegida y aplicar stats
    if vq0b_ruta == "respeto":
        $ obtener_npc("violet").modificar_stat1(2, reserva=True)
    elif vq0b_ruta == "confrontar":
        $ obtener_npc("violet").modificar_stat2(2, reserva=True)

    # Finalizar Quest
    $ avanzar_horario()
    $ sistema_locaciones.mover_a_locacion("casa_hmc")
    $ completar_quest_actual("violet", quest_id="violet_questprincipal_0_b")
    $ activar_estado_especial_npc("violet", "violet_feliz")
    # Acá se llamaba post_completar_violet_quest0(), que abria el stock del
    # casco VR y avisaba por Libre Mercado. Los dos efectos se movieron al
    # trigger de ventajas/juegosnuevos/jn_cascovr.rpy: ahora el casco sale a la
    # venta recien con el hito de amor 20, que es cuando Violet lo menciona.

    # Restaurar HUD y devolver control al jugador
    window hide
    $ mostrar_hud()
    show screen hud_navegacion
    jump game_loop
