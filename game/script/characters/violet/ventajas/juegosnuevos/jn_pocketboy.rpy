################################################################################
## Juego Nuevo — POCKET BOY  (arco parkeado)
################################################################################
## ⚠️ HOY NO SE PUEDE JUGAR. Esta registrado en el sistema de Juegos Nuevos pero
## con `_jn_pocketboy_jugado()` devolviendo True a proposito, asi que Violet no
## lo menciona nunca y ninguna de sus escenas es alcanzable. Para revivirlo, ver
## "COMO REVIVIRLO" al final de esta cabecera.
##
## DE DONDE VIENE: era la quest de amor 15 ("Juegos Viejos"), la de buscar la
## Portatil Boy en el altillo. Se saco de la linea de amor —que se rehace de
## cero— y todo su arco se mudo acá entero: escenas, chat, accion de locacion,
## rutina, imagenes y flags. El archivo es autocontenido.
##
## ⚠️ TODO SE RENOMBRO de `va15_*` / `violet_amor_15_*` a `jnpb_*` /
## `jn_pocketboy_*`. NO es cosmetico: la quest 15 nueva va a definir sus propios
## flags y labels, y con los nombres viejos se pisarian. El costo es que una
## partida a mitad del arco viejo lo pierde — asumido, porque el contenido queda
## inalcanzable igual.
##
## LAS ESCENAS, en orden:
##   1. jn_pocketboy_pasillo   Violet lo llama desde el altillo, sin aparecer.
##   2. jn_pocketboy_altillo   La charla antes de ponerse a buscar.
##   3. jn_pocketboy_molestar  Click en su sprite mientras buscan; a la 5a vez...
##   4. jn_pocketboy_charla    ...se abre esta escena (primer plano).
##   5. jn_pocketboy_cierre    La accion "Buscar": encuentran la consola y caen.
##
## COMO REVIVIRLO:
##   1. `_jn_pocketboy_jugado()` -> que devuelva el flag real, no True.
##   2. Reponer el enganche del click en el sprite de Violet, que se saco de
##      characters/violet/interaction/interactions_violet.rpy:
##          if getattr(store, 'jnpb_fase', 0) == 2 and <condicion>:
##              jump jn_pocketboy_molestar
##   3. Darle un disparador: los labels estan, pero el trigger de game_loop de
##      abajo pide una quest que ya no existe (ver _gl_trigger_jn_pocketboy).


################################################################################
## Estado
################################################################################

# Dia (dias_totales) en que se completo el chat. None = todavia no paso.
default jnpb_dia_chat = None

# 0 = nada · 1 = Violet ya lo llamo desde el pasillo · 2 = charla hecha, buscando
default jnpb_fase = 0

# Veces que el jugador clickeo a Violet mientras buscan. Se acumula acá y no en
# una variable de escena porque entre click y click el jugador esta suelto en el
# loop y puede guardar la partida.
default jnpb_clicks_violet = 0


