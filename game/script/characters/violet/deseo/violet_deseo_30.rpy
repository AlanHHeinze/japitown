################################################################################
## Violet — Deseo 30 · "Sinceridad" + "Distancia"
################################################################################
##     archivo   violet_deseo_30.rpy
##     quests    violet_deseo_06 "Sinceridad"  — la noche de la charla
##               violet_deseo_07 "Distancia"   — los tres dias y la visita
##               (las dos en quests_deseo_violet.rpy; la 07 nace al completar
##               la 06 y pide el mismo umbral, 30)
##     labels    quest_violet_deseo_06     (lo fija el motor: "quest_" + id)
##               violet_deseo_30_visita    (cierre de la 07)
##
## POR QUE SON DOS QUESTS (planificador, punto 2): la noche de la charla es
## DE CORRIDO —congela el reloj, acota el recorrido, necesita a Violet en su
## pieza— y los tres dias de ignorarla no consumen nada: son juego libre con
## un contador. Una sola quest obligaba a declarar la conflictiva por tres
## dias y a que nada naciera mientras tanto. Partida, la 06 pide y protege
## solo esa noche, y la 07 es tolerante.
##
## DE QUE VA LA HISTORIA (las dos quests seguidas):
##
##   1. El MC intenta intimar un poco mas con Violet y ella se hace la dificil.
##      (Es la charla en su pieza — quest_violet_deseo_06.)
##
##   2. El MC se enoja y decide ignorarla. De ahi sale la etapa 2: tres dias
##      completos sin tener ningun contacto con ella.
##
##   3. Cumplidos los tres dias, VIOLET va a buscarlo a el, de noche, para
##      preguntarle que le pasa. (violet_deseo_30_visita.)
##
##   4. En esa charla el MC le dice lo que piensa. Violet contesta que piensa
##      igual, pero que quiere ir a otro ritmo: no quiere matar el juego entre
##      los dos, que es justamente lo divertido.
##
##   5. Y le confiesa que le gusta como la mira con lujuria, y que eso la
##      calienta.
##
## ESE ULTIMO PASO ES EL QUE ABRE LA VENTAJA `provocacion` del hito "Sinceridad"
## (hitos_violet.rpy): de ahi en mas es ELLA la que arma situaciones para
## calentarlo — dejar la puerta del baño entornada y demas. La quest tiene que
## dejar eso plantado en el dialogo, o la ventaja aparece sin explicacion.
##
## DOS QUESTS, y `vd30_fase` marca en cual se esta:
##
##   QUEST 06 "Sinceridad" — la charla en su pieza
##     0  esperando       → trigger de game_loop: de noche, el MC en SU pieza y
##                          Violet libre en la suya
##     1  yendo a verla   → recorrido acotado; entrar a casa_hviolet dispara la
##                          escena. Al salir queda en el pasillo, en modo libre,
##                          la 06 se completa y NACE la 07
##
##   QUEST 07 "Distancia" — ignorarla tres dias
##     2  contando        → hay que dormir 3 noches SIN hacer nada con ella
##     3  terminada
##
## MIGRACION de partidas de 0.1.9a que estaban contando (fase >= 2 con la 06
## todavia activa): _gl_trigger_vd30_migracion completa la 06 en silencio y
## deja nacer la 07 con el contador como estaba.
##
## LA QUEST 07 SE MIDE AL REVES QUE TODO EL RESTO DEL JUEGO: no se pide hacer
## algo, se pide NO hacerlo. El contador lo lleva `vd30_dias_ignorada` y lo mueve
## un trigger de dormir que lee `hubo_contacto_npc("violet")`.
##
## QUE CUENTA COMO "hacer algo con ella" no lo decide esta quest: lo marcan los
## embudos del motor (cambio de stat, cierre de quest, cierre de chat, fin del
## talk). Ver core/npcs/npc_contacto.rpy — ahi esta la lista y el porque. Asi
## una interaccion NUEVA queda cubierta sola, sin tocar este archivo.
##
## EL CIERRE TIENE DOS PUERTAS Y UN SOLO LABEL:
##   - dormir la 3ra noche  → se despierta esa misma noche y ella ya esta ahi
##   - estar en su pieza de noche con el contador ya en 3 → ella entra
## La segunda es la red de la primera: cubre al que llego a 3 y no vio la escena
## (cargo una partida vieja, o el contador subio por otro camino).


################################################################################
## Estado
################################################################################

# 0 espera · 1 yendo a su pieza · 2 contando dias ignorandola · 3 fin
default vd30_fase = 0

