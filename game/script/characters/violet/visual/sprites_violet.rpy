################################################################################
## Sprites de Violet
################################################################################
## Definición de sprites para el personaje Violet

################################################################################
## Layeredimage: violet_parada
################################################################################

layeredimage violet_parada:
    # Area
    group area:
        attribute a_base default:
            "images/characters/casa/violet/violet_parada_area.webp"
        attribute a_none:
            Null()
    
    # Cabeza
    group cabeza:
        attribute ca_base default:
            "images/characters/casa/violet/violet_parada_cabeza_rbase.webp"
        attribute ca_pijama:
            "images/characters/casa/violet/violet_parada_cabeza_pijama.webp"
        attribute ca_none:
            Null()

    # Cuerpo completo — sprites que YA incluyen cabeza/cara (ej: cosplay eva).
    # Va ANTES de boca/ojos para dibujarse DEBAJO de ellos, asi las expresiones
    # faciales (boca/ojos) siguen siendo visibles encima del sprite.
    # Usar con c_none (cuerpo base en Null) y ca_none (cabeza base en Null).
    group cuerpocompleto:
        attribute cc_none default:
            Null()
        attribute cc_eva_base:
            "images/characters/casa/violet/violet_parada_cuerpo_eva_base.webp"

    # Boca
    group boca:
        attribute b_aburrida default:
            "images/characters/casa/violet/violet_parada_boca_aburrida.webp"
        attribute b_bostezogrande:
            "images/characters/casa/violet/violet_parada_boca_bostezogrande.webp"
        attribute b_abiertachica:
            "images/characters/casa/violet/violet_parada_boca_abiertachica.webp"
        attribute b_cerradachica:
            "images/characters/casa/violet/violet_parada_boca_cerradachica.webp"
        attribute b_contenta:
            "images/characters/casa/violet/violet_parada_boca_contenta.webp"
        attribute b_feliz:
            "images/characters/casa/violet/violet_parada_boca_feliz.webp"
        attribute b_gritandomucho:
            "images/characters/casa/violet/violet_parada_boca_gritandomucho.webp"
        attribute b_hablando:
            "images/characters/casa/violet/violet_parada_boca_hablando.webp"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_hablandochica.webp"
        attribute b_mordiendo:
            "images/characters/casa/violet/violet_parada_boca_mordiendo.webp"
        attribute b_sexy:
            "images/characters/casa/violet/violet_parada_boca_sexy.webp"
        attribute b_sonrisacerrada:
            "images/characters/casa/violet/violet_parada_boca_sonrisacerrada.webp"
        attribute b_sonrisacostado:
            "images/characters/casa/violet/violet_parada_boca_sonrisacostado.webp"
        attribute b_sonrisaleve:
            "images/characters/casa/violet/violet_parada_boca_sonrisaleve.webp"
        attribute b_sonrisapequeña:
            "images/characters/casa/violet/violet_parada_boca_sonrisapequena.webp"
        attribute b_triste:
            "images/characters/casa/violet/violet_parada_boca_triste.webp"
        attribute b_none:
            Null()
    
    # Ojos
    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_base.webp"
        attribute o_bostezograndenm:
            "images/characters/casa/violet/violet_parada_ojos_bostezograndenm.webp"
        attribute o_abajonm:
            "images/characters/casa/violet/violet_parada_ojos_abajonm.webp"
        attribute o_abiertos:
            "images/characters/casa/violet/violet_parada_ojos_abiertos.webp"
        attribute o_arribanm:
            "images/characters/casa/violet/violet_parada_ojos_arribanm.webp"
        attribute o_cerrados:
            "images/characters/casa/violet/violet_parada_ojos_cerrados.webp"
        attribute o_felicesnm:
            "images/characters/casa/violet/violet_parada_ojos_felicesnm.webp"
        attribute o_dormidos:
            "images/characters/casa/violet/violet_parada_ojos_dormidos.webp"
        attribute o_enojados:
            "images/characters/casa/violet/violet_parada_ojos_enojados.webp"
        attribute o_felices:
            "images/characters/casa/violet/violet_parada_ojos_felices.webp"
        attribute o_guiñando:
            "images/characters/casa/violet/violet_parada_ojos_guinando.webp"
        attribute o_juzgandonm:
            "images/characters/casa/violet/violet_parada_ojos_juzgandonm.webp"
        attribute o_llorandomuchonm:
            "images/characters/casa/violet/violet_parada_ojos_llorandomuchonm.webp"
        attribute o_sexys:
            "images/characters/casa/violet/violet_parada_ojos_sexys.webp"
        attribute o_tristes:
            "images/characters/casa/violet/violet_parada_ojos_tristes.webp"
        attribute o_pensando:
            "images/characters/casa/violet/violet_parada_ojos_pensando.webp"
        attribute o_costadobase:
            "images/characters/casa/violet/violet_parada_ojos_costadobase.webp"
        attribute o_none:
            Null()
    
    # Cuerpo
    group cuerpo:
        attribute c_rbase_base default:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_base.webp"
        attribute c_rbase_brazoscruzados:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_brazoscruzados.webp"
        attribute c_rbase_celu:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_celu.webp"
        attribute c_rbase_chek:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_chek.webp"
        attribute c_rbase_cola:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cola.webp"
        attribute c_rbase_dedolabio:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_dedolabio.webp"
        attribute c_rbase_enojada:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_enojada.webp"
        attribute c_rbase_fuckyou:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_fuckyou.webp"
        attribute c_rbase_gestito:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_gestito.webp"
        attribute c_rbase_idea:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_idea.webp"
        attribute c_rbase_live:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_live.webp"
        attribute c_rbase_notok:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_notok.webp"
        attribute c_rbase_ok:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_ok.webp"
        attribute c_rbase_paz:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_paz.webp"
        attribute c_rbase_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_pensando.webp"
        attribute c_rbase_señalando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_senalando.webp"
        attribute c_rbase_sorprendido:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_sorprendida.webp"
        attribute c_rbase_tetas:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_tetas.webp"
        attribute c_rbase_verguenza:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_verguenza.webp"
        attribute c_rbase_victoria:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_victoria.webp"
        attribute c_rbase_regalo:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cajaregalo.webp"
        attribute c_rbase_cajacosplay:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cajacoxplay.webp"
        attribute c_rbase_saludando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_saludando.webp"
        attribute c_rbase_mangas:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_mangas.webp"
        attribute c_rbase_bolsamadera:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_bolsamadera.webp"

        # Pijama
        attribute c_pijama_base:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_base.webp"
        attribute c_pijama_agotada:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_agotada.webp"
        attribute c_pijama_bostezo1:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bostezo1.webp"
        attribute c_pijama_bostezo2:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bostezo2.webp"
        attribute c_pijama_brazoscruzados:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_brazoscruzados.webp"
        attribute c_pijama_rascando1:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_rascando1.webp"
        attribute c_pijama_rascando2:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_rascando2.webp"
        attribute c_pijama_escoba:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_escoba.webp"
        attribute c_pijama_celu:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_celu.webp"
        attribute c_pijama_dedolabio:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_dedolabio.webp"
        attribute c_pijama_fuckyou:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_fuckyou.webp"
        attribute c_pijama_idea:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_idea.webp"
        attribute c_pijama_notok:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_notok.webp"
        attribute c_pijama_ok:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_ok.webp"
        attribute c_pijama_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_pensando.webp"
        attribute c_pijama_saludando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_saludando.webp"
        attribute c_pijama_señalando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_senalando.webp"
        attribute c_pijama_tetas:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_tetas.webp"
        attribute c_pijama_verguenza:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_verguenza.webp"
        attribute c_pijama_victoria:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_victoria.webp"
        attribute c_pijama_mangas:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_mangas.webp"
        attribute c_pijama_cajacosplay:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_cajacoxplay.webp"
        attribute c_pijama_bolsamadera:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bolsamadera.webp"

        # (Acá vivía el placeholder `c_tanga_base`, que apuntaba al cuerpo base.
        # La tanga pasó a ser su propio layeredimage `violet_tanga`, al final de
        # este archivo, junto con `violet_mojada`.)

        attribute c_none:
            Null()
    
    # Otros (efectos adicionales)
    group otros:
        attribute ot_none default:
            Null()
        attribute ot_avergonzada:
            "images/characters/casa/violet/violet_parada_otros_avergonzada.webp"

