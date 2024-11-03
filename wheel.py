import utils
import math
import time
import machine

I2C_ADDRESS=0x54

## touchwheel last, with a wait loop,  b/c it doesn't init until animation is over
## probably need to implement a timeout here?
bus: machine.I2C = None
touchwheel_counter = 0
while not bus:
    try:
        bus = utils.which_bus_has_device_id(0x54)[0]
    except:
        pass
    time.sleep_ms(100)
    touchwheel_counter = touchwheel_counter + 1
    if touchwheel_counter > 50:
        break
if not bus:
    print(f"Warning: Touchwheel not found.")


def touchwheel_read():
    """Returns 0 for no touch, 1-255 clockwise around the circle from the south"""
    return(bus.readfrom_mem(84, 0, 1)[0])

last_value = 0
def char_select():
    global last_value
    new_value = touchwheel_read()
    if new_value == 0:
        last_value = 0
        return 0
    if last_value == 0:
        last_value = new_value
        return 0
    
    diff = (new_value - last_value + 128) % 256 - 128

    if abs(diff) > 255/6:
        result = math.copysign(1, diff)
        last_value = new_value
        return result
    return 0

if __name__=="__main__":
    print(bus)
    while True:
        print(char_select())
        time.sleep_ms(100)
