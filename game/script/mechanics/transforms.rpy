
# Posicionamiento 

# --- Posicion Micro Prota Noche ---
transform mc_intro_micro_noche_transform:
    xalign 0.62
    yalign 1.0

# Movimientos

# --- Azafata Transforms ---
# se mueve suavemente desde fuera de la pantalla a la posición izquierda
transform azafata_entrar:
    xalign -0.5 yalign 1.0
    linear 1.2 xalign 0.0  

# se va hacia la izquierda
transform azafata_salir:
    linear 1.0 xalign -0.6  

# voltea horizontalmente
transform azafata_vuelta:
    xzoom -1.0  

# vuelve a la dirección normal
transform azafata_normal:
    xzoom 1.0  

#Efectos

# --- Fade Blanco ---
define fade_white = Fade(1.0, 0.5, 1.0, color="#FFFFFF")

# --- Texto entrando en el centro de la pantalla ---
transform remember_text_anim:
    alpha 0.0
    linear 0.3 alpha 1.0
    pause 1.2
    linear 0.5 alpha 0.0



