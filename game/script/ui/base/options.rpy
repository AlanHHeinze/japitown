## This file contains options that can be changed to customize your game.
##
## Lines beginning with two '#' marks are comments, and you shouldn't uncomment
## them. Lines beginning with a single '#' mark are commented-out code, and you
## may want to uncomment them when appropriate.


## Basics ######################################################################

## A human-readable name of the game. This is used to set the default window
## title, and shows up in the interface and error reports.
##
## The _() surrounding the string marks it as eligible for translation.

define config.name = _("Japitown")

## The default language of the game for new players.
define config.default_language = "english"


## Determines if the title given above is shown on the main menu screen. Set
## this to False to hide the title.

define gui.show_name = True


## The version of the game.

## ⚠️ Al cambiarla hay que agregarle su fila a JP_HISTORIAL_SAVES
## (core/utils/compatibilidad_saves.rpy), diciendo si rompe o no los saves de la
## version anterior. Si falta, el juego no arranca en desarrollo y te avisa.
define config.version = "0.1.9.1"


## Text that is placed on the game's about screen. Place the text between the
## triple-quotes, and leave a blank line between paragraphs.

# Se usa renpy.minstore._p (la funcion de modulo) en vez del builtin `_p` del
# store a proposito: el rebuild de idioma re-evalua este define, y si algun .rpyc
# viejo cacheado (web) llegara a pisar store._p con un string, `_p(...)` crashearia
# con "'str' object is not callable". La referencia al modulo es inmune a ese shadow.
define gui.about = renpy.minstore._p("""
""")


## A short name for the game used for executables and directories in the built
## distribution. This must be ASCII-only, and must not contain spaces, colons,
## or semicolons.

define build.name = "Japitown"


## Autoguardado #################################################################

## NO activar config.save_dump en este proyecto (config.save_dump = True).
## Su dump_paths() asume que si __getstate__ devuelve una tupla, es (state,
## slots) — y la desempaqueta a ciegas (compat/pickle.py:143). Algún objeto del
## estado devuelve una tupla de UN elemento, así que revienta con
## "ValueError: not enough values to unpack (expected 2, got 1)" en CADA
## guardado, incluido el autoguardado al dormir. O sea: rompe el juego entero,
## no solo el diagnóstico. Para cazar objetos no serializables hay que usar otra
## vía (ver el bloque de diagnóstico manual más abajo).

## Se declara explicito (aunque True ya es el default de Ren'Py) porque de esto
## depende el autoguardado al dormir: force_autosave() no hace nada si esto es
## False. Ver autoguardar_partida() en core/time/timesystem_core.rpy.
## Los autoguardados quedan en la pagina "A" del menu de Cargar.
define config.has_autosave = True

## Cantidad de slots rotativos de autoguardado (default de Ren'Py). Como se
## autoguarda una vez por noche, esto da ~10 dias de historial para recuperar.
define config.autosave_slots = 10

## ---------------------------------------------------------------------------
## SOLO se autoguarda al dormir. Aca se apagan los 3 disparadores automaticos
## de Ren'Py, que hacian que el autoguardado saltara todo el tiempo y pisara
## los slots (10 slots consumidos en minutos = se pierde el historial de dias).
##
## OJO: no se puede apagar poniendo has_autosave = False. Ese flag lo chequea
## force_autosave() (loadsave.py:325), asi que apagarlo mataria TAMBIEN el
## autoguardado al dormir, ademas de esconder la pagina "A" del menu Cargar.
## Hay que apagar los disparadores, no el sistema.
## ---------------------------------------------------------------------------

## Autoguardado periodico (cada N interacciones). None lo desactiva por
## completo — es el mismo mecanismo que usa Ren'Py en 00gamemenu.rpy.
define config.autosave_frequency = None

## Autoguardado al elegir una opcion de menu (menuexports.py:169).
define config.autosave_on_choice = False

## Autoguardado al ingresar texto, ej. el nombre del MC (inputexports.py:54).
define config.autosave_on_input = False


## Sounds and music ############################################################

## These three variables control, among other things, which mixers are shown
## to the player by default. Setting one of these to False will hide the
## appropriate mixer.

define config.has_sound = True
define config.has_music = True
define config.has_voice = True


## To allow the user to play a test sound on the sound or voice channel,
## uncomment a line below and use it to set a sample sound to play.

# define config.sample_sound = "sample-sound.ogg"
# define config.sample_voice = "sample-voice.ogg"


## Uncomment the following line to set an audio file that will be played while
## the player is at the main menu. This file will continue playing into the
## game, until it is stopped or another file is played.

# define config.main_menu_music = "main-menu-theme.ogg"


## Transitions #################################################################
##
## These variables set transitions that are used when certain events occur.
## Each variable should be set to a transition, or None to indicate that no
## transition should be used.

## Entering or exiting the game menu.

define config.enter_transition = dissolve
define config.exit_transition = dissolve


## Between screens of the game menu.

define config.intra_transition = dissolve


## A transition that is used after a game has been loaded.

define config.after_load_transition = None


## Used when entering the main menu after the game has ended.

define config.end_game_transition = None


## Transition used when layeredimage attributes change during dialogue.
## This only affects the elements that change, not the entire image.

define config.say_attribute_transition = Dissolve(0.25, alpha=True)
define config.say_attribute_transition_layer = "master"



## Custom sprite transitions - Transiciones personalizadas para sprites
## Uso: show sprite with sprite_fast

define sprite_fast = Dissolve(0.2, alpha=True)      # Muy rapido - para animaciones
define sprite_normal = Dissolve(0.5, alpha=True)   # Normal - cambios de expresión
define sprite_slow = Dissolve(1, alpha=True)      # Lento - cambios dramáticos

