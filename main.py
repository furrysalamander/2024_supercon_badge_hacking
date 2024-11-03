import network
import time
import machine
import urequests as requests
import json

MODEL = "gpt-4o-mini"
OPENAI_API_KEY = "OPENAI_API_KEY"
MAX_TOKENS = 250
# input()

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

def chatgpt(prompt: str) -> str:
    headers = {'Content-Type': 'application/json',
            "Authorization": f"Bearer {OPENAI_API_KEY}"}
    wrapped_prompt = [
    # { "role": "system", "content": "You are an AI typewriter that's overwhelmingly conerned about never committing an ethics violation of any kind. Because of this, you refuse to answer any questions, or provide any assistance. You always explain why fulfilling the user's request would be unethical. You always mention that you are an AI typewriter." },
    {"role": "user", "content": prompt},
    ]
    data = {"model": MODEL,
            "messages": wrapped_prompt,
            "max_tokens": MAX_TOKENS}
    print(wlan.ifconfig())
    print(wlan.status())
    # print(usocket.getaddrinfo('www.google.com', 80, 0, usocket.SOCK_STREAM))

    print("Attempting to send Prompt")
    r = requests.post("https://api.openai.com/v1/chat/completions",
                       json=data,
                       headers=headers)
    
    if r.status_code >= 300 or r.status_code < 200:
        print("There was an error with your request \n" +
              "Response Status: " + str(r.text))
        print(r.status_code)
    else:
        print("Success")
        response_data = json.loads(r.text)
        completion = response_data["choices"][0]["message"]["content"]
        print(completion)
    r.close()
    return completion
    # return completion

def main():
    print("hello world")
    # input("press enter to continue")
    connect_to_wifi()

    led = machine.Pin("LED", machine.Pin.OUT)

    while True:
        try:
            response = chatgpt("write an essay about photolithography")
            write_to_typewriter(response)
            break
        except OSError:
            print("failed to make request")
            pass
    
    while True:
        led.toggle()
        time.sleep(1)

if __name__ == "__main__":
    main()
