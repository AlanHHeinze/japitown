################################################################################
## COMPATIBILIDAD DE PARTIDAS ENTRE VERSIONES
################################################################################
##
##   ⇩⇩⇩  LO ÚNICO QUE HAY QUE TOCAR AL SACAR UNA VERSIÓN ESTÁ ABAJO  ⇩⇩⇩
##             (buscá JP_HISTORIAL_SAVES, unas lineas mas abajo)
##
## Antes de cada actualizacion se decide UNA cosa: si rompe las partidas de la
## version anterior o no. Esa decision se declara agregando una fila al
## historial, con True o False. No hay ningun contador que llevar ni ningun
## numero que recordar.
##
## De ese historial se deriva la "generacion de guardado" de cada version:
##
##     Dos partidas son compatibles si y solo si tienen la MISMA generacion.
##
## Cada True del historial arranca una generacion nueva. Los False se suman a la
## generacion en curso.
##
################################################################################
## CUÁNDO PONER True Y CUÁNDO False
################################################################################
##
## ⚠️ True ES IRREVERSIBLE PARA EL JUGADOR: pierde el acceso a sus partidas.
## Ante la duda va False: es peor romper partidas de gente que dejar pasar una
## incompatibilidad menor, que ademas el merge de `persistencia_sistemas.rpy`
## suele absorber solo.
##
## Va True cuando cargar un save viejo dejaria el juego roto o incoherente:
##   - Se renombro o se borro una variable `default` que el contenido lee.
##   - Cambio la forma de un objeto guardado (campos de Quest, NPC, sistemas).
##   - Cambio el SIGNIFICADO de un valor existente (un stat que pasa de 0-100 a
##     0-35, un id de quest reutilizado para otra cosa).
##   - Se reordenaron etapas de una quest y una partida a mitad de camino
##     quedaria en un estado que ya no existe.
##
## Va False para todo lo demas:
##   - Contenido nuevo: quests, eventos, ventajas, dialogos, imagenes.
##     `persistencia_sistemas.rpy` ya mergea el contenido nuevo hacia los saves
##     viejos en after_load.
##   - Fixes de logica que no tocan datos guardados.
##   - Cambios de UI, traducciones, assets.
##
################################################################################


################################################################################
## EL HISTORIAL — una fila por version publicada
################################################################################
## Formato:  ("version tal cual config.version",  rompe_saves)
##
##     False = los saves de la version anterior SIGUEN sirviendo
##     True  = los saves de todas las versiones anteriores dejan de servir
##
## Se agrega al FINAL, en orden de publicacion. La version que figure en
## `config.version` (ui/base/options.rpy) tiene que estar en esta lista: si no
## esta, el juego no arranca en modo desarrollo y avisa cual falta.
##
## La primera fila es la version en la que se instalo este sistema. Las partidas
## anteriores a el no tienen marca de generacion y se cuentan como pertenecientes
## a esa primera generacion — o sea que hoy siguen andando, y van a romper recien
## cuando pongas el primer True.

## (El -100 es prioridad de init: el historial tiene que existir antes del
## `init -50` que deriva la generacion. No cambia nada de como se edita.)
define -100 JP_HISTORIAL_SAVES = [
    ("0.1.8.5", False),   # primera version con el sistema
    ("0.1.9",   True),    # ROMPE: no carga partidas de ninguna version anterior
    ("0.1.9a",  False),   # soft lock de Mensajear, saneo al cargar, viaje rapido con recorrido; saves de 0.1.9 siguen
    ("0.1.9.1", False),   # controlador de quests, punto de activacion, deseo 30 partida (migra sola), tinte por horario, dormir recorre horarios; todo se lee con getattr y las quests nuevas entran por merge
]

## Ejemplo de como se veria despues de unas cuantas versiones:
##
##     define JP_HISTORIAL_SAVES = [
##         ("0.1.8.5", False),
##         ("0.1.9",   True),    # cambio el formato de los hitos
##         ("0.1.9a",  False),   # solo fixes
##         ("0.1.9b",  True),    # renombre variables de quest
##     ]
##
## Ahi 0.1.8.5 es generacion 1, 0.1.9 y 0.1.9a son generacion 2, y 0.1.9b es 3.
## Los saves de 0.1.9 y 0.1.9a se cargan entre si; los de 0.1.9b con ninguno.


################################################################################
## Derivacion de la generacion
################################################################################
## De aca para abajo no hay nada que tocar al sacar una version.

init -50 python:

    def _jp_calcular_generacion():
        """
        Cuenta generaciones recorriendo el historial hasta config.version.

        Devuelve (generacion, version_encontrada). La generacion arranca en 1 y
        sube con cada True, incluido el de la propia version en curso.
        """
        gen = 1
        for version, rompe in JP_HISTORIAL_SAVES:
            if rompe:
                gen += 1
            if version == config.version:
                return gen, True
        return gen, False

    JP_SAVE_GEN, _jp_version_en_historial = _jp_calcular_generacion()

    # Si `config.version` no figura en el historial no se puede saber que
    # generacion le toca, y el riesgo es serio: una version que rompe saves
    # saldria tratando las partidas viejas como validas.
    #
    # Revienta SOLO en desarrollo (config.developer es False en un build), asi
    # que olvidarse de la fila es imposible para vos y no puede afectar a un
    # jugador. Ren'Py muestra el mensaje en la pantalla de error de arranque.
    if not _jp_version_en_historial and config.developer:
        raise Exception(
            u"compatibilidad_saves.rpy: config.version = %r no esta en "
            u"JP_HISTORIAL_SAVES. Agregale una fila con True (si esta version "
            u"rompe los saves de la anterior) o False (si no)." % (config.version,)
        )


