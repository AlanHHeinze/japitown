################################################################################
## Violet — Deseo 30 · "Sinceridad"
################################################################################
##     archivo   violet_deseo_30.rpy
##     quest     violet_deseo_06           (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_06     (lo fija el motor: "quest_" + id)
##
## DOS ETAPAS bien distintas, encadenadas por `vd30_fase`:
##
##   ETAPA 1 — la charla en su pieza
##     0  esperando       → trigger de game_loop: de noche, el MC en SU pieza y
##                          Violet libre en la suya
##     1  yendo a verla   → recorrido acotado; entrar a casa_hviolet dispara la
##                          escena. Al salir queda en el pasillo, en modo libre
##
##   ETAPA 2 — ignorarla tres dias
##     2  contando        → hay que dormir 3 noches SIN hacer nada con ella
##     3  terminada
##
## LA ETAPA 2 SE MIDE AL REVES QUE TODO EL RESTO DEL JUEGO: no se pide hacer
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

    def _vd30_activa():
        return quest_lista_para_boton("violet_deseo_06")

    def _vd30_violet_libre():
        """
        Violet en su habitacion y sin nada encima.

        La locacion ya descarta casi todo (si se baña esta en el baño, si salio
        esta afuera), pero se chequean igual la rutina especial y los bloqueos:
        una rutina de quest puede tenerla en su pieza metida en otra cosa.
        """
        if tracker_locacion_npc("violet") != "casa_hviolet":
            return False

        _v30 = obtener_npc("violet")
        if _v30 is None or _v30.obtener_rutina_especial_actual() is not None:
            return False

        return not npc_esta_oculto("violet") and npc_interactuable("violet")

    def _gl_trigger_violet_deseo_30():
        """
        Trigger de game_loop. Las tres entradas de la quest, cada una en su fase.

        Va por game_loop y no por registrar_trigger_avanzar porque el horario
        tambien lo mueven las acciones y el talk, que llaman a avanzar_horario()
        directo sin pasar por el label del boton.
        """
        if not _vd30_activa():
            return None

        _loc = store.sistema_locaciones.locacion_actual
        _loc_id = _loc.id if _loc else None

        # Fase 0 → arranque: de noche, el MC en su pieza y ella disponible.
        if (store.vd30_fase == 0 and store.horario_actual == 2
                and _loc_id == "casa_hmc" and _vd30_violet_libre()):
            return "violet_deseo_30_inicio"

        # Fase 1 → llegar a su habitacion. Va por game_loop y no por un override
        # de puerta a proposito: con la ventaja "puerta_dejar_pasar_noche" del
        # hito de deseo 20 el MC entra directo sin menu, y el trigger de
        # locacion lo agarra por los dos caminos.
        if store.vd30_fase == 1 and _loc_id == "casa_hviolet":
            return "quest_violet_deseo_06"

        # Fase 2 → la red del cierre: ya cumplio los dias y esta de noche en su
        # pieza. El camino normal es el trigger de dormir.
        if (store.vd30_fase == 2 and store.horario_actual == 2
                and _loc_id == "casa_hmc"
                and store.vd30_dias_ignorada >= VD30_DIAS_PARA_VISITA):
            return "violet_deseo_30_visita"

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
        if not _vd30_activa() or store.vd30_fase != 2:
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
                                _gl_trigger_violet_deseo_30)

    registrar_trigger_dormir("violet_deseo_30_ignorar", "antes",
                             _vd30_trigger_dormir)


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

    piensa "..."
    piensa "..."

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
## Cierra la ETAPA 1, no la quest: de acá arranca la cuenta de los tres dias.

label quest_violet_deseo_06:

    # Se levanta antes de la escena: si se cortara a la mitad, el jugador
    # quedaria con el recorrido acotado y sin forma de destrabarlo.
    $ desactivar_restriccion()

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

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
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

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 3 · LA VISITA — cierre de la quest
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

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    $ completar_quest_actual("violet", quest_id="violet_deseo_06")

    window hide
    $ mostrar_hud()
    jump game_loop