################################################################################
## Layeredimage: violet_espalda
################################################################################

layeredimage violet_espalda:

    # Grupo skin base — Violet de espaldas con su ropa de siempre.
    # Era un placeholder vacio hasta que llegó la primera imagen; NO se creó un
    # grupo aparte para la ropa base porque este ya lo era, y dos grupos para el
    # mismo atuendo se dibujarian como dos capas superpuestas.
    group skinbase:
        attribute sb_none default:
            Null()
        attribute sb_celular:
            "images/characters/casa/violet/violet_parada_espalda_rbase_celular.webp"

    # Grupo pijama — imágenes de espalda con skin pijama
    group pijama:
        attribute p_none default:
            Null()
        attribute p_base:
            "images/characters/casa/violet/violet_parada_espalada_pijama_base.webp"
        attribute p_cyberpunk:
            "images/characters/casa/violet/violet_parada_espalada_pijama_cyberpunk.webp"
        attribute p_fantasia:
            "images/characters/casa/violet/violet_parada_espalada_pijama_fantasia.webp"
        attribute p_novela:
            "images/characters/casa/violet/violet_parada_espalada_pijama_novela.webp"
        attribute p_pensando:
            "images/characters/casa/violet/violet_parada_espalada_pijama_pensando.webp"
        attribute p_rascando1:
            "images/characters/casa/violet/violet_parada_espalada_pijama_rascando1.webp"
        attribute p_rascando2:
            "images/characters/casa/violet/violet_parada_espalada_pijama_rascando2.webp"

    # Grupo eva — imágenes de espalda con skin eva
    group eva:
        attribute e_none default:
            Null()
        attribute e_base:
            "images/characters/casa/violet/violet_parada_espalada_eva_base.webp"
        attribute e_lista:
            "images/characters/casa/violet/violet_parada_espalada_eva_lista.webp"
        attribute e_pelo:
            "images/characters/casa/violet/violet_parada_espalada_eva_pelo.webp"
        attribute e_cola1:
            "images/characters/casa/violet/violet_parada_espalada_eva_cola1.webp"
        attribute e_cola2:
            "images/characters/casa/violet/violet_parada_espalada_eva_cola2.webp"


