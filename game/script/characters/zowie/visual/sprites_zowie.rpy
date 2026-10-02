################################################################################
## Sprites de Zowie
################################################################################
## Un solo layeredimage: `zowie_parada`.
##
## COMO SE USA — igual que el MC, Violet y Leah: el cuerpo se deja puesto y la
## boca se prende y se apaga alrededor de cada linea.
##
##     show zowie_parada c_rbase_saludando at right with sprite_normal
##     show zowie_parada b_hablando
##     zowie "¡Hola!"
##     show zowie_parada b_none
##
## LOS GRUPOS VAN EN ORDEN DE DIBUJO: `cuerpo` primero y `boca` despues, asi la
## boca queda ENCIMA. Invertirlos la esconde detras del cuerpo.
##
## HOY NO HAY GRUPO DE OJOS: los cuerpos ya traen la cara. Cuando existan los
## assets, el grupo `ojos` va entre `cuerpo` y `boca`, con `o_none` de default
## para no romper los `show` ya escritos.
##
## OJO — Zowie NO tiene la pose `idea` que si tiene Leah: son cuatro cuerpos,
## no cinco. Si una escena la necesita, hay que pedir el asset.
##
## EL PREFIJO `c_rbase_` es la ropa: "rbase" = ropa base, la misma convencion
## que el MC (`c_rbase_celular`) y Violet (`c_pijama_base`). Cuando Zowie tenga
## otro conjunto, entra como `c_<ropa>_<pose>` en este mismo grupo.
##
## Assets: game/images/characters/amigas/zowie/ — WebP con alpha, 600x1080.
################################################################################

layeredimage zowie_parada:

    # Cuerpo (incluye cabeza y cara)
    group cuerpo:
        attribute c_rbase_base default:
            "images/characters/amigas/zowie/zowie_rbase_cuerpo_base.webp"
        attribute c_rbase_brazoscruzados:
            "images/characters/amigas/zowie/zowie_rbase_cuerpo_brazoscruzados.webp"
        attribute c_rbase_pensando:
            "images/characters/amigas/zowie/zowie_rbase_cuerpo_pensando.webp"
        attribute c_rbase_saludando:
            "images/characters/amigas/zowie/zowie_rbase_cuerpo_saludando.webp"

    # Boca — `b_none` por defecto: el cuerpo ya trae la boca cerrada, y
    # `b_hablando` se superpone solo mientras dice una linea.
    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/characters/amigas/zowie/zowie_rbase_boca_hablando.webp"
