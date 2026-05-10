################################################################################
## Sistema de Elementos Posicionables
################################################################################
## Permite registrar cualquier imagen del juego como "elemento posicionable"
## con propiedades de grupo y estado editable, para operar con la herramienta
## de posicionamiento (pestaña "Otros").
##
## GRUPOS ESTÁNDAR RECOMENDADOS:
##   "npc_sprite"      — sprites de NPCs en locaciones
##   "idle"            — personajes/objetos estáticos (repartidor, paquete, etc.)
##   "quest_elemento"  — elementos interactivos de quests
##   "prop"            — props de escena no interactivos
##   "efecto"          — overlays y efectos visuales
##   "ui"              — elementos de interfaz posicionables
##
## CONVENCIÓN DE IDs:
##   Formato: {locacion}_{elemento}_{variante}
##   Ejemplos: "casa_frente_repartidor", "casa_hmc_paquete", "sala_sillon_quest1"
##
## USO:
##   init python:
##       sistema_pos.registrar(
##           id="casa_frente_repartidor",
##           imagen="images/characters/repartidor/idle_puerta.png",
##           nombre="Repartidor - Frente de casa",
##           grupo="idle",
##           x=1270, y=540,
##           xanchor=0.5, yanchor=1.0
##       )
################################################################################

init -5 python:

    class ElementoPosicionable:
        """
        Representa un elemento del juego que puede ser posicionado
        con la herramienta de posicionamiento.

        Atributos:
            id          — Identificador único. Formato: {locacion}_{elemento}_{variante}
            imagen      — Path de la imagen (relativo a game/)
            nombre      — Nombre descriptivo para mostrar en la herramienta
            grupo       — Grupo al que pertenece (npc_sprite, idle, quest_elemento, prop, efecto, ui)
            x, y        — Posición actual del punto de anclaje en píxeles
            xanchor     — Anclaje horizontal (0.0=izquierda, 0.5=centro, 1.0=derecha)
            yanchor     — Anclaje vertical   (0.0=arriba,    0.5=centro, 1.0=abajo)
            editable    — Si puede ser movido por la herramienta
            x_original  — Posición original antes de modificar en la sesión
            y_original  — Posición original antes de modificar en la sesión
        """
        def __init__(self, id, imagen, nombre, grupo, x, y, xanchor=0.5, yanchor=1.0, editable=True, screen=""):
            self.id = id
            self.imagen = imagen
            self.nombre = nombre
            self.grupo = grupo
            self.screen = screen
            self.x = x
            self.y = y
            self.xanchor = xanchor
            self.yanchor = yanchor
            self.editable = editable
            # Snapshot de posición original para mostrar "antes" en el export
            self.x_original = x
            self.y_original = y

        def resetear_original(self):
            """Actualiza el snapshot de posición original (ej: al abrir herramienta)."""
            self.x_original = self.x
            self.y_original = self.y

        def fue_modificado(self):
            """Retorna True si la posición fue cambiada respecto al original."""
            return self.x != self.x_original or self.y != self.y_original

        def __repr__(self):
            return "ElementoPosicionable(id={}, grupo={}, x={}, y={})".format(
                self.id, self.grupo, self.x, self.y)


    class SistemaPosicionamiento:
        """
        Registro central de todos los elementos posicionables del juego.
        Permite registrar, consultar y actualizar posiciones de imágenes.
        """

        GRUPOS_VALIDOS = ["npc_sprite", "idle", "quest_elemento", "prop", "efecto", "ui"]

        def __init__(self):
            self.elementos = {}  # {id: ElementoPosicionable}

        def registrar(self, id, imagen, nombre, grupo, x, y, xanchor=0.5, yanchor=1.0, editable=True, screen=""):
            """
            Registra un elemento posicionable en el sistema.
            Si ya existe un elemento con el mismo ID, actualiza sus datos.

            Args:
                id       — ID único del elemento (formato: {locacion}_{elemento}_{variante})
                imagen   — Path de la imagen relativo a game/
                nombre   — Nombre descriptivo
                grupo    — Grupo del elemento (ver GRUPOS_VALIDOS)
                x, y     — Posición del punto de anclaje en píxeles
                xanchor  — Anclaje horizontal (0.0–1.0)
                yanchor  — Anclaje vertical   (0.0–1.0)
                editable — Si puede ser movido por la herramienta
                screen   — Nombre del screen de Ren'Py donde se usa este elemento
            """
            if id in self.elementos:
                # Actualizar datos sin perder snapshot si ya existe
                elem = self.elementos[id]
                elem.imagen = imagen
                elem.nombre = nombre
                elem.grupo = grupo
                elem.screen = screen
                elem.xanchor = xanchor
                elem.yanchor = yanchor
                elem.editable = editable
                # No actualizar x,y para preservar cambios hechos en sesión
            else:
                self.elementos[id] = ElementoPosicionable(
                    id=id, imagen=imagen, nombre=nombre, grupo=grupo,
                    x=x, y=y, xanchor=xanchor, yanchor=yanchor, editable=editable,
                    screen=screen
                )

        def obtener(self, id):
            """Retorna el ElementoPosicionable con ese ID, o None si no existe."""
            return self.elementos.get(id, None)

        def obtener_por_grupo(self, grupo):
            """Retorna lista de elementos editables del grupo especificado."""
            return [e for e in self.elementos.values() if e.grupo == grupo and e.editable]

        def obtener_grupos_disponibles(self):
            """Retorna lista de grupos únicos que tienen al menos un elemento editable."""
            grupos = set()
            for e in self.elementos.values():
                if e.editable:
                    grupos.add(e.grupo)
            return sorted(list(grupos))

        def obtener_por_screen(self, screen):
            """Retorna lista de elementos editables del screen especificado."""
            return [e for e in self.elementos.values() if e.screen == screen and e.editable]

        def obtener_screens_disponibles(self):
            """Retorna lista de screens únicos que tienen al menos un elemento editable."""
            screens = set()
            for e in self.elementos.values():
                if e.editable and e.screen:
                    screens.add(e.screen)
            return sorted(list(screens))

        def todos_editables(self):
            """Retorna lista de todos los elementos con editable=True."""
            return [e for e in self.elementos.values() if e.editable]

        def actualizar_posicion(self, id, x, y):
            """Actualiza la posición (punto de anclaje) de un elemento."""
            elem = self.elementos.get(id)
            if elem:
                elem.x = x
                elem.y = y

        def tomar_snapshot(self):
            """
            Actualiza el snapshot 'original' de todos los elementos.
            Llamar al abrir la herramienta para registrar el estado inicial.
            """
            for elem in self.elementos.values():
                elem.resetear_original()

        def elementos_modificados(self):
            """Retorna lista de elementos cuya posición fue cambiada en la sesión."""
            return [e for e in self.elementos.values() if e.fue_modificado()]

        def __repr__(self):
            return "SistemaPosicionamiento({} elementos)".format(len(self.elementos))