# Noches seguidas durmiendo sin haber hecho nada con Violet. Llega a 3 y ella
# aparece. Cualquier contacto lo devuelve a 0.
default vd30_dias_ignorada = 0


init python:

    # Cuantas noches seguidas hay que ignorarla.
    VD30_DIAS_PARA_VISITA = 3

    # ── Los textos de la guia, que cambian con la fase ───────────────────────
    # La 06 se queda en ETAPA_BOTON_LISTO de punta a punta, pero por el medio
    # lo que hay que hacer cambia (esperar la noche / ir a su pieza). La 07
    # muestra el contador: es la unica quest del juego que pide NO hacer algo,
    # y ver el numero es la unica forma de entender la regla.
    #
    # Van como funciones de MODULO y no como lambdas: la ConfigEtapa vive dentro
    # del Quest, y el Quest se guarda (regla anti-PicklingError del proyecto).
    # Devuelven el texto ya traducido; que _resolver lo pase de nuevo por
    # translate_string no molesta, un string sin traduccion vuelve igual.

    def vd30_pista_listo():
        """Pista de ETAPA_BOTON_LISTO de la 06."""
        if getattr(store, 'vd30_fase', 0) == 1:
            return renpy.translate_string("Quiero hablar con Violet ahora")
        return renpy.translate_string("Hay algo que quiero hablar con Violet")

    def _vd30_dias_a_mostrar():
        """
        El contador COMO VA A QUEDAR esta noche, no como quedo la anterior.

        `vd30_dias_ignorada` lo mueve el trigger de dormir, asi que si el
        jugador le habla a Violet al mediodia el numero real recien cae a cero
        cuando se va a acostar — y hasta entonces la guia le miente. Aca se
        anticipa ese reseteo mirando el registro de contacto del dia, que se
        marca en el momento y vive hasta que dormir() lo limpia.

        Es SOLO para mostrar: no toca la variable. El reseteo de verdad lo
        sigue haciendo un unico lugar, `_vd30_trigger_dormir`, con la misma
        condicion.
        """
        if hubo_contacto_npc("violet"):
            return 0
        return getattr(store, 'vd30_dias_ignorada', 0)

    def vd30_que_hacer_listo():
        """Que hacer de ETAPA_BOTON_LISTO de la 06."""
        if getattr(store, 'vd30_fase', 0) == 1:
            return renpy.translate_string("Ir a la habitacion de Violet")
        return renpy.translate_string("Estar de noche en mi habitacion")

    def vd30b_que_hacer_listo():
        """
        Que hacer de ETAPA_BOTON_LISTO de la 07: el contador de dias.

        Se muestra aunque este en 0 —y sobre todo cuando VUELVE a 0—: cualquier
        contacto con Violet lo reinicia, y verlo caer es la unica forma que
        tiene el jugador de entender por que la cuenta no avanza.

        NO NOMBRA EL DORMIR a proposito, aunque dormir sea lo que mueve el
        contador: decirlo invita a pasar los tres dias durmiendo de corrido y
        saltearse el juego. El objetivo que se enuncia es el que importa,
        ignorarla; como pasan los dias es cosa del jugador.

        La plantilla se traduce ANTES de meterle los numeros: si se tradujera
        el resultado ya armado haria falta una entrada por cada valor del
        contador. Mismo criterio que el "Esperar {} dias" de la amor 25.
        """
        return renpy.translate_string(
            "Pasar {} dias ignorando a Violet ({}/{})").format(
                VD30_DIAS_PARA_VISITA,
                _vd30_dias_a_mostrar(),
                VD30_DIAS_PARA_VISITA)

    def _vd30_activa():
        """La 06 (la noche de la charla) lista y sin completar."""
        return quest_lista_para_boton("violet_deseo_06")

    def _vd30b_activa():
        """La 07 (los tres dias) lista y sin completar."""
        return quest_lista_para_boton("violet_deseo_07")

    def _gl_trigger_violet_deseo_30():
        """
        Trigger de game_loop de la 06: las dos entradas de la noche de la
        charla, cada una en su fase.

        Va por game_loop y no por registrar_trigger_avanzar porque el horario
        tambien lo mueven las acciones y el talk, que llaman a avanzar_horario()
        directo sin pasar por el label del boton.
        """
        if not _vd30_activa():
            return None

        _loc = store.sistema_locaciones.locacion_actual
        _loc_id = _loc.id if _loc else None

        # Fase 0 → arranque. De noche, el MC en su pieza y ella en la suya y
        # libre: son las demandas de la quest (capa 2, adentro de _vd30_activa).
        if store.vd30_fase == 0:
            return "violet_deseo_30_inicio"

        # Fase 1 → llegar a su habitacion. Va por game_loop y no por un override
        # de puerta a proposito: con la ventaja "puerta_dejar_pasar_noche" del
        # hito de deseo 20 el MC entra directo sin menu, y el trigger de
        # locacion lo agarra por los dos caminos.
        if store.vd30_fase == 1 and _loc_id == "casa_hviolet":
            return "quest_violet_deseo_06"

        return None

    def _gl_trigger_violet_deseo_30b():
        """
        Trigger de game_loop de la 07: la red del cierre. Ya cumplio los dias
        y esta de noche en su pieza — el camino normal es el trigger de dormir;
        este cubre al que llego a 3 y no vio la escena (cargo una partida
        vieja, o el contador subio por otro camino).
        """
        if not _vd30b_activa():
            return None
        _loc = store.sistema_locaciones.locacion_actual
        if (store.horario_actual == 2 and _loc is not None and _loc.id == "casa_hmc"
                and store.vd30_dias_ignorada >= VD30_DIAS_PARA_VISITA):
            return "violet_deseo_30_visita"
        return None

    def _gl_trigger_vd30_migracion():
        """
        Migracion de partidas de 0.1.9a: la version de una sola quest dejaba la
        06 activa durante los tres dias (fase 2). Con la 06 partida, esa
        partida tiene que completar la 06 en silencio para que nazca la 07 y
        siga contando con el contador que ya tenia. Solo efectos python; nunca
        devuelve label. Una partida nueva nunca entra: la 06 se completa en la
        charla antes de que la fase pase a 2.
        """
        _q06 = store.sistema_quests.obtener_quest("violet_deseo_06")
        if (getattr(store, 'vd30_fase', 0) >= 2 and _q06 is not None
                and _q06.activa and not _q06.completada):
            if config.developer:
                print("[Deseo 30] migracion: partida contando dias con la 06 "
                      "activa; se completa para que nazca la 07")
            completar_quest_actual("violet", quest_id="violet_deseo_06")
        # Segunda red: hasta el 2026-09-15 la visita cerraba la 06 en vez de
        # la 07, asi que una partida que ya vio la visita (fase 3) quedo con
        # "Distancia" activa para siempre y sin el hito de deseo 30. Se cierra
        # aca; el hito lo otorga actualizar_hitos en esta misma vuelta.
        _q07 = store.sistema_quests.obtener_quest("violet_deseo_07")
        if (getattr(store, 'vd30_fase', 0) >= 3 and _q07 is not None
                and _q07.activa and not _q07.completada):
            if config.developer:
                print("[Deseo 30] migracion: la visita ya paso y la 07 sigue "
                      "activa; se completa")
            completar_quest_actual("violet", quest_id="violet_deseo_07")
        return None

    def _vd30_trigger_dormir():
        """
        Trigger de dormir, fase "antes": corre con la animacion ya mostrada y
        ANTES de que dormir() cambie el dia.

        Hace las DOS cosas de la etapa 2:
          1. mueve el contador segun si hoy hubo contacto con Violet
          2. si con esta noche llega a los 3, devuelve el label de la visita

        LA FASE IMPORTA POR PARTIDA DOBLE. Primero, el registro de contacto se
        limpia dentro de dormir(), asi que en "despues" ya no habria dato que
        leer. Y segundo, devolver el label desde "antes" es lo que permite que
        el MC se despierte ESA MISMA NOCHE: dormir() no llega a correr, el dia
        no cambia y la escena mueve el horario a mano.
        """
        if not _vd30b_activa():
            return None

        if hubo_contacto_npc("violet"):
            store.vd30_dias_ignorada = 0
            return None

        store.vd30_dias_ignorada += 1

        if store.vd30_dias_ignorada >= VD30_DIAS_PARA_VISITA:
            return "violet_deseo_30_visita"
        return None


