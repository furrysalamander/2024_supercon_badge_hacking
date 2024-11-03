import time
from ssd1306 import SSD1306_I2C
import wheel
import utils

HOME_X = 0
HOME_Y = 0
MAX_X = 15 * 8 
MAX_Y = 16
CHAR_PIXEL_SIZE = 8

def selection_menu(oled, buttonA, buttonB, buttonC):
    myFourRowScreen = four_row_screen(oled)
    selector = 0
    cursorMark = "-> " 
    noneCursorMark = "   "
    
    while True:
        myFourRowScreen.display_rows = ["Hackaday",
                                        "OpenAI",
                                        "Manual Input"]
        
        # Color wheel select
        dir = wheel.char_select()
        if dir == 1:
            selector += 1
        elif dir == -1:
            selector -= 1

        if utils.button_pressed(buttonA): #buttonA.value() == 0: #button.is_pressed(buttonA):
            print("ButtonA is Pressed")
            selector += 1
        if utils.button_pressed(buttonC): #buttonC.value() == 0: #button.is_pressed(buttonC):
            print("ButtonC is Pressed")
            selector -= 1
        if utils.button_pressed(buttonB): #buttonB.value() == 0: #button.is_pressed(buttonB):
            print("ButtonB is Pressed")
            return  myFourRowScreen.display_rows[selector]
        
        if selector < 0:
            selector = 0
        if selector > len(myFourRowScreen.display_rows)-1:
            selector = len(myFourRowScreen.display_rows)-1
        for i, row in enumerate(myFourRowScreen.display_rows):
            if selector == i:
                myFourRowScreen.display_rows[i] = cursorMark + myFourRowScreen.display_rows[i]
            else:
                myFourRowScreen.display_rows[i] = noneCursorMark + myFourRowScreen.display_rows[i]


        myFourRowScreen.display_all_rows()
        time.sleep(0.1)


def letterSelector(oled, buttonA, buttonB, buttonC):
    myFourRowScreen = four_row_screen(oled)
    selector = 0
    abc = "abcdefghijklmnopqrstuvwxyz;_"
    wheelInput = wheel.char_select()

    inputSting = ""

    while True:
        selector = selector % len(abc)
        myFourRowScreen.insert_char(myChar=abc[selector])
        # myFourRowScreen.current_x_pos -= CHAR_PIXEL_SIZE
        while True:
            # Button select 
            if utils.button_pressed(buttonA): #buttonA.value() == 0: #button.is_pressed(buttonA):
                print("ButtonA is Pressed")
                selector += 1
                myFourRowScreen.deleteLastChar()
                break
            if utils.button_pressed(buttonB): #buttonB.value() == 0: #button.is_pressed(buttonB):
                print("ButtonB is Pressed")
                # myFourRowScreen.current_x_pos += CHAR_PIXEL_SIZE
                #myFourRowScreen.increment_pos()
                if abc[selector] == ";":
                    return inputSting.replace("_", " ")
                inputSting += abc[selector]
                break
            if utils.button_pressed(buttonC): #buttonC.value() == 0: #button.is_pressed(buttonC):
                print("ButtonC is Pressed")
                selector -= 1
                myFourRowScreen.deleteLastChar()
                break

            # Color wheel select
            dir = wheel.char_select()
            if dir == 1:
                selector += 1
                myFourRowScreen.deleteLastChar()
                break
            elif dir == -1:
                selector -= 1
                myFourRowScreen.deleteLastChar()
                break

            time.sleep(0.05)

            # if (buttonPush()):
            #     myFourRowScreen.current_x_pos += 1
            #     break
        
        time.sleep(0.05)

class four_row_screen(): 
    current_x_pos = HOME_X
    current_y_pos = HOME_X
    
    display_rows = []

    def __init__(self, oled_object):
        self.oled_object = oled_object

    def display_all_rows(self):
        self.oled_object.fill(0)
        for i, row in enumerate(self.display_rows):
            self.oled_object.text(row, 1, (0 + (CHAR_PIXEL_SIZE * i)))
        self.oled_object.show()

    def insert_char(self, myChar):
        self.oled_object.text(myChar, self.current_x_pos, self.current_y_pos)
        self.increment_pos()
        self.oled_object.show()

    def increment_pos(self):
        self.current_x_pos += CHAR_PIXEL_SIZE 
        if self.current_x_pos > MAX_X:
            self.current_x_pos = HOME_X
            self.current_y_pos += CHAR_PIXEL_SIZE
        if self.current_y_pos > MAX_Y:
            # TODO Scroll down 1 CHAR_PIXEL_SIZE 
            self.scroll_down()
            self.current_y_pos = MAX_Y

    def decrement_pos(self):
        self.current_x_pos -= CHAR_PIXEL_SIZE 
        if self.current_x_pos < HOME_X:
            self.current_x_pos = HOME_X
            # self.current_y_pos -= CHAR_PIXEL_SIZE
        # if self.current_y_pos < 0:
        #     # TODO Scroll down 1 CHAR_PIXEL_SIZE 
        #     self.scroll_up()
        #     self.current_y_pos = HOME_Y

    def scroll_down(self):
        for i in range(8):
            self.oled_object.scroll(0,-1)
            self.oled_object.show()
            time.sleep(0.1)
        self.oled_object.text("                ", 0, 0)
        self.oled_object.show()

    def scroll_up(self):
        for i in range(8):
            self.oled_object.scroll(0,1)
            self.oled_object.show()
            time.sleep(0.1)

    def deleteLastChar(self):
        #self.decrement_pos()
        self.oled_object.rect(self.current_x_pos-CHAR_PIXEL_SIZE, self.current_y_pos, CHAR_PIXEL_SIZE, CHAR_PIXEL_SIZE, 0, True)
        self.decrement_pos()
