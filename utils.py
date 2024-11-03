import machine
import network
import time


## Initialize I2C peripherals
i2c0 = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400_000)
i2c1 = machine.I2C(1, sda=machine.Pin(26), scl=machine.Pin(27), freq=400_000)

led = machine.Pin("LED", machine.Pin.OUT)
btn_a = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)
btn_b = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)
btn_c = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)

def button_pressed(button: machine.Pin) -> bool:
    if not button.value():
        time.sleep_ms(100)
        while not button.value():
            time.sleep_ms(100)
        return True
    return False

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


def connect_to_wifi():
    SSID = "Supercon"
    PASSWORD = "whatpassword"
    global wlan

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print("Connected to WiFi")

    # # Make GET request
    # response = requests.get("http://www.google.com/")
    # # Get response code
    # response_code = response.status_code
    # # Get response content
    # response_content = response.content

    # # Print results
    # print('Response code: ', response_code)
    # print('Response content:', response_content)

uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))

def write_to_typewriter(text: str):
    chars_since_newline = 0
    for char in text:
        if char == "\n":
            chars_since_newline = 0
        else:
            chars_since_newline += 1
        if chars_since_newline > 70:
            if char == " ":
                char = "\n"
                chars_since_newline = 0
        print(chars_since_newline)
        uart.write(char)
    
        while uart.read() is None:
            pass