################################################################################
## Layeredimage: violet_mojada
################################################################################

layeredimage violet_mojada:
    group cuerpo:
        attribute c_mojada default:
            "images/quest/violet/quest08/violet_parada_mojada.webp"

    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_base.webp"

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/characters/casa/violet/violet_parada_boca_hablando.webp"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_hablandochica.webp"
        attribute b_sonrisaleve:
            "images/characters/casa/violet/violet_parada_boca_sonrisaleve.webp"
        attribute b_sorprendida:
            "images/characters/casa/violet/violet_parada_boca_abiertachica.webp"


################################################################################
## Layeredimage: violet_tanga_qd10
################################################################################
## Violet en ropa interior. Antes era `c_tanga_base`, una sección del grupo
## `cuerpo` de `violet_parada`; se separó a layeredimage propio para que su arte
## no tenga que encajar con los atributos de la ropa de siempre.
##
## El sufijo `_qd10` es a propósito: por ahora este arte se usa SOLO en la quest
## de deseo 10. Si más adelante aparece en otras escenas, ahí sí conviene
## renombrarlo a algo genérico y actualizar los `show`.
##
## NO tiene grupo de ojos: el arte del cuerpo ya los trae dibujados. Solo la boca
## va aparte, y su grupo se declara DESPUÉS del cuerpo para que se dibuje encima
## (en un layeredimage el orden de los grupos es el orden de las capas). Por lo
## mismo `otros` va ÚLTIMO: el rubor tiene que quedar sobre todas las demás.
##
## Los seis assets son de 680x1080, el mismo lienzo, así que las capas alinean
## sin offsets.

