import utils
import ssd1306

DISP_WIDTH=128
DISP_HEIGHT=32

I2C_ADDR = 0x3C

bus = utils.which_bus_has_device_id(I2C_ADDR)[0]
display = ssd1306.SSD1306_I2C(DISP_WIDTH, DISP_HEIGHT, bus)
# display.init_display()
# display.poweron()

def write_text(text: str):
    display.fill(0)
    display.text(text, 0, 0)
    display.show()

if __name__=="__main__":
    import time
    display.init_display()
    display.poweron()
    while True:
        display.fill(0)
        display.text("hi", 0, 0)
        display.show()
        time.sleep(1)
        display.fill(0)
        display.text("beans", 0, 0)
        display.show()
        time.sleep(1)
    pass