init 5 python:

    registrar_trigger_game_loop("violet_deseo_30_fases",
                                _gl_trigger_violet_deseo_30, duenio="violet_deseo_30",
                                quest_id="violet_deseo_06")

    registrar_trigger_game_loop("violet_deseo_30_visita_red",
                                _gl_trigger_violet_deseo_30b,
                                quest_id="violet_deseo_07")

    # Prioridad alta: tiene que correr antes que el trigger de la 07 en la
    # misma vuelta, para que la 07 ya exista cuando este la mire.
    registrar_trigger_game_loop("violet_deseo_30_migracion",
                                _gl_trigger_vd30_migracion, prioridad=50)

    registrar_trigger_dormir("violet_deseo_30_ignorar", "antes",
                             _vd30_trigger_dormir, quest_id="violet_deseo_07")


################################################################################
## 1 · EL ARRANQUE — de noche, en su propia habitacion
################################################################################

label violet_deseo_30_inicio:

    $ ocultar_hud()
    window show

    # Su habitacion de noche: el trigger solo salta ahi y a esa hora.
    $ _vd30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd30_bg

    # (Mc cuerpo pensando ojos base boca neutral)
    show mc_parado_base c_rbase_pensando o_base b_none at center with sprite_normal

    # =========================================================================
    # CONTENIDO — lo que le esta dando vueltas
    # =========================================================================

    piensa "Cada vez me cuesta más controlar las ganas que tengo de estar con Violet"
    piensa "Y tenerla a solo unos metros todo el tiempo no ayuda"
    piensa "La voy a ir a ver"

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base with dissolve

    # Se mueve libre por adentro pero no hace nada mas hasta llegar a su pieza.
    # La lista se arma en runtime en vez de a mano para que una locacion nueva
    # no quede afuera por olvido; la unica que se saca es casa_frente, que es
    # la salida.
    $ _vd30_dentro = [_l for _l in sistema_locaciones.locaciones if _l != "casa_frente"]
    $ activar_restriccion(
        duenio="violet_deseo_30",
        congelar_reloj=True,
        locaciones_permitidas=_vd30_dentro,
        acciones_bloqueadas=["avanzar_tiempo", "dormir", "entrenar", "trabajar",
                             "usar_item", "comprar", "cocinar", "ver_tv"],
        mensaje_movimiento="Tengo que hablar con Violet",
        mensaje_accion_default="Tengo que hablar con Violet",
        npcs_interactuables=["violet"],
    )

    $ vd30_fase = 1

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA CHARLA — al entrar a su habitacion
################################################################################
## Cierra la 06. Al completarla nace la 07 y de acá arranca la cuenta de los
## tres dias.

