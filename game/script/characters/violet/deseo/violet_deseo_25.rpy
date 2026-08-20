################################################################################
## Violet — Deseo 25 · "En su habitacion"
################################################################################
##     archivo   violet_deseo_25.rpy
##     quest     violet_deseo_05          (quests_deseo_violet.rpy)
##     label     quest_violet_deseo_05    (lo fija el motor: "quest_" + id)
##
## DOS DISPARADORES, y no rompen la regla de "uno solo" porque los separa el
## horario: el boton del menu de Violet (a cualquier hora) y la opcion de su
## puerta (SOLO de noche). Los dos desembocan en el mismo router.
##
## LOS DOS CAMINOS:
##
##   de dia o de tarde  →  se lo propone, ella acepta        (vd25_acordado)
##                         y a la noche se ve en su pieza
##
##   de noche           →  ¿ya se lo habia propuesto?
##                           no  →  violet_deseo_25_previa  →┐
##                           si  →──────────────────────────→┴→ quest_violet_deseo_05
##
## POR QUE EL SEGUNDO LABEL VUELVE A MOSTRAR LOS SPRITES: se llega ahi por dos
## caminos. Por el jump de la previa ya estan en escena (repetir el `show` no
## molesta, Ren'Py no reinicia nada) y por el salto directo todavia no hay
## nadie. Ponerlos en los dos lados seria duplicar; ponerlos solo en la previa
## dejaria la escena vacia en el camino directo.
##
## LA RUTINA DE LA NOCHE ES INCONDICIONAL, y es una diferencia con lo pedido:
## `rutina_quest` es un dict estatico del Quest y se aplica al llegar a
## ETAPA_RUTINA — no hay forma declarativa de prenderla desde un label. En la
## practica casi no se nota: de lunes a sabado Violet YA pasa la noche en su
## habitacion por su rutina base, asi que el unico dia en que cambia algo es el
## domingo (que normalmente estaria en el living). Y tiene que estar ahi de
## noche igual, porque el camino de "no se lo pedi antes" existe y necesita
## encontrarla.


################################################################################
## Estado
################################################################################

# True si se lo propuso de dia o de tarde. Decide si de noche hay escena previa.
default vd25_acordado = False


init python:

    def _vd25_activa():
        return quest_lista_para_boton("violet_deseo_05")

    def _vd25_boton_violet():
        """Boton "Ver anime" del menu de Violet. A cualquier hora."""
        return _vd25_activa()

    def _vd25_puerta_ver_anime():
        """
        Opcion "Ver anime" de la puerta. Solo de noche: de dia la propuesta se
        le hace en persona, y desde la puerta no tendria a quien decirselo —
        de dia Violet ni siquiera esta en su habitacion.
        """
        return _vd25_activa() and store.horario_actual == 2


init 5 python:

    registrar_opcion_puerta("violet", "Ver anime",
                            "violet_deseo_25_noche", _vd25_puerta_ver_anime,
                            ocultar_golpear=True)


################################################################################
## Routers
################################################################################
## El del menu de Violet reparte por horario; el de la noche, por si ya se lo
## habia propuesto. Ninguno de los dos muestra nada: solo saltan.

label violet_deseo_25_pedir:
    if horario_actual < 2:
        jump violet_deseo_25_acordar
    jump violet_deseo_25_noche


label violet_deseo_25_noche:
    if vd25_acordado:
        jump quest_violet_deseo_05
    jump violet_deseo_25_previa


################################################################################
## 1 · LA PROPUESTA — de dia o de tarde, donde este
################################################################################

label violet_deseo_25_acordar:

    $ ocultar_hud()
    window show

    $ _vd25_bg = sistema_locaciones.locacion_actual.background if sistema_locaciones.locacion_actual else "#1a1a1a"
    scene expression _vd25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda

    # cuerpo_activo() para no asumir la ropa: puede estar en pijama.
    $ _vd25_cuerpo = cuerpo_activo("violet")
    if _vd25_cuerpo == "c_pijama":
        # (Violet cuerpo pijama ojos base boca neutral)
        show violet_parada c_pijama_base ca_pijama o_base b_none at right
    else:
        # (Violet cuerpo base ojos base boca neutral)
        show violet_parada c_rbase_base ca_base o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — se lo propone y ella acepta para esa noche
    # =========================================================================

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    hide mc_parado_base
    hide violet_parada
    with dissolve

    # De noche ya no hace falta la escena previa: quedaron en algo.
    $ vd25_acordado = True

    window hide
    $ mostrar_hud()
    jump game_loop


################################################################################
## 2 · LA PREVIA — de noche, sin haberlo hablado antes
################################################################################
## Cae acá el que sube directo sin habersela cruzado en el dia. Termina con un
## jump al cierre, no con game_loop: es la primera mitad de la misma escena.

label violet_deseo_25_previa:

    $ ocultar_hud()
    window show

    # La habitacion de Violet explicitamente y no locacion_actual: acá se puede
    # llegar desde el pasillo (opcion de puerta) o desde adentro (click en
    # ella), y la escena pasa siempre en su pieza.
    $ _vd25_loc_hv = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _vd25_bg = _vd25_loc_hv.background if _vd25_loc_hv else "#1a1a1a"
    scene expression _vd25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — llega de sorpresa y se lo propone ahi mismo
    # =========================================================================

    # (Mc boca hablando)
    show mc_parado_base b_hablando
    mc "..."
    # (Mc boca neutral)
    show mc_parado_base b_none

    # (Violet boca hablando)
    show violet_parada b_hablando
    violet "..."
    # (Violet boca neutral)
    show violet_parada b_none

    # =========================================================================
    # FIN DEL CONTENIDO
    # =========================================================================

    jump quest_violet_deseo_05


################################################################################
## 3 · LA ESCENA — cierre de la quest
################################################################################
## Se llega por dos caminos (el jump de la previa y el salto directo), asi que
## vuelve a plantar la escena entera. Por el jump los sprites ya estan puestos y
## el `show` no hace nada visible; por el salto directo son imprescindibles.

label quest_violet_deseo_05:

    $ ocultar_hud()
    window show

    $ _vd25_loc_hv = sistema_locaciones.obtener_locacion("casa_hviolet")
    $ _vd25_bg = _vd25_loc_hv.background if _vd25_loc_hv else "#1a1a1a"
    scene expression _vd25_bg

    # (Mc cuerpo base ojos base boca neutral)
    show mc_parado_base c_rbase_base o_base b_none at mc_izquierda
    # (Violet cuerpo pijama ojos base boca neutral)
    show violet_parada c_pijama_base ca_pijama o_base b_none at right
    with sprite_normal

    # =========================================================================
    # CONTENIDO — la escena entera: ven el capitulo juntos
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

    $ completar_quest_actual("violet", quest_id="violet_deseo_05")

    # Sale de la habitacion y se le fue la noche: pasillo y horario +1.
    $ sistema_locaciones.mover_a_locacion("casa_pasilloarriba")
    $ avanzar_horario()

    window hide
    $ mostrar_hud()
    jump game_loop
