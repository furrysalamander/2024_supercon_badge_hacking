import time
import machine
import utils
import hackaday
import openai
import user_input
import ultraGraphicsLibrary
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import display
import characters

def hackaday_demo():
    for article in hackaday.get_articles():
        utils.write_to_typewriter(
            article
        )

def main():
    print("hello world")
    display.write_text("connecting to wifi")
    
    utils.connect_to_wifi()
    display.write_text("connected")

    while True:
        display.write_text("press a to continue")
        while True:
            utils.led.toggle()
            time.sleep_ms(100)
            if utils.button_pressed(utils.btn_a):
                break
        try:
            display.write_text("printing hackaday")
            hackaday_demo()
            # response = openai.chatgpt("write an essay about photolithography")
            # utils.write_to_typewriter(response)
            break
        except OSError:
            print("failed to make request")
            pass
    
    while True:
        utils.led.toggle()
        time.sleep(1)


WIDTH  = 128                                      
HEIGHT = 32    
def main2():
    print("hello world")
    display.write_text("connecting to wifi")
    
    utils.connect_to_wifi()
    display.write_text("connected")

    oled = SSD1306_I2C(WIDTH, HEIGHT, utils.which_bus_has_device_id(display.I2C_ADDR)[0])                  # Init oled display
    oled.rotate(False)
    oled.fill(0)

    while True: 
        menu_selection = ultraGraphicsLibrary.selection_menu(oled, utils.btn_a, utils.btn_b, utils.btn_c)
        print(menu_selection)
        oled.fill(0)
        if menu_selection == "Hackaday":
            # Get hackaday articles
            print("Printing Hackaday article")
            display.write_text("printing hackaday")
            hackaday_demo()
        elif menu_selection == "OpenAI":
            # Collect prompt to send up. 
            print("Getting AI prompt")
            # prompt = ultraGraphicsLibrary.letterSelector(oled, utils.btn_a, utils.btn_b, utils.btn_c)
            prompt = user_input.enter_data()
            print("Sending to ChatGPT:", prompt)
            display.write_text("getting response")
            utils.write_to_typewriter(openai.chatgpt(prompt))
            utils.write_to_typewriter("\n")
        elif menu_selection == "Manual Input":
            # Manual Input
            print("Collecting Manual Input...")
            user_input.enter_data(True)
            utils.write_to_typewriter("\n")

        time.sleep(0.1)

if __name__ == "__main__":
    main2()