init python:

    # ── Requisitos y textos de la quest (los usa quests_amor_violet.rpy) ─────

    def _jnpb_paso_un_dia():
        """
        True cuando paso al menos un dia desde que se completo el chat.

        dias_totales es el contador absoluto (sube en cada dormir()), asi que
        compararlo evita todo el enredo de fin de mes o de semana.
        """
        _dia = getattr(store, 'jnpb_dia_chat', None)
        if _dia is None:
            return False
        return getattr(store, 'dias_totales', 0) > _dia

    def _jnpb_pista_condiciones():
        """Pista de ETAPA_CONDICIONES — cambia segun el tramo."""
        if obtener_stat1("violet") < 15:
            return renpy.translate_string("Puedo seguir acercandome a Violet.")
        # NO repetir acá la descripcion de la quest: dos `old` con el mismo
        # texto en el tl rompen el lint.
        return renpy.translate_string("Tengo que ver si aparece la Portatil Boy.")

    def _jnpb_quehacer_condiciones():
        """Que hacer en ETAPA_CONDICIONES — los tres tramos, en orden."""
        if obtener_stat1("violet") < 15:
            return _quehacer_amor_violet(15)
        if not store.sistema_mensajes.grupo_completado("violet_jnpb_chat"):
            return renpy.translate_string("Esperar el mensaje de Violet")
        return renpy.translate_string("Darle tiempo para que la busque")

    # ── Chat ─────────────────────────────────────────────────────────────────

    def _jnpb_chat_separados():
        """
        condicion_entrega del chat: que NO esten en la misma locacion.

        Si Violet esta fuera de casa tracker_locacion_npc devuelve None, que
        nunca va a coincidir con la locacion del MC — o sea que estando ella
        afuera el mensaje tambien llega, que es lo correcto.
        """
        _loc_mc = store.sistema_locaciones.locacion_actual
        if _loc_mc is None:
            return False
        return tracker_locacion_npc("violet") != _loc_mc.id

    def _jnpb_chat_completado():
        """
        accion_al_completar del chat: anota el dia para empezar a contar la
        espera. Funcion de MODULO — se guarda en el save via el grupo.
        """
        store.jnpb_dia_chat = getattr(store, 'dias_totales', 0)

    # ── Disparadores ─────────────────────────────────────────────────────────

    def _gl_trigger_jn_pocketboy():
        """
        Trigger de game_loop del arco. HOY ESTA APAGADO (ver el return de la
        primera linea): el arco esta parkeado y ninguna de sus escenas debe
        dispararse.

        Cuando lo revivas, ademas de sacar ese return hay que darle un
        disparador propio: la condicion de abajo mira la quest de amor 15, que
        se rehizo de cero y ya no gobierna este contenido.

        Lo que hacia, segun la etapa:
        - ETAPA_CONDICIONES con amor >= 15: disparaba el chat y devolvia None.
        - ETAPA_BOTON_LISTO: devolvia el label de la escena que tocaba.
        """
        return None

        _q = store.sistema_quests.obtener_quest("violet_amor_03")
        if _q is None or not _q.activa or _q.completada:
            return None

        if _q.etapa_actual == ETAPA_CONDICIONES:
            if obtener_stat1("violet") >= 15:
                store.sistema_mensajes.disparar_por_trigger(
                    "manual", "violet_jnpb_chat", "violet")
            return None

        if _q.etapa_actual != ETAPA_BOTON_LISTO:
            return None

        # La charla del altillo ya paso: de acá en mas manda la accion Buscar.
        if store.jnpb_fase >= 2:
            return None

        if store.horario_actual != 2:
            return None

        _loc = store.sistema_locaciones.locacion_actual
        if _loc is None:
            return None

        if _loc.id == "casa_altillo":
            return "jn_pocketboy_altillo"

        if store.jnpb_fase == 0 and _loc.id == "casa_pasilloarriba":
            return "jn_pocketboy_pasillo"

        return None

    def _jnpb_buscar_visible():
        """
        Condicion de la AccionLocacion 'Buscar' (actions_catalog).

        Es `== 2` y no `>= 2`: la escena de cierre sube la fase a 3 antes de
        empezar, y con `>=` el boton habria quedado en el altillo para siempre
        despues de terminar la quest.
        """
        return getattr(store, 'jnpb_fase', 0) == 2

    # ── Juegos Nuevos ────────────────────────────────────────────────────────

    def _jn_pocketboy_jugado():
        """
        ⚠️ DEVUELVE True FIJO PARA MANTENER EL ARCO PARKEADO.

        El controlador solo ofrece los juegos NO jugados, asi que con True
        constante Violet nunca lo menciona y el arco queda invisible.

        Al revivirlo, cambiar por la lectura del flag real:

            return getattr(store, 'jnpb_fase', 0) >= 3
        """
        return True


init 5 python:

    # Registrado aunque este apagado: asi figura en el sistema y no hay que
    # acordarse de agregarlo, solo de destrabar _jn_pocketboy_jugado().
    registrar_juego_nuevo(
        "pocketboy",
        "Todavía tengo por ahí la Portátil Boy, si la encontramos podríamos jugar",
        _jn_pocketboy_jugado,
    )

    registrar_trigger_game_loop("jn_pocketboy_escenas",
                                _gl_trigger_jn_pocketboy)

    # (La accion "Buscar" del altillo NO se registra acá: TODAS las acciones del
    # juego viven en core/actions/actions_catalog.rpy. Su condicion sigue siendo
    # _jnpb_buscar_visible, de este archivo.)


################################################################################
## 1 · EL PASILLO — Violet lo llama desde arriba, sin aparecer
################################################################################