################################################################################
## COMO FUNCIONA
################################################################################
## La generacion se graba en DOS lados, porque cada uno cubre un caso:
##
## 1. En el JSON del save (config.save_json_callbacks). Se puede leer SIN cargar
##    la partida, asi que es lo que usa la pantalla de Cargar para deshabilitar
##    los slots incompatibles antes de que el jugador los toque.
##
## 2. En la variable `jp_gen_partida` de la propia partida. Es la red de
##    seguridad: cubre las vias de carga que no pasan por la pantalla (carga
##    rapida, sync, cualquier cosa futura). Se chequea en `after_load`.


# Generacion con la que se creo la partida en curso.
#
# El default es 1 LITERAL, no JP_SAVE_GEN: la generacion 1 es "todo lo anterior
# al sistema". Un save viejo no trae la variable, Ren'Py le aplica este default
# al cargarlo, y asi queda contado como generacion 1 — que es lo correcto: hoy
# tiene que seguir andando, y va a romper recien con el primer True del
# historial.
#
# Si dijera JP_SAVE_GEN, un save viejo cargado en una version futura adoptaria
# la generacion actual y pasaria el control sin ser compatible de verdad.
#
# Para las partidas NUEVAS lo pisa `label start` (intro_main.rpy) con la
# generacion real de la version que las creo.
default jp_gen_partida = 1


# Texto del aviso de partida incompatible. Con `default` por la misma razon que
# `_nc_nombre` (S08): si el bloque python que lo arma fallara, el jugador toca
# "Ignore", la ejecucion sigue en la linea de abajo y el `centered "[_jp_aviso]"`
# reventaria con NameError — un segundo error encima del primero. Paso de
# verdad: el KeyError de S15 dejo la variable sin asignar y el NameError llego
# 12 segundos despues (S15, evento 6147d11c). El valor de aca es un fallback
# plano: sin tags y sin placeholder, o sea que no puede fallar al mostrarse.
default _jp_aviso = u"Partida incompatible: fue creada con una versión anterior de Japitown."


init python:

    def _jp_stamp_save(d):
        """Graba la generacion en el JSON del slot, junto al resto de metadata."""
        d["jp_save_gen"] = JP_SAVE_GEN

    config.save_json_callbacks.append(_jp_stamp_save)


################################################################################
## Consultas
################################################################################

init python:

    def jp_slot_gen(slot):
        """
        Generacion de un slot, sin cargarlo. None si el slot esta vacio.

        Lee el JSON del save, que Ren'Py cachea (loadsave.get_cache), asi que es
        barato llamarlo desde una screen en cada re-render.

        `missing=1` por lo mismo que el default de jp_gen_partida: un save
        anterior a este sistema no tiene el campo y es generacion 1.
        """
        return FileJson(slot, "jp_save_gen", empty=None, missing=1)

    def jp_slot_compatible(slot):
        """True si el slot se puede cargar con esta version. Vacio = True."""
        gen = jp_slot_gen(slot)
        return (gen is None) or (gen == JP_SAVE_GEN)

    def jp_slot_version(slot):
        """config.version con la que se creo el slot, para mostrarla."""
        return FileJson(slot, "_version", empty=None, missing="?")

    def jp_partida_compatible():
        """
        True si la partida CARGADA es de esta generacion.

        Se llama desde `after_load`. Usa getattr y no la variable directa porque
        en un save viejo puede no existir todavia en el momento del chequeo.
        """
        return getattr(store, "jp_gen_partida", 1) == JP_SAVE_GEN


################################################################################
## Red de seguridad al cargar
################################################################################
## Lo llama `label after_load` (intro_main.rpy). Si la partida es de otra
## generacion ya esta cargada — no hay forma de abortar una carga a mitad de
## camino — asi que se avisa y se vuelve al menu principal con full_restart(),
## que descarta el estado cargado por completo.

label jp_save_incompatible:

    scene black with fade

    # renpy.translate_string y NO un literal traducible: el mensaje lleva
    # config.version interpolado, y en un `centered "..."` con placeholder la
    # traduccion se buscaria sobre el literal crudo y saldria en español igual
    # (mismo caso que los mensajes de despertar_system.rpy). El `old`/`new` de
    # la plantilla vive en tl/english/compatibilidad_saves_strings.rpy y debe
    # conservar el {version}.
    #
    # ⚠️ .replace() Y NO .format(): el texto lleva tags de Ren'Py ({size=+8},
    # {/size}) y str.format los lee como campos → KeyError: 'size=+8', en los
    # dos idiomas. O sea que este aviso NUNCA se mostro: el jugador que caia
    # aca veia la pantalla de error en vez del mensaje (Sentry S15, 2026-09-19).
    # Escapar las llaves obligaria a tocar el `old` de la traduccion; replace
    # no le pide nada al texto.
    python:
        _jp_aviso = renpy.translate_string(
            u"{size=+8}Partida incompatible{/size}\n\nEsta partida fue creada "
            u"con una versión anterior de Japitown y no se puede continuar en "
            u"la versión actual ({version}).\n\nTus partidas anteriores siguen "
            u"en el disco: si quieres retomarlas, puedes volver a instalar la "
            u"versión con la que las creaste."
        ).replace(u"{version}", unicode(config.version) if str is bytes else str(config.version))

    centered "[_jp_aviso]"

    # Descarta por completo el estado cargado y vuelve al menu principal.
    $ renpy.full_restart()
