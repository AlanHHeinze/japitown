################################################################################
## Violet — Deseo 25 · "En su habitacion"
################################################################################
##     archivo   violet_deseo_25.rpy
##     quest     violet_deseo_05          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_05    (lo fija el motor: "quest_" + id)
##
## TRES TRAMOS, encadenados por `vd25_fase`:
##
##   fase 0 → el jugador usa "Ver TV" en el sotano. Violet quedo en bajar a ver
##            un capitulo y no aparecio: el MC se queda solo y decide subir a
##            buscarla.
##   fase 1 → juego libre acotado: no puede adelantar el tiempo ni salir de la
##            casa. Lo unico que destraba es ir hasta la puerta de Violet.
##   fase 2 → la escena en su habitacion, cierre de la quest, pasillo y +1 hora.
##
## DISPARADOR UNICO: la accion "Ver TV" del sotano, interceptada con un
## ListenerAccion. No hay boton en el menu de Violet ni opcion de puerta suelta
## — el unico camino es el sotano.
##
## POR QUE UN LISTENER Y NO UNA ACCION PROPIA: la accion del sotano ya existe
## (`vd15_ver_tv_sotano`, la creo la quest de deseo 15 y despues quedo como la
## ventaja "Ver Anime" del hito de deseo 20). Registrar una segunda accion en la
## misma locacion pondria dos botones "Ver TV" al lado. El listener se cuelga de
## la que ya esta y la intercepta mientras la quest esta lista.
##
## Y el listener corre ANTES de los bloqueos y del "ya la usaste hoy"
## (accion_locacion_ejecutar, punto 0), asi que la quest arranca aunque el
## jugador ya haya visto anime esa noche. Es justo lo que se quiere de un
## disparador.
##
## LA PUERTA VA CON OVERRIDE, no con una opcion mas del menu: la escena tiene
## que pasar SI O SI y sin que el jugador pueda golpear ni elegir otra cosa. El
## override se evalua primero que todo en interaccion_puerta_npc, asi que
## tambien le gana al ingreso directo que da la ventaja
## "puerta_dejar_pasar_noche" del hito de deseo 20 — sin el, con deseo alto el
## MC entraria de una a la habitacion y se saltearia la escena de la puerta.
##
## LA RUTINA DE LA NOCHE ES INCONDICIONAL. `rutina_quest` es un dict estatico
## del Quest y se aplica al llegar a ETAPA_RUTINA; no hay forma declarativa de
## prenderla desde un label. En la practica casi no se nota: de lunes a sabado
## Violet YA pasa la noche en su habitacion por su rutina base, asi que el unico
## dia que cambia algo es el domingo. Y hace falta que este ahi: la rutina de
## quest le gana a la rutina especial, o sea que no puede pasar que el MC suba a
## buscarla y ella se haya ido o este en la ducha.


################################################################################
## Estado
################################################################################

# 0 sin empezar · 1 buscandola por la casa · 2 terminada.
# Se guarda: entre la fase 1 y la 2 el jugador anda suelto y puede guardar.
default vd25_fase = 0


init python:

    def _vd25_listener_sotano():
        """
        Condicion del ListenerAccion: ¿la accion del sotano arranca la quest?

        Las condiciones van de la mas barata a la mas cara. El horario 2 no es
        capricho: es cuando la `rutina_quest` la tiene en su habitacion, o sea
        lo unico que garantiza que el MC la encuentre al subir.
        """
        if getattr(store, 'vd25_fase', 0) != 0:
            return False

        if not quest_lista_para_boton("violet_deseo_05"):
            return False

        if store.horario_actual != 2:          # Noche
            return False

        # En la casa. tracker_locacion_npc devuelve None si esta afuera o si
        # una restriccion la escondio, asi que cubre las dos cosas de una.
        if tracker_locacion_npc("violet") is None:
            return False

        # Y que no la este tapando otro contenido.
        return not npc_esta_oculto("violet") and npc_interactuable("violet")

    def _vd25_override_puerta():
        """
        Condicion del override de puerta: solo mientras la esta buscando.

        Sin el chequeo de fase el override se comeria la puerta de Violet para
        siempre; con el, vale unicamente entre el sotano y la escena.
        """
        return getattr(store, 'vd25_fase', 0) == 1


