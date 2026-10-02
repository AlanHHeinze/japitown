################################################################################
## Dev — Control de fixes: las escenas que hay que verificar a ojo
################################################################################
## Cada fix que toca algo VISUAL o que no se puede probar headless deja acá su
## entrada: a que escena hay que entrar y que hay que mirar. La herramienta arma
## el mundo y te deja adentro. Cuando la verificacion esta hecha, la entrada se
## saca — la lista es lo pendiente, no un historial (el historial vive en
## docs/errores/).
##
## USO (consola, Shift+O, con config.developer):
##     jp_fix()               -> lista los fixes pendientes de verificar
##     jp_fix("ducha_08a")    -> arma el estado y entra a la escena
## O desde el menu de cheats: "Control de fixes".
##
## ⚠️ USAR EN UNA PARTIDA DESCARTABLE. Cada entrada reescribe el estado de su
## linea (marca completadas las quests previas, mueve el reloj y a los NPCs) y
## la escena sigue su curso normal: completa la quest, cambia el horario, otorga
## hitos. No es un visor: es el juego, empezado mas adelante.
##
## Reusa las primitivas de escenarios_controlador.rpy (_esc_reloj, _esc_mc,
## _esc_npc_a, _esc_dejar_lista, _esc_limpiar, _esc_stats,
## _esc_marcar_completada). El ORDEN importa: `_esc_reloj` reaplica las
## rutinas, asi que mover NPCs a mano va SIEMPRE despues.
##
## Cada funcion arma el estado y devuelve el LABEL al que hay que saltar.

init python:

    import collections as _fix_collections

    # ── Escenas de verificacion ──────────────────────────────────────────────

    def _fix_ducha_08a():
        """
        S13: la ducha de la 08_a. Las cuatro capas de agua pasaron de
        Animation() a ATL; hay que ver que las gotas caigan al mismo ritmo y
        con la misma transparencia de antes.
        """
        _esc_limpiar()
        _esc_reloj(dias_totales=30, dia_semana=2, horario=3)
        _esc_dejar_lista("violet_questprincipal_08_a")
        activar_quest("violet_questprincipal_08_a", origen="control_fixes")
        _esc_mc("casa_banioarriba")
        _esc_npc_a("violet", "casa_banioarriba")
        return "violet_quest08a_entrar_baño"

    def _fix_espiar():
        """
        S13: el minijuego de espiar. Las tres lluvias y la Violet
        enjabonandose pasaron a ATL; hay que ver el ritmo de la lluvia y que
        el fundido entre frames de Violet (0.5 s) siga igual, incluido el de
        vuelta al primer frame al cerrar el ciclo (26 s).

        Hacen falta tres cosas: la ventaja `provocacion` (hito de deseo 30),
        Violet metida en el baño de arriba, y la puerta entreabierta —
        `violet_ducha_puerta_abierta()` sortea una vez por (dia, horario) y
        cachea el resultado, asi que se escribe la cache directamente.
        """
        _esc_limpiar()
        _esc_reloj(dias_totales=30, dia_semana=2, horario=2)
        _esc_mc("casa_pasilloarriba")
        _esc_npc_a("violet", "casa_banioarriba")
        _esc_stats("violet", deseo=30)
        _esc_marcar_completada("violet_deseo_07")
        try:
            actualizar_hitos()
        except Exception as e:
            print("[control_fixes] actualizar_hitos: %r" % (e,))
        store.violet_provocacion_ducha = {
            "clave": (getattr(store, "dias_totales", 0),
                      getattr(store, "horario_actual", 0)),
            "abierta": True,
        }
        store._espiar_npc_temp = "violet"
        return "jp_fix_espiar"

    def _fix_precarga():
        """
        S11 (variante precarga): la pantalla de carga paso a un solo bloque
        Python. Hay que ver que el contador suba hasta 100 y vuelva al juego.
        No arma nada: la precarga no depende del estado.
        """
        return "jp_fix_precarga"

    # nombre -> (titulo, que mirar, funcion). Sacar la entrada al verificarla.
    FIXES_PENDIENTES = _fix_collections.OrderedDict([
        ("precarga", (
            u"S11 · Pantalla de carga",
            u"El contador sube hasta 100 y vuelve al juego. Tab en segundo plano opcional.",
            _fix_precarga)),
        ("ducha_08a", (
            u"S13 · Ducha de la 08_a (capas de agua en ATL)",
            u"Las gotas caen al mismo ritmo y con la misma transparencia que antes.",
            _fix_ducha_08a)),
        ("espiar", (
            u"S13 · Minijuego de espiar (lluvia y Violet en ATL)",
            u"Ritmo de la lluvia; fundido de 0.5 s entre frames de Violet y al cerrar el ciclo.",
            _fix_espiar)),
    ])

    def jp_fix(nombre=None):
        """Lista los fixes pendientes, o arma uno y entra."""
        if nombre is None or nombre not in FIXES_PENDIENTES:
            print("=" * 70)
            print("CONTROL DE FIXES — jp_fix(\"<nombre>\")")
            for _n, (_t, _v, _f) in FIXES_PENDIENTES.items():
                print("  %-14s %s" % (_n, _t))
                print("  %-14s   → %s" % ("", _v))
            print("=" * 70)
            return
        store._jp_fix_pendiente = nombre
        renpy.jump("jp_fix_ir")