label quest_violet_deseo_06:

    # Se levanta antes de la escena: si se cortara a la mitad, el jugador
    # quedaria con el recorrido acotado y sin forma de destrabarlo.
    $ desactivar_restriccion(duenio="violet_deseo_30")

    $ ocultar_hud()
    window show

    $ _vd30_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd30_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la charla en su habitacion
    # =========================================================================

    show violet_parada b_hablando
    violet "¿Qué pasa?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Vine a verte, estuve pensando en ti todo el día y no aguanto las ganas"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "¿Ganas de qué?"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "De estar contigo, ¿de qué más?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Todo el tiempo con cosas pervertidas en la cabeza"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No puedo evitarlo, es lo que siento"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Bueno, pero te tienes que controlar un poco"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "¿Por?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Porque sí"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Al final no te entiendo... Si no actúo, por qué no actúo"
    show mc_parado_base b_abiertachica
    mc "Pero si quiero avanzar, por qué quiero avanzar"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "La situación es un poco complicada..."
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Tu indecisión pone la situación complicada"
    show mc_parado_base b_none


    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    # Sale al pasillo y queda en modo libre: empieza la cuenta de los dias.
    # El contador arranca en 0 explicitamente y no se confia en el default:
    # la quest se puede reintentar y un valor viejo la cerraria de una.
    $ vd30_fase = 2
    $ vd30_dias_ignorada = 0
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")

    # Se completa la 06 y nace la 07 ("Distancia"): la noche de corrido
    # termino, lo que sigue es juego libre con un contador.
    $ completar_quest_actual("violet", quest_id="violet_deseo_06")

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · LA VISITA — cierre de la 07
################################################################################
## DOS ENTRADAS, un solo label:
##   - el trigger de DORMIR, cuando la tercera noche completa la cuenta. La
##     animacion de dormir ya corrio y dormir() NO llego a ejecutarse, asi que
##     el dia no cambio: la escena empuja el horario a noche a mano.
##   - el trigger de game_loop, estando de noche en su pieza con la cuenta ya
##     hecha. Ahi el horario ya es el que corresponde y el empuje no hace nada.

