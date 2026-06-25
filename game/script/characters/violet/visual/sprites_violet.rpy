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
            "images/characters/casa/violet/violet_parada_area.png"
        attribute a_none:
            Null()
    
    # Cabeza
    group cabeza:
        attribute ca_base default:
            "images/characters/casa/violet/violet_parada_cabeza_rbase.png"
        attribute ca_pijama:
            "images/characters/casa/violet/violet_parada_cabeza_pijama.png"
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
            "images/characters/casa/violet/violet_parada_cuerpo_eva_base.png"

    # Boca
    group boca:
        attribute b_aburrida default:
            "images/characters/casa/violet/violet_parada_boca_aburrida.png"
        attribute b_bostezogrande:
            "images/characters/casa/violet/violet_parada_boca_bostezogrande.png"
        attribute b_abiertachica:
            "images/characters/casa/violet/violet_parada_boca_abiertachica.png"
        attribute b_cerradachica:
            "images/characters/casa/violet/violet_parada_boca_cerradachica.png"
        attribute b_contenta:
            "images/characters/casa/violet/violet_parada_boca_contenta.png"
        attribute b_feliz:
            "images/characters/casa/violet/violet_parada_boca_feliz.png"
        attribute b_gritandomucho:
            "images/characters/casa/violet/violet_parada_boca_gritandomucho.png"
        attribute b_hablando:
            "images/characters/casa/violet/violet_parada_boca_hablando.png"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_hablandochica.png"
        attribute b_mordiendo:
            "images/characters/casa/violet/violet_parada_boca_mordiendo.png"
        attribute b_sexy:
            "images/characters/casa/violet/violet_parada_boca_sexy.png"
        attribute b_sonrisacerrada:
            "images/characters/casa/violet/violet_parada_boca_sonrisacerrada.png"
        attribute b_sonrisacostado:
            "images/characters/casa/violet/violet_parada_boca_sonrisacostado.png"
        attribute b_sonrisaleve:
            "images/characters/casa/violet/violet_parada_boca_sonrisaleve.png"
        attribute b_sonrisapequeña:
            "images/characters/casa/violet/violet_parada_boca_sonrisapequeña.png"
        attribute b_triste:
            "images/characters/casa/violet/violet_parada_boca_triste.png"
        attribute b_none:
            Null()
    
    # Ojos
    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_base.png"
        attribute o_bostezograndenm:
            "images/characters/casa/violet/violet_parada_ojos_bostezograndenm.png"
        attribute o_abajonm:
            "images/characters/casa/violet/violet_parada_ojos_abajonm.png"
        attribute o_abiertos:
            "images/characters/casa/violet/violet_parada_ojos_abiertos.png"
        attribute o_arribanm:
            "images/characters/casa/violet/violet_parada_ojos_arribanm.png"
        attribute o_cerrados:
            "images/characters/casa/violet/violet_parada_ojos_cerrados.png"
        attribute o_felicesnm:
            "images/characters/casa/violet/violet_parada_ojos_felicesnm.png"
        attribute o_dormidos:
            "images/characters/casa/violet/violet_parada_ojos_dormidos.png"
        attribute o_enojados:
            "images/characters/casa/violet/violet_parada_ojos_enojados.png"
        attribute o_felices:
            "images/characters/casa/violet/violet_parada_ojos_felices.png"
        attribute o_guiñando:
            "images/characters/casa/violet/violet_parada_ojos_guiñando.png"
        attribute o_juzgandonm:
            "images/characters/casa/violet/violet_parada_ojos_juzgandonm.png"
        attribute o_llorandomuchonm:
            "images/characters/casa/violet/violet_parada_ojos_llorandomuchonm.png"
        attribute o_sexys:
            "images/characters/casa/violet/violet_parada_ojos_sexys.png"
        attribute o_tristes:
            "images/characters/casa/violet/violet_parada_ojos_tristes.png"
        attribute o_pensando:
            "images/characters/casa/violet/violet_parada_ojos_pensando.png"
        attribute o_costadobase:
            "images/characters/casa/violet/violet_parada_ojos_costadobase.png"
        attribute o_none:
            Null()
    
    # Cuerpo
    group cuerpo:
        attribute c_rbase_base default:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_base.png"
        attribute c_rbase_brazoscruzados:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_brazoscruzados.png"
        attribute c_rbase_celu:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_celu.png"
        attribute c_rbase_chek:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_chek.png"
        attribute c_rbase_cola:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cola.png"
        attribute c_rbase_dedolabio:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_dedolabio.png"
        attribute c_rbase_enojada:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_enojada.png"
        attribute c_rbase_fuckyou:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_fuckyou.png"
        attribute c_rbase_gestito:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_gestito.png"
        attribute c_rbase_idea:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_idea.png"
        attribute c_rbase_notok:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_notok.png"
        attribute c_rbase_ok:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_ok.png"
        attribute c_rbase_paz:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_paz.png"
        attribute c_rbase_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_pensando.png"
        attribute c_rbase_señalando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_señalando.png"
        attribute c_rbase_sorprendido:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_sorprendida.png"
        attribute c_rbase_tetas:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_tetas.png"
        attribute c_rbase_verguenza:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_verguenza.png"
        attribute c_rbase_victoria:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_victoria.png"
        attribute c_rbase_regalo:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cajaregalo.png"
        attribute c_rbase_cajacosplay:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_cajacoxplay.png"
        attribute c_rbase_saludando:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_saludando.png"
        attribute c_rbase_mangas:
            "images/characters/casa/violet/violet_parada_cuerpo_rbase_mangas.png"

        # Pijama
        attribute c_pijama_base:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_base.png"
        attribute c_pijama_agotada:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_agotada.png"
        attribute c_pijama_bostezo1:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bostezo1.png"
        attribute c_pijama_bostezo2:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_bostezo2.png"
        attribute c_pijama_brazoscruzados:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_brazoscruzados.png"
        attribute c_pijama_rascando1:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_rascando1.png"
        attribute c_pijama_rascando2:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_rascando2.png"
        attribute c_pijama_escoba:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_escoba.png"
        attribute c_pijama_celu:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_celu.png"
        attribute c_pijama_dedolabio:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_dedolabio.png"
        attribute c_pijama_fuckyou:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_fuckyou.png"
        attribute c_pijama_idea:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_idea.png"
        attribute c_pijama_notok:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_notok.png"
        attribute c_pijama_ok:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_ok.png"
        attribute c_pijama_pensando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_pensando.png"
        attribute c_pijama_saludando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_saludando.png"
        attribute c_pijama_señalando:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_señalando.png"
        attribute c_pijama_tetas:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_tetas.png"
        attribute c_pijama_verguenza:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_verguenza.png"
        attribute c_pijama_victoria:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_victoria.png"
        attribute c_pijama_mangas:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_mangas.png"
        attribute c_pijama_cajacosplay:
            "images/characters/casa/violet/violet_parada_cuerpo_pijama_cajacoxplay.png"

        attribute c_none:
            Null()
    
    # Otros (efectos adicionales)
    group otros:
        attribute ot_none default:
            Null()
        attribute ot_avergonzada:
            "images/characters/casa/violet/violet_parada_otros_avergonzada.png"

################################################################################
## Layeredimage: violet_espalda
################################################################################

layeredimage violet_espalda:

    # Grupo skin base — placeholder para imágenes futuras
    group skinbase:
        attribute sb_none default:
            Null()

    # Grupo pijama — imágenes de espalda con skin pijama
    group pijama:
        attribute p_none default:
            Null()
        attribute p_base:
            "images/characters/casa/violet/violet_parada_espalada_pijama_base.png"
        attribute p_cyberpunk:
            "images/characters/casa/violet/violet_parada_espalada_pijama_cyberpunk.png"
        attribute p_fantasia:
            "images/characters/casa/violet/violet_parada_espalada_pijama_fantasia.png"
        attribute p_novela:
            "images/characters/casa/violet/violet_parada_espalada_pijama_novela.png"
        attribute p_pensando:
            "images/characters/casa/violet/violet_parada_espalada_pijama_pensando.png"
        attribute p_rascando1:
            "images/characters/casa/violet/violet_parada_espalada_pijama_rascando1.png"
        attribute p_rascando2:
            "images/characters/casa/violet/violet_parada_espalada_pijama_rascando2.png"

    # Grupo eva — imágenes de espalda con skin eva
    group eva:
        attribute e_none default:
            Null()
        attribute e_base:
            "images/characters/casa/violet/violet_parada_espalada_eva_base.png"
        attribute e_lista:
            "images/characters/casa/violet/violet_parada_espalada_eva_lista.png"
        attribute e_pelo:
            "images/characters/casa/violet/violet_parada_espalada_eva_pelo.png"
        attribute e_cola1:
            "images/characters/casa/violet/violet_parada_espalada_eva_cola1.png"
        attribute e_cola2:
            "images/characters/casa/violet/violet_parada_espalada_eva_cola2.png"


################################################################################
## Layeredimage: violet_mojada
################################################################################

layeredimage violet_mojada:
    group cuerpo:
        attribute c_mojada default:
            "images/quest/violet/quest08/violet_parada_mojada.png"

    group ojos:
        attribute o_base default:
            "images/characters/casa/violet/violet_parada_ojos_base.png"

    group boca:
        attribute b_none default:
            Null()
        attribute b_hablando:
            "images/characters/casa/violet/violet_parada_boca_hablando.png"
        attribute b_hablandochica:
            "images/characters/casa/violet/violet_parada_boca_hablandochica.png"
        attribute b_sonrisaleve:
            "images/characters/casa/violet/violet_parada_boca_sonrisaleve.png"
        attribute b_sorprendida:
            "images/characters/casa/violet/violet_parada_boca_abiertachica.png"
