import machine

uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))
uart.write('hello')
print("hello")
