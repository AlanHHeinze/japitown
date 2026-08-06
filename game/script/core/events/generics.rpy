################################################################################
## Eventos genéricos
################################################################################
## Escenas e imágenes reutilizables que pueden dispararse desde varios contextos
## (quests, eventos, rutinas) sin duplicar assets.

# =============================================================================
# EVENTO GENÉRICO — Ducha de noche
# =============================================================================
# Fondo nocturno de la ducha + dos capas superiores (vapor/vidrio) que se
# superponen sobre el fondo: una normal y una más densa.
# Las capas son WebP (tienen alpha); el fondo es JPG (full-frame sin transparencia).
image ducha_gen_noche       = "images/eventos/ducha/ducha_generica_noche.jpg"
image ducha_gen_capa_normal = "images/eventos/ducha/capa_superior_normal.webp"
image ducha_gen_capa_densa  = "images/eventos/ducha/capa_superior_densa.webp"

# Secuencias del agua cayendo — un solo grupo por secuencia para pasar de un
# frame al siguiente sin hide ni reposicionar.
# Uso: show ducha_gen_agua_adelante f1 / show ducha_gen_agua_adelante f2 ...
layeredimage ducha_gen_agua_adelante:
    group secuencia:
        attribute f1 default:
            "images/eventos/ducha/ducha_secuencia_agua_adelante1.webp"
        attribute f2:
            "images/eventos/ducha/ducha_secuencia_agua_adelante2.webp"
        attribute f3:
            "images/eventos/ducha/ducha_secuencia_agua_adelante3.webp"
        attribute f4:
            "images/eventos/ducha/ducha_secuencia_agua_adelante4.webp"
        attribute f5:
            "images/eventos/ducha/ducha_secuencia_agua_adelante5.webp"
        attribute f6:
            "images/eventos/ducha/ducha_secuencia_agua_adelante6.webp"
        attribute f7:
            "images/eventos/ducha/ducha_secuencia_agua_adelante7.webp"
        attribute f8:
            "images/eventos/ducha/ducha_secuencia_agua_adelante8.webp"
        attribute f9:
            "images/eventos/ducha/ducha_secuencia_agua_adelante9.webp"

layeredimage ducha_gen_agua_atras:
    group secuencia:
        attribute f1 default:
            "images/eventos/ducha/ducha_secuencia_agua_atras1.webp"
        attribute f2:
            "images/eventos/ducha/ducha_secuencia_agua_atras2.webp"
        attribute f3:
            "images/eventos/ducha/ducha_secuencia_agua_atras3.webp"
        attribute f4:
            "images/eventos/ducha/ducha_secuencia_agua_atras4.webp"
        attribute f5:
            "images/eventos/ducha/ducha_secuencia_agua_atras5.webp"
        attribute f6:
            "images/eventos/ducha/ducha_secuencia_agua_atras6.webp"
        attribute f7:
            "images/eventos/ducha/ducha_secuencia_agua_atras7.webp"
        attribute f8:
            "images/eventos/ducha/ducha_secuencia_agua_atras8.webp"
        attribute f9:
            "images/eventos/ducha/ducha_secuencia_agua_atras9.webp"


# Animaciones automáticas en loop para las capas de agua (50% transparencia, rápidas)
# Primarias: columna derecha
image ducha_agua_atras_animado = Transform(
    Animation(
        "images/eventos/ducha/ducha_secuencia_agua_atras1.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras2.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras3.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras4.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras5.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras6.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras7.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras8.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras9.webp", 0.05,
        loop=True
    ),
    alpha=0.3
)

image ducha_agua_adelante_animado = Transform(
    Animation(
        "images/eventos/ducha/ducha_secuencia_agua_adelante1.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante2.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante3.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante4.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante5.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante6.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante7.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante8.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante9.webp", 0.05,
        loop=True
    ),
    alpha=0.3
)

# Alternadas: columna izquierda (300px a la izquierda, comienzan en frame diferente para desincronización)
image ducha_agua_atras_animado_alt = Transform(
    Animation(
        "images/eventos/ducha/ducha_secuencia_agua_atras5.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras6.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras7.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras8.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras9.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras1.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras2.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras3.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_atras4.webp", 0.05,
        loop=True
    ),
    alpha=0.3, xoffset=-200
)

image ducha_agua_adelante_animado_alt = Transform(
    Animation(
        "images/eventos/ducha/ducha_secuencia_agua_adelante5.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante6.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante7.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante8.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante9.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante1.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante2.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante3.webp", 0.05,
        "images/eventos/ducha/ducha_secuencia_agua_adelante4.webp", 0.05,
        loop=True
    ),
    alpha=0.3, xoffset=-200
)