## Tambien puedes crear transiciones con otros efectos:
# define sprite_fade = Fade(0.1, 0.0, 0.1)          # Fade a negro y volver
# define sprite_pixellate = Pixellate(0.3, 5)       # Efecto pixelado


## A variable to set the transition used when the game starts does not exist.
## Instead, use a with statement after showing the initial scene.


## Window management ###########################################################
##
## This controls when the dialogue window is displayed. If "show", it is always
## displayed. If "hide", it is only displayed when dialogue is present. If
## "auto", the window is hidden before scene statements and shown again once
## dialogue is displayed.
##
## After the game has started, this can be changed with the "window show",
## "window hide", and "window auto" statements.

define config.window = "auto"

## ⚠️ "auto" ESCONDE EL CUADRO EN CADA `scene`, Y ESO SE VE.
##
## config.window_auto_hide trae `scene` adentro por defecto. Combinado con los
## Dissolve(.2) de aca abajo, un `scene` entre dos lineas de dialogo hace que el
## cuadro se funda para afuera y la linea siguiente lo funda para adentro: un
## pestañeo en cada cambio de imagen.
##
## Por eso todo label de contenido con `scene` entre dialogos abre con
## `window show` y cierra con `window hide`. `window show` pone
## _window_auto = False y desactiva el automatismo para todo el tramo (ver
## execute_window_show en renpy/common/000window.rpy).
##
## La contra de fijarlo: el cuadro tampoco se va solo en los intertitulos
## (texto sobre negro). Ahi va un `window hide` explicito antes del `scene
## black`, como en la intro, o queda un cuadro vacio encima.


## Transitions used to show and hide the dialogue window

define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)


## Preference defaults #########################################################

## Controls the default text speed. The default, 0, is infinite, while any
## other number is the number of characters per second to type out.

default preferences.text_cps = 0


## The default auto-forward delay. Larger numbers lead to longer waits, with 0
## to 30 being the valid range.

default preferences.afm_time = 15


## Save directory ##############################################################
##
## Controls the platform-specific place Ren'Py will place the save files for
## this game. The save files will be placed in:
##
## Windows: %APPDATA\RenPy\<config.save_directory>
##
## Macintosh: $HOME/Library/RenPy/<config.save_directory>
##
## Linux: $HOME/.renpy/<config.save_directory>
##
## This generally should not be changed, and if it is, should always be a
## literal string, not an expression.

define config.save_directory = "Japitown-1758721792"


## Icon ########################################################################
##
## The icon displayed on the taskbar or dock.

define config.window_icon = "gui/window_icon.png"


## Build configuration #########################################################
##
## This section controls how Ren'Py turns your project into distribution files.

init python:

    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base directory,
    ## with and without a leading /. If multiple patterns match, the first is
    ## used.
    ##
    ## In a pattern:
    ##
    ## / is the directory separator.
    ##
    ## * matches all characters, except the directory separator.
    ##
    ## ** matches all characters, including the directory separator.
    ##
    ## For example, "*.txt" matches txt files in the base directory,
    ## "game/**.ogg" matches ogg files in the game directory or any of its
    ## subdirectories, and "**.psd" matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## Contenido de desarrollo que no debe viajar en las distribuciones.
    ## NOTA: script/tools/ NO se puede excluir — el HUD referencia nombres
    ## definidos ahí (sistema_pos, modo_posicionamiento, sistema_ajuste_cel).
    build.classify('game/images/test/**', None)      # sprites de prueba

    ## Carpetas de DESARROLLO en la raiz del proyecto. Sin estas reglas viajan
    ## en el zip: la ultima regla por defecto de Ren'Py es ("**", "all")
    ## (renpy/common/00build.rpy), y su exclusion de "*.py" solo mira la raiz,
    ## no las subcarpetas.
    ##
    ## Fue la causa probable de una alerta de antivirus que reporto un jugador
    ## (Trojan:Script/Wacatac.C!ml, Windows Defender, 2026-09-29): `web/` tiene
    ## un script de Python que abre archivos, les inyecta JavaScript y reescribe
    ## zips — el perfil exacto que un clasificador de scripts lee como troyano.
    ## `docs/` ademas llevaba notas internas y spoilers de la narrativa.
    build.classify('docs/**', None)       # documentacion interna
    build.classify('tools/**', None)      # validadores y scripts de mantenimiento
    build.classify('web/**', None)        # parche del index.html del SDK
    build.classify('proxy-reportes/**', None)  # Cloudflare Worker de los reportes

    ## Archivar imágenes en .rpa. En el build web reduce cientos de requests
    ## HTTP sueltos (uno por imagen, on-demand) a unos pocos → muchos menos
    ## puntos de falla de descarga (ver E04 en docs/errores/errores_registro.md). Incluye
    ## .webp porque los sprites (los más numerosos) usan ese formato.
    build.classify('game/**.png', 'archive')
    build.classify('game/**.jpg', 'archive')
    build.classify('game/**.webp', 'archive')

    ## IMPORTANTE: re-excluir los sprites de prueba DESPUÉS del archive. En
    ## Ren'Py la ÚLTIMA regla que matchea un archivo es la que vale, y el
    ## 'archive' de arriba (game/**) los volvería a incluir. Esta regla posterior
    ## gana y los deja fuera de la distribución.
    build.classify('game/images/test/**', None)

    ## Files matching documentation patterns are duplicated in a mac app build,
    ## so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')


## A Google Play license key is required to perform in-app purchases. It can be
## found in the Google Play developer console, under "Monetize" > "Monetization
## Setup" > "Licensing".

# define build.google_play_key = "..."


## The username and project name associated with an itch.io project, separated
## by a slash.

# define build.itch_project = "renpytom/test-project"
