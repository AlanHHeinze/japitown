################################################################################
## Violet — Amor 35 · "Las amigas"
################################################################################
##     archivo   violet_amor_35.rpy
##     quest     violet_amor_07          (quests_amor_violet.rpy)
##     label     quest_violet_amor_07    (lo fija el motor: "quest_" + id)
##
## LA ESCENA DEL SOTANO YA ESTA ESCRITA (2026-09-28, dictada linea por linea).
## Lo que queda:
##
## 1. TRADUCCION AL INGLES de la escena: ninguna de sus lineas tiene bloque en
##    tl/english todavia. Se generan con el extractor del SDK.
##
## 2. EL TEXTO DEL CHAT (`violet_amor_35_aviso`, mas abajo): el mensaje inicial
##    y la respuesta del jugador siguen siendo de relleno.
##
## 3. EL PENSAMIENTO AL SALIR ("Van a estar ahi abajo toda la noche") y EL DEL
##    CIERRE de la mañana siguiente (`violet_amor_35_cierre`) no estan dictados:
##    son de relleno. El del cierre tiene que dejar el gancho para la quest de
##    40 — ella se quedo con algo sin decir.
##
## 4. NOMBRE Y DESCRIPCION de la quest ("Las amigas" / "Violet bajo al sotano
##    con sus amigas."), en quests_amor_violet.rpy: se ven en Pistas y son
##    provisorios.
##
## 5. LA ESCENA NO TIENE ELECCION, y TAMPOCO DEJA NINGUN FLAG. El esquema
##    preveia elegir como responder a Zowie (seguir / esquivar / cortar) para
##    que la quest de 40 midiera el reproche con eso; la eleccion quedo para
##    retrabajarla mas adelante y el flag se saco entero (2026-09-28) en vez de
##    dejarlo fijo: un flag que nadie elige es deuda invisible — al rediseñar la
##    eleccion se construye encima sin acordarse de que estaba.
##
##    LO QUE LA 40 TIENE PARA COBRAR NO ES UN FLAG, ES LA ESCENA: Zowie lo
##    invita delante de Violet ("Cuando quieras ver una película con alguien me
##    puedes invitar"), Leah se suma, y el MC les agradece. Violet estuvo ahi.
##    Si la eleccion vuelve, el lugar natural es la respuesta a "Bueno,
##    entonces te puedes quedar".
##
## LA NOCHE DE PELICULA. Violet baja al sotano con Zowie y Leah un viernes o un
## sabado a la noche y le escribe al MC para que la ayude con el proyector.
##
## LAS FASES (flag `va35_fase`):
##
##   0  esperando el viernes o el sabado a la noche  → trigger de game_loop
##                                                     (manda el chat)
##   1  avisado: ellas estan abajo                   → trigger de game_loop
##                                                     (entrar al sotano)
##   2  la escena paso; siguen abajo y el SOTANO     → trigger de dormir
##      QUEDA CERRADO hasta el dia siguiente           ("despues")
##   3  cerrada
##
## POR QUE LA QUEST NO SE COMPLETA AL TERMINAR LA ESCENA: completar_quest()
## RESTAURA LA RUTINA DEL NPC. Si se completara al salir del sotano, Violet
## volveria a su habitacion al instante y no podria "seguir con las amigas".
## Viva en fase 2, su rutina_quest la sostiene abajo la noche y la trasnoche.
##
## UN SOLO DISPARADOR: entrar al sotano. El chat es un AVISO, no una llave —
## por eso el trigger de la escena acepta las fases 0 y 1 por igual. Si el
## jugador baja sin haber leido el mensaje, la escena corre lo mismo: estan
## ahi. Dos disparadores dejarian uno inalcanzable (caso real: la 04_b).
##
## EL CHAT NO ES PRIORITARIO, a proposito. Un prioritario sin responder bloquea
## dormir y avanzar, y acá el jugador tiene OTRO camino para dejarlo obsoleto
## (bajar al sotano): quedaria un bloqueo vivo cuya salida ya no existe, que es
## la forma exacta de E10. Lo que frena el reloj es la reserva del MC, que se
## levanta sola al terminar la escena.


################################################################################
## Estado
################################################################################

# 0 esperando · 1 avisado · 2 la escena paso (sotano cerrado) · 3 cerrada
default va35_fase = 0

