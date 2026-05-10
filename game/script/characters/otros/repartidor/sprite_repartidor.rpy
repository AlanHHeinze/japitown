################################################################################
## Sprites del Repartidor
################################################################################
## Definición visual del repartidor y elementos relacionados

################################################################################
## Layeredimage principal
################################################################################

layeredimage repartidor_parado:
    
    # Cuerpo (único grupo)
    group cuerpo:
        attribute c_base default:
            "images/characters/otros/repartidor/sprite/repartido_parado_cuerpo_base.png"
        attribute c_hablando:
            "images/characters/otros/repartidor/sprite/repartido_parado_cuerpo_hablando.png"


################################################################################
## Idles interactuables
################################################################################

# Repartidor en frente de la casa (mañana de entrega)
image idle_repartidor_puerta = "images/characters/otros/repartidor/idle/idle_repartidor_frentecasa.png"

# Paquete en la habitación del MC (entrega perdida)
image idle_paquete_hmc = "images/characters/otros/repartidor/idle/idle_paquete_hmc.png"