layeredimage violet_tanga_qd10:

    group cuerpo:
        attribute c_tanga default:
            "images/characters/casa/violet/violet_tanga_qd10_cuerpo.webp"
        attribute c_tomando:
            "images/characters/casa/violet/violet_tanga_qd10_cuerpotomando.webp"

    # Después del cuerpo = encima del cuerpo. El default es Null: boca cerrada.
    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/characters/casa/violet/violet_tanga_qd10_bocahablando.webp"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_tanga_qd10_bocahablandochica.webp"
        attribute b_sonrisa:
            "images/characters/casa/violet/violet_tanga_qd10_bocasonrisa.webp"

    # Otros (efectos adicionales). Último grupo = capa de más arriba.
    group otros:
        attribute ot_none default:
            Null()
        attribute ot_colorada:
            "images/characters/casa/violet/violet_tanga_qd10_rubor.webp"


################################################################################
## (Las imagenes de la quest de amor 15 se mudaron)
################################################################################
## Los fondos y los layeredimage de sus escenas (primer plano, caida, Violet
## sentada) vivian acá. El arco entero paso a
## ventajas/juegosnuevos/jn_pocketboy.rpy y quedo parkeado, asi que sus
## imagenes se declaran ahi junto al contenido que las usa.


################################################################################
## Layeredimage: violet_magica
################################################################################
## Violet disfrazada de maga. Es un layeredimage propio y no un grupo de
## `violet_parada` porque el disfraz trae su propia cabeza dibujada: no combina
## con los grupos `cabeza` ni `ojos` del sprite normal.
##
## DOS GRUPOS DE BOCA, y hay que elegir el que corresponde al cuerpo:
##   - de frente (c_base, c_mostrando, c_1..c_5) -> grupo `boca_frente`
##   - de espaldas (c_espalda)                   -> grupo `boca_espalda`
## Son archivos distintos porque la boca cae en otro lugar segun para donde
## mire. Los dos arrancan en Null: boca cerrada.
##
## Al cambiar de un cuerpo de frente a c_espalda hay que bajar la boca de frente
## a bf_none y subir la de espalda (y al revés), o quedarian las dos puestas.
##
## Los 12 assets son 680x1080, el mismo lienzo que el resto de los sprites de
## Violet, asi que se muestra con las mismas posiciones (`at right`, etc).

layeredimage violet_magica:

    group cuerpo:
        attribute c_base default:
            "images/characters/casa/violet/violet_parada_cuerpo_magica_base.webp"
        attribute c_espalda:
            "images/characters/casa/violet/violet_parada_cuerpo_magica_espalda.webp"
        attribute c_mostrando:
            "images/characters/casa/violet/violet_parada_cuerpo_magica_mostrando.webp"

    # Ojos. UN solo grupo con las dos versiones, no dos grupos: los ojos SIEMPRE
    # se ven (no hay estado "sin ojos"), asi que dos grupos con imagen por
    # defecto dibujarian los dos pares a la vez. Con un grupo unico se ve
    # exactamente uno, y `o_base` —la version de frente— es el default.
    #
    # Al girar hay que cambiarlo a mano, igual que la boca.
    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_magica_base.webp"
        attribute o_espalda:
            "images/characters/casa/violet/violet_parada_ojos_magica_espaldabase.webp"

    # Boca para los cuerpos de FRENTE.
    group boca_frente:
        attribute bf_none default:
            Null()
        attribute bf_hablando:
            "images/characters/casa/violet/violet_parada_boca_magica_hablando_frente.webp"
        attribute bf_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_magica_hablandochica_frente.webp"

    # Boca para el cuerpo de ESPALDAS.
    #
    # `be_sonrisa` es la boca "en reposo" de espaldas: al girar va esa, no
    # be_none. Se vuelve a ella al terminar cada linea, igual que en los cuerpos
    # de frente se vuelve a bf_none.
    group boca_espalda:
        attribute be_none default:
            Null()
        attribute be_sonrisa:
            "images/characters/casa/violet/violet_parada_boca_magica_espaldasonrisa.webp"
        attribute be_hablando:
            "images/characters/casa/violet/violet_parada_boca_magica_hablando_espalda.webp"
        attribute be_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_magica_hablandochica_espalda.webp"