label jn_pocketboy_pasillo:

    $ ocultar_hud()
    window show

    $ _jnpb_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _jnpb_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — Violet habla SIN sprite: esta arriba, en el altillo
    # =========================================================================

    violet "[mc_name], sube a ayudarme por favor"
    violet "Hay un montón de cajas, no voy a terminar más"

    # (Mc ojos arriba)
    show mc_parado_base o_arribanm b_hablando
    mc "Ahora voy"
    # (Mc ojos base boca neutral)
    show mc_parado_base o_base b_none

    violet "Gracias"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # Quedo en ir a ayudarla: hasta subir al altillo no se hace otra cosa.
    $ activar_restriccion(
        locaciones_permitidas=["casa_altillo"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("Le dije que la iba a ayudar, primero subo al altillo"),
        mensaje_accion_default=_("Le dije que la iba a ayudar, primero subo al altillo"),
        celular_bloqueado=True,
        mensaje_celular=_("Le dije que la iba a ayudar, primero subo al altillo"),
    )

    $ jnpb_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · EL ALTILLO — la charla, y arranca la busqueda
################################################################################

label jn_pocketboy_altillo:

    $ ocultar_hud()
    window show

    $ _jnpb_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _jnpb_bg

    # Violet revolviendo cajas: el MISMO idle y la MISMA posicion que usa su
    # rutina en el altillo, para que al terminar la escena y volver al loop no
    # se note ningun salto — el sprite del HUD aparece donde estaba este.
    #
    # Las constantes salen de quests_amor_violet.rpy. El anclaje se replica a
    # mano porque aca es un `show` comun y no el imagebutton del HUD: centro
    # abajo, igual que dibuja el motor los sprites de NPC.
    show expression JNPB_ALTILLO_SPRITE as violet_altillo:
        xanchor 0.5
        yanchor 1.0
        xpos JNPB_ALTILLO_POS[0]
        ypos JNPB_ALTILLO_POS[1]

    violet "No te quedes ahí mirando y empieza a buscar"

    mc "No te estaba mirando"

    violet "... no dije que me estés mirando a mí, dije que dejes de mirar"

    mc "Bueno, ¿tienes idea por dónde puede estar?"

    violet "¿No te parece que si tendría idea no estaría hace una hora revisando cajas?"

    mc "Buen punto, habrá que revisar todo"


    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_altillo
    with dissolve

    # Encerrado en el altillo hasta encontrar la consola. Violet SI queda
    # interactuable (npcs_interactuables): el click en su sprite es medio
    # disparador de la quest — lo atiende jn_pocketboy_molestar.
    $ activar_restriccion(
        locaciones_permitidas=["casa_altillo"],
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento=_("No me puedo ir hasta encontrarla"),
        mensaje_accion_default=_("No me puedo ir hasta encontrarla"),
        npcs_interactuables=["violet"],
        celular_bloqueado=True,
        mensaje_celular=_("No me puedo ir hasta encontrarla"),
    )

    # Recien acá aparece la accion "Buscar" en el altillo.
    $ jnpb_fase = 2

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · MOLESTARLA — click en el sprite de Violet mientras buscan
################################################################################
## Entra por el jump del principio de `interaccion_violet`: en vez de abrir el
## menu, Violet contesta una linea y el jugador vuelve al loop. Es la excepcion
## a "clickear al NPC siempre abre el menu" — durante la busqueda no hay nada
## que elegir (talk, quests y evento estan todos bloqueados por la restriccion).
##
## Cada click tiene SU linea: la 1, la 2, la 3 y la 4 son distintas y van
## escalando. A la QUINTA vez se abre una escena. Despues el contador vuelve a
## cero, asi que el ciclo se puede repetir mientras la quest siga abierta.

label jn_pocketboy_molestar:

    $ jnpb_clicks_violet += 1

    if jnpb_clicks_violet >= 5:
        $ jnpb_clicks_violet = 0
        jump jn_pocketboy_charla

    $ ocultar_hud()
    window show

    # Una linea por click. El ultimo tramo va con `else` y no con `== 4` para
    # que un valor inesperado (un save viejo con el contador en otra cosa) caiga
    # igual en una linea valida en vez de saltearse el dialogo.
    if jnpb_clicks_violet == 1:
        violet "Acá estoy buscando yo, busca por otro lado"

    elif jnpb_clicks_violet == 2:
        violet "No hay espacio para los dos acá"

    elif jnpb_clicks_violet == 3:
        violet "Me tocaste el trasero..."

    else:
        violet "¿Lo estás haciendo a propósito, no?"

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 4 · LA CHARLA DE LA QUINTA VEZ — escena suelta, la quest sigue abierta
################################################################################

label jn_pocketboy_charla:

    $ ocultar_hud()
    window show

    # Escena de primer plano: tiene fondo propio, no el del altillo. Todo el
    # arte es full-frame 1920x1080 — fondo y capas — asi que los `show` van
    # pelados, sin `at`: las capas alinean solas.
    scene escena_primerplano_fondo with fade

    # =========================================================================
    # CONTENIDO — de tanto interrumpirla, terminan hablando de otra cosa
    # =========================================================================

    # Arranca de espaldas. No se le ve la cara, asi que la boca queda en b_none:
    # la unica boca del layered esta dibujada para la pose "mirando".
    show violet_qa15_primerplano c_violetespalda b_none
    violet "..."

    piensa "Creo que la hice enojar"

    # Se da vuelta y lo mira. Solo cambia el cuerpo; la boca sigue en b_none.
    show violet_qa15_primerplano c_violetmirando

    piensa "Sí, la hice enojar"

    # Ahora si se le ve la cara, asi que la boca acompaña lo que dice.
    show violet_qa15_primerplano b_hablando
    violet "¿Es tan divertido molestarme?"
    show violet_qa15_primerplano b_none

    mc "Un poco sí"

    show violet_qa15_primerplano b_hablando
    violet "Esa fue la última advertencia, la próxima te pateo"
    show violet_qa15_primerplano b_none

    mc "Prometo no molestarte más"

    show violet_qa15_primerplano b_hablando
    violet "Sigue buscando entonces"
    show violet_qa15_primerplano b_none

    show violet_qa15_primerplano c_violetespalda b_none

    piensa "Debería concentrarme en buscar la consola"
    piensa "Un último disfrute a esta vista"
    piensa "..."
    piensa "Listo"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide violet_qa15_primerplano

    # Vuelta al altillo. El fondo de la escena tiene que salir de pantalla antes
    # del loop; el sprite de Violet lo redibuja solo el HUD desde su rutina, asi
    # que no hay que reponerlo a mano.
    $ _jnpb_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _jnpb_bg with fade

    # La quest NO se completa acá: la consola sigue sin aparecer.
    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 5 · BUSCAR — cierre de la quest (accion de locacion del altillo)
################################################################################

label jn_pocketboy_cierre:

    # Levantar la restriccion primero: si la escena se cortara mas adelante, el
    # jugador quedaria encerrado en el altillo para siempre.
    $ jnpb_fase = 3
    $ desactivar_restriccion()

    $ ocultar_hud()
    window show

    # Arranca donde estaba el jugador: el altillo, con Violet en su idle — la
    # misma imagen y posicion que usa su rutina (constantes de
    # quests_amor_violet.rpy).
    $ _jnpb_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _jnpb_bg

    show expression JNPB_ALTILLO_SPRITE as violet_altillo:
        xanchor 0.5
        yanchor 1.0
        xpos JNPB_ALTILLO_POS[0]
        ypos JNPB_ALTILLO_POS[1]

    # =========================================================================
    # CONTENIDO — PARTE A · se ponen a buscar
    # =========================================================================

    piensa "Es hora de ponerse a buscar"

    # Elipsis temporal. Mismo recurso que la intro (intro_main.rpy): negro,
    # cartel centrado, pausa y se va. `pause` con numero NO espera al jugador,
    # corre solo — es lo que hace que se sienta un salto de tiempo.
    scene black with fade
    show text Text(renpy.translate_string("Luego de algunos minutos"),
                   size=50, color="#FFFFFF",
                   outlines=[(2, "#000000", 0, 0)]) at truecenter
    pause 2.0
    hide text with dissolve

    # =========================================================================
    # CONTENIDO — PARTE B · sentados, descansando de la busqueda
    # =========================================================================

    # Vuelve el altillo, ahora con Violet sentada. `violet_sentada` es
    # full-frame, asi que va sin `at`.
    scene expression _jnpb_bg
    show violet_sentada
    with fade

    mc "¿Ya está?"

    show violet_sentada b_hablando
    violet "Me rindo, estoy agotada"
    show violet_sentada b_none

    mc "Vamos un poco más"

    show violet_sentada b_hablando
    violet "No tenía tantas ganas de jugar a la Pocket Boy"
    show violet_sentada b_none

    mc "Creo que está por acá"
    mc "Pero es en la caja de abajo"

    with hpunch

    mc "No la puedo sacar"

    with hpunch

    show violet_sentada b_hablando
    violet "Ahí te ayudo"
    show violet_sentada b_none

    mc "Agarra la de arriba"

    scene black with fade

    # Movimiento brusco: hpunch sacude en horizontal y vpunch en vertical. Van
    # sobre el negro, asi que se siente el golpe sin mostrar todavia el porque.
    with hpunch
    with vpunch

    "¡Zas... claf, pum, plaf!"

    scene escena_caida_fondo with fade

    # ⚠️ ORDENAR — abajo esta llamado UNA VEZ cada atributo de los dos layered,
    # para que se puedan ver todos y armar la secuencia real. Los cuerpos ya
    # vienen pintados en el fondo: estas dos imagenes son solo las caras, y por
    # eso arrancan las dos en Null (o_none / b_none).
    #
    #   violet_qa15_caidos_mc      ojos: o_cerrados     boca: b_feliz, b_hablando
    #   violet_qa15_caidos_violet  ojos: o_enojada      boca: b_hablando, b_hablandochica

    show violet_qa15_caidos_violet b_hablando
    violet "¿Estás bien?"
    show violet_qa15_caidos_violet b_none

    show violet_qa15_caidos_mc b_hablando
    mc "Sí, solo que se me cayó algo pesado encima"
    show violet_qa15_caidos_mc b_none

    show violet_qa15_caidos_violet o_enojada b_hablando
    violet "No soy algo pesado"
    show violet_qa15_caidos_violet b_hablandochica
    violet "Ahora me voy a quedar así"
    show violet_qa15_caidos_violet b_none

    show violet_qa15_caidos_mc o_cerrados b_feliz
    piensa "Así se debe sentir estar en el cielo"

    show violet_qa15_caidos_violet b_hablando
    violet "¿Qué es esa cara de que lo estás disfrutando?"
    show violet_qa15_caidos_violet b_none

    show violet_qa15_caidos_mc b_hablando o_none
    mc "No voy a mentirte"
    show violet_qa15_caidos_mc b_none

    show violet_qa15_caidos_violet o_enojada b_hablando
    violet "Solo sirves para ser un pervertido"
    show violet_qa15_caidos_violet b_none

    show violet_qa15_caidos_mc b_hablando
    mc "No lo niego, pero encontré la caja correcta"
    show violet_qa15_caidos_mc b_none

    show violet_qa15_caidos_violet o_enojada b_hablando
    violet "Gracias, solo me va a faltar encontrar pilas"
    show violet_qa15_caidos_violet b_none

    show violet_qa15_caidos_mc b_hablando
    mc "Pero tú sola, yo ya me cansé de esto"
    show violet_qa15_caidos_mc b_none

    show violet_qa15_caidos_violet o_enojada b_hablando
    violet "¿No era que lo estabas disfrutando?"
    show violet_qa15_caidos_violet b_none

    show violet_qa15_caidos_mc b_hablando
    mc "Ya tuve mi recompensa, ahora es hora de partir"
    show violet_qa15_caidos_mc b_none

    show violet_qa15_caidos_violet o_enojada b_hablando
    violet "Eres un idiota"
    show violet_qa15_caidos_violet b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide violet_qa15_caidos_mc
    hide violet_qa15_caidos_violet
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_amor_03")

    # El MC sale de la habitacion y se le fue la noche buscando: vuelve al
    # pasillo y el horario avanza (noche → trasnoche).
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## Chat
################################################################################
## Vivia en characters/violet/chat/chat_violet.rpy; se trajo acá con el resto
## del arco. Lo dispararia el trigger de game_loop de mas arriba, que hoy esta
## apagado, asi que el grupo nunca se entrega.

init 5 python:

    # =========================================================================
    # CHAT DEL ARCO — Violet pide la Portatil Boy
    # =========================================================================
    # Lo dispara el trigger de game_loop de este archivo al llegar a 15 de
    # amor. La UNICA condicion de entrega es que no esten en la misma locacion:
    # si estan cara a cara, escribirse por chat no tendria sentido, asi que el
    # grupo queda EN ESPERA y sale solo cuando el jugador se aparta.
    #
    # Las dos primeras lineas de Violet van en una sola burbuja porque
    # mensaje_inicial es un unico mensaje (la API solo permite varias burbujas
    # seguidas del NPC via respuesta_npc, que va DESPUES de una respuesta del
    # jugador). Si se prefieren separadas hay que mover la segunda a un paso.

    chat_violet_jnpb = GrupoMensajes(
        id="violet_jnpb_chat",
        npc_id="violet",
        mensaje_inicial="Hola, estaba con ganas de jugar al Pocketmonster y mi vieja Portatil Boy no anda\n¿Todavia tienes la tuya para prestarmela?",
        trigger_id="violet_jnpb_chat",
        condicion_entrega=_jnpb_chat_separados,
        accion_al_completar=_jnpb_chat_completado,
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Debe haber quedado aqui en algun lado",
                        respuesta_npc="",
                        saltar_a_paso=1,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="No me la lleve cuando me fui",
                        respuesta_npc=["Debe estar en el altillo entonces",
                                       "Luego la busco"],
                        saltar_a_paso=2,
                    ),
                ]
            ),
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="OK",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", chat_violet_jnpb)