# 'define' corre en init priority 0 (después de las clases en -5, antes de los
# registros en init 1). A diferencia de 'default', no se guarda en el savefile.
define sistema_pos = SistemaPosicionamiento()


################################################################################
## Registros de elementos posicionables del juego
################################################################################
## Agregar acá los elementos que deben ser editables con la herramienta.
## Convención de IDs: {locacion}_{elemento}_{variante}
##
## IMPORTANTE: el par (x, y) debe ser el punto de ANCLAJE del elemento,
## es decir, la posición tal como se usa en el código del juego.
## xanchor=0.0 yanchor=0.0 → x,y es la esquina superior-izquierda (top-left)
## xanchor=0.5 yanchor=1.0 → x,y es el centro-inferior (sprites de NPC)
################################################################################

init 1 python:

    # ── Idles del repartidor ─────────────────────────────────────────────────
    # Repartidor parado frente a la casa (mañana de entrega)
    sistema_pos.registrar(
        id="casa_frente_repartidor",
        imagen="images/characters/otros/repartidor/idle/idle_repartidor_frentecasa.png",
        nombre="Repartidor - Frente de casa",
        grupo="idle",
        screen="elementos_escena",
        x=1270, y=540,
        xanchor=0.0, yanchor=0.0  # top-left (igual al comportamiento original)
    )

    # Paquete en la habitación del MC (entrega perdida)
    sistema_pos.registrar(
        id="casa_hmc_paquete",
        imagen="images/characters/otros/repartidor/idle/idle_paquete_hmc.png",
        nombre="Paquete - Habitación MC",
        grupo="idle",
        screen="elementos_escena",
        x=1000, y=530,
        xanchor=0.0, yanchor=0.0  # top-left (igual al comportamiento original)
    )

    # ── Violet Quest 01 — Limpieza del Living ────────────────────────────────
    # Todos usan xanchor=0.5 yanchor=1.0 (centro-inferior), igual que los imagebuttons del screen.
    # Los valores de x,y provienen de los defaults originales del screen.

    sistema_pos.registrar(
        id="casa_living_chimenea_vq2",
        imagen="images/quest/violet/quest1/violet_quest01_interaccion_chimenea.png",
        nombre="Chimenea - Limpieza VQ2",
        grupo="quest_elemento",
        screen="limpieza_quest2_violet",
        x=1361, y=876,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="casa_living_escalera_vq2",
        imagen="images/quest/violet/quest1/violet_quest01_interaccion_escalera.png",
        nombre="Escalera - Limpieza VQ2",
        grupo="quest_elemento",
        screen="limpieza_quest2_violet",
        x=281, y=964,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="casa_living_sillon_vq2",
        imagen="images/quest/violet/quest1/violet_quest01_interaccion_sillon.png",
        nombre="Sillon - Limpieza VQ2",
        grupo="quest_elemento",
        screen="limpieza_quest2_violet",
        x=880, y=1024,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="casa_cocina_alacena_vq2",
        imagen="images/quest/violet/quest1/violet_quest01_interaccion_alacena.png",
        nombre="Alacena - Buscar trapeador VQ2",
        grupo="quest_elemento",
        screen="buscar_trapeador_quest2_violet",
        x=651, y=795,  # 20/02/2026 12:04
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="casa_pasilloarriba_violet_barriendo_vq2",
        imagen="images/quest/violet/quest1/violet_quest01_violetbarriendo.png",
        nombre="Violet barriendo - Pasillo VQ2",
        grupo="quest_elemento",
        screen="limpieza_quest2_violet",
        x=881, y=987,
        xanchor=0.5, yanchor=1.0
    )

    # ── Violet Quest 04 — Solo en casa ────────────────────────────────────────

    # Sillon en el living (misma posicion que quest 3)
    sistema_pos.registrar(
        id="casa_living_sillon_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccionsillon.png",
        nombre="Sillon - Living VQ4",
        grupo="quest_elemento",
        screen="vq4_sillon_living",
        x=880, y=1024,
        xanchor=0.5, yanchor=1.0
    )

    # Habitacion de Violet — elementos explorables
    sistema_pos.registrar(
        id="hviolet_cajonera_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_cajonera.png",
        nombre="Cajonera - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=234, y=1080,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_compu_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_compu.png",
        nombre="Compu - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=1636, y=775,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_mangas_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_mangas.png",
        nombre="Mangas - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=1680, y=496,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_mochila_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_mochila.png",
        nombre="Mochila - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=1249, y=896,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_muñecos_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_muñecos.png",
        nombre="Muñecos - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=1867, y=812,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_peluches_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_peluches.png",
        nombre="Peluches - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=830, y=767,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_ropero_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_ropero.png",
        nombre="Ropero - H.Violet VQ4",
        grupo="quest_elemento",
        screen="vq4_habitacion_violet",
        x=234, y=908,
        xanchor=0.5, yanchor=1.0
    )

    # Ropero — elementos internos
    sistema_pos.registrar(
        id="hviolet_ropero_caja_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_caja.png",
        nombre="Caja - Ropero VQ4",
        grupo="quest_elemento",
        screen="vq4_screen_ropero",
        x=1185, y=1078,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_ropero_pijama_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_pijama.png",
        nombre="Pijama - Ropero VQ4",
        grupo="quest_elemento",
        screen="vq4_screen_ropero",
        x=821, y=824,
        xanchor=0.5, yanchor=1.0
    )

    # Cajonera — elementos internos
    sistema_pos.registrar(
        id="hviolet_cajonera_grande_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_grande.png",
        nombre="Grande - Cajonera VQ4",
        grupo="quest_elemento",
        screen="vq4_screen_cajonera",
        x=816, y=491,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_cajonera_normal_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_normal.png",
        nombre="Normal - Cajonera VQ4",
        grupo="quest_elemento",
        screen="vq4_screen_cajonera",
        x=338, y=482,
        xanchor=0.5, yanchor=1.0
    )

    sistema_pos.registrar(
        id="hviolet_cajonera_tanga_vq4",
        imagen="images/quest/violet/quest4/violet_quest04_interaccion_tanga.png",
        nombre="Tanga - Cajonera VQ4",
        grupo="quest_elemento",
        screen="vq4_screen_cajonera",
        x=507, y=879,
        xanchor=0.5, yanchor=1.0
    )
