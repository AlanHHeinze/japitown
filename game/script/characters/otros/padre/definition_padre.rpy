################################################################################
## Definición del Padre
################################################################################
## Personaje de la intro — aparece en el aeropuerto

################################################################################
## Character Definition
################################################################################

define padre = Character("Papá", color="#c8a96e")
define terminal_micros = Character("Terminal", color="#aaaaaa", what_prefix="{i}", what_suffix="{/i}")
define vozoff = Character(None, what_prefix="{i}{color=#c8c8c8}", what_suffix="{/color}{/i}")

################################################################################
## Layeredimage principal
################################################################################

layeredimage padre_intro:

    # Dimensiones (escala base, siempre visible)
    group dimensiones:
        attribute ddimensiones default:
            "images/intro/characters/padre/intro_padre_dimensiones.png"

    # Cabeza
    group cabeza:
        attribute cabase default:
            "images/intro/characters/padre/padre_intro_cabeza_base.png"

    # Cuerpo — grupo marcador, siempre cbase (sin imagen propia)
    group cuerpo:
        attribute cbase default:
            Null()

    # Ojos
    group ojos:
        attribute omirando default:
            "images/intro/characters/padre/padre_intro_ojos_mirando.png"
        attribute onone:
            Null()

    # Boca
    group boca:
        attribute bnone default:
            Null()
        attribute bhablando:
            "images/intro/characters/padre/padre_intro_boca_hablando.png"

    # Pose corporal (el cuerpo visible real)
    group pose:
        attribute pbase default:
            "images/intro/characters/padre/padre_intro_cuerpo_base.png"
        attribute pbrazoscruzados:
            "images/intro/characters/padre/padre_intro_cuerpo_brazoscruzados.png"
        attribute ptarjeta:
            "images/intro/characters/padre/padre_intro_cuerpo_tarjeta.png"