label violet_deseo_30_visita:

    # Solo hacia adelante: si ya es de noche (o mas tarde) la cuenta da <= 0 y
    # avanzar_horario_multiple no mueve nada, que es lo correcto.
    $ _vd30_saltos = max(0, 2 - horario_actual)
    if _vd30_saltos:
        $ avanzar_horario_multiple(_vd30_saltos)

    $ vd30_fase = 3

    $ ocultar_hud()
    window show

    # Su habitacion explicitamente y no locacion_actual: por el camino de dormir
    # el jugador podria haberse acostado en otro lado.
    $ _vd30_loc_hmc = sistema_locaciones.obtener_locacion("casa_hmc")
    $ _vd30_bg = _vd30_loc_hmc.background if _vd30_loc_hmc else "#1a1a1a"
    scene expression _vd30_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — ella vino a buscarlo
    # =========================================================================

    show violet_parada b_hablando
    violet "Hola"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Hola"
    show mc_parado_base b_none

    show violet_parada b_hablando c_pijama_pensando with sprite_normal
    violet "¿Todo bien?"
    show violet_parada b_none c_pijama_base with sprite_normal

    show mc_parado_base b_hablando c_rbase_brazoscruzados with sprite_normal
    mc "Sí, ¿y tú?"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Yo bien también, pero estás algo raro"
    show violet_parada b_none

    show mc_parado_base b_hablando c_rbase_pensando with sprite_normal
    mc "¿Por qué lo dices?"
    show mc_parado_base b_none c_rbase_brazoscruzados with sprite_normal

    show violet_parada b_hablando c_pijama_brazoscruzados with sprite_normal
    violet "Siento que me estás evitando"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "No te evito a ti, evito situaciones complicadas nada más"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "Ahhhh, es por eso... Tienes una visión muy drástica de las cosas"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Es mi forma de ser"
    show mc_parado_base b_none

    show violet_parada b_hablando
    violet "No, tu forma de ser es la de un pervertido que se la pasa comiéndome con la mirada"
    show violet_parada b_none

    show mc_parado_base b_hablando
    mc "Quizás no lo sea"
    show mc_parado_base b_none

    show violet_parada b_hablando c_pijama_pensando with sprite_normal
    violet "¿Estás seguro?"
    show violet_parada b_none c_pijama_base with sprite_normal

    show mc_parado_base b_hablando
    mc "Sí, muy seguro"
    show mc_parado_base b_none

    # Violet se saca el short hasta quedar en tanga.
    #
    # El sprite de pijama sale y entra `violet_tanga` en el mismo lugar (`at
    # right`): las dos cosas van bajo un unico `with`, asi que se cruzan en una
    # sola disolvencia en vez de verse un hueco entre medio.
    #
    # Los cuatro cuadros son atributos del mismo grupo `cuerpo`, o sea
    # excluyentes: cada `show` apaga el anterior y no hay que bajar nada a mano.
    # Van sin dialogo y sin clicks, con `pause` de duracion fija, para que la
    # secuencia corra sola. El pause es 0.5 porque sprite_normal es un
    # Dissolve(0.5): con menos, el cuadro siguiente entraria antes de que el
    # anterior termine de aparecer.
    hide violet_parada
    show violet_tanga c_sacandoshort b30_none at right
    with sprite_normal
    pause 0.5

    show violet_tanga c_sacandoshort2 with sprite_normal
    pause 0.5

    show violet_tanga c_sacandoshort3 with sprite_normal
    pause 0.5

    show violet_tanga c_paradobase with sprite_normal
    pause 0.5

    show mc_parado_base c_rbase_asustado with sprite_normal
    piensa "¿Y ahora qué le pasa?"
    show mc_parado_base c_rbase_brazoscruzados with sprite_normal

    # Las bocas de este arte son las `b30_*`: las `b_*` estan dibujadas para la
    # pose de la quest de deseo 10, que tiene la cabeza en otro lado.
    show violet_tanga b30_hablando
    violet "Entonces no hay problema si me quedo en tanga"
    show violet_tanga b30_hablandochica
    violet "Ya que no hay ningún pervertido acá"
    show violet_tanga b30_none

    show mc_parado_base c_rbase_avergonzado with sprite_normal
    piensa "Ya entiendo por dónde va esto"
    show mc_parado_base c_rbase_brazoscruzados with sprite_normal

    show mc_parado_base b_hablando
    mc "No hay ningún problema"
    show mc_parado_base b_none

    show violet_tanga b30_hablando
    violet "Tenía ganas de jugar un ratito a algo, una lástima"
    show violet_tanga b30_hablandochica
    violet "Me voy entonces"
    show violet_tanga b30_none

    hide violet_tanga with dissolve

    piensa "Creo que después de esto la voy entendiendo mejor, ella quiere llevar las cosas a su ritmo, pero le molesta que no le preste atención"
    piensa "Ahora está en mí cómo usar esto, cuanto más la pueda ignorar más lejos ella va a llegar y al final va a resultar mejor para mí"


    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    with dissolve

    # Cierra la 07 ("Distancia"): es la quest del hito de deseo 30, asi que
    # aca se gana el hito y su ventaja `provocacion`.
    $ completar_quest_actual("violet", quest_id="violet_deseo_07")

    window hide
    $ mostrar_hud()
    jump game_loop
