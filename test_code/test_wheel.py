from machine import I2C, Pin
import time
import math

## Initialize I2C peripherals
i2c0 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
i2c1 = I2C(1, sda=Pin(26), scl=Pin(27), freq=400_000)

def which_bus_has_device_id(i2c_id, debug=False):
    '''Returns a list of i2c bus objects that have the requested id on them.
    Note this can be of length 0, 1, or 2 depending on which I2C bus the id is found'''

    i2c0_bus = i2c0.scan() 
    if debug:
        print("Bus 0: ")
        print(str([hex(x) for x in i2c0_bus]))

    i2c1_bus = i2c1.scan()
    if debug:
        print("Bus 1: ")
        print(str([hex(x) for x in i2c1_bus]))

    busses = []
    if i2c_id in i2c0_bus:
        busses.append(i2c0)
    if i2c_id in i2c1_bus:
        busses.append(i2c1)

    return(busses)

## touchwheel last, with a wait loop,  b/c it doesn't init until animation is over
## probably need to implement a timeout here?
touchwheel_bus: I2C = None
touchwheel_counter = 0
while not touchwheel_bus:
    try:
        touchwheel_bus =  which_bus_has_device_id(0x54)[0]
    except:
        pass
    time.sleep_ms(100)
    touchwheel_counter = touchwheel_counter + 1
    if touchwheel_counter > 50:
        break
if not touchwheel_bus:
    print(f"Warning: Touchwheel not found.")


def touchwheel_read():
    """Returns 0 for no touch, 1-255 clockwise around the circle from the south"""
    return(touchwheel_bus.readfrom_mem(84, 0, 1)[0])


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


print(touchwheel_bus)
while True:
    # print(touchwheel_read())
    print(char_select())
    time.sleep_ms(100)