################################################################################
## Imagenes de las escenas
################################################################################
## Dos escenas del altillo, cada una con su fondo y sus capas de expresion.
## Assets en images/quest/violet/amor15/.
##
## TODO es full-frame 1920x1080 — fondos y capas — asi que las capas alinean
## solas con el fondo y NO llevan posicion: van con un `show` pelado, sin `at`.
## Los fondos quedan en JPG (no tienen alpha) y las capas en WebP (si lo tienen),
## que es la convencion de assets del proyecto.
##
## Los fondos se declaran a mano en vez de dejarlos al auto-nombrado de Ren'Py
## para que el nombre no dependa de donde este el archivo.

image escena_primerplano_fondo = "images/quest/violet/amor15/escena_primerplano_fondo.jpg"
image escena_caida_fondo = "images/quest/violet/amor15/escena_caida_fondo.jpg"


## PRIMER PLANO — Violet de espaldas o mirando, sobre escena_primerplano_fondo.
##
## ⚠️ La boca es la de "mirando": solo pega con c_violetmirando. Con
## c_violetespalda no se le ve la cara, asi que ahi la boca va en b_none.
layeredimage violet_qa15_primerplano:

    group cuerpo:
        attribute c_violetespalda default:
            "images/quest/violet/amor15/escena_primerplano_violetespalda.webp"
        attribute c_violetmirando:
            "images/quest/violet/amor15/escena_primerplano_violetmirando.webp"

    # Despues del cuerpo = encima del cuerpo.
    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/quest/violet/amor15/escena_primerplano_violetmirando_hablando.webp"


