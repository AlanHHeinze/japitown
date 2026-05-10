
# Posicionamiento 

# --- Posicion Micro Prota Noche ---
transform mc_intro_micro_noche_transform:
    xalign 0.62
    yalign 1.0

# --- Movimientos Generales ---

# --- Posición izquierda de la pantalla ---

# entra desde fuera por la izquierda hacia posición izquierda
transform personaje_entrar_pizquierda:
    xalign -0.5 yalign 1.0
    linear 1.4 xalign 0.0  

# entra desde la derecha hacia posición izquierda
transform personaje_entrar_derecha_pizquierda:
    xalign 1.5 yalign 1.0
    linear 1.4 xalign 0.0  

# entra desde la derecha, mirando hacia la izquierda, y se da vuelta al llegar
transform personaje_entrar_derecha_y_giro_pizquierda:
    xzoom -1.0
    xalign 1.5 yalign 1.0
    easein 1.8 xalign 0.0
    pause 0.1
    xzoom 1.0   # giro instantáneo al llegar


# --- Movimientos generales de salida / giro ---

# se va hacia la izquierda
transform personaje_salir_izquierda:
    xalign 0.0 yalign 1.0
    linear 1.4 xalign -0.6  

# se va hacia la derecha
transform personaje_salir_derecha:
    xalign 0.0 yalign 1.0
    linear 1.5 xalign 1.5  

# voltea horizontalmente instantáneamente
transform personaje_flip:
    xzoom -1.0
    yzoom 1.0


# vuelve a la dirección normal instantáneamente
transform personaje_enderezar:
    xzoom 1.0
    yzoom 1.0

transform mc_izquierda:
    xpos 0.15
    xanchor 0.5
    xzoom -1.0

# Posiciona al MC cerca del centro (borde derecho en pixel 960)
# El sprite mira hacia la derecha (flip horizontal)
transform mc_cerca:
    xpos 960
    xanchor 1.0  # Ancla en el borde derecho del sprite
    xzoom -1.0   # Flip para mirar hacia la derecha

# Posiciona al NPC cerca del centro (borde izquierdo en pixel 960)
# El sprite mira hacia la izquierda (normal)
transform npc_cerca:
    xpos 960
    xanchor 0.0  # Ancla en el borde izquierdo del sprite

transform mc_salir_izquierda:
    # Vuelve a la orientación normal
    xzoom 1.0
    yzoom 1.0

    # Movimiento hacia fuera de la pantalla
    ease 0.8 xpos -0.2

# Flip y salir hacia la izquierda (para sprites de quest)
transform flip_y_salir_izquierda:
    xzoom -1.0
    ease 0.8 xalign -0.3




#Efectos

# --- Fade Blanco ---
define fade_white = Fade(1.0, 0.5, 1.0, color="#FFFFFF")

# --- Texto entrando en el centro de la pantalla ---
transform remember_text_anim:
    alpha 0.0
    linear 0.3 alpha 1.0
    pause 1.2
    linear 0.5 alpha 0.0




# --- Movimiento hacia el centro ---
# Mueve un sprite desde su posición actual hacia el centro de la pantalla con movimiento suave
transform mover_al_centro:
    easein 1.0 xalign 0.5 yalign 0.5

# Variante con tiempo personalizable (más rápido)
transform mover_al_centro_rapido:
    easein 0.5 xalign 0.5 yalign 0.5

# Variante con tiempo personalizable (más lento)
transform mover_al_centro_lento:
    easein 1.5 xalign 0.5 yalign 0.5

# Variante que solo centra horizontalmente (mantiene Y)
transform mover_al_centro_horizontal:
    easein 1.0 xalign 0.5

# Mueve desde la posición derecha hacia el centro suavemente
transform derecha_a_centro:
    xalign 1.0
    easein 0.8 xalign 0.5
