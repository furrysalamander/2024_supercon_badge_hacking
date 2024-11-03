import time
import machine
import utils
import hackaday
import openai
import ultraGraphicsLibrary
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import display
import characters

def main():
    print("hello world")
    display.write_text("connecting to wifi")
    
    utils.connect_to_wifi()
    display.write_text("connected")

    def hackaday_demo():
        for article in hackaday.get_articles():
            utils.write_to_typewriter(
                article
            )

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
i2c = I2C(0) 
def main2():
    buttonA = Pin(8, Pin.IN, Pin.PULL_UP)
    buttonB = Pin(9, Pin.IN, Pin.PULL_UP)
    buttonC = Pin(28, Pin.IN, Pin.PULL_UP)
    oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
    oled.fill(0)

    while True: 
        menu_selection = ultraGraphicsLibrary.selection_menu(oled, buttonA, buttonB, buttonC)
        print(menu_selection)
        oled.fill(0)
        if menu_selection == "Hackaday":
            # Get hackaday articles
            print("Printing Hackaday article")
        elif menu_selection == "OpenAI":
            # Collect prompt to send up. 
            print("Getting AI prompt")
            prompt = ultraGraphicsLibrary.letterSelector(oled, buttonA, buttonB, buttonC)
            print("Sending to ChatGPT:", prompt)
        elif menu_selection == "Manual Input":
            # Manual Input
            print("Collecting Manual Input...")

        time.sleep(0.1)




    inputed = ultraGraphicsLibrary.letterSelector(oled, buttonA, buttonB, buttonC)
    print(inputed)
    oled.fill(0)
    time.sleep(0.2)
    

if __name__ == "__main__":
    main2()