## CAIDA — los dos en el piso, sobre escena_caida_fondo.
##
## Los cuerpos ya vienen pintados EN EL FONDO: estos dos layeredimage son solo
## las expresiones, y por eso los dos grupos arrancan en Null(). Son dos
## imagenes separadas (una por personaje) para poder moverles la cara de a uno.
layeredimage violet_qa15_caidos_mc:

    group ojos:
        attribute o_none default:
            Null()
        attribute o_cerrados:
            "images/quest/violet/amor15/escena_caida_mc_ojos_cerrados.webp"

    group boca:
        attribute b_none default:
            Null()
        attribute b_feliz:
            "images/quest/violet/amor15/escena_caida_mc_boca_feliz.webp"
        attribute b_hablando:
            "images/quest/violet/amor15/escena_caida_mc_boca_hablando.webp"


layeredimage violet_qa15_caidos_violet:

    group ojos:
        attribute o_none default:
            Null()
        attribute o_enojada:
            "images/quest/violet/amor15/escena_caida_violet_ojos_enojada.webp"

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/quest/violet/amor15/escena_caida_violet_boca_hablando.webp"
        attribute b_hablandochica:
            "images/quest/violet/amor15/escena_caida_violet_boca_hablandochica.webp"


## SENTADA — Violet sentada en el altillo, sobre el fondo normal de la locacion
## (no tiene fondo propio, a diferencia de las dos escenas de arriba).
##
## El cuerpo va en `always` y no en un grupo: es una sola pose, siempre visible.
## El unico grupo es la boca, para que hable.
layeredimage violet_sentada:

    always:
        "images/quest/violet/amor15/violet_sentada.webp"

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/quest/violet/amor15/violet_sentada_hablando.webp"
