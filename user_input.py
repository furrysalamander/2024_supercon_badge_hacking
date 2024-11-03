import utils
import characters
import display
import time

def enter_data(send_to_typewriter: bool = False) -> str:
    my_string = ""
    while True:
        selection = characters.poll()
        button_pressed = utils.button_pressed(utils.btn_a)
        
        input = characters.poll()
        display.write_text(my_string + input)

        if button_pressed:
            print("button pressed")
            if selection == ";":
                return my_string
            elif selection == "\\":
                selection = "\n"
            elif selection == "_":
                selection = " "
            if send_to_typewriter:
                utils.write_to_typewriter(selection)
            my_string += selection
        time.sleep_ms(1)

print(enter_data())
