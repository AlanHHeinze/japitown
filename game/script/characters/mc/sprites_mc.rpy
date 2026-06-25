

#------------------------------------------------Voces ------------------------------------------------

#Prota pensando
define piensa = Character(None, what_italic=True, what_prefix="«", what_suffix="»", color="#AAAAAA")


#------------------------------------------------Layer------------------------------------------------


#Personaje parado ropa Base
layeredimage mc_parado_base:

    group dimensiones:
        attribute ddimensiones default:
            "images/characters/mc/base/mc_base_dimensiones.png"
        attribute d_none:
            Null()

    group cabeza:
        attribute ca_cabeza default:
            "images/characters/mc/base/mc_base_cabeza.png"
        attribute ca_none:
            Null()

    group ojos:
        attribute o_aburridosnm default:
            "images/characters/mc/base/mc_base_ojos_aburridosnm.png"
        attribute o_aburridos:
            "images/characters/mc/base/mc_base_ojos_aburridos.png"
        attribute o_felicesnm:
            "images/characters/mc/base/mc_base_ojos_felicesnm.png"
        attribute o_felices:
            "images/characters/mc/base/mc_base_ojos_felices.png"
        attribute o_asustadosnm:
            "images/characters/mc/base/mc_base_ojos_asustadosnm.png"
        attribute o_asustados:
            "images/characters/mc/base/mc_base_ojos_asustados.png"
        attribute o_abajonm:
            "images/characters/mc/base/mc_base_ojos_abajonm.png"
        attribute o_arribanm:
            "images/characters/mc/base/mc_base_ojos_arribanm.png"
        attribute o_base:
            "images/characters/mc/base/mc_base_ojos_base.png"
        attribute o_cerrados:
            "images/characters/mc/base/mc_base_ojos_cerrados.png"
        attribute o_disgustonm:
            "images/characters/mc/base/mc_base_ojos_disgustonm.png"
        attribute o_enojadosnm:
            "images/characters/mc/base/mc_base_ojos_enojadosnm.png"
        attribute o_enojados:
            "images/characters/mc/base/mc_base_ojos_enojados.png"
        attribute o_felicescerrados:
            "images/characters/mc/base/mc_base_ojos_felicescerrados.png"
        attribute o_molestosnm:
            "images/characters/mc/base/mc_base_ojos_molestosnm.png"
        attribute o_molestos:
            "images/characters/mc/base/mc_base_ojos_molestos.png"
        attribute o_seriosnm:
            "images/characters/mc/base/mc_base_ojos_seriosnm.png"
        attribute o_serios:
            "images/characters/mc/base/mc_base_ojos_serios.png"
        attribute o_sorprendidosnm:
            "images/characters/mc/base/mc_base_ojos_sorprendidosnm.png"
        attribute o_sorprendidos:
            "images/characters/mc/base/mc_base_ojos_sorprendidos.png"
        attribute o_tristesnm:
            "images/characters/mc/base/mc_base_ojos_tristesnm.png"
        attribute o_none:
            Null()

    group boca:
        attribute b_abierta default:
            "images/characters/mc/base/mc_base_boca_abierta.png"
        attribute b_abiertachica:
            "images/characters/mc/base/mc_base_boca_abiertachica.png"
        attribute b_aburrida:
            "images/characters/mc/base/mc_base_boca_aburrida.png"
        attribute b_asustada:
            "images/characters/mc/base/mc_base_boca_asustada.png"
        attribute b_disgusto:
            "images/characters/mc/base/mc_base_boca_disgusto.png"
        attribute b_enojadacerrada:
            "images/characters/mc/base/mc_base_boca_enojadacerrada.png"
        attribute b_felizabierta:
            "images/characters/mc/base/mc_base_boca_felizabierta.png"
        attribute b_felizcerrada:
            "images/characters/mc/base/mc_base_boca_felizcerrada.png"
        attribute b_hablando:
            "images/characters/mc/base/mc_base_boca_hablando.png"
        attribute b_molesta:
            "images/characters/mc/base/mc_base_boca_molesta.png"
        attribute b_seria:
            "images/characters/mc/base/mc_base_boca_seria.png"
        attribute b_triste:
            "images/characters/mc/base/mc_base_boca_triste.png"
        attribute b_none:
            Null()

    group otros:
        attribute xnone default null


    group cuerpo:
        attribute c_rbase_base default:
            "images/characters/mc/base/mc_base_cuerpo_base.png"
        attribute c_rbase_asustado:
            "images/characters/mc/base/mc_base_cuerpo_asustado.png"
        attribute c_rbase_avergonzado:
            "images/characters/mc/base/mc_base_cuerpo_avergonzado.png"
        attribute c_rbase_brazoscruzados:
            "images/characters/mc/base/mc_base_cuerpo_brazoscruzados.png"
        attribute c_rbase_celular:
            "images/characters/mc/base/mc_base_cuerpo_celular.png"
        attribute c_rbase_confianza:
            "images/characters/mc/base/mc_base_cuerpo_confianza.png"
        attribute c_rbase_enojado:
            "images/characters/mc/base/mc_base_cuerpo_enojado.png"
        attribute c_rbase_idea:
            "images/characters/mc/base/mc_base_cuerpo_idea.png"
        attribute c_rbase_pensando:
            "images/characters/mc/base/mc_base_cuerpo_pensando.png"
        attribute c_rbase_señalando:
            "images/characters/mc/base/mc_base_cuerpo_señalando.png"
        attribute c_rbase_victoria:
            "images/characters/mc/base/mc_base_cuerpo_victoria.png"
        attribute c_rbase_perfume:
            "images/characters/mc/base/mc_base_cuerpo_rbase_perfume.png"
        attribute c_rbase_mochila1:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila1.png"
        attribute c_rbase_mochila2:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila2.png"
        attribute c_rbase_mochila3:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila3.png"
        attribute c_rbase_mochila4:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mochila4.png"
        attribute c_rbase_regalojasmine:
            "images/characters/mc/base/mc_base_cuerpo_rbase_regalojasmine.png"
        attribute c_rbase_regaloviolet:
            "images/characters/mc/base/mc_base_cuerpo_rbase_regaloviolet.png"
        attribute c_rbase_regalovioletabierto:
            "images/characters/mc/base/mc_base_cuerpo_rbase_regalovioletabierto.png"
        attribute c_rbase_mangayamete:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mangayamete.png"
        attribute c_rbase_mangayametepp:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mangayametepp.png"
        attribute c_rbase_facepalm:
            "images/characters/mc/base/mc_base_cuerpo_rbase_facepalm.png"
        attribute c_rbase_vr:
            "images/characters/mc/base/mc_base_cuerpo_rbase_vr.png"
        attribute c_rbase_cuestionando:
            "images/characters/mc/base/mc_base_cuerpo_cuestionando.png"
        attribute c_rbase_cajacosplay:
            "images/characters/mc/base/mc_base_cuerpo_rbase_cajacoxplay.png"
        attribute c_rbase_mangas:
            "images/characters/mc/base/mc_base_cuerpo_rbase_mangas.png"
        attribute c_rbase_tanga:
            "images/characters/mc/base/mc_base_cuerpo_tanga.png"
        attribute c_rbase_leyendocyberpunk:
            "images/characters/mc/base/mc_base_cuerpo_rbase_leyendocyberpunk.png" 
        attribute c_rbase_perdon:
            "images/characters/mc/base/mc_base_cuerpo_perdon.png"
        attribute c_none:
            Null()




image mc_intro_parado_espalda = "images/intro/characters/mc/mc_intro_parado_espalda.png"
image mc_intro_parado_espalda_foto = "images/intro/characters/mc/mc_intro_parado_espalda_foto.png"
image mc_intro_parado_espalda_mostrandofoto = "images/intro/characters/mc/mc_intro_parado_espalda_mostrandofoto.png"


#Personaje de espalda ropa Base
layeredimage mc_espalda_base:

    group cuerpo:
        attribute brazoscruzados default:
            "images/characters/mc/espalda/mc_base_espalda_brazoscruzados.png"
        attribute golpeando:
            "images/characters/mc/espalda/mc_base_espalda_golpeando.png"
        attribute golpeandoruido:
            "images/characters/mc/espalda/mc_base_espalda_golpeandoruido.png"
        attribute rascarse1:
            "images/characters/mc/espalda/mc_base_espalda_rascarse1.png"
        attribute rascarse2:
            "images/characters/mc/espalda/mc_base_espalda_rascarse2.png"