init 5 python:

    registrar_override_puerta("violet", _vd25_override_puerta,
                              "violet_deseo_25_puerta")


################################################################################
## 1 · EL PLANTON — la dispara "Ver TV" en el sotano
################################################################################
## Entra por `call expression` desde el executor de acciones, pero es CONTENIDO:
## cierra devolviendo al juego libre, asi que termina en jump game_loop (el
## drenaje del loop se encarga del frame).

label violet_deseo_25_sotano:

    $ ocultar_hud()
    window show

    # El sotano de noche: el listener solo salta desde esa accion y a esa hora,
    # asi que la locacion actual ya es la correcta.
    $ _vd25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # (Mc cuerpo pensando ojos arriba sin mirar)
    show mc_parado_base c_rbase_pensando o_arribanm with sprite_fast
    piensa "Violet me dijo que iba a bajar a ver un capitulo conmigo y no aparecio"
    piensa "Voy a subir a buscarla"

    hide mc_parado_base with dissolve

    # Juego libre pero acotado: no puede adelantar el tiempo ni irse de la casa.
    # La lista de locaciones se arma en runtime en vez de a mano para que una
    # locacion nueva no quede afuera por olvido; la unica que se saca es
    # casa_frente, que es la salida ("Salida" del living).
    $ vd25_fase = 1
    $ _vd25_dentro = [_l for _l in sistema_locaciones.locaciones if _l != "casa_frente"]
    $ activar_restriccion(
        locaciones_permitidas=_vd25_dentro,
        acciones_bloqueadas=["avanzar_tiempo", "dormir"],
        mensaje_movimiento="Primero voy a ver que paso con Violet",
        mensaje_accion_default="Primero voy a ver que paso con Violet",
    )

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA PUERTA — override, mientras dura la fase 1
################################################################################
## Se entra por `jump expression` desde interaccion_puerta_npc, o sea SIN frame
## propio: el flujo de puerta ya no continua despues. Sigue de largo hasta la
## escena y cierra ahi.

label violet_deseo_25_puerta:

    $ ocultar_hud()
    window show

    # El pasillo: la puerta se toca desde afuera. locacion_actual sirve porque
    # al override solo se llega desde el pasillo.
    $ _vd25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at center with sprite_normal

    # Ella contesta del otro lado de la puerta: SIN sprite, a proposito. Todavia
    # no se la ve.
    violet "Espera que me estoy poniendo el short"

    piensa "..."
    piensa "¿Cuanto mas le falta?"
    
    show mc_parado_base b_hablando
    mc "¿Ya esta?"
    show mc_parado_base b_none

    violet "Pasa"

    hide mc_parado_base with dissolve

    # Entra. El movimiento es de verdad (no solo un cambio de fondo): el cierre
    # lo devuelve al pasillo, asi que el motor tiene que saber que estuvo dentro.
    $ sistema_locaciones.mover_a_locacion("casa_hviolet")

    jump quest_violet_deseo_05


################################################################################
## 3 · LA ESCENA — cierre de la quest
################################################################################

label quest_violet_deseo_05:

    $ ocultar_hud()
    window show

    $ _vd25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd25_bg with fade

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la conversacion en su habitacion
    # =========================================================================

    show violet_parada b_hablando
    violet "¿Que pasa?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Me habias dicho que venias a ver el capitulo conmigo y te estuve esperando bastante"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Perdon me colgue haciendo unas cosas, pero ya iba a bajar"
    show violet_parada b_hablandochica
    violet "No hacia falta que me vengas a buscar o ¿Estabas muy apurado por verme?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Me descubriste, ya extrañaba ese lindo trasero y no podia esperar mas para verlo"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Aunque lo estes diciendo de forma sarcastica, se que en el fondo es asi"
    show violet_parada b_hablandochica
    violet "Asi que no hace falta que lo ocultes, puedes ser sincero jajaja"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Te recomiendo que no me provoques"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "¿Que me va a pasar por hacerlo?"
    show violet_parada b_none

    # Introducir secuencia del beso

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ vd25_fase = 2
    $ desactivar_restriccion()
    $ completar_quest_actual("violet", quest_id="violet_deseo_05")

    # Sale de la habitacion y se le fue la noche: pasillo y horario +1.
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop
