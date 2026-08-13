

#------------------------------------------------Voces ------------------------------------------------

#Prota pensando
define piensa = Character(None, what_italic=True, what_prefix="«", what_suffix="»", color="#AAAAAA")


#------------------------------------------------Layer------------------------------------------------


#Personaje parado ropa Base
layeredimage mc_parado_base:

    group dimensiones:
        attribute ddimensiones default:
            "images/characters/mc/base/mc_base_dimensiones.webp"
        attribute d_none:
            Null()

    group cabeza:
        attribute ca_cabeza default:
            "images/characters/mc/base/mc_base_cabeza.webp"
        attribute ca_none:
            Null()

    group ojos:
        attribute o_aburridosnm default:
            "images/characters/mc/base/mc_base_ojos_aburridosnm.webp"
        attribute o_aburridos:
            "images/characters/mc/base/mc_base_ojos_aburridos.webp"
        attribute o_felicesnm:
            "images/characters/mc/base/mc_base_ojos_felicesnm.webp"
        attribute o_felices:
            "images/characters/mc/base/mc_base_ojos_felices.webp"
        attribute o_asustadosnm:
            "images/characters/mc/base/mc_base_ojos_asustadosnm.webp"
        attribute o_asustados:
            "images/characters/mc/base/mc_base_ojos_asustados.webp"
        attribute o_abajonm:
            "images/characters/mc/base/mc_base_ojos_abajonm.webp"
        attribute o_arribanm:
            "images/characters/mc/base/mc_base_ojos_arribanm.webp"
        attribute o_base:
            "images/characters/mc/base/mc_base_ojos_base.webp"
        attribute o_cerrados:
            "images/characters/mc/base/mc_base_ojos_cerrados.webp"
        attribute o_disgustonm:
            "images/characters/mc/base/mc_base_ojos_disgustonm.webp"
        attribute o_enojadosnm:
            "images/characters/mc/base/mc_base_ojos_enojadosnm.webp"
        attribute o_enojados:
            "images/characters/mc/base/mc_base_ojos_enojados.webp"
        attribute o_felicescerrados:
            "images/characters/mc/base/mc_base_ojos_felicescerrados.webp"
        attribute o_molestosnm:
            "images/characters/mc/base/mc_base_ojos_molestosnm.webp"
        attribute o_molestos:
            "images/characters/mc/base/mc_base_ojos_molestos.webp"
        attribute o_seriosnm:
            "images/characters/mc/base/mc_base_ojos_seriosnm.webp"
        attribute o_serios:
            "images/characters/mc/base/mc_base_ojos_serios.webp"
        attribute o_sorprendidosnm:
            "images/characters/mc/base/mc_base_ojos_sorprendidosnm.webp"
        attribute o_sorprendidos:
            "images/characters/mc/base/mc_base_ojos_sorprendidos.webp"
        attribute o_tristesnm:
            "images/characters/mc/base/mc_base_ojos_tristesnm.webp"
        attribute o_none:
            Null()

    group boca:
        attribute b_abierta default:
            "images/characters/mc/base/mc_base_boca_abierta.webp"
        attribute b_abiertachica:
            "images/characters/mc/base/mc_base_boca_abiertachica.webp"
        attribute b_aburrida:
            "images/characters/mc/base/mc_base_boca_aburrida.webp"
        attribute b_asustada:
            "images/characters/mc/base/mc_base_boca_asustada.webp"
        attribute b_disgusto:
            "images/characters/mc/base/mc_base_boca_disgusto.webp"
        attribute b_enojadacerrada:
            "images/characters/mc/base/mc_base_boca_enojadacerrada.webp"
        attribute b_felizabierta:
            "images/characters/mc/base/mc_base_boca_felizabierta.webp"
        attribute b_felizcerrada:
            "images/characters/mc/base/mc_base_boca_felizcerrada.webp"
        attribute b_hablando:
            "images/characters/mc/base/mc_base_boca_hablando.webp"
        attribute b_molesta:
            "images/characters/mc/base/mc_base_boca_molesta.webp"
        attribute b_seria:
            "images/characters/mc/base/mc_base_boca_seria.webp"
        attribute b_triste:
            "images/characters/mc/base/mc_base_boca_triste.webp"
        attribute b_none:
            Null()

    group otros:
        attribute xnone default null


    group cuerpo:
        attribute c_rbase_base default:
            "images/characters/mc/base/mc_base_cuerpo_base.webp"
        attribute c_rbase_asustado:
            "images/characters/mc/base/mc_base_cuerpo_asustado.webp"
        attribute c_rbase_avergonzado:
            "images/characters/mc/base/mc_base_cuerpo_avergonzado.webp"
        attribute c_rbase_brazoscruzados:
            "images/characters/mc/base/mc_base_cuerpo_brazoscruzados.webp"
        attribute c_rbase_celular:
            "images/characters/mc/base/mc_base_cuerpo_celular.webp"
        attribute c_rbase_confianza:
            "images/characters/mc/base/mc_base_cuerpo_confianza.webp"
        attribute c_rbase_enojado:
            "images/characters/mc/base/mc_base_cuerpo_enojado.webp"
        attribute c_rbase_idea:
            "images/characters/mc/base/mc_base_cuerpo_idea.webp"
        attribute c_rbase_pensando:
            "images/characters/mc/base/mc_base_cuerpo_pensando.webp"
        attribute c_rbase_señalando:
            "images/characters/mc/base/mc_base_cuerpo_senalando.webp"
        attribute c_rbase_victoria:
            "images/characters/mc/base/mc_base_cuerpo_victoria.webp"
        attribute c_rbase_perfume:
            "images/characters/mc/base/mc_base_cuerpo_rbase_perfume.webp"
        attribute c_rbase_mochila1:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila1.webp"
        attribute c_rbase_mochila2:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila2.webp"
        attribute c_rbase_mochila3:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila3.webp"
        attribute c_rbase_mochila4:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila4.webp"
        attribute c_rbase_regalojasmine:
            "images/characters/mc/base/mc_base_cuerpo_rbase_regalojasmine.webp"
        attribute c_rbase_regaloviolet:
            "images/characters/mc/base/mc_base_cuerpo_rbase_regaloviolet.webp"
        attribute c_rbase_regalovioletabierto:
            "images/characters/mc/base/mc_base_cuerpo_rbase_regalovioletabierto.webp"
        attribute c_rbase_mangayamete:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mangayamete.webp"
        attribute c_rbase_mangayametepp:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mangayametepp.webp"
        attribute c_rbase_facepalm:
            "images/characters/mc/base/mc_base_cuerpo_rbase_facepalm.webp"
        attribute c_rbase_vr:
            "images/characters/mc/base/mc_base_cuerpo_rbase_vr.webp"
        attribute c_rbase_cuestionando:
            "images/characters/mc/base/mc_base_cuerpo_cuestionando.webp"
        attribute c_rbase_cajacosplay:
            "images/characters/mc/base/mc_base_cuerpo_rbase_cajacoxplay.webp"
        attribute c_rbase_mangas:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mangas.webp"
        attribute c_rbase_bolsamadera:
            "images/characters/mc/base/mc_base_cuerpo_bolsamadera.webp"
        attribute c_rbase_tanga:
            "images/characters/mc/base/mc_base_cuerpo_tanga.webp"
        attribute c_rbase_leyendocyberpunk:
            "images/characters/mc/base/mc_base_cuerpo_rbase_leyendocyberpunk.webp" 
        attribute c_rbase_perdon:
            "images/characters/mc/base/mc_base_cuerpo_perdon.webp"
        attribute c_none:
            Null()



#Personaje de espalda ropa Base
layeredimage mc_espalda_base:

    group cuerpo:
        attribute brazoscruzados default:
            "images/characters/mc/espalda/mc_base_espalda_brazoscruzados.webp"
        attribute golpeando:
            "images/characters/mc/espalda/mc_base_espalda_golpeando.webp"
        attribute golpeandoruido:
            "images/characters/mc/espalda/mc_base_espalda_golpeandoruido.webp"
        attribute rascarse1:
            "images/characters/mc/espalda/mc_base_espalda_rascarse1.webp"
        attribute rascarse2:
            "images/characters/mc/espalda/mc_base_espalda_rascarse2.webp"
