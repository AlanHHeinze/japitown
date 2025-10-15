
# Pedir nombre
# arriba del todo (fuera de labels)
default mc_name = ""    # valor inicial
define mc = Character("[mc_name]",color="#56b6c2")

# screen para ingresar nombre
screen name_input_screen():
    # screen variable que contendrá el texto actual
    default name = mc_name
    # InputValue que actualiza la screen-variable 'name' y permite que Enter devuelva el valor
    default name_iv = ScreenVariableInputValue("name", returnable=True)

    modal True

    frame:
        align (0.5, 0.5)
        has vbox
        spacing 10
        text "Ingresa tu nombre:" size 36
        input value name_iv length 20

        hbox:
            spacing 20
            textbutton "Confirmar":
                action Return(name)   # devuelve el texto actual de 'name'
            textbutton "Cancelar":
                action Return(mc_name)  # devuelve el nombre previo si cancela

# label que llama la screen y guarda el resultado en mc_name
label choose_name:
    $ mc_name = renpy.call_screen("name_input_screen")
    $ mc_name = mc_name.strip()
    return


