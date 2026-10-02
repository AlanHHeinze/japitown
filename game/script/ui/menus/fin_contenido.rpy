################################################################################
## Fin del contenido — la pantalla al terminar TODO lo publicado
################################################################################
## Cuando el jugador completa la ULTIMA quest publicada de TODAS las ramas (la
## de amor, la de deseo y la principal de Violet), el juego le muestra UNA vez
## esta pantalla: que llego al final, el agradecimiento, Patreon, Discord y
## seguir.
##
## UNA SOLA VEZ Y AL FINAL DE TODO, no una por rama: tres pantallas iguales
## pidiendo apoyo en la misma partida se leen como spam. La contra es que el
## que juega una sola rama no la ve hasta terminar las otras.
##
## ES UN REGISTRO, como el resto de los enganches contenido → motor: cada rama
## declara su quest final desde su propio archivo, en `init 5`:
##
##     registrar_fin_de_rama("violet_amor_10", _("Rama de amor de Violet"))
##
## ⚠️ AL PUBLICAR UNA QUEST NUEVA AL FINAL DE UNA RAMA, SE MUEVE ESE REGISTRO a
## la quest nueva. Nada mas: ni esta pantalla ni los labels de las quests saben
## cual es la ultima. Y como lo visto se guarda por quest, al moverlo la
## pantalla vuelve a salir cuando el jugador termine el contenido nuevo.
##
## POR QUE UN TRIGGER DE GAME_LOOP y no un `call` al final de cada quest: la
## rama principal tiene CUATRO formas de cerrar (la visita, lo planto, las dos
## ramas que cierran solas al dia siguiente) y la de deseo cierra con la 07,
## que tiene su propia red de migracion. Un trigger que mira si la quest esta
## completada las cubre a todas, y tambien a las que se agreguen.
##
## PRIORIDAD MINIMA a proposito: si en la misma vuelta arranca otra escena, la
## pantalla espera a la vuelta siguiente — nunca le corta nada a nadie. Y sin
## dueño: con una restriccion activa no salta (ver registrar_trigger_game_loop),
## que es justo lo que se quiere en el medio de una secuencia.
##
## PARTIDAS VIEJAS: el que cargue un save con las tres ya completadas ve la
## pantalla una vez al cargar. Es a proposito — llego al final del contenido
## igual, y es la unica forma de que se entere del mensaje.


################################################################################
## Registro y estado
################################################################################

init -1 python:

    # {quest_id: nombre de la rama}, en orden de registro.
    FIN_DE_RAMA = {}

    def registrar_fin_de_rama(quest_id, nombre):
        """
        Declara que `quest_id` es la ultima quest publicada de una rama.
        `nombre` va marcado con _() para el extractor de traducciones.
        """
        FIN_DE_RAMA[quest_id] = nombre


# Quests de fin de rama por las que ya se mostro la pantalla en esta partida.
# Se guarda por quest y no como un si/no: al mover un registro a una quest
# nueva, esa no esta en la lista y la pantalla vuelve a quedar pendiente.
default fin_contenido_visto = []


init python:

    def _fin_contenido_todo_completo():
        """True si TODAS las quests de fin de rama estan completadas."""
        for _qid in FIN_DE_RAMA:
            _q = store.sistema_quests.obtener_quest(_qid)
            if _q is None or not _q.completada:
                return False
        return bool(FIN_DE_RAMA)

    def _fin_contenido_pendientes():
        """
        Las quests de fin de rama a marcar como vistas, o [] si la pantalla no
        toca: hace falta que esten TODAS completadas y que alguna no se haya
        visto todavia.
        """
        if not _fin_contenido_todo_completo():
            return []
        _vistos = getattr(store, "fin_contenido_visto", [])
        return [_q for _q in FIN_DE_RAMA if _q not in _vistos]

    def _gl_trigger_fin_contenido():
        """
        Salta a la pantalla cuando se termino la ultima rama. NO marca nada:
        eso lo hace el label, asi si el motor ignora este label (restriccion
        activa) la pantalla queda pendiente para la vuelta siguiente.
        """
        if _fin_contenido_pendientes():
            return "fin_contenido"
        return None

    def fin_contenido_ramas_texto():
        """Todas las ramas registradas, traducidas y juntas."""
        return u" · ".join(renpy.translate_string(FIN_DE_RAMA[_q])
                           for _q in FIN_DE_RAMA)


init 5 python:

    registrar_trigger_game_loop("fin_contenido", _gl_trigger_fin_contenido,
                                prioridad=-1000)


################################################################################
## La pantalla
################################################################################

style fin_contenido_boton is button:
    padding (34, 16)
    hover_background "#FFB74D"

style fin_contenido_boton_text is button_text:
    size 30
    color "#FFFFFF"
    hover_color "#1a1a1a"
    xalign 0.5

screen fin_contenido(ramas):

    modal True
    zorder 200

    add Solid("#000000")

    vbox:
        xalign 0.5
        yalign 0.5
        xmaximum 1300
        spacing 18

        text _("Llegaste al final del contenido actual"):
            size 54
            color "#FFB74D"
            bold True
            xalign 0.5
            text_align 0.5

        text ramas:
            size 32
            color "#4FC3F7"
            xalign 0.5
            text_align 0.5

        null height 36

        text _("Gracias por jugar Japitown. Todavía es un proyecto joven, y cada persona que llega hasta aquí significa mucho para mí."):
            size 30
            color "#FFFFFF"
            xalign 0.5
            text_align 0.5

        text _("Si te gustó el juego y crees en lo que Japitown puede llegar a ser, apoyarlo en Patreon es lo que le permite seguir creciendo."):
            size 30
            color "#FFFFFF"
            xalign 0.5
            text_align 0.5

        text _("Y si quieres seguir su desarrollo, estás invitado a unirte al Discord."):
            size 30
            color "#FFFFFF"
            xalign 0.5
            text_align 0.5

        null height 36

        hbox:
            xalign 0.5
            spacing 30

            textbutton _("Apoyar en Patreon"):
                style "fin_contenido_boton"
                background "#F96854"
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action OpenURL(JP_URL_PATREON)

            textbutton _("Unirse al Discord"):
                style "fin_contenido_boton"
                background "#5865F2"
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action OpenURL(JP_URL_DISCORD)

            textbutton _("Continuar"):
                style "fin_contenido_boton"
                background "#37474F"
                if modo_posicionamiento:
                    action NullAction()
                else:
                    action Return()

        null height 20

        text "— Alan":
            size 30
            color "#BBBBBB"
            italic True
            xalign 0.5


################################################################################
## El label
################################################################################
## CONTENIDO: termina en game_loop. Marca las tres quests como vistas antes de
## mostrar: es una sola pantalla para todo el contenido.

label fin_contenido:

    $ ocultar_hud()
    window hide

    $ _fin_ramas = fin_contenido_ramas_texto()
    $ fin_contenido_visto = fin_contenido_visto + _fin_contenido_pendientes()

    call screen fin_contenido(_fin_ramas) with dissolve

    $ mostrar_hud()
    jump game_loop


################################################################################
## Testeo — se entra desde el menu de cheats (seccion PANTALLAS)
################################################################################
## Muestra la pantalla con TODAS las ramas registradas y NO marca nada como
## visto: se puede abrir las veces que haga falta sin tocar la partida.

label fin_contenido_test:

    $ ocultar_hud()
    window hide

    $ _fin_ramas = fin_contenido_ramas_texto()

    call screen fin_contenido(_fin_ramas) with dissolve

    $ mostrar_hud()
    jump game_loop