default _jp_fix_pendiente = "precarga"


label jp_fix_ir:

    # Cerrar todo lo que pueda estar abierto (el menu de cheats vive dentro del
    # celular, asi que hay que bajar los dos).
    $ renpy.hide_screen("menu_cheats")
    $ renpy.hide_screen("control_fixes")
    $ renpy.hide_screen("menu_celular")
    $ menu_celular_abierto = False
    $ desactivar_restriccion(duenio="*")

    python:
        _fix_titulo, _fix_que_mirar, _fix_fn = FIXES_PENDIENTES[_jp_fix_pendiente]
        _fix_destino = _fix_fn()
        actualizar_quests()
        print("=" * 70)
        print("FIX %s — %s" % (_jp_fix_pendiente, _fix_titulo))
        print("Mirar: %s" % _fix_que_mirar)
        print("=" * 70)

    $ ocultar_hud()
    jump expression _fix_destino


## El minijuego de espiar NO se puede saltar con `jump`: `espiar_iniciar`
## muestra la screen y termina en `return`, o sea que es una SUBRUTINA — en el
## flujo real el frame se lo pone el `Call` del HUD. Sin frame, ese return se
## comeria el del game_loop y cerraria el juego al menu principal.
##
## El `pause` de despues sostiene la screen igual que hace el game_loop; cuando
## el jugador toca "Salir", ese Call corta el pause y el flujo sigue en la
## linea siguiente (mismo patron que el bucle del minijuego de la 09).

label jp_fix_espiar:

    hide screen hud_navegacion
    call espiar_iniciar from _call_jp_fix_espiar
    pause
    jump game_loop


## La pantalla de carga es el splashscreen que Ren'Py corre al arrancar; se
## puede llamar de nuevo. Termina en `scene black` + return, asi que despues
## hay que repintar el fondo de la locacion.

label jp_fix_precarga:

    hide screen hud_navegacion
    call splashscreen from _call_jp_fix_precarga
    $ actualizar_bg_master()
    jump game_loop


################################################################################
## La lista, desde el menu de cheats
################################################################################

screen control_fixes():
    zorder 290
    modal True

    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        background "#00000066"
        action Hide("control_fixes")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        background "#0d0d1eFF"
        padding (20, 16)

        vbox:
            xfill True
            spacing 8

            hbox:
                xfill True
                text "Dev — Control de fixes" size 20 color "#4FC3F7" bold True xfill True
                textbutton "Cerrar" action Hide("control_fixes")

            text "Escenas pendientes de verificar a ojo después de un fix. Reescriben el estado de esa línea: usar en una partida descartable." size 13 color "#aaaaaa"

            if not FIXES_PENDIENTES:
                text "Nada pendiente." size 14 color "#66DD88"

            for _nombre in FIXES_PENDIENTES:
                $ _cf_titulo, _cf_que_mirar, _cf_fn = FIXES_PENDIENTES[_nombre]
                button:
                    xfill True
                    background "#1a1a3aCC"
                    hover_background "#2a2a5aCC"
                    padding (12, 8)
                    action [SetVariable("_jp_fix_pendiente", _nombre),
                            Hide("control_fixes"),
                            Hide("menu_cheats"),
                            Jump("jp_fix_ir")]
                    vbox:
                        spacing 2
                        text _cf_titulo size 14 color "#FFD54F" bold True
                        text "Mirar: " + _cf_que_mirar size 12 color "#aaaaaa"