init python:

    # ── Estado de la quest ───────────────────────────────────────────────────

    def _va35_lista():
        """
        Viva y en la etapa del disparo. NO es `quest_lista_para_boton`, y es a
        proposito — las dos veces que se aparta del predicado estandar tienen
        su motivo:

        1. Ese predicado corre la CAPA 2 ENTERA, y la capa 2 exige el mundo tal
           como las demandas lo piden... incluido `Rec("locacion",
           en="casa_sotano")`, o sea el MC ya abajo. El aviso por chat llega
           antes de bajar: con el predicado estandar no se mandaria nunca.
        2. El trigger de la ESCENA es la unica salida de la noche que la quest
           se reservo. Si dependiera de que Violet siga disponible o de que el
           mundo cumpla, cualquier cosa ajena que la apague dejaria al jugador
           con el reloj congelado y sin escena: el soft lock de E10.

        Lo estructural igual se chequea: el motor pasa por
        `planificador_trigger_permitido` antes de evaluar un trigger con
        `quest_id=`, y ahi entran los conflictos (reservas y de_corrido ajenos).
        Lo del mundo lo garantiza la rutina_quest, que pone a Violet abajo esas
        cuatro franjas.
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_07")
        return (_q is not None and _q.activa and not _q.completada
                and _q.etapa_actual == ETAPA_BOTON_LISTO)

    def _va35_viva():
        """
        Activa y sin completar, sin pedir ETAPA_BOTON_LISTO.

        La usan el bloqueo del sotano y el cierre al dormir, que corren DESPUES
        de que la escena activo la quest (ahi ya es narrativa_activa).
        """
        _q = store.sistema_quests.obtener_quest("violet_amor_07")
        return _q is not None and _q.activa and not _q.completada

    def _va35_es_la_noche():
        """
        Viernes o sabado, de noche o de madrugada.

        La trasnoche entra a proposito: si el jugador se las arregla para pasar
        de la noche sin bajar, ellas siguen abajo y la escena tiene que poder
        correr igual. Un disparador que solo existe una hora es una forma de
        perder la quest sin enterarse.
        """
        return (getattr(store, "dia_semana_actual", 0) in (4, 5)
                and getattr(store, "horario_actual", 0) in (2, 3))

    def _va35_locacion_mc():
        _loc = store.sistema_locaciones.locacion_actual
        return _loc.id if _loc else None

    # ── Textos de ETAPA_BOTON_LISTO (los usa quests_amor_violet.rpy) ─────────
    # Funciones de MODULO: quedan guardadas dentro del ConfigEtapa de la quest.

    def _pista_va35_listo():
        if getattr(store, "va35_fase", 0) >= 2:
            return renpy.translate_string("Violet sigue en el sótano con sus amigas.")
        return renpy.translate_string("Violet está en el sótano con sus amigas.")

    def _quehacer_va35_listo():
        if getattr(store, "va35_fase", 0) >= 2:
            return renpy.translate_string("Dejarlas tranquilas hasta mañana")
        return renpy.translate_string("Bajar al sótano el viernes o el sábado por la noche")

    # ── Disparadores ─────────────────────────────────────────────────────────

    def _gl_trigger_va35_aviso():
        """
        Trigger de game_loop: llegada la noche del viernes o del sabado, Violet
        le escribe. Solo hace efectos python — el mensaje no es una escena.

        Ademas RESERVA al MC. La reserva normal la toma activar_quest, o sea al
        bajar al sotano, y para entonces ya no sirve de nada: lo que hay que
        proteger es el rato que va del mensaje a la escena. Con el MC reservado
        ninguna otra quest se activa en el medio y el reloj queda congelado, asi
        que la unica salida es bajar — que es justo lo que la quest pide.
        """
        if not _va35_lista() or store.va35_fase != 0:
            return None
        if getattr(store, "dia_semana_actual", 0) not in (4, 5):
            return None
        if getattr(store, "horario_actual", 0) != 2:
            return None
        # El chequeo de dia y horario va acá y no solo en las demandas:
        # planificador_trigger_permitido gatea por conflictos y a proposito NO
        # mira la parte momentanea.
        if not npc_disponible("violet") or npc_esta_oculto("violet"):
            return None
        _res = planificador_mc_reservado_por()
        if _res is not None and _res != "violet_amor_07":
            return None
        if _va35_locacion_mc() == "casa_sotano":
            # Ya esta abajo: las ve. Avisarle por chat de algo que tiene
            # enfrente sobra, y el trigger de la escena salta en esta misma
            # vuelta del game_loop.
            return None

        store.sistema_mensajes.disparar_por_trigger(
            "quest", "violet_amor_35_aviso", "violet")
        planificador_reservar(store.sistema_quests.obtener_quest("violet_amor_07"))
        store.va35_fase = 1
        return None

    def _gl_trigger_va35_sotano():
        """
        Trigger de game_loop: el MC baja al sotano la noche de la juntada.

        Lo mas laxo posible a proposito: fase, momento y lugar, nada mas. No
        pregunta si Violet esta disponible ni si esta oculta — si otro contenido
        la apagara despues de que la quest tomo la noche, este disparador seria
        el unico camino de salida y no puede depender de eso (regla A1).
        """
        if not _va35_lista():
            return None
        if store.va35_fase > 1:
            return None
        if not _va35_es_la_noche():
            return None
        if _va35_locacion_mc() != "casa_sotano":
            return None
        return "quest_violet_amor_07"

    def _va35_trigger_dormir():
        """
        Trigger de dormir, fase "despues": a la mañana siguiente.

        - Fase 2 → la escena paso: se cierra la quest (y con ella el bloqueo
          del sotano y la rutina que tenia a Violet abajo).
        - Fase 1 → la noche paso sin que bajara: vuelve a esperar. No se pierde
          nada, la quest reintenta el proximo viernes; lo que no vuelve es el
          mensaje, y por eso la pista del panel dice donde y cuando.
        """
        if not _va35_viva():
            return None
        if getattr(store, "va35_fase", 0) == 2:
            return "violet_amor_35_cierre"
        if getattr(store, "va35_fase", 0) == 1:
            store.va35_fase = 0
        return None

    # ── El sotano cerrado (fase 2) ───────────────────────────────────────────

    def _va35_sotano_cerrado():
        """
        Mientras la escena ya paso y la quest sigue viva, abajo no se baja.

        La condicion se apaga al completar la quest, que es lo que hace el
        trigger de dormir a la mañana siguiente: la salida es dormir, y dormir
        no depende de nada que este bloqueado (la reserva del MC se libero al
        terminar la escena).
        """
        return _va35_viva() and getattr(store, "va35_fase", 0) == 2


init 5 python:

    registrar_trigger_game_loop("violet_amor_35_aviso", _gl_trigger_va35_aviso,
                                quest_id="violet_amor_07")

    # Prioridad mayor que el aviso: si el jugador ya esta abajo cuando la quest
    # toma la noche, la escena gana y el chat no llega a mandarse.
    registrar_trigger_game_loop("violet_amor_35_sotano", _gl_trigger_va35_sotano,
                                prioridad=10, quest_id="violet_amor_07")

    registrar_trigger_dormir("violet_amor_35_cierre", "despues",
                             _va35_trigger_dormir, quest_id="violet_amor_07")

    registrar_bloqueo_locacion("casa_sotano", _va35_sotano_cerrado,
                               "Violet sigue con las amigas, mejor no molestarlas")


init 6 python:

    # ── El aviso ─────────────────────────────────────────────────────────────
    # Un paso y una sola respuesta: es un llamado, no una conversacion. Sin
    # `prioritario` (ver la cabecera) y sin `quest_id`, porque el punto de
    # activacion de esta quest es bajar al sotano, no abrir el chat.

    grupo_va35_aviso = GrupoMensajes(
        id="violet_amor_35_aviso",
        npc_id="violet",
        mensaje_inicial="¿Estás en casa? Baja al sótano, no podemos hacer andar el proyector",
        trigger_id="violet_amor_35_aviso",
        pasos=[
            PasoConversacion(
                opciones_jugador=[
                    OpcionRespuesta(
                        texto="Bajo en un rato",
                        respuesta_npc="",
                        saltar_a_paso=-1,
                    ),
                ]
            ),
        ],
    )
    sistema_mensajes.registrar_grupo("violet", grupo_va35_aviso)


################################################################################
## LA ESCENA — el sotano, las tres y el proyector
################################################################################
## El jugador ya esta en el sotano (lo exige el trigger), asi que el fondo sale
## de la locacion actual como en la quest de 30.
##
## POSICIONES: Violet la mas a la izquierda de las tres, Zowie en el medio y
## Leah contra la derecha; el MC entra por la izquierda. La profundidad la da el
## orden de los `show`, pero acá no se superponen, asi que el orden es el de
## lectura.
##
## LA PANTALLA DEL PROYECTOR es una capa full-frame de 1920x1080 con alpha: solo
## pinta la zona de la pantalla. Queda DEBAJO de las chicas y ENCIMA del fondo
## sin hacer nada — los sprites de personaje viven en la capa `personajes`
## (tinte_horario.rpy) y esta imagen, que no lleva prefijo de personaje, se queda
## en `master` junto al fondo.
##
## ⚠️ NADA DE `zorder -1`: en master el fondo lo pone `scene` con zorder 0, asi
## que un zorder negativo la mandaria DEBAJO del fondo, que es opaco. Se veria
## negro. Alcanza con mostrarla despues del `scene`.
##
## ⚠️ ZOWIE NO TIENE LA POSE `c_rbase_idea` (Leah si): son cuatro cuerpos, no
## cinco. Esta escena no la necesita.

image amor35_pantalla = "images/quest/violet/amor35/pantalla_anime.webp"

label quest_violet_amor_07:

    $ ocultar_hud()
    window show

    $ _va35_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va35_bg

    ## ── HACIA DONDE MIRA CADA UNA ───────────────────────────────────────────
    ## De izquierda a derecha: MC, Violet, Zowie, Leah. Las tres miran por
    ## defecto a la IZQUIERDA (hacia el MC). Para mirar a alguien que tiene a
    ## su derecha se usa la version `_flip` de su lugar (transforms_common).
    ## Violet, la primera vez que se gira, se APARTA a la izquierda
    ## (grupo3_izq_apartarse) y de ahi en mas gira en ese lugar (_aparte).
    ##   Violet  se gira para mirar a Zowie o a Leah.
    ##   Zowie   se gira solo para mirar a Leah.
    ##   Leah    nunca se gira: todos le quedan a la izquierda.
    ## La regla: se gira el que le habla a alguien en particular, y el que
    ## recibe esa frase mira al que se la dice. Tambien cuando alguien toma la
    ## posta de la conversacion. Los comentarios al pasar (los de Leah, casi
    ## todos) NO hacen girar a nadie: tantos giros molestan.

    # Las tres ya estan abajo, en su sprite base.
    show violet_parada c_rbase_base ca_base o_base b_none at grupo3_izq
    show zowie_parada c_rbase_base b_none at grupo3_centro
    show leah_parada c_rbase_base b_none at grupo3_der
    with sprite_normal

    # El MC llega y saluda.
    show mc_parado_base c_rbase_base o_base b_none at mc_entrar_izquierda
    pause 0.8
    show mc_parado_base at mc_izquierda

    show mc_parado_base b_hablando
    mc "Hola"
    show mc_parado_base b_none

    # Las dos le devuelven el saludo con el cuerpo de saludar y vuelven a base.
    show zowie_parada c_rbase_saludando b_hablando with sprite_normal
    zowie "¡Hola!"
    show zowie_parada c_rbase_base b_none with sprite_normal

    show leah_parada c_rbase_saludando b_hablando with sprite_normal
    leah "Hola"
    show leah_parada c_rbase_base b_none with sprite_normal

    show mc_parado_base c_rbase_pensando b_hablando with sprite_normal
    mc "¿Qué pasó?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Queríamos ver una película pero el proyector no anda, reproduce todo pero no da imagen"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Te fijaste si estaba conectado?"
    show mc_parado_base b_none

    show zowie_parada b_hablando c_rbase_pensando with sprite_normal
    zowie "Sí, fue lo primero que hicimos, pero no era eso"
    show zowie_parada b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "Hicimos todo lo que se nos ocurrió y nada, por eso te escribí"
    show violet_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base c_rbase_avergonzado b_hablando with sprite_normal
    mc "¿Lo enchufaron y desenchufaron?"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show leah_parada b_hablando c_rbase_idea with sprite_normal
    leah "Yo les dije, pero no me escucharon"
    show leah_parada b_none c_rbase_base with sprite_normal

    show mc_parado_base b_abiertachica
    mc "Ahora me fijo si eso lo arregla"
    show mc_parado_base b_none

    # Se da vuelta y sale por la izquierda (el transform lo endereza primero).
    show mc_parado_base at mc_salir_izquierda
    pause 0.8
    hide mc_parado_base

    # Lo que dicen de él apenas se va. Es LA razón de ser de la escena: lo que
    # se elija en la quest de 40 se cobra sobre este momento.
    #
    # Zowie le habla a Violet (la tiene a la izquierda: no se gira) y Violet,
    # que es a quien le habla, la mira. Antes de girarse se APARTA unos pasos a
    # la izquierda para no quedar encimada sobre Zowie, y se queda en ese lugar
    # hasta el final de la escena: los giros siguientes son en el lugar.
    show violet_parada at grupo3_izq_apartarse
    pause 0.6
    show zowie_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    zowie "Lo tenías escondido jajaja"
    show zowie_parada b_none

    show violet_parada b_hablando c_rbase_pensando with sprite_normal
    violet "¿Qué cosa?"
    show violet_parada b_none c_rbase_base with sprite_normal

    show zowie_parada b_hablando
    zowie "Que vivías con un chico lindo"
    show zowie_parada b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "No es un chico lindo, es un chico normal"
    show violet_parada b_none

    show leah_parada b_hablando c_rbase_pensando with sprite_normal
    leah "A mí me parece lindo también"
    show leah_parada b_none c_rbase_base with sprite_normal

    show zowie_parada b_hablando
    zowie "Estás viviendo tu propio anime donde el chico de tu infancia vuelve y tienen que vivir juntos, qué envidia"
    show zowie_parada b_none

    show violet_parada b_hablando
    violet "No es así, no es un anime, es la vida real y no pasa nada con él"
    show violet_parada b_none

    show zowie_parada b_hablando c_rbase_pensando with sprite_normal
    zowie "¿Entonces está disponible?"
    show zowie_parada b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando o_arribanm
    violet "Sí, está disponible..."
    show violet_parada b_none o_base

    show leah_parada b_hablando
    leah "Es bueno saberlo"
    show leah_parada b_none

    # El proyector arranca: la pantalla entra por debajo de las tres.
    show amor35_pantalla with dissolve

    # El MC les habla desde afuera, por la izquierda: Violet deja de mirar a
    # Zowie y mira hacia ahi.
    show violet_parada at grupo3_izq_aparte
    mc "¿Arrancó?"

    show violet_parada b_hablando
    violet "Sí, ahí funciona"
    show violet_parada b_none

    # Vuelve por donde se fue.
    show mc_parado_base c_rbase_base o_base b_none at mc_entrar_izquierda
    pause 0.8
    show mc_parado_base at mc_izquierda

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Nada más efectivo que una buena reiniciada"
    show mc_parado_base b_abiertachica c_rbase_base with sprite_normal
    mc "¿Qué estaban por mirar?"
    show mc_parado_base b_none

    show zowie_parada b_hablando
    zowie "Es una película de anime, se llama Nuestro Nombre"
    show zowie_parada b_none

    show mc_parado_base b_hablando
    mc "Ahhh escuché hablar muy bien de esa película"
    show mc_parado_base b_none

    show zowie_parada b_hablando c_rbase_pensando with sprite_normal
    zowie "¿Te gusta el anime?"
    show zowie_parada b_none

    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "Sí, miro bastante"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    show zowie_parada b_hablando
    zowie "¿Quieres ver la película con nosotras?"
    show zowie_parada b_none c_rbase_brazoscruzados with sprite_normal

    # Violet le contesta a Zowie por él: se gira a mirarla.
    show violet_parada at grupo3_izq_aparte_flip
    show violet_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    violet "No, no quiere, este no es su tipo de película"
    show violet_parada b_none

    # El MC la contradice: Violet lo mira a él.
    show violet_parada at grupo3_izq_aparte
    show mc_parado_base b_hablando
    mc "En realidad sí jajajaja"
    show mc_parado_base b_abiertachica c_rbase_avergonzado with sprite_normal
    mc "Un poco culpable pero me gustan esas cosas"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    # ── LA DISCUSION ────────────────────────────────────────────────────────
    # Acá esta el enganche con la quest de 40: Zowie lo invita de frente, Leah
    # se suma, y Violet se pone territorial sin poder decir por que. Es el
    # material que la 40 le cobra.
    #
    # La discusion es entre Violet y Zowie: Violet queda girada hacia ella
    # hasta que el MC corta la pelea.

    show violet_parada at grupo3_izq_aparte_flip
    show violet_parada b_hablando
    violet "No se puede quedar, es una noche de amigas"
    show violet_parada b_none

    show leah_parada b_hablando c_rbase_idea with sprite_normal
    leah "A mí no me molesta"
    show leah_parada b_none c_rbase_brazoscruzados with sprite_normal

    show zowie_parada b_hablando
    zowie "Listo, entonces te puedes quedar"
    show zowie_parada b_none

    show mc_parado_base b_hablando
    mc "Gracias por la invitación"
    show mc_parado_base b_none

    show violet_parada b_hablando c_rbase_idea with sprite_normal
    violet "A mí sí me molesta que se quede"
    show violet_parada b_none c_rbase_idea with sprite_normal

    show zowie_parada b_hablando c_rbase_pensando with sprite_normal
    zowie "¿Te molesta?"
    show zowie_parada b_none c_rbase_base with sprite_normal

    show violet_parada b_hablando
    violet "Sí, arreglamos ver la película nosotras tres y no había otra persona en los planes"
    show violet_parada b_none

    show zowie_parada b_hablando c_rbase_brazoscruzados with sprite_normal
    zowie "Porque no sabíamos la existencia de otra persona jajaja"
    show zowie_parada b_none

    show violet_parada b_hablando c_rbase_fuckyou with sprite_normal
    violet "No es gracioso"
    show violet_parada b_none c_rbase_brazoscruzados with sprite_normal

    show zowie_parada b_hablando
    zowie "No seas mala, nos ayudó con el proyector y dijo que la quería ver"
    show zowie_parada b_none

    show violet_parada b_hablando
    violet "Soy mala, cuando quiera ver una película con amigos que invite a los suyos"
    show violet_parada b_none

    # El MC corta la pelea: Violet lo mira.
    show violet_parada at grupo3_izq_aparte
    show mc_parado_base b_hablando c_rbase_avergonzado with sprite_normal
    mc "No se peleen, Violet tiene razón, era su plan y no tengo que interrumpirlo"
    show mc_parado_base b_abiertachica
    mc "Veré la película en otro momento"
    show mc_parado_base b_hablando
    mc "Gracias igual por invitarme"
    show mc_parado_base b_none c_rbase_base with sprite_normal

    # LA LINEA QUE LA 40 COBRA: Zowie lo invita a el, delante de ella.
    show zowie_parada b_hablando c_rbase_saludando with sprite_normal
    zowie "Cuando quieras ver una película con alguien me puedes invitar"
    show zowie_parada b_none c_rbase_base with sprite_normal

    show leah_parada b_hablando
    leah "A mí también"
    show leah_parada b_none

    show mc_parado_base b_hablando
    mc "Jajaja gracias, son muy buenas, me alegra haberlas conocido"
    show mc_parado_base b_abiertachica
    mc "Nos vemos, si tienen algún otro problema me avisan"
    show mc_parado_base b_none

    show leah_parada b_hablando c_rbase_saludando with sprite_normal
    leah "Adiós"
    show leah_parada b_none c_rbase_base with sprite_normal

    show zowie_parada b_hablando c_rbase_saludando with sprite_normal
    zowie "Nos vemos en otro momento"
    show zowie_parada b_none c_rbase_base with sprite_normal

    # El MC se va.
    show mc_parado_base at mc_salir_izquierda
    pause 0.8
    hide mc_parado_base

    jump violet_amor_35_salida


label violet_amor_35_salida:

    hide violet_parada
    hide zowie_parada
    hide leah_parada
    hide amor35_pantalla
    with dissolve

    # La escena paso: abajo siguen ellas y el sotano queda cerrado hasta mañana.
    $ va35_fase = 2

    # LA RESERVA SE LEVANTA ACA. Ya cumplio lo suyo —que nadie se metiera entre
    # el mensaje y la escena— y si quedara puesta congelaria el reloj el resto
    # de la noche... justo cuando la unica salida de la quest es dormir. Ese es
    # el deadlock de E10/E11 y se evita soltando lo que ya no hace falta.
    $ planificador_liberar("violet_amor_07")

    $ sistema_locaciones.mover_a_locacion("casa_living", escena=True)

    $ _va35_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _va35_bg with fade

    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal
    piensa "Van a estar ahí abajo toda la noche."
    hide mc_parado_base with dissolve

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## EL CIERRE — a la mañana siguiente
################################################################################
## Trigger de dormir "despues": la quest se completa acá y no al salir del
## sotano, para que la rutina que tiene a Violet abajo sobreviva la noche.
## Al completar, el motor restaura su rutina solo.

label violet_amor_35_cierre:

    $ ocultar_hud()
    window show

    piensa "Anoche se quedaron hasta cualquier hora."

    $ va35_fase = 3
    $ completar_quest_actual("violet", quest_id="violet_amor_07")

    window hide
    $ mostrar_hud()
    jump game_loop
