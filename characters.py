import wheel

CHARACTERS = "abcdefghijklmnopqrstuvwxyz_;"
index = 0

def poll():
    global index
    index = int(index + wheel.char_select()) % len(CHARACTERS)
    return CHARACTERS[index